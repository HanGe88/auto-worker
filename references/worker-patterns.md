# Worker Patterns

## State-machine model

An auto-worker works because each run reads and writes state files. The current Claude process does not need previous chat context.

```text
TASKS.md   defines the durable task queue and permissions
STATE.md   defines current runtime progress
HANDOFF.md summarizes the most recent run
FAILURES.md records failure details
```

## Run lifecycle

```text
scheduler wakes wrapper
wrapper creates lock
wrapper starts claude --print worker-prompt
worker reads state files
worker chooses one small task
worker modifies allowed files
worker validates
worker updates STATE/HANDOFF/FAILURES
wrapper writes log and RUNS.jsonl
wrapper removes lock
```

## Task granularity

Good per-run tasks:

- create one scaffold file;
- write one section outline;
- draft one chapter;
- inspect one file;
- fix one small validation failure;
- summarize one batch of results;
- update one handoff.

Bad per-run tasks:

- write an entire book;
- refactor a whole codebase;
- modify many unrelated files;
- perform irreversible external actions;
- ask the user a question and wait.

## Quality loop

Each worker run should produce evidence:

- changed files;
- validation command;
- validation result;
- next recommended task;
- failure details if applicable.
