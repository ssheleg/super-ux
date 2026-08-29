#!/usr/bin/env node
/*
 * super-ux installer CLI.
 *
 * No arguments: interactive multi-select menu (arrow keys + space, `a` for
 * all) covering: skills for any agent via the `skills` CLI picker, Cursor
 * rules into a project, Claude Code plugin user-globally. Non-TTY stdin gets
 * a text fallback ("1,3" / "all"). Flags keep the non-interactive paths:
 * --cursor [dir] [--force].
 *
 * The skills handoff is gated: while super-ux is installed as a Claude Code
 * plugin, delegating to the skills CLI would recreate the plain
 * ~/.claude/skills/super-ux copy that shadows the plugin, so the handoff is
 * refused (exit 3) unless --force records the two-channel choice.
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const readline = require('readline');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const REPO = 'ssheleg/super-ux';
const NAME = 'super-ux';

// Exit codes are the contract: 0 installed or nothing selected, 1 error,
// 3 refused — the plugin channel owns this agent (--force overrides).
const EXIT_PLUGIN_PRESENT = 3;

/**
 * The plugin spec (`<name>@<marketplace>`) installed for `name` in this home,
 * or null.
 *
 * `installed_plugins.json` is the record of what is actually installed. The
 * `plugins/marketplaces/<name>` directory under-reports: a marketplace added
 * from a local `directory` source has no dir there at all, and plugin names
 * differ from marketplace names, so a check keyed on it stays green while the
 * shadow lands. Absence and corruption both read as "no plugin": the fresh
 * HOME is the common case, and an installer that crashes on a parse error
 * refuses the machines that need it most.
 */
function installedPluginSpec(home, name) {
  try {
    const raw = fs.readFileSync(
      path.join(home, '.claude', 'plugins', 'installed_plugins.json'), 'utf8');
    const parsed = JSON.parse(raw);
    const plugins =
      parsed && typeof parsed === 'object' &&
      parsed.plugins && typeof parsed.plugins === 'object'
        ? parsed.plugins
        : parsed;
    if (!plugins || typeof plugins !== 'object') return null;
    for (const spec of Object.keys(plugins)) {
      if (spec === name) return `${name}@${name}`;
      if (spec.startsWith(name + '@')) return spec;
    }
  } catch {
    // missing or corrupt = no plugin — fail open on absence, never crash
  }
  return null;
}

const MENU_ITEMS = [
  { key: 'skills', label: 'Skills for any AI agent (Claude Code, Codex, Cursor, 70+; opens agent picker)' },
  { key: 'cursor', label: 'Cursor rules + docs/ux skeleton + docs/brand pack + linters, into a project' },
  { key: 'claude', label: 'Claude Code plugin (skills + /ux commands, user-global)' },
];

function usage() {
  console.log(`super-ux installer

Usage:
  npx super-ux [--force]                        interactive menu (multi-select)
  npx super-ux --cursor [project-dir] [--force] Cursor rules, non-interactive
  npx super-ux --help

Exit codes:
  0 installed or nothing selected   1 error
  3 refused: the super-ux PLUGIN is installed in this home, and the skills
    CLI would write the plain ~/.claude/skills copy that shadows it
    (pass --force to run the picker anyway)

Menu items (select any combination, 'a' = all):
  1. Skills for any AI agent (Claude Code, Codex, Cursor, 70+) — delegates to
     'npx skills add ${REPO}' with its agent/global/project picker.
     Refused while the super-ux plugin is installed (see exit code 3).
  2. Cursor rules: cursor/rules/*.mdc -> <project>/.cursor/rules/, plus the
     docs/ux skeleton, the docs/brand pack, and all three linters
     (docs/ux/lint.py, docs/ux/doctor.py, docs/brand/lint.py). Existing
     scenario base and brand pack are NEVER overwritten; existing rule files
     are skipped unless --force. docs/ux/vision.md is not seeded: an empty
     vision reads as a decided one — write it with the vision skill.
  3. Claude Code plugin (skills + /ux commands, user-global) — runs
     'claude plugin marketplace add ${REPO}' + 'claude plugin install' when
     the claude CLI is available, otherwise prints the /plugin commands.`);
}

