#!/usr/bin/env node
/*
 * Installer functional tests — the CLI and install.sh, against throwaway HOMEs.
 *
 * The case that earns this file its place is PLUGIN-PRESENT: this bin never
 * writes ~/.claude/skills itself, but its skills-menu item delegates to
 * `npx skills add`, which auto-detects Claude Code and writes
 * ~/.claude/skills/super-ux even when claude-code is never picked — a plain
 * copy that shadows the installed plugin and serves its frozen version
 * forever. Until v0.49.1 nothing consulted the target home before that
 * handoff, and every member's CI in this family tested a fresh HOME only, so
 * the plugin-present case had never run anywhere; reproduced live 2026-08-29
 * with a bare `npx @ssheleg/telegram-dev` shipping three shadows past the
 * same class of hole.
 *
 * The real skills CLI would hit the network and open an interactive picker,
 * so every case runs with a fake `npx` on PATH that records its argv and
 * exits 0 — what is asserted is whether the handoff happened at all.
 *
 * House residue rule: a passing case loses its temp HOME at exit, a failing
 * case KEEPS it (a defect is debugged by reading the tree it landed in), and
 * the run ends with one line saying what it left, `nothing` included.
 */
'use strict';

const { spawnSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const BIN = path.join(ROOT, 'bin', 'super-ux.js');
const SH = path.join(ROOT, 'install.sh');
const POSIX = process.platform !== 'win32';

let failures = 0;
const homes = []; // { dir, label, failed }

function freshHome(label) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'super-ux-test-home-'));
  homes.push({ dir, label, failed: false });
  return dir;
}

/**
 * A fake `npx` first on PATH, logging its argv to <home>/npx.log. POSIX-only
 * (a .cmd shim would be needed on win32); the suite skips those cases there.
 */
function fakeNpx(home) {
  const bin = path.join(home, 'fakebin');
  fs.mkdirSync(bin, { recursive: true });
  const log = path.join(home, 'npx.log');
  fs.writeFileSync(
    path.join(bin, 'npx'),
    `#!/bin/sh\necho "$@" >> "${log}"\nexit 0\n`
  );
  fs.chmodSync(path.join(bin, 'npx'), 0o755);
  return { bin, log };
}

function npxLog(home) {
  try {
    return fs.readFileSync(path.join(home, 'npx.log'), 'utf8');
  } catch {
    return '';
  }
}

function run(home, args, input) {
  const { bin } = fakeNpx(home);
  const r = spawnSync(process.execPath, [BIN, ...args], {
    cwd: home, // never the repo: npx inside the package's own repo resolves locally
    env: Object.assign({}, process.env, {
      HOME: home,
      USERPROFILE: home,
      PATH: `${bin}${path.delimiter}${process.env.PATH}`,
    }),
    input: input === undefined ? '' : input,
    encoding: 'utf8',
    timeout: 120000,
  });
  return { status: r.status, out: (r.stdout || '') + (r.stderr || '') };
}

function shRun(home, args) {
  const r = spawnSync('bash', [SH, ...args], {
    cwd: home,
    env: Object.assign({}, process.env, { HOME: home, USERPROFILE: home }),
    encoding: 'utf8',
    timeout: 120000,
  });
  return { status: r.status, out: (r.stdout || '') + (r.stderr || '') };
}

function skillDir(home) {
  return path.join(home, '.claude', 'skills', 'super-ux');
}

function declarePlugin(home, spec) {
  const dir = path.join(home, '.claude', 'plugins');
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'installed_plugins.json'), JSON.stringify({
    version: 2,
    plugins: { [spec]: [{ scope: 'user', installPath: '/nonexistent', version: '0.49.0' }] },
  }, null, 2));
}

