# PHASE 003H SMOKE TEST

## Repo audit

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003H_repo_audit.ps1"
```

## Generate dashboard

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard
```

Expected:

- `Saved/CICADAForge/Dashboard/index.html`
- `Saved/CICADAForge/Dashboard/cicada_dashboard_snapshot.json`
- browser opens dashboard

## Quick check dashboard

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_dashboard_quick_check.ps1"
```

Expected:

- dashboard title marker present
- machine bridge marker present
- `machine_bridge: LOCKED`

## Full no-Unreal flow

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command full-check -OpenReport
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard
```

Expected:

- STL generated
- STL quality gate passes
- report generated
- run report generated
- dashboard refreshed
- direct printer send false
- machine bridge locked

## Verdict

- [ ] PASS
- [ ] PARTIAL
- [ ] FAIL
