# PHASE 003L SMOKE TEST

## Repo audit

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003L_repo_audit.ps1"
```

## Environment doctor

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command env-doctor -OpenReport
```

Expected:

- current Python reported
- CadQuery current Python status shown
- CadQuery venv status shown
- report written under `Saved/CICADAForge/EnvReports`

## Slicer readiness

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command slicer-readiness -OpenReport
```

Expected:

- slicer candidates reported
- latest STL reported if one exists
- report written under `Saved/CICADAForge/SlicerReports`
- `gcode_generated: false`
- `direct_printer_send: false`
- `machine_bridge: LOCKED`

## Combined

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command env-slicer-full-check -OpenReport
```

## Optional CadQuery venv creation

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command env-create-cadquery
```

This only creates a venv. It does not install CadQuery.

## Optional CadQuery install

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command env-install-cadquery
```

This is explicit and may use internet.
