# Windows Task Scheduler Reference

## Find schtasks from Git Bash

Use absolute Windows system paths when `schtasks.exe` is not in PATH:

```bash
/c/Windows/System32/schtasks.exe
/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe
```

When calling `schtasks.exe` from Git Bash, set `MSYS_NO_PATHCONV=1` so flags like `/Create` are not converted into paths.

## Create a repeated task

```bash
MSYS_NO_PATHCONV=1 /c/Windows/System32/schtasks.exe /Create \
  /TN WorkerName \
  /TR 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\path\to\run-worker.ps1"' \
  /SC MINUTE \
  /MO 30 \
  /F
```

## Query a task

```bash
MSYS_NO_PATHCONV=1 /c/Windows/System32/schtasks.exe /Query /TN WorkerName /FO LIST /V
```

## Change interval

```bash
MSYS_NO_PATHCONV=1 /c/Windows/System32/schtasks.exe /Change /TN WorkerName /RI 15
```

## Stop and disable

```bash
MSYS_NO_PATHCONV=1 /c/Windows/System32/schtasks.exe /End /TN WorkerName
MSYS_NO_PATHCONV=1 /c/Windows/System32/schtasks.exe /Change /TN WorkerName /DISABLE
```

## Enable

```bash
MSYS_NO_PATHCONV=1 /c/Windows/System32/schtasks.exe /Change /TN WorkerName /ENABLE
```

## Common notes

- A high-frequency schedule may create many `skipped_locked` entries. This is usually safe because lock prevents concurrent writes.
- If Windows reports a negative last result, inspect power/session conditions and the worker log.
- For Chinese logs, ensure the PowerShell wrapper sets UTF-8 console and environment encoding.