function fail(message) {
  console.error(`error: ${message}`);
  process.exit(1);
}

function installCursor(target, force) {
  if (!fs.existsSync(target) || !fs.statSync(target).isDirectory()) {
    fail(`'${target}' is not a directory`);
  }

  const rulesSrc = path.join(ROOT, 'cursor', 'rules');
  const rulesDst = path.join(target, '.cursor', 'rules');
  fs.mkdirSync(rulesDst, { recursive: true });

  let installed = 0;
  let skipped = 0;
  let seeded = 0;
  const rules = fs.readdirSync(rulesSrc).filter((f) => f.endsWith('.mdc')).sort();
  if (rules.length === 0) fail(`no .mdc rules found in ${rulesSrc}`);

  for (const name of rules) {
    const dst = path.join(rulesDst, name);
    if (fs.existsSync(dst) && !force) {
      console.log(`skip:    ${dst} exists (use --force to overwrite)`);
      skipped += 1;
    } else {
      fs.copyFileSync(path.join(rulesSrc, name), dst);
      console.log(`install: ${dst}`);
      installed += 1;
    }
  }

  for (const dir of ['audits', 'plans']) {
    fs.mkdirSync(path.join(target, 'docs', 'ux', dir), { recursive: true });
  }
  for (const tpl of ['scenarios', 'foundation', 'flows', 'screens', 'README']) {
    const dst = path.join(target, 'docs', 'ux', `${tpl}.md`);
    if (fs.existsSync(dst)) {
      console.log(`keep:    ${dst} exists (never overwritten)`);
    } else {
      fs.copyFileSync(path.join(ROOT, 'templates', `${tpl}.md`), dst);
      console.log(`seed:    ${dst}`);
      seeded += 1;
    }
  }
  // The brand pack lives beside the UX chain, not inside it: it also governs
  // surfaces that are not UX at all — a store listing, an ad, a post.
  fs.mkdirSync(path.join(target, 'docs', 'brand', 'locales'), { recursive: true });
  for (const tpl of [
    'README', 'voice', 'terminology', 'facts', 'channels', 'strings',
  ]) {
    const dst = path.join(target, 'docs', 'brand', `${tpl}.md`);
    if (fs.existsSync(dst)) {
      console.log(`keep:    ${dst} exists (never overwritten)`);
    } else {
      fs.copyFileSync(path.join(ROOT, 'templates', 'brand', `${tpl}.md`), dst);
      console.log(`seed:    ${dst}`);
      seeded += 1;
    }
  }
  {
    const dst = path.join(target, 'docs', 'brand', 'locales', 'en.md');
    if (!fs.existsSync(dst)) {
      fs.copyFileSync(path.join(ROOT, 'templates', 'brand', 'locale.md'), dst);
      console.log(`seed:    ${dst}`);
      seeded += 1;
    }
  }

  // The linter is code, not a template — refresh it to the shipped version.
  // Shipped via package.json files[]; if that ever regresses, warn instead of
  // dying on an ENOENT stack trace after the rules are already installed.
  // Paths stay literal so test/validate.py can read them out of this source and
  // check them against package.json files[] — a variable segment here silently
  // turns that check into a directory prefix nobody ships.
  for (const [src, from, area, dst] of [
    ['ux_lint.py', path.join(ROOT, 'plugins', 'super-ux', 'scripts', 'ux_lint.py'), 'ux', 'lint.py'],
    ['ux_doctor.py', path.join(ROOT, 'plugins', 'super-ux', 'scripts', 'ux_doctor.py'), 'ux', 'doctor.py'],
    ['brand_lint.py', path.join(ROOT, 'plugins', 'super-ux', 'scripts', 'brand_lint.py'), 'brand', 'lint.py'],
  ]) {
    const to = path.join(target, 'docs', area, dst);
    if (fs.existsSync(from)) {
      fs.copyFileSync(from, to);
      console.log(`sync:    ${to}`);
    } else {
      console.error(
        `warning: ${src} not found in this package (${from}); docs/${area}/${dst} was not installed.\n` +
          `         Get it from https://github.com/${REPO}/blob/main/plugins/super-ux/scripts/${src}`
      );
    }
  }

  // Report what happened, not one third of it: the old line counted rules
  // only, so a run that wrote twenty files announced eight.
  console.log(
    `done: ${installed} rule(s) installed, ${skipped} skipped, ` +
      `${seeded} doc(s) seeded, linters synced`
  );
}

