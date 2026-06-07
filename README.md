# auto-worker

A Claude Code skill for turning long-running local work into safe, resumable, scheduled AI worker loops.

> Stop trying to keep one huge Claude session alive. Let many small Claude workers pick up state, do one task, verify, hand off, and exit.

## What problem does this solve?

Claude Code is excellent at focused work, but long-running projects often become messy:

- the conversation context grows too large;
- a single failure can interrupt the whole workflow;
- it is hard to know what has already been done;
- scheduled or repeated work becomes manual again;
- autonomous runs can become risky if the prompt is too broad;
- logs, handoffs, and recovery state are often missing.

`auto-worker` gives you a repeatable pattern for long tasks:

```text
External Scheduler
  -> wrapper script
  -> fresh claude --print process
  -> reads TASKS / STATE / HANDOFF / FAILURES
  -> completes one small task
  -> runs validation
  -> updates state and handoff
  -> writes logs
  -> exits
```

Instead of one giant AI session, you get a sequence of short, auditable, recoverable AI worker runs.

## Who is this for?

Use this skill if you want Claude Code to keep making progress on local files while staying controlled and inspectable.

Good fits:

- writers building books, courses, articles, newsletters, or scripts;
- developers doing low-risk code maintenance, tests, docs, migrations, or cleanup;
- knowledge workers maintaining notes, documentation, research folders, or knowledge bases;
- creators turning long ideas into content libraries;
- power users who want scheduled Claude Code automation without losing control.

Not a good fit for fully autonomous high-risk actions such as trading, public posting, production deployment, mass messaging, credential testing, or deleting unknown files.

## What can it do?

The skill helps Claude Code:

- create a new auto-worker scaffold;
- generate `TASKS.md`, `STATE.md`, `HANDOFF.md`, `FAILURES.md`, and `worker-prompt.md`;
- create PowerShell and Git Bash wrapper scripts;
- run one manual dry run;
- register or change a Windows Task Scheduler job;
- inspect current progress from state files and logs;
- pause or resume a worker;
- explain the auto-worker structure in plain language;
- apply conservative safety defaults.

## Example use cases

### Write a book over time

```text
/auto-worker Create a writing worker for my book project. Each run should write or revise one chapter section, validate structure, update handoff, and stop. Do not publish anything.
```

### Maintain documentation

```text
/auto-worker Create a docs-worker that reviews one file in docs/ each run, improves clarity, runs a link/style check, and updates STATE.md.
```

### Build a knowledge base

```text
/auto-worker Create a notes-worker that reads one note at a time, extracts key ideas, links related notes, and writes a summary. No network access.
```

### Low-risk code maintenance

```text
/auto-worker Create a test-worker that adds or improves one test file per run, then runs the relevant test command. Do not commit or push automatically.
```

### Check worker status

```text
/auto-worker Check where my book worker is now. Summarize latest STATE, HANDOFF, RUNS, and logs.
```

### Pause automation

```text
/auto-worker Pause this worker. Do not delete any generated files or logs.
```

## Installation

Install from GitHub with the Skills CLI:

```bash
npx skills add HanGe88/auto-worker
```

Or copy this repository into your Claude skills directory:

```text
~/.claude/skills/auto-worker/
```

Then use it in Claude Code:

```text
/auto-worker Create a worker for my long-running local task.
```

## Core design

An auto-worker has three layers.

### 1. Your work area

This is where the actual output lives, such as:

```text
book/
docs/
notes/
work/
```

### 2. Worker state

This is the worker's memory and rulebook:

```text
.claude/auto-worker/<worker-name>/
  TASKS.md
  STATE.md
  HANDOFF.md
  FAILURES.md
  worker-prompt.md
  RUNS.jsonl
  logs/
```

Meaning:

| File | Purpose |
| --- | --- |
| `TASKS.md` | Durable task queue, goals, permissions, forbidden actions |
| `STATE.md` | Current progress and consecutive failure count |
| `HANDOFF.md` | Latest run summary and next recommendation |
| `FAILURES.md` | Failure details and debugging notes |
| `worker-prompt.md` | Fixed prompt given to every fresh Claude worker |
| `RUNS.jsonl` | Machine-readable wrapper run records |
| `logs/` | Per-run Claude output logs |

### 3. Execution wrapper

The wrapper script starts Claude and manages lock/log/run records:

```text
.claude/auto-worker/run-<worker-name>-worker.ps1
.claude/auto-worker/run-<worker-name>-worker.sh
```

External schedulers such as Windows Task Scheduler can run the wrapper repeatedly.

## Why this pattern works

Every Claude run is stateless, but the project is not.

Each fresh Claude worker restores context from files:

```text
read TASKS.md
read STATE.md
read HANDOFF.md
read FAILURES.md
choose one small task
edit allowed files
run validation
update STATE.md and HANDOFF.md
exit
```

That makes the workflow:

- resumable;
- auditable;
- safer;
- easier to pause;
- easier to inspect;
- less dependent on long chat context.

## Safety defaults

Generated workers should default to conservative behavior:

- no network access;
- no external API calls;
- no dependency downloads;
- no push, publish, or deploy;
- no deleting unknown files;
- no system/user config changes;
- no secrets, passwords, tokens, cookies, or private keys;
- no spawning new Claude processes from inside the worker;
- no infinite loops;
- one small task per run;
- validation and handoff every run;
- stop modifying after repeated failures.

If a task needs higher-risk permissions, require explicit human approval and write the authorization into `TASKS.md`.

## Included resources

```text
SKILL.md
README.md

templates/
  worker/
    TASKS.md.template
    STATE.md.template
    HANDOFF.md.template
    FAILURES.md.template
    worker-prompt.md.template
  scripts/
    run-worker.ps1.template
    run-worker.sh.template

references/
  worker-patterns.md
  windows-task-scheduler.md
  safety-rules.md
  troubleshooting.md
  glossary.md

scripts/
  inspect_worker.py

evals/
  evals.json
  trigger-evals.json
```

## Status and maturity

This is an MVP skill extracted from a real Claude Code auto-worker experiment.

It is already useful for local-file, long-running, low-risk automation. It is not intended to be a fully autonomous production operations system.

Current strengths:

- proven pattern from a real writing automation workflow;
- conservative safety model;
- file-based recovery and handoff;
- Windows Task Scheduler guidance;
- PowerShell/Git Bash wrapper templates;
- status inspection script;
- eval prompts for future testing.

Known gaps:

- no deterministic `create_worker.py` generator yet;
- Windows support is the most complete; macOS/Linux scheduler docs are not yet built out;
- no full benchmark/eval viewer run yet;
- no graphical status dashboard yet;
- quality still depends on a well-written `TASKS.md` and periodic human review.

## Roadmap

Planned improvements:

- `create_worker.py` to generate workers from templates deterministically;
- `schedule_windows.py` to manage Task Scheduler create/query/pause/resume/frequency;
- Markdown status reports for non-technical users;
- stage gates such as “pause after each phase” or “pause every N tasks”; 
- macOS/Linux scheduler support;
- formal skill evals and trigger description optimization;
- packaged `.skill` release.

## Philosophy

The goal is not to make AI run wild.

The goal is to make long-running AI work:

```text
small enough to verify,
safe enough to schedule,
clear enough to inspect,
and structured enough to resume.
```

Use `auto-worker` when you want automation with memory, boundaries, logs, and a stop button.
