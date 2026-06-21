# PHASE CLUSTER 003L - CAD ENGINE BOOTSTRAP AND SLICER READINESS

## Build type

Mainline cumulative patch.

## Why this phase exists

003K made CAD intent more useful, but the next bottleneck is not more part JSON.

The next bottleneck is environment truth:

- Is CadQuery available?
- Is an isolated CadQuery venv ready?
- Is a slicer installed?
- Is there an STL to inspect?
- Can we prepare for slicer dry-runs without generating G-code or sending to a printer?

Phase 003L answers those questions without touching machines.

## Added

- environment manager:
  `tools/cicada_env/cicada_environment_manager.py`
- slicer readiness reporter:
  `tools/cicada_slicer/cicada_slicer_readiness.py`
- env scripts:
  - `scripts/env/cicada_env_doctor.ps1`
  - `scripts/env/cicada_env_plan.ps1`
  - `scripts/env/cicada_env_create_cadquery_venv.ps1`
  - `scripts/env/cicada_env_install_cadquery.ps1`
- slicer script:
  - `scripts/slicer/cicada_slicer_readiness.ps1`
- combined headless check:
  - `scripts/headless/cicada_headless_env_slicer_full_check.ps1`
- dashboard now tracks:
  - EnvReports
  - SlicerReports
- wrapper commands:
  - `env-doctor`
  - `env-plan`
  - `env-create-cadquery`
  - `env-install-cadquery`
  - `slicer-readiness`
  - `env-slicer-full-check`

## Safety boundary

Slicer readiness does not generate G-code.

It only reports installed slicer candidates and whether a safe dry-run could be attempted later.

## Main command

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command env-slicer-full-check -OpenReport
```