function run(cmd, args) {
  const result = spawnSync(cmd, args, { stdio: 'inherit' });
  if (result.error && result.error.code === 'ENOENT') return 'missing';
  return result.status === 0 ? 'ok' : 'failed';
}

/**
 * One channel per agent. The skills CLI auto-detects Claude Code and writes
 * ~/.claude/skills/super-ux even when claude-code is never picked, and on a
 * machine where super-ux is installed as a Claude Code plugin that plain copy
 * shadows the plugin and serves the version it was copied from forever. So
 * the handoff consults the TARGET home's installed_plugins.json first and
 * refuses LOUDLY: a refusal that exits 0 reads as success to every script
 * above it. The marketplaces/<name> dir is only the fallback signal — a
 * directory-sourced marketplace has no dir there, and plugin names differ
 * from marketplace names. Reproduced live 2026-08-29: a bare
 * `npx @ssheleg/telegram-dev` shipped three shadows past exactly this class
 * of hole while the plugin was enabled.
 */
function installSkillsCli(force) {
  const home = os.homedir();
  const spec = installedPluginSpec(home, NAME);
  const marketplace = path.join(home, '.claude', 'plugins', 'marketplaces', NAME);
  const viaMarketplaceDir = !spec && fs.existsSync(marketplace);
  if ((spec || viaMarketplaceDir) && !force) {
    const found = spec
      ? `installed as the Claude Code plugin ${spec}\n` +
        '         (declared in ~/.claude/plugins/installed_plugins.json)'
      : `registered as a Claude Code marketplace\n         (${marketplace})`;
    console.error(
      `refused: super-ux is already ${found}.\n` +
      '         The skills CLI auto-detects Claude Code and would write a plain copy\n' +
      '         to ~/.claude/skills/super-ux, which shadows the plugin and serves the\n' +
      '         version it was copied from forever. Update the plugin channel instead:\n' +
      '           claude plugin marketplace update super-ux\n' +
      `           claude plugin update ${spec || 'super-ux@super-ux'}\n` +
      '         Family launcher (updates every member, prunes shadow copies):\n' +
      '           npx --yes sshlg-skills@latest update\n' +
      '         Pass --force (npx super-ux --force) to run the picker anyway: a\n' +
      '         deliberate choice to run two channels, where the stale one wins.'
    );
    return 'refused';
  }
  console.log(`\n--- Skills for any agent: delegating to the skills CLI picker ---`);
  const status = run('npx', ['--yes', 'skills', 'add', REPO]);
  if (status !== 'ok') console.error(`warning: 'npx skills add ${REPO}' ${status}`);
  return status;
}

/**
 * The last line of a successful run says how the next version arrives —
 * "Installed" is not a complete sentence. Auto-update is off on purpose:
 * this member composes with its family, and per-marketplace autoUpdate moves
 * each member on its own clock, into combinations nobody tested together.
 */
function printUpdateLine() {
  console.log(
    '\nUpdates: rerun npx super-ux@latest (--cursor <dir> --force refreshes a\n' +
    "project's rules and linters), or refresh the whole family with\n" +
    'npx --yes sshlg-skills@latest update (every channel, and it prunes plain\n' +
    'copies that would shadow a plugin).'
  );
}

