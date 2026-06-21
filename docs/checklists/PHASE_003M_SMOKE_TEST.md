# PHASE 003M SMOKE TEST

## Repo audit

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003M_repo_audit.ps1"
```

## CAD engine launcher doctor

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-engine-doctor -OpenReport
```

Expected:

- current Python probed
- `.cicada_envs/cadquery` Python probed if present
- selected Python reported
- machine bridge locked

## CAD generate through engine launcher

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-generate-engine -Part "examples\cad_parts\robot_sensor_plate_v02.part.json" -OpenReport
```

Expected:

- if CadQuery venv exists: sidecar runs through that Python
- if no CadQuery: exact STEP blocked honestly
- CAD report still generated

## Slicer dry-run plan

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command slicer-dryrun-plan -OpenReport
```

Expected:

- plan report generated
- `executed: false`
- `gcode_generated: false`
- `direct_printer_send: false`
- `machine_bridge: LOCKED`

## Full check

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command phase003M-full-check -OpenReport
```
