#!/usr/bin/env node
/*
 * super-ux installer CLI.
 * Cross-platform equivalent of install.sh: copies Cursor rules into a target
 * project and seeds the docs/ux skeleton. Claude Code needs no installer —
 * see usage.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

function usage() {
  console.log(`super-ux installer

Usage:
  npx github:ssheleg/super-ux --cursor [project-dir] [--force]
  npx super-ux --cursor [project-dir] [--force]        (once published to npm)

Copies cursor/rules/*.mdc into <project-dir>/.cursor/rules/ (default:
current directory) and seeds docs/ux/scenarios.md from templates/ if absent.
An existing scenario base is NEVER overwritten. Existing rule files are
skipped unless --force is given.

Claude Code (no installer needed):
  /plugin marketplace add ssheleg/super-ux
  /plugin install super-ux@super-ux
  Then in your project: /ux`);
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

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    usage();
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