function installClaudePlugin() {
  console.log(`\n--- Claude Code plugin ---`);
  const probe = spawnSync('claude', ['--version'], { stdio: 'ignore' });
  if (probe.error && probe.error.code === 'ENOENT') {
    console.log(`claude CLI not found. Run inside Claude Code instead:
  /plugin marketplace add ${REPO}
  /plugin install super-ux@super-ux`);
    return;
  }
  if (run('claude', ['plugin', 'marketplace', 'add', REPO]) !== 'ok') {
    console.log('(marketplace may already be added, continuing)');
  }
  if (run('claude', ['plugin', 'install', 'super-ux@super-ux']) === 'ok') {
    console.log('Claude Code plugin installed (scope: user). Restart sessions to pick it up; then run /ux in any project.');
  } else {
    console.error('warning: claude plugin install failed, see output above');
  }
}

function makePrompter() {
  // A persistent 'line' listener with a buffer: with piped stdin, lines that
  // arrive between two questions are kept instead of being lost.
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const buffered = [];
  let pending = null;
  let closed = false;
  rl.on('line', (line) => {
    if (pending) {
      const resolve = pending;
      pending = null;
      resolve(line);
    } else {
      buffered.push(line);
    }
  });
  rl.on('close', () => {
    closed = true;
    if (pending) {
      const resolve = pending;
      pending = null;
      resolve('');
    }
  });
  return {
    ask(question) {
      process.stdout.write(question);
      if (buffered.length > 0) return Promise.resolve(buffered.shift());
      if (closed) return Promise.resolve('');
      return new Promise((resolve) => {
        pending = resolve;
      });
    },
    close() {
      rl.close();
    },
  };
}

function parseSelection(input, count) {
  const value = input.trim().toLowerCase();
  if (value === '' || value === 'q' || value === 'quit') return [];
  if (value === 'a' || value === 'all' || value === '*') {
    return Array.from({ length: count }, (_, i) => i);
  }
  const picked = new Set();
  for (const part of value.split(/[\s,]+/)) {
    if (part === '') continue;
    const n = Number(part);
    if (!Number.isInteger(n) || n < 1 || n > count) return null;
    picked.add(n - 1);
  }
  return [...picked].sort();
}

function selectInteractive(items) {
  // Raw-mode checkbox list: up/down or j/k move, space or 1..9 toggle,
  // a = toggle all, enter = confirm, q/esc/ctrl+c = quit.
  return new Promise((resolve) => {
    const selected = new Set();
    let cursor = 0;
    let rendered = false;

    const line = (i) =>
      `${i === cursor ? '❯' : ' '} ${selected.has(i) ? '◉' : '◯'} ${i + 1}) ${items[i].label}`;

    const render = () => {
      if (rendered) process.stdout.write(`\x1b[${items.length + 1}A`);
      for (let i = 0; i < items.length; i += 1) {
        process.stdout.write(`\x1b[2K${line(i)}\n`);
      }
      process.stdout.write(
        '\x1b[2K  ↑/↓ move · space/number toggle · a all · enter confirm · q quit\n'
      );
      rendered = true;
    };

    const finish = (result) => {
      process.stdin.setRawMode(false);
      process.stdin.pause();
      process.stdin.removeListener('keypress', onKeypress);
      resolve(result);
    };

    const onKeypress = (str, key) => {
      const name = key && key.name;
      if ((key && key.ctrl && name === 'c') || name === 'escape' || str === 'q') {
        finish([]);
        return;
      }
      if (name === 'up' || str === 'k') cursor = (cursor - 1 + items.length) % items.length;
      else if (name === 'down' || str === 'j') cursor = (cursor + 1) % items.length;
      else if (name === 'space') {
        if (selected.has(cursor)) selected.delete(cursor);
        else selected.add(cursor);
      } else if (str === 'a') {
        if (selected.size === items.length) selected.clear();
        else for (let i = 0; i < items.length; i += 1) selected.add(i);
      } else if (str && /^[1-9]$/.test(str) && Number(str) <= items.length) {
        const idx = Number(str) - 1;
        if (selected.has(idx)) selected.delete(idx);
        else selected.add(idx);
        cursor = idx;
      } else if (name === 'return') {
        finish([...selected].sort());
        return;
      }
      render();
    };

    readline.emitKeypressEvents(process.stdin);
    process.stdin.setRawMode(true);
    process.stdin.resume();
    process.stdin.on('keypress', onKeypress);
    render();
  });
}

