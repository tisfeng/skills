import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { homedir, tmpdir } from 'node:os';
import { basename, dirname, isAbsolute, join, resolve } from 'node:path';

const LOCK_VERSION = 1;

function usage() {
  return `Usage:
  codex-agents add <git-source[#ref]|local-path> [--agent <name>] [--global] [--force]
  codex-agents add <git-source[#ref]|local-path> --list
  codex-agents update [--agent <name>] [--global] [--force]

Options:
  --agent <name>       Install or update one agent. Repeatable; '*' selects every agent.
  --global             Use ~/.codex/agents instead of the current project's .codex/agents.
  --force              Replace a file whose contents differ from its recorded lock hash.
  --list               List the agents available in a source without writing files.
  --codex-home <path>  Override the global Codex home (useful for testing and automation).
  --help               Show this help text.

Git sources may select a revision with #ref. Local paths always use their current checkout.`;
}

function sha256(content) {
  return createHash('sha256').update(content).digest('hex');
}

function parseArgs(argv) {
  const options = { agents: [], force: false, global: false, list: false, codexHome: null };
  const positional = [];

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--agent') {
      const agent = argv[++index];
      if (!agent) throw new Error('--agent requires a name');
      options.agents.push(agent);
    } else if (value === '--global') {
      options.global = true;
    } else if (value === '--force') {
      options.force = true;
    } else if (value === '--list') {
      options.list = true;
    } else if (value === '--codex-home') {
      options.codexHome = argv[++index];
      if (!options.codexHome) throw new Error('--codex-home requires a path');
    } else if (value === '--help' || value === '-h') {
      options.help = true;
    } else if (value.startsWith('-')) {
      throw new Error(`Unknown option: ${value}`);
    } else {
      positional.push(value);
    }
  }

  return { options, positional };
}

function splitSource(source) {
  const separator = source.lastIndexOf('#');
  return separator === -1
    ? { location: source, ref: null, hasRef: false }
    : { location: source.slice(0, separator), ref: source.slice(separator + 1) || null, hasRef: true };
}

function isLocalSource(location) {
  return location.startsWith('.') || location.startsWith('/') || isAbsolute(location);
}

