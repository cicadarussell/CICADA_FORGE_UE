# CADQUERY SETUP NOTES

## Current state

Phase 003I PowerShell showed:

- CadQuery module not detected.
- FreeCAD module not detected.
- selected engine: none.
- exact STEP available: false.

That is a valid partial state.

## Check

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cadquery-check
```

## Optional install attempt

This is explicit. It does not run automatically.

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cadquery-install-user
```

## Truth boundary

If this install fails, do not panic.

The sidecar still validates intent and writes reports. Exact STEP just remains blocked until a CAD engine is installed properly.
