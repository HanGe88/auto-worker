# Troubleshooting

## Logs show Chinese mojibake

Cause: Windows PowerShell 5.1 encoding mismatch.

Fix: ensure wrapper sets:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
$env:PYTHONIOENCODING = "utf-8"
$env:LANG = "zh_CN.UTF-8"
$env:LC_ALL = "zh_CN.UTF-8"
```

Old logs already written as mojibake will not automatically repair.

## Many skipped_locked records

Cause: schedule interval is shorter than typical worker runtime.

This is usually safe. The lock is preventing concurrent writes. Reduce frequency if the log noise is undesirable.

## Scheduled task exists but does not run

Check:

- task is enabled;
- user is logged in if task is interactive only;
- laptop power/sleep conditions;
- command path and quoting;
- Claude CLI availability in scheduled environment;
- latest log and RUNS.jsonl.

## Validation fails

Read validator output. Fix missing files or required snippets first. Do not keep running the worker blindly if scaffold validation fails.

## Worker edits too much

Tighten TASKS.md and worker-prompt.md:

- specify one task per run;
- list exact allowed directories;
- add phase ordering;
- require handoff and validation;
- pause after a stage for human review.
