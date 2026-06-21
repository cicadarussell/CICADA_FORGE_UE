# PHASE 003P FULL INTEGRATION TEST

## 1. Repo audit

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003P_repo_audit.ps1"
```

Expected:

```text
AUDIT PASS: Phase 003P full integration bugfix files present.
```

## 2. Full project audit

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command full-project-audit -OpenReport
```

Expected:

- Python compile checks pass
- no old external `-OpenReport:$OpenReport` script calls found
- machine safety scan passes
- current phase includes 003P

## 3. Full integration check

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command phase003P-full-check -OpenReport -OpenDashboard
```

Expected:

- no SwitchParameter conversion errors
- CadQuery engine is selected from `.cicada_envs/cadquery`
- sensor plate exact STEP/STL export succeeds if CadQuery behaves
- generated STL appears under `Saved/CICADAForge/STL`
- slicer dry-run plan sees latest STL and OrcaSlicer if installed
- dashboard refreshes before release gate
- release gate is RC_READY or RC_PARTIAL with zero FAIL
- machine bridge remains LOCKED
- direct printer send remains false
- G-code generated remains false

## 4. Release gate

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command release-gate -OpenReport
```

Expected:

- RC_READY or RC_PARTIAL
- not BLOCKED
