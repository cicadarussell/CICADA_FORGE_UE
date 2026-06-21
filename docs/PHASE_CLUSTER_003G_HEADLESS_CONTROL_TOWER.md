# PHASE CLUSTER 003G - HEADLESS FORGE CONTROL TOWER

## Build type

Mainline cumulative patch.

## Why this phase exists

Opening Unreal after every patch is slow and annoying. The current pipeline is already useful headlessly:

- job file
- STL
- print handoff manifest
- receipt
- analyzer
- report
- quality gate

Phase 003G adds a master no-Unreal control tower around that.

## Added

- headless control tower:
  `tools/cicada_headless/cicada_forge_headless.py`
- master wrapper:
  `scripts/cicada_forge.ps1`
- headless scripts:
  - `scripts/headless/cicada_headless_full_check.ps1`
  - `scripts/headless/cicada_headless_demo_box.ps1`
  - `scripts/headless/cicada_headless_custom_box.ps1`
  - `scripts/headless/cicada_headless_doctor.ps1`
  - `scripts/headless/cicada_headless_inventory.ps1`
  - `scripts/headless/cicada_headless_run_report.ps1`
- run reports:
  `Saved/CICADAForge/RunReports`
- upgraded on-track check
- upgraded artifact inventory

## Headless commands

Doctor:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command doctor
```

Full check:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command full-check -OpenReport
```

Custom box:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command custom-box -Name "bracket_blank" -Width 95 -Depth 35 -Height 8 -Material PETG -Infill 25 -OpenReport
```

Inventory:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command inventory
```

## What full-check proves

- required project files exist
- Python tooling exists
- box job runner works
- STL generation works
- STL quality gate passes
- report generation works
- manifest says direct printer send is false
- manifest says machine bridge is locked
- inventory is produced
- run report is saved

## Still locked

- direct printer send
- G-code streaming
- serial ports
- slicer CLI automation
- CAD/STEP sidecar

## Next phase

Phase 003H should start one of these:

1. Local dashboard/index page linking latest jobs/STLs/reports/manifests.
2. CAD sidecar contract.
3. Unreal buttons that call headless scripts.

Do not add direct printer control yet.
