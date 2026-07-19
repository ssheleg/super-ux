#!/usr/bin/env node
/*
 * super-ux installer CLI.
 *
 * No arguments: interactive menu (skills for any agent via the `skills` CLI
 * picker, Cursor rules into a project, Claude Code plugin user-globally).
 * Flags keep the non-interactive paths: --cursor [dir] [--force].
 */
'use strict';

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const REPO = 'ssheleg/super-ux';

function usage() {
  console.log(`super-ux installer

Usage:
  npx super-ux                                  interactive menu
  npx super-ux --cursor [project-dir] [--force] Cursor rules, non-interactive
  npx super-ux --help

Menu options (also available directly):
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

  const base = path.join(target, 'docs', 'ux', 'scenarios.md');
  if (fs.existsSync(base)) {
    console.log(`keep:    ${base} exists (never overwritten)`);
  } else {
    fs.mkdirSync(path.join(target, 'docs', 'ux', 'audits'), { recursive: true });
    fs.copyFileSync(path.join(ROOT, 'templates', 'scenarios.md'), base);
    console.log(`seed:    ${base}`);
  }

  console.log(`done: ${installed} installed, ${skipped} skipped`);
}

function run(cmd, args) {
  const result = spawnSync(cmd, args, { stdio: 'inherit' });
  if (result.error && result.error.code === 'ENOENT') return 'missing';
  return result.status === 0 ? 'ok' : 'failed';
}

function installSkillsCli() {
  console.log(`Delegating to the skills CLI (agent/global/project picker)...`);
  const status = run('npx', ['--yes', 'skills', 'add', REPO]);
  if (status !== 'ok') fail(`'npx skills add ${REPO}' ${status}`);
}

function installClaudePlugin() {
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
    fail('claude plugin install failed — see output above');
  }
}

function makePrompter() {
  // A persistent 'line' listener with a buffer: with piped stdin, lines that
  // arrive between two questions are kept instead of being lost (which is
  // what plain sequential rl.question() does).
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

async function menu() {
  const prompter = makePrompter();
  console.log(`super-ux — scenario-driven UI development. What do you want to install?

  1) Skills for any AI agent (Claude Code, Codex, Cursor, 70+ — interactive picker)
  2) Cursor rules (always-on hard rule + docs/ux skeleton) into a project
  3) Claude Code plugin (skills + /ux commands, user-global)
  q) Quit
`);
  const choice = (await prompter.ask('Choice [1/2/3/q]: ')).trim().toLowerCase();
  if (choice === '1') {
    prompter.close();
    installSkillsCli();
  } else if (choice === '2') {
    const dir = (await prompter.ask('Project directory [.]: ')).trim() || '.';
    prompter.close();
    installCursor(path.resolve(dir), false);
  } else if (choice === '3') {
    prompter.close();
    installClaudePlugin();
  } else {
    prompter.close();
    if (choice !== 'q' && choice !== '') fail(`unknown choice '${choice}'`);
  }
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
