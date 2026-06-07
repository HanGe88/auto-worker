---
name: auto-worker
description: Create, manage, inspect, pause, resume, and tune Claude Code auto-workers for long-running local file tasks. Use this skill whenever the user wants Claude Code to periodically continue a task, create an automated worker, run a long project in small recoverable steps, inspect worker progress, change a worker schedule, pause/resume automation, or reuse the pattern of external scheduler + fresh Claude process + TASKS/STATE/HANDOFF/FAILURES files. This skill is especially relevant for writing projects, documentation projects, code maintenance, knowledge-base整理, course creation, and other local-file workflows that need repeated autonomous progress.
---

# Auto Worker Skill

This skill helps create and manage Claude Code auto-workers: short-lived Claude Code processes launched by an external scheduler, each completing one small verifiable task, updating file-based state, and exiting.

Use it to turn a long-running local-file task into a recoverable automation system.

## Core idea

An auto-worker is not one long Claude session. It is many short runs:

```text
scheduler -> wrapper script -> claude --print worker-prompt -> one small task -> validate -> update state -> exit
```

Each run restores context from files instead of chat history:

```text
TASKS.md     what the worker is allowed and expected to do
STATE.md     current runtime progress and failure count
HANDOFF.md   most recent handoff summary
FAILURES.md  failure details and debugging notes
```

This makes long work auditable, restartable, and safer than an always-running session.

## Supported operations

Infer the operation from the user's request.

### setup

Use when the user wants to create a new auto-worker.

Examples:

- “帮我创建一个自动 worker”
- “让 Claude Code 持续推进这个项目”
- “把这个长期任务做成可恢复的自动化”

Workflow:

1. Identify the target project root.
2. Ask only for missing decisions that affect generated files:
   - worker name;
   - long-term goal;
   - allowed output/edit directories;
   - validation command;
   - run frequency if they want scheduling now.
3. Prefer safe defaults:
   - no network;
   - no external API;
   - no push/publish/deploy;
   - no deleting unknown files;
   - no secrets handling;
   - one minimal task per run;
   - max consecutive failures: 3;
   - schedule frequency: 30 minutes unless user chooses otherwise.
4. Create the worker directory and wrapper scripts from the templates in `templates/`.
5. Do not register a schedule unless the user explicitly asks or confirms.
6. Recommend a manual dry run before scheduling.

### run-once

Use when the user wants to manually run one worker iteration.

Before running, explain that it launches a new Claude Code process and may modify the allowed files. Then run the wrapper, inspect logs, read STATE/HANDOFF, and summarize.

### schedule

Use when the user wants periodic execution.

Examples:

- “每 10 分钟跑一次”
- “挂到定时任务”
- “让它自动跑下去”

For Windows MVP, use Task Scheduler via `schtasks.exe` or PowerShell. Confirm before creating or changing a scheduled task. After scheduling, query the task and report:

- task name;
- next run time;
- frequency;
- command;
- whether it is enabled.

### status

Use when the user asks current progress.

Read, in this order:

1. `.claude/auto-worker/<worker>/STATE.md`
2. `.claude/auto-worker/<worker>/HANDOFF.md`
3. `.claude/auto-worker/<worker>/RUNS.jsonl`
4. latest `.claude/auto-worker/<worker>/logs/*.log`

Report:

```text
current state
completed work
remaining work
last run status
latest verification
failure count
whether automation is scheduled/enabled
recommended next action
```

### pause

Use when the user wants to stop automation.

Stop the currently running scheduled task if possible, disable future triggers, and preserve all files. Do not delete the worker unless the user explicitly asks and confirms deletion.

### resume

Use when the user wants automation to continue.

Check STATE.md first. If consecutive failures reached the maximum, do not resume blindly; explain the blocker and ask whether to reset the failure count after fixing the issue.

### change-frequency

Use when the user asks to change interval.

Warn briefly if the interval is aggressive. Intervals below 5 minutes can create many `skipped_locked` records because the previous run may still be active. This is usually safe but noisy.

### explain

Use when the user wants to understand directories, English terms, or how the automation continues.

Explain in plain language. Avoid assuming the user knows scheduler, JSONL, lock, stdout, or PowerShell.

## Generated structure

Default worker structure:

```text
.claude/auto-worker/<worker-name>/
  TASKS.md
  STATE.md
  HANDOFF.md
  FAILURES.md
  worker-prompt.md
  RUNS.jsonl
  logs/

.claude/auto-worker/run-<worker-name>-worker.ps1
.claude/auto-worker/run-<worker-name>-worker.sh
```

Optional business workspace for generic tasks:

```text
work/<worker-name>/
  README.md
  brief.md
  plan.md
  inputs/
  outputs/
  review/
```

For writing projects, use a writing-specific workspace:

```text
writing/<project-name>/
  README.md
  brief.md
  outline.md
  style-guide.md
  materials/
  drafts/
  review/
```

## Safety model

Default worker prompts should prohibit:

- network access;
- external APIs;
- dependency downloads;
- push, publish, deploy;
- deleting unknown files;
- modifying system/user config;
- secrets, passwords, tokens, cookies, private keys;
- starting new Claude processes from inside the worker;
- infinite loops;
- waiting for user input.

If a user requests a high-risk worker, narrow the scope. For example, refuse automated trading or automatic public publishing, but offer local research summaries or draft generation with human approval.

## Scheduling notes

Windows Task Scheduler from Git Bash often path-converts `/Create` style flags. Use `MSYS_NO_PATHCONV=1` when calling `schtasks.exe` from Git Bash.

Example:

```bash
MSYS_NO_PATHCONV=1 /c/Windows/System32/schtasks.exe /Query /TN WorkerName /FO LIST
```

For scheduled PowerShell workers that output Chinese, set UTF-8 encoding in the PowerShell wrapper:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
$env:PYTHONIOENCODING = "utf-8"
$env:LANG = "zh_CN.UTF-8"
$env:LC_ALL = "zh_CN.UTF-8"
```

## Quality gates

Before claiming a worker is ready:

1. Confirm expected files exist.
2. Run the project validator if one exists.
3. Check wrapper syntax:
   - Bash: `bash -n <script>`
   - PowerShell: parse with `[scriptblock]::Create(...)`
4. Do one manual dry run unless the user declines.
5. Inspect STATE.md, HANDOFF.md, RUNS.jsonl, and latest log.
6. If scheduling was created, query the scheduled task.

## When to ask before acting

Always ask before:

- registering or changing an external schedule unless the user explicitly asked for that exact action;
- running a worker that may modify files, unless the user explicitly said to execute;
- deleting a worker, logs, or generated outputs;
- enabling network, API, publish, deploy, push, or broad delete permissions.

## Useful references

Read these files when needed:

- `references/worker-patterns.md` — conceptual model and state-machine pattern.
- `references/windows-task-scheduler.md` — Windows scheduling commands.
- `references/safety-rules.md` — safety defaults and refusal boundaries.
- `references/troubleshooting.md` — common failures and fixes.

Use templates from:

- `templates/worker/`
- `templates/scripts/`

Use scripts from:

- `scripts/inspect_worker.py`