function gitOutput(args, cwd) {
  return execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

function sourceUrl(location) {
  if (location.includes('://') || location.startsWith('git@')) return location;
  if (/^[^/]+\/[^/]+$/.test(location)) return `https://github.com/${location}.git`;
  throw new Error(`Unsupported source: ${location}. Use owner/repo, a Git URL, or a local path.`);
}

function withSource(source, callback) {
  const { location, ref, hasRef } = splitSource(source);
  if (isLocalSource(location)) {
    const root = resolve(location);
    if (!existsSync(root)) throw new Error(`Source path does not exist: ${root}`);
    if (hasRef) {
      throw new Error(
        `Local source refs are not supported: ${source}. Use the local checkout directly or a Git URL with #ref.`,
      );
    }
    let revision = 'local';
    try {
      revision = gitOutput(['rev-parse', 'HEAD'], root);
    } catch {
      // A local directory is useful for development even before its first commit.
    }
    return callback({ root, revision, source, ref: ref ?? 'HEAD' });
  }

  const temporaryRoot = mkdtempSync(join(tmpdir(), 'codex-agents-'));
  const cloneDirectory = join(temporaryRoot, 'source');
  try {
    const args = ['clone', '--depth', '1'];
    if (ref) args.push('--branch', ref);
    args.push(sourceUrl(location), cloneDirectory);
    try {
      execFileSync('git', args, { stdio: ['ignore', 'pipe', 'pipe'] });
    } catch (error) {
      const stderr = error.stderr?.toString().trim();
      throw new Error(`Could not clone ${source}${stderr ? `: ${stderr}` : ''}`);
    }
    const revision = gitOutput(['rev-parse', 'HEAD'], cloneDirectory);
    return callback({ root: cloneDirectory, revision, source, ref: ref ?? 'HEAD' });
  } finally {
    rmSync(temporaryRoot, { recursive: true, force: true });
  }
}

function parseAgentName(file, content) {
  const match = content.toString('utf8').match(/^name\s*=\s*"([a-z0-9][a-z0-9_-]*)"\s*$/m);
  if (!match) throw new Error(`${file} must define a simple string name`);
  return match[1];
}

function discoverAgents(sourceRoot) {
  const directory = join(sourceRoot, '.codex', 'agents');
  if (!existsSync(directory)) throw new Error(`No .codex/agents directory found in source: ${sourceRoot}`);
  const agents = readdirSync(directory, { withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name.endsWith('.toml'))
    .sort((left, right) => left.name.localeCompare(right.name))
    .map((entry) => {
      const path = join(directory, entry.name);
      const content = readFileSync(path);
      const name = parseAgentName(path, content);
      if (basename(entry.name, '.toml') !== name) {
        throw new Error(`${path} filename must match its name field (${name})`);
      }
      return { name, filename: entry.name, content };
    });
  if (agents.length === 0) throw new Error(`No agent TOML files found in ${directory}`);
  return agents;
}

function targetPaths(options, cwd = process.cwd()) {
  const codexRoot = options.global
    ? resolve(options.codexHome ?? join(homedir(), '.codex'))
    : join(cwd, '.codex');
  return { codexRoot, agentsDirectory: join(codexRoot, 'agents'), lockPath: join(codexRoot, 'agents-lock.json') };
}

function readLock(lockPath) {
  if (!existsSync(lockPath)) return { version: LOCK_VERSION, agents: {} };
  try {
    const parsed = JSON.parse(readFileSync(lockPath, 'utf8'));
    if (parsed.version !== LOCK_VERSION || typeof parsed.agents !== 'object' || !parsed.agents) {
      throw new Error('unsupported lock format');
    }
    return parsed;
  } catch (error) {
    throw new Error(`Invalid agents lock file ${lockPath}: ${error.message}`);
  }
}

function writeAtomically(path, content) {
  const temporaryPath = `${path}.tmp-${process.pid}`;
  try {
    writeFileSync(temporaryPath, content);
    renameSync(temporaryPath, path);
  } finally {
    rmSync(temporaryPath, { force: true });
  }
}

function selectedAgents(available, requested) {
  if (requested.length === 0 || requested.includes('*')) return available;
  const byName = new Map(available.map((agent) => [agent.name, agent]));
  return requested.map((name) => {
    const agent = byName.get(name);
    if (!agent) throw new Error(`Agent '${name}' is not available. Available: ${available.map((item) => item.name).join(', ')}`);
    return agent;
  });
}

function installAgents({ agents, source, ref, revision, options, paths }) {
  const lock = readLock(paths.lockPath);
  const nextLock = { ...lock, agents: { ...lock.agents } };
  const operations = agents.map((agent) => {
    const target = join(paths.agentsDirectory, agent.filename);
    const previousContent = existsSync(target) ? readFileSync(target) : null;
    const targetHash = previousContent === null ? null : sha256(previousContent);
    const incomingHash = sha256(agent.content);
    const previous = lock.agents[agent.name];
    const unchanged = targetHash === incomingHash;
    const canReplace = options.force || (previous && targetHash === previous.fileHash);

    if (targetHash && !unchanged && !canReplace) {
      throw new Error(
        `Refusing to overwrite locally modified ${target}. Use --force after reviewing the change.`,
      );
    }
    nextLock.agents[agent.name] = {
      source,
      ref,
      revision,
      relativePath: `.codex/agents/${agent.filename}`,
      fileHash: incomingHash,
    };
    return { ...agent, target, previousContent, changed: !unchanged };
  });

  const previousLockContent = existsSync(paths.lockPath) ? readFileSync(paths.lockPath) : null;
  const writtenOperations = [];
  try {
    // No target is created until every selected agent has passed conflict checks.
    mkdirSync(paths.agentsDirectory, { recursive: true });
    for (const operation of operations) {
      if (operation.changed) {
        writeAtomically(operation.target, operation.content);
        writtenOperations.push(operation);
      }
    }
    mkdirSync(dirname(paths.lockPath), { recursive: true });
    writeAtomically(paths.lockPath, `${JSON.stringify(nextLock, null, 2)}\n`);
  } catch (error) {
    const rollbackErrors = [];
    for (const operation of [...writtenOperations].reverse()) {
      try {
        if (operation.previousContent === null) {
          rmSync(operation.target, { force: true });
        } else {
          writeAtomically(operation.target, operation.previousContent);
        }
      } catch (rollbackError) {
        rollbackErrors.push(`${operation.target}: ${rollbackError.message}`);
      }
    }
    try {
      if (previousLockContent === null) {
        rmSync(paths.lockPath, { force: true });
      } else {
        writeAtomically(paths.lockPath, previousLockContent);
      }
    } catch (rollbackError) {
      rollbackErrors.push(`${paths.lockPath}: ${rollbackError.message}`);
    }
    const rollbackDetail = rollbackErrors.length > 0
      ? ` Rollback also failed: ${rollbackErrors.join('; ')}`
      : '';
    throw new Error(`Could not install selected agents: ${error.message}.${rollbackDetail}`);
  }
  return operations.map(({ name, changed }) => ({ name, changed }));
}

async function add(source, options) {
  const paths = targetPaths(options);
  return withSource(source, ({ root, revision, ref }) => {
    const available = discoverAgents(root);
    if (options.list) {
      for (const agent of available) console.log(agent.name);
      return;
    }
    const agents = selectedAgents(available, options.agents);
    const installed = installAgents({ agents, source, ref, revision, options, paths });
    for (const item of installed) console.log(`${item.changed ? 'Installed' : 'Already current'} ${item.name}`);
    console.log(`Lock: ${paths.lockPath}`);
  });
}

async function update(options) {
  const paths = targetPaths(options);
  const lock = readLock(paths.lockPath);
  const wanted = options.agents.length === 0 || options.agents.includes('*') ? Object.keys(lock.agents) : options.agents;
  if (wanted.length === 0) throw new Error(`No agents recorded in ${paths.lockPath}`);

  for (const name of wanted) {
    const entry = lock.agents[name];
    if (!entry) throw new Error(`Agent '${name}' is not recorded in ${paths.lockPath}`);
    await add(entry.source, { ...options, agents: [name], list: false, force: options.force });
  }
}

export async function main(argv) {
  try {
    const { options, positional } = parseArgs(argv);
    if (options.help || positional[0] === 'help') {
      console.log(usage());
      return;
    }
    const command = positional.shift();
    if (command === 'add') {
      const source = positional.shift();
      if (!source || positional.length > 0) throw new Error('add requires exactly one source');
      await add(source, options);
    } else if (command === 'update') {
      if (positional.length > 0) throw new Error('update does not accept a source');
      await update(options);
    } else {
      throw new Error(`Unknown command: ${command ?? '(missing)'}`);
    }
  } catch (error) {
    console.error(`codex-agents: ${error.message}`);
    process.exitCode = 1;
  }
}
