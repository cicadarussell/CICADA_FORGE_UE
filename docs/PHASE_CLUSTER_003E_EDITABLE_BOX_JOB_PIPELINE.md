# PHASE CLUSTER 003E - EDITABLE BOX JOB PIPELINE

## Build type

Mainline cumulative patch.

## Why this phase exists

The project needed to stay on track and become more useful without pretending it already has a full CAD kernel.

Phase 003E makes the box workflow editable through job files, scripts, and a tiny local browser editor.

## Added

- upgraded box job runner with commands:
  - `init`
  - `summary`
  - `run`
- local browser job editor:
  `tools/cicada_job_editor/local_box_job_editor.html`
- open editor script:
  `scripts/open_box_job_editor.ps1`
- create editable job script:
  `scripts/new_box_job.ps1`
- create + run script:
  `scripts/new_and_run_box_job.ps1`
- job summary script:
  `scripts/diagnostics/cicada_box_job_summary.ps1`
- updated run scripts for the new runner interface
- updated project tracker

## Useful result

A user can now choose arbitrary dimensions like:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\new_and_run_box_job.ps1" -Name "bracket_blank" -Width 95 -Depth 35 -Height 8 -Material PETG -Infill 25
```

This creates:

- editable JSON job
- STL
- print handoff manifest
- receipt

## Still locked

- direct printer send
- G-code streaming
- serial ports
- slicer CLI automation
- CAD/STEP sidecar

## Next phase

Phase 003F should add a simple STL preview/thumbnail proof and maybe a basic mesh stats panel, before slicer CLI integration.
