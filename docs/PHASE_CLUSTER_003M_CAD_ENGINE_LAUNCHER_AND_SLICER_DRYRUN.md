# PHASE CLUSTER 003M - CAD ENGINE LAUNCHER AND SLICER DRY-RUN PLANNER

## Build type

Mainline cumulative patch.

## Why this phase exists

003L created environment and slicer readiness reports. 003M makes those reports operational, still safely.

This phase adds:

1. CAD engine launcher that prefers `.cicada_envs/cadquery` if available.
2. Slicer dry-run planner that writes command plans but does not execute slicing or generate G-code.

## Added

- CAD engine launcher:
  `tools/cicada_env/cicada_cad_engine_launcher.py`
- slicer dry-run planner:
  `tools/cicada_slicer/cicada_slicer_dryrun_planner.py`
- scripts:
  - `scripts/env/cicada_cad_engine_launcher_doctor.ps1`
  - `scripts/cad/cicada_cad_generate_part_engine.ps1`
  - `scripts/slicer/cicada_slicer_dryrun_plan.ps1`
  - `scripts/headless/cicada_headless_phase003M_full_check.ps1`
- wrapper commands:
  - `cad-engine-doctor`
  - `cad-generate-engine`
  - `slicer-dryrun-plan`
  - `phase003M-full-check`

## Safety boundary

Slicer dry-run planner does not execute export commands.

No G-code is generated.

No printer is contacted.

Machine bridge remains locked.

## Main command

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command phase003M-full-check -OpenReport
```
