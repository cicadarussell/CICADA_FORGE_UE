# PHASE CLUSTER 003N - COMMAND CENTER AND PASSIVE HEALTH

## Build type

Mainline cumulative patch.

## Why this phase exists

The pipeline now has many useful tools. That creates a new problem: remembering which cursed PowerShell spell to cast.

Phase 003N adds:

- passive health reports that understand NOT_RUN vs FAIL
- command center page
- generated launcher scripts
- interactive PowerShell control room
- 003N full check

## Added

- health report:
  `tools/cicada_health/cicada_health_report.py`
- command center:
  `tools/cicada_launcher/cicada_command_center.py`
- scripts:
  - `scripts/diagnostics/cicada_health_report.ps1`
  - `scripts/launcher/cicada_generate_command_center.ps1`
  - `scripts/open_cicada_command_center.ps1`
  - `scripts/cicada_control_room.ps1`
  - `scripts/headless/cicada_headless_phase003N_full_check.ps1`
- wrapper commands:
  - `health-report`
  - `command-center`
  - `control-room`
  - `phase003N-full-check`

## Main command

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command phase003N-full-check -OpenReport
```

## Important diagnostic rule

Missing generated artifacts are NOT_RUN in passive mode, not FAIL.

This matters because wiping Saved or skipping generation should not be misread as broken code.
