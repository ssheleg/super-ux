#!/usr/bin/env node
/*
 * super-ux installer CLI.
 *
 * No arguments: interactive multi-select menu (arrow keys + space, `a` for
 * all) covering: skills for any agent via the `skills` CLI picker, Cursor
 * rules into a project, Claude Code plugin user-globally. Non-TTY stdin gets
 * a text fallback ("1,3" / "all"). Flags keep the non-interactive paths:
 * --cursor [dir] [--force].
 */
'use strict';

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const REPO = 'ssheleg/super-ux';

const MENU_ITEMS = [
  { key: 'skills', label: 'Skills for any AI agent (Claude Code, Codex, Cursor, 70+ — opens agent picker)' },
  { key: 'cursor', label: 'Cursor rules (always-on hard rule + docs/ux skeleton) into a project' },
  { key: 'claude', label: 'Claude Code plugin (skills + /ux commands, user-global)' },
];

function usage() {
  console.log(`super-ux installer

Usage:
  npx super-ux                                  interactive menu (multi-select)
  npx super-ux --cursor [project-dir] [--force] Cursor rules, non-interactive
  npx super-ux --help

Menu items (select any combination, 'a' = all):
  1. Skills for any AI agent (Claude Code, Codex, Cursor, 70+) — delegates to
     'npx skills add ${REPO}' with its agent/global/project picker.
  2. Cursor rules: cursor/rules/*.mdc -> <project>/.cursor/rules/ plus the
     docs/ux skeleton. Existing scenario base is NEVER overwritten; existing
     rule files are skipped unless --force.
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

  fs.mkdirSync(path.join(target, 'docs', 'ux', 'audits'), { recursive: true });
  for (const tpl of ['scenarios', 'foundation', 'flows', 'screens']) {
    const dst = path.join(target, 'docs', 'ux', `${tpl}.md`);
    if (fs.existsSync(dst)) {
      console.log(`keep:    ${dst} exists (never overwritten)`);
    } else {
      fs.copyFileSync(path.join(ROOT, 'templates', `${tpl}.md`), dst);
      console.log(`seed:    ${dst}`);
    }
  }

  console.log(`done: ${installed} installed, ${skipped} skipped`);
}

function run(cmd, args) {
  const result = spawnSync(cmd, args, { stdio: 'inherit' });
  if (result.error && result.error.code === 'ENOENT') return 'missing';
  return result.status === 0 ? 'ok' : 'failed';
}

function installSkillsCli() {
  console.log(`\n--- Skills for any agent: delegating to the skills CLI picker ---`);
  const status = run('npx', ['--yes', 'skills', 'add', REPO]);
  if (status !== 'ok') console.error(`warning: 'npx skills add ${REPO}' ${status}`);
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
    console.log('(marketplace may already be added — continuing)');
  }
  if (run('claude', ['plugin', 'install', 'super-ux@super-ux']) === 'ok') {
    console.log('Claude Code plugin installed (scope: user). Restart sessions to pick it up; then run /ux in any project.');
  } else {
    console.error('warning: claude plugin install failed — see output above');
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

async function menu() {
  console.log('super-ux — scenario-driven UI development. Select what to install:\n');
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
    console.log('Nothing selected.');
    return;
  }

  const keys = picked.map((i) => MENU_ITEMS[i].key);

  // Gather all our own questions BEFORE running anything, so they don't
  // interleave with the external skills-CLI picker.
  let cursorDir = null;
  if (keys.includes('cursor')) {
    if (!prompter) prompter = makePrompter();
    const dir = (await prompter.ask('Cursor rules — project directory [.]: ')).trim() || '.';
    cursorDir = path.resolve(dir);
  }
  if (prompter) prompter.close();

  if (keys.includes('cursor')) installCursor(cursorDir, false);
  if (keys.includes('claude')) installClaudePlugin();
  if (keys.includes('skills')) installSkillsCli();
}

function main() {
  const args = process.argv.slice(2);
  if (args[0] === '--help' || args[0] === '-h') {
    usage();
    return;
  }
  if (args.length === 0) {
    menu();
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
}

main();
