# PHASE 003I SMOKE TEST

## Repo audit

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003I_repo_audit.ps1"
```

## CAD doctor

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-doctor
```

Expected:

- schema exists
- example parts listed
- CadQuery availability reported
- FreeCAD availability reported
- direct printer send false
- machine bridge locked

## Validate examples

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-validate
```

Expected:

- all examples pass validation

## CAD demo

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-demo -OpenReport
```

Expected:

- CAD report created
- intent JSON created
- dashboard refreshed
- if CadQuery exists: STEP/STL exported
- if CadQuery missing: report says STEP blocked
- direct printer send remains false
- machine bridge remains locked

## Quick check

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_cad_sidecar_quick_check.ps1"
```

## Dashboard

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard
```

Expected:

- dashboard includes CADIntent
- dashboard includes CADExports
- dashboard includes CADReports

## Verdict

- [ ] PASS
- [ ] PARTIAL - likely if no CadQuery, but report correctly blocks STEP
- [ ] FAIL