function caseRun(label, fn) {
  const home = freshHome(label);
  const rec = homes[homes.length - 1];
  try {
    fn(home);
    console.log(`ok: ${label}`);
  } catch (e) {
    rec.failed = true;
    failures++;
    console.error(`FAIL: ${label}\n  ${e.message}`);
  }
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

// The refusal is only observable through the fake npx, so every case below
// needs POSIX. On win32 the suite still syntax-checks the CLI and exits.
{
  const r = spawnSync(process.execPath, ['--check', BIN], { encoding: 'utf8' });
  if (r.status !== 0) {
    console.error(`FAIL: node --check bin/super-ux.js\n${r.stderr}`);
    process.exit(1);
  }
  console.log('ok: node --check bin/super-ux.js');
}

if (!POSIX) {
  console.log('skip: installer cases (POSIX only — the fake npx is a shell script)');
  process.exit(0);
}

// ---------------------------------------------------------------- node CLI --

caseRun('fresh HOME: the skills handoff runs, and the run says how updates arrive', (home) => {
  const r = run(home, [], '1\n');
  assert(r.status === 0, `exit ${r.status}, expected 0\n${r.out}`);
  assert(npxLog(home).includes('skills add ssheleg/super-ux'),
    `the skills CLI was not invoked:\n${npxLog(home)}`);
  // the last thing an installer states is how the next version arrives
  assert(r.out.includes('sshlg-skills@latest update'), `no update path named:\n${r.out}`);
});

caseRun('plugin present in installed_plugins.json: refuse, exit 3, remedy, nothing delegated or written', (home) => {
  declarePlugin(home, 'super-ux@super-ux');
  const r = run(home, [], '1\n');
  assert(r.status === 3, `exit ${r.status}, expected 3\n${r.out}`);
  assert(r.out.includes('refused'), `no "refused" in output:\n${r.out}`);
  assert(r.out.includes('claude plugin update super-ux@super-ux'),
    `remedy does not name the plugin spec:\n${r.out}`);
  assert(r.out.includes('--force'), `override flag not offered:\n${r.out}`);
  assert(!npxLog(home).includes('skills add'),
    `the skills CLI ran despite the refusal:\n${npxLog(home)}`);
  assert(!fs.existsSync(skillDir(home)), 'a plain copy appeared despite the refusal');
});

caseRun('plugin under a differently-named marketplace: remedy names the real spec', (home) => {
  declarePlugin(home, 'super-ux@sshlg-skills');
  const r = run(home, [], '1\n');
  assert(r.status === 3, `exit ${r.status}, expected 3\n${r.out}`);
  assert(r.out.includes('claude plugin update super-ux@sshlg-skills'),
    `remedy does not carry the spec from the JSON:\n${r.out}`);
  assert(!npxLog(home).includes('skills add'),
    `the skills CLI ran despite the refusal:\n${npxLog(home)}`);
});

caseRun('--force overrides the refusal, deliberately', (home) => {
  declarePlugin(home, 'super-ux@super-ux');
  const r = run(home, ['--force'], '1\n');
  assert(r.status === 0, `exit ${r.status}, expected 0\n${r.out}`);
  assert(npxLog(home).includes('skills add ssheleg/super-ux'),
    `--force did not reach the skills CLI:\n${npxLog(home)}`);
});

caseRun('corrupt installed_plugins.json reads as "no plugin" — delegate, never crash', (home) => {
  const dir = path.join(home, '.claude', 'plugins');
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'installed_plugins.json'), '{ this is not json');
  const r = run(home, [], '1\n');
  assert(r.status === 0, `exit ${r.status}, expected 0 (fail open)\n${r.out}`);
  assert(npxLog(home).includes('skills add ssheleg/super-ux'),
    `the handoff did not happen:\n${npxLog(home)}`);
});

