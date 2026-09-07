import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const REPOSITORY_ROOT = new URL('..', import.meta.url).pathname;
const CLI = join(REPOSITORY_ROOT, 'bin', 'codex-agents.mjs');

function makeTemporaryDirectory() {
  return mkdtempSync(join(tmpdir(), 'codex-agents-test-'));
}

function makeSource(root, description = 'Read-only planner.') {
  const agents = join(root, '.codex', 'agents');
  mkdirSync(agents, { recursive: true });
  writeFileSync(
    join(agents, 'planner.toml'),
    `name = "planner"\ndescription = "${description}"\nmodel = "gpt-6-astra"\nmodel_reasoning_effort = "medium"\nsandbox_mode = "read-only"\ndeveloper_instructions = "Read only."\n`,
  );
}

function run(args, cwd) {
  return spawnSync(process.execPath, [CLI, ...args], { cwd, encoding: 'utf8' });
}

test('lists agents without changing the project', () => {
  const root = makeTemporaryDirectory();
  const source = makeTemporaryDirectory();
  try {
    makeSource(source);
    const result = run(['add', source, '--list'], root);
    assert.equal(result.status, 0, result.stderr);
    assert.equal(result.stdout.trim(), 'planner');
    assert.equal(readFileSync(join(source, '.codex', 'agents', 'planner.toml'), 'utf8').includes('planner'), true);
  } finally {
    rmSync(root, { recursive: true, force: true });
    rmSync(source, { recursive: true, force: true });
  }
});

test('installs a selected agent and records a project lock', () => {
  const root = makeTemporaryDirectory();
  const source = makeTemporaryDirectory();
  try {
    makeSource(source);
    const result = run(['add', source, '--agent', 'planner'], root);
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /Installed planner/);
    const target = join(root, '.codex', 'agents', 'planner.toml');
    assert.equal(readFileSync(target, 'utf8'), readFileSync(join(source, '.codex', 'agents', 'planner.toml'), 'utf8'));
    const lock = JSON.parse(readFileSync(join(root, '.codex', 'agents-lock.json'), 'utf8'));
    assert.equal(lock.version, 1);
    assert.equal(lock.agents.planner.source, source);
  } finally {
    rmSync(root, { recursive: true, force: true });
    rmSync(source, { recursive: true, force: true });
  }
});

test('refuses to overwrite a locally modified agent', () => {
  const root = makeTemporaryDirectory();
  const source = makeTemporaryDirectory();
  try {
    makeSource(source);
    assert.equal(run(['add', source], root).status, 0);
    const target = join(root, '.codex', 'agents', 'planner.toml');
    writeFileSync(target, 'name = "planner"\n# local change\n');
    const result = run(['add', source], root);
    assert.equal(result.status, 1);
    assert.match(result.stderr, /Refusing to overwrite locally modified/);
    assert.match(readFileSync(target, 'utf8'), /local change/);

    const forced = run(['add', source, '--force'], root);
    assert.equal(forced.status, 0, forced.stderr);
    assert.doesNotMatch(readFileSync(target, 'utf8'), /local change/);
  } finally {
    rmSync(root, { recursive: true, force: true });
    rmSync(source, { recursive: true, force: true });
  }
});

test('updates a lock-managed agent and supports a global target override', () => {
  const root = makeTemporaryDirectory();
  const source = makeTemporaryDirectory();
  const globalHome = makeTemporaryDirectory();
  try {
    makeSource(source, 'First version.');
    assert.equal(run(['add', source], root).status, 0);
    makeSource(source, 'Second version.');
    const update = run(['update'], root);
    assert.equal(update.status, 0, update.stderr);
    assert.match(readFileSync(join(root, '.codex', 'agents', 'planner.toml'), 'utf8'), /Second version/);

    const global = run(['add', source, '--global', '--codex-home', globalHome], root);
    assert.equal(global.status, 0, global.stderr);
    assert.equal(readFileSync(join(globalHome, 'agents', 'planner.toml'), 'utf8').includes('Second version'), true);
  } finally {
    rmSync(root, { recursive: true, force: true });
    rmSync(source, { recursive: true, force: true });
    rmSync(globalHome, { recursive: true, force: true });
  }
});
