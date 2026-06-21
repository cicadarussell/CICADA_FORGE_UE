# PHASE CLUSTER 003H - LOCAL DASHBOARD CONTROL ROOM

## Build type

Mainline cumulative patch.

## Why this phase exists

The headless pipeline works, but the artifacts are spread across folders.

Phase 003H creates one local control-room dashboard so the project can be checked quickly without opening Unreal.

## Added

- dashboard generator:
  `tools/cicada_dashboard/cicada_artifact_dashboard.py`
- dashboard command added to:
  `tools/cicada_headless/cicada_forge_headless.py`
- master wrapper supports:
  `-Command dashboard`
- open dashboard script:
  `scripts/open_cicada_dashboard.ps1`
- dashboard helper:
  `scripts/headless/cicada_headless_dashboard.ps1`
- dashboard quick check:
  `scripts/diagnostics/cicada_dashboard_quick_check.ps1`
- artifact inventory now includes Dashboard
- full-check now also refreshes dashboard snapshot

## Dashboard output

Dashboard files:

- `Saved/CICADAForge/Dashboard/index.html`
- `Saved/CICADAForge/Dashboard/cicada_dashboard_snapshot.json`

The dashboard shows:

- current phase
- safety state
- latest manifest safety flags
- git changed file count
- capability matrix
- latest box jobs
- latest STL files
- latest reports
- latest run reports
- latest print manifests
- latest receipts
- recommended next command
- raw snapshot JSON

## Main command

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard
```

## Full proof command

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command full-check -OpenReport
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard
```

## Still locked

- direct printer send
- G-code streaming
- serial ports
- slicer CLI automation
- CAD/STEP sidecar

## Next phase

Phase 003I should start the CAD sidecar contract and exact-geometry boundary, or add a local dashboard command launcher.

Do not add direct printer sending.
