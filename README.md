# auto-worker skill

A Claude Code skill for creating and managing long-running local-file auto-workers.

It packages the pattern:

```text
external scheduler -> wrapper script -> fresh claude --print worker -> TASKS/STATE/HANDOFF/FAILURES -> one small verified task -> exit
```

## What it helps with

Use this skill when you want Claude Code to:

- create a local auto-worker for a long task;
- run a worker once for a dry run;
- register or change a schedule;
- inspect worker progress;
- pause or resume automation;
- explain the auto-worker file structure.

It is best for local-file workflows such as writing projects, documentation maintenance, knowledge-base整理, course creation, low-risk code maintenance, and recurring review tasks.

## Install

From this repository:

```bash
npx skills add HanGe88/auto-worker
```

Or copy this repository folder into your Claude skills directory:

```text
~/.claude/skills/auto-worker/
```

## Use

In Claude Code:

```text
/auto-worker 创建一个 notes-worker，用来每 30 分钟整理一次 notes 目录。
/auto-worker 查看 book worker 现在跑到哪了。
/auto-worker 暂停这个自动 worker，不要删除文件。
/auto-worker 把 worker 改成每 15 分钟运行一次。
```

## Safety defaults

Generated workers default to conservative behavior:

- no network access;
- no external APIs;
- no push/publish/deploy;
- no deleting unknown files;
- no secrets handling;
- one minimal task per run;
- validation and handoff every run.

## Status

This is an MVP skill extracted from a real Claude Code auto-worker experiment. It is suitable for local long-running task automation, but high-risk actions such as automated trading, public posting, production deployment, or destructive file operations should require explicit human approval or be refused.