async function selectFallback(items, prompter) {
  for (let i = 0; i < items.length; i += 1) {
    console.log(`  ${i + 1}) ${items[i].label}`);
  }
  const answer = await prompter.ask(`Select [e.g. 1,3 | all | q]: `);
  const picked = parseSelection(answer, items.length);
  if (picked === null) fail(`invalid selection '${answer.trim()}'`);
  return picked;
}

async function menu(force) {
  console.log('super-ux: scenario-driven UI development. Select what to install:\n');
  const interactive = Boolean(process.stdin.isTTY && process.stdout.isTTY);

  // ONE prompter for the whole flow: with piped stdin, all pending lines are
  // buffered by its persistent listener; a second prompter would lose them.
  let prompter = null;
  let picked;
  if (interactive) {
    picked = await selectInteractive(MENU_ITEMS);
  } else {
    prompter = makePrompter();
    picked = await selectFallback(MENU_ITEMS, prompter);
  }

  if (picked.length === 0) {
    if (prompter) prompter.close();
    console.log('Nothing selected');
    return;
  }

  const keys = picked.map((i) => MENU_ITEMS[i].key);

  // Gather all our own questions BEFORE running anything, so they don't
  // interleave with the external skills-CLI picker.
  let cursorDir = null;
  if (keys.includes('cursor')) {
    if (!prompter) prompter = makePrompter();
    const dir = (await prompter.ask('Cursor rules, project directory [.]: ')).trim() || '.';
    cursorDir = path.resolve(dir);
  }
  if (prompter) prompter.close();

  if (keys.includes('cursor')) installCursor(cursorDir, false);
  if (keys.includes('claude')) installClaudePlugin();
  let refused = false;
  if (keys.includes('skills')) refused = installSkillsCli(force) === 'refused';

  // Same offer the --cursor flag path makes. Two doors into one install that
  // behave differently is how a feature comes to exist for half its users.
  // Offered on the refused path too: the skill IS present on this machine —
  // as the plugin — so the routing block is exactly as wanted.
  offerRouters();
  if (refused) {
    // The refusal already carries the update commands; repeating the update
    // line under it would bury the remedy. Exit 3 so scripts read the refusal.
    process.exitCode = EXIT_PLUGIN_PRESENT;
  } else {
    printUpdateLine();
  }
}

/**
 * Ask the launcher to write the family's routing block.
 *
 * Delegated rather than reimplemented. The block lists several routers and a
 * precedence table describing what this machine actually has, so a lone
 * member rendering it would produce a table for routers nobody installed.
 * `--no-install` keeps this from silently downloading a package the user did
 * not ask for; when the launcher is absent we print the one command instead.
 */
function offerRouters() {
  const { spawnSync } = require('child_process');
  const r = spawnSync(
    'npx',
    ['--no-install', 'sshlg-skills', 'routers', '--member', 'super-ux'],
    { stdio: 'inherit', shell: process.platform === 'win32' }
  );
  if (r.status !== 0) {
    console.log(
      '\nTo have these skills apply by default in every project, add the\n' +
      "family's routing block to your agent's global instructions:\n\n" +
      '  npx --yes sshlg-skills routers --member super-ux\n'
    );
  }
}

function main() {
  const args = process.argv.slice(2);
  if (args[0] === '--help' || args[0] === '-h') {
    usage();
    return;
  }
  if (args.length === 0) {
    menu(false);
    return;
  }
  // `--force` alone still opens the menu: it is the named override for the
  // skills-handoff refusal, so it must be reachable from the same door the
  // refusal names.
  if (args.length === 1 && args[0] === '--force') {
    menu(true);
    return;
  }
  if (args[0] !== '--cursor') {
    console.error(`error: unknown mode '${args[0]}'`);
    usage();
    process.exit(1);
  }
  const force = args.includes('--force');
  const dirArg = args[1] && args[1] !== '--force' ? args[1] : '.';
  installCursor(path.resolve(dirArg), force);
  offerRouters();
  printUpdateLine();
}

main();
