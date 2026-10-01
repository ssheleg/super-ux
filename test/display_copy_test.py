#!/usr/bin/env python3
"""Regressions for semantic display-copy coverage (stdlib only)."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'plugins/super-ux/scripts'))
import brand_lint
sys.path.insert(0, str(ROOT / 'test'))
from brand_lint_test import MINIMAL


class DisplayCopy(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.brand = self.root / 'docs/brand'
        self.brand.mkdir(parents=True)
        for name, text in MINIMAL.items():
            (self.brand / name).write_text(text)
        self.source('page.html', '')
        self.declare('page.html')

    def source(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def declare(self, glob):
        (self.brand / 'README.md').write_text('Contract: brand-contract v1\n\nSources:\n  marketing: ' + glob + '\n')

    def headings(self):
        return [f for f in brand_lint.run(self.brand) if f.code == 'B063']

    def test_nested_html_and_source_line(self):
        self.source('page.html', '<main>\n<h1>Your <em>teams.</em></h1>\n</main>')
        findings = self.headings()
        self.assertEqual(len(findings), 1)
        self.assertEqual((findings[0].path, findings[0].line), ('page.html', 2))

    def test_break_fragments_and_entities(self):
        self.source('page.html', '<h1>Your agents. Your tools.<br>Your way of working</h1>\n<h2>Plan &amp; build&#46;</h2>')
        self.assertEqual(len(self.headings()), 2)

    def test_accessibility_hidden_is_still_visible(self):
        self.source('page.html', '<h1 aria-hidden="true">Visible heading.</h1>')
        self.assertEqual(len(self.headings()), 1)

    def test_hidden_scripts_attributes_and_paragraphs_are_not_headings(self):
        self.source('page.html', '<script>"<h1>Script title.</h1>"</script><style>.x { content: "Fake title." }</style><template><h1>Template.</h1></template><div hidden><h1>Hidden.</h1></div><h1 style="display: none">Hidden CSS.</h1><h1 title="Tooltip.">Clean heading</h1><p>This is a sentence. Another sentence.</p>')
        self.assertEqual(self.headings(), [])

    def test_title_exceptions(self):
        self.source('page.html', '<h1>What happens next?</h1><h2>Open...</h2><h2>Wait…</h2><h2>Built on Node.js</h2><h2>Version 1.2.3</h2><h2>Visit https://example.com</h2><h2>Logs, etc.</h2><h2>Made in the U.S.</h2>')
        self.assertEqual(self.headings(), [])

    def test_markdown_inline_formatting_and_staccato(self):
        self.declare('page.md')
        self.source('page.md', '## **Your tools.**\n\n## [Your agents.](https://example.com)\n\n## Your agents. Your tools.\n\n## <em>Build together.</em>\n\n```md\n# Example code.\n```\n\nA paragraph ends normally.\n')
        self.assertEqual(len(self.headings()), 4)

    def test_html_copy_does_not_read_attributes_as_quoted_literals(self):
        self.source('page.html', '<h1 data-copy="This is not public copy">Build <em>together</em></h1>')
        documents = brand_lint.documents(self.brand, brand_lint.load_sources(self.brand), 'marketing')
        self.assertIn('Build together', documents[0][2])
        self.assertNotIn('This is not public copy', documents[0][2])
        self.assertNotIn('<em>', documents[0][2])

    def test_empty_source_glob_is_error(self):
        self.declare('missing/**/*.html')
        findings = brand_lint.run(self.brand)
        self.assertTrue(any(f.code == 'B009' and f.severity == 'error' for f in findings))

    def test_blank_source_key_is_not_silently_omitted(self):
        (self.brand / 'README.md').write_text('Contract: brand-contract v1\nSources:\n  marketing: page.html\n  store: \n')
        self.assertTrue(any(f.code == 'B009' for f in brand_lint.run(self.brand)))

    def test_contract_brace_glob_and_overlapping_sources(self):
        self.declare('pages/*.{html,htm} pages/*.html')
        self.source('pages/index.html', '<h1>Start here.</h1>')
        self.source('pages/help.htm', '<h2>More help.</h2>')
        self.assertEqual(len(self.headings()), 2)
        self.assertFalse(any(f.code == 'B009' for f in brand_lint.run(self.brand)))

    def test_markdown_evidence_preserves_frontmatter_and_fence_lines(self):
        self.declare('page.md')
        self.source('page.md', '---\nchannel: landing hero\n---\n\n```md\n# Example.\n```\n\n## **Actual title.**\n')
        findings = self.headings()
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line, 9)

    def test_registry_html_does_not_sweep_attributes(self):
        self.source('page.html', '<h1 aria-label="Attribute text">Build <em>together</em></h1>')
        (self.brand / 'strings.md').write_text('Contract: brand-contract v1\n\n| Key | Text | Location | Scenario | Status |\n|---|---|---|---|---|\n| title.home | Build together | page.html:1 | SCN-001 | agreed |\n')
        findings = brand_lint.run(self.brand)
        self.assertFalse(any(f.code in {'B021', 'B022'} for f in findings), findings)

    def test_distributed_copy_rules_share_critical_guards(self):
        skill = (ROOT / 'plugins/super-ux/skills/copywriting/SKILL.md').read_text()
        cursor = (ROOT / 'cursor/rules/copywriting.mdc').read_text()
        for text in (skill, cursor):
            self.assertIn('No decorative full stop in headings or labels', text)
            self.assertIn('--fail-on B063', text)
            self.assertIn('paragraph punctuation', text)
            self.assertNotIn('Never write to `docs/brand/`', text)
        command = (ROOT / 'plugins/super-ux/commands/copy.md').read_text()
        self.assertIn('actual brand linter', command)
        self.assertIn('--fail-on B063', command)

    def test_unknown_selective_gate_code_is_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            brand_lint.main([str(self.brand), '--fail-on', 'B603'])
        self.assertEqual(raised.exception.code, 2)

    def test_cli_selective_warning_gate_and_json_contract(self):
        self.source('page.html', '<h1>Your workspace.</h1>')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = brand_lint.main([str(self.brand), '--json', '--fail-on', 'B063'])
        self.assertEqual(code, 1)
        self.assertIsInstance(json.loads(output.getvalue()), list)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(brand_lint.main([str(self.brand), '--brief']), 0)
        self.source('page.html', '<h1>Your workspace</h1>')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(brand_lint.main([str(self.brand), '--fail-on', 'B063']), 0)


if __name__ == '__main__':
    unittest.main()
