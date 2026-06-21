# PHASE 003N SMOKE TEST

## Repo audit

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003N_repo_audit.ps1"
```

## Passive health

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command health-report -OpenReport
```

Expected:

- HealthReports updated
- missing generated artifacts marked NOT_RUN unless strict
- direct printer send false
- machine bridge locked

## Command center

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command command-center -OpenReport
```

Expected:

- `Saved/CICADAForge/CommandCenter/index.html`
- `Saved/CICADAForge/CommandCenter/command_center.json`
- launchers under `Saved/CICADAForge/Launchers`

## Interactive control room

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command control-room
```

## Full check

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command phase003N-full-check -OpenReport
```