caseRun('other plugins, and a prefix-collider, do not trigger a false refusal', (home) => {
  const dir = path.join(home, '.claude', 'plugins');
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'installed_plugins.json'), JSON.stringify({
    version: 2,
    plugins: {
      'telegram-dev@telegram-dev': [{ scope: 'user', installPath: '/x', version: '1.0.0' }],
      'super-ux-extra@somewhere': [{ scope: 'user', installPath: '/y', version: '1.0.0' }],
    },
  }));
  const r = run(home, [], '1\n');
  assert(r.status === 0, `exit ${r.status}, expected 0\n${r.out}`);
  assert(npxLog(home).includes('skills add ssheleg/super-ux'),
    `the handoff did not happen:\n${npxLog(home)}`);
});

caseRun('marketplaces/<name> dir alone still refuses (fallback signal, exit 3)', (home) => {
  fs.mkdirSync(path.join(home, '.claude', 'plugins', 'marketplaces', 'super-ux'),
    { recursive: true });
  const r = run(home, [], '1\n');
  assert(r.status === 3, `exit ${r.status}, expected 3\n${r.out}`);
  assert(r.out.includes('claude plugin update super-ux@super-ux'),
    `no default remedy spec:\n${r.out}`);
  assert(!npxLog(home).includes('skills add'),
    `the skills CLI ran despite the refusal:\n${npxLog(home)}`);
});

caseRun('only the Claude Code channel is gated: --cursor installs beside the plugin', (home) => {
  declarePlugin(home, 'super-ux@super-ux');
  const proj = path.join(home, 'proj');
  fs.mkdirSync(proj);
  const r = run(home, ['--cursor', proj]);
  assert(r.status === 0, `exit ${r.status}, expected 0\n${r.out}`);
  assert(fs.existsSync(path.join(proj, '.cursor', 'rules')), 'no rules installed');
  assert(fs.existsSync(path.join(proj, 'docs', 'ux', 'scenarios.md')), 'no docs/ux seeded');
  assert(!fs.existsSync(skillDir(home)), 'the project install wrote into ~/.claude/skills');
  assert(r.out.includes('sshlg-skills@latest update'), `no update path named:\n${r.out}`);
});

caseRun('--help names the refusal exit code and writes nothing', (home) => {
  const r = run(home, ['--help']);
  assert(r.status === 0, `exit ${r.status}, expected 0\n${r.out}`);
  assert(/3 refused/.test(r.out), `exit code 3 not documented:\n${r.out}`);
  assert(!fs.existsSync(path.join(home, '.claude')), '--help wrote into the home');
});

// --------------------------------------------------------------- install.sh --

caseRun('install.sh never touches ~/.claude, so the gate does not apply to it', (home) => {
  // The sh installer's only mode is --cursor into a project; asserting that a
  // plugin-present home stays untouched is what documents the gate's scope.
  declarePlugin(home, 'super-ux@super-ux');
  const proj = path.join(home, 'proj');
  fs.mkdirSync(proj);
  const r = shRun(home, ['--cursor', proj]);
  assert(r.status === 0, `exit ${r.status}, expected 0\n${r.out}`);
  assert(fs.existsSync(path.join(proj, '.cursor', 'rules')), 'no rules installed');
  assert(!fs.existsSync(skillDir(home)), 'install.sh wrote into ~/.claude/skills');
});

// ----------------------------------------------------------------- residue --

let removed = 0;
const kept = [];
for (const h of homes) {
  if (h.failed) {
    kept.push(h);
  } else {
    fs.rmSync(h.dir, { recursive: true, force: true });
    removed++;
  }
}
if (kept.length === 0) {
  console.log(`residue: this run left nothing — ${homes.length} temp home(s) created, ${removed} removed`);
} else {
  console.log(`residue: ${kept.length} of ${homes.length} temp home(s) KEPT`);
  for (const h of kept) {
    console.log(`  ${h.dir}  (case: ${h.label})  — rm -rf '${h.dir}' when done`);
  }
}

if (failures) {
  console.error(`FAIL: installer — ${failures} case(s) red`);
  process.exit(1);
}
console.log(`PASS: installer — ${homes.length} case(s)`);
