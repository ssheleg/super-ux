#!/bin/sh
# One-shot finalize for v0.12.1 (consistency-audit release).
# Run from the repo root: sh scripts/finalize-0.12.1.sh
set -e
cd "$(dirname "$0")/.."

echo "=== installer tests ==="
node --check bin/super-ux.js && echo "SYNTAX OK"
T1=$(mktemp -d); ./install.sh --cursor "$T1" | tail -3
[ -f "$T1/docs/ux/foundation.md" ] && [ -f "$T1/docs/ux/flows.md" ] && echo "SH-SEED OK"
T2=$(mktemp -d); node bin/super-ux.js --cursor "$T2" >/dev/null
echo marker >> "$T2/docs/ux/foundation.md"
node bin/super-ux.js --cursor "$T2" >/dev/null
grep -q marker "$T2/docs/ux/foundation.md" && echo "JS-KEEP OK"
rm -rf "$T1" "$T2"

echo "=== validate ==="
python3 test/validate.py

echo "=== commit + push ==="
git add -A
git commit -q -m "fix: consistency audit - templates to contract v3, unified hard rule, chain-aware ux-update, installers seed all templates (v0.12.1)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" || echo "(nothing to commit)"
git push -q origin main && echo PUSHED

echo "=== plugin update ==="
claude plugin update super-ux@super-ux 2>&1 | tail -1
echo "=== DONE — this script can be deleted ==="
