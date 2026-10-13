#!/usr/bin/env python3
"""FW05 structural acceptance; this never certifies owner/metric truth."""
from pathlib import Path
import re
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'plugins/super-ux/scripts'))
import brand_lint as b
import ux_lint as u

count = 0

def expect(value, label):
    global count
    assert value, label
    count += 1

seed = (ROOT / 'templates/brand/copy-brief.md').read_text()
fields = re.findall(r'(?m)^([A-Za-z ]+):', seed)
expect(set(fields) - {'Contract'} == set(b.COPY_BRIEF_FIELDS), 'every seeded brief field has a code reader')
contract = (ROOT / 'plugins/super-ux/skills/references/brand-contract.md').read_text()
for field in b.COPY_BRIEF_FIELDS:
    expect(field + ': unknown' in contract, field + ' contract seed parity')
expect('- **Owner:** unknown' in (ROOT / 'templates/foundation.md').read_text(), 'new journey seed names unknown owner')
with tempfile.TemporaryDirectory(prefix='fw05-copy-controls-') as tmp:
    d = Path(tmp)
    expect(not b.check_copy_brief(d, {}), 'unrelated task has no brief requirement')
    warnings = b.check_copy_brief(d, {'marketing': ['page.md']})
    expect(len(warnings) == 1 and warnings[0].code == 'B074' and warnings[0].severity == 'warn', 'legacy missing brief stays advisory')
    (d / 'copy-brief.md').write_text(seed)
    expect(not b.check_copy_brief(d, {'marketing': ['page.md']}), 'unknowns are explicit valid inputs')
    (d / 'copy-brief.md').write_text(seed.replace('Voice reference: unknown', 'Voice reference: voice.md#voice-references'))
    voice = '## Voice references\n- **Admired:** clear examples\n- **Refused:** unsupported promises\n'
    (d / 'voice.md').write_text(voice)
    expect(not b.check_copy_brief(d, {}), 'voice resolves its own pair')
    (d / 'voice.md').write_text(voice.replace('## Voice references', '## Elsewhere') + '\n## Voice references\n')
    expect(any(f.code == 'B075' for f in b.check_copy_brief(d, {})), 'pair outside cited section cannot satisfy reference')
    (d / 'voice.md').write_text(voice.replace('clear examples', 'unknown'))
    expect(any(f.code == 'B075' for f in b.check_copy_brief(d, {})), 'unresolved pair must keep voice reference unknown')
    (d / 'copy-brief.md').write_text(seed.replace('Constraints: unknown', '<!-- Constraints: unknown -->'))
    expect(any(f.code == 'B075' for f in b.check_copy_brief(d, {})), 'commented field does not satisfy brief')
    (d / 'foundation.md').write_text((ROOT / 'templates/foundation.md').read_text())
    u.WARNS.clear()
    u.check_journey_owners(u.read(d / 'foundation.md'))
    expect(not u.WARNS, 'pristine commented journey seed stays clean')
print(f'FW05 journey/copy: {count} controls passed')
