# PHASE 003O1 CLEAN TEST

## 1. Cleanup audit

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003O1_cleanup_audit.ps1"
```

Expected:

```text
AUDIT PASS: Phase 003O1 cleanup files present.
```

## 2. Full no-Unreal check

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command phase003O-full-check -OpenReport
```

Expected:

- no `SwitchParameter` conversion error
- health report generated
- command center generated
- CAD report generated or STEP blocked honestly
- slicer readiness/dry-run plan generated
- release gate generated
- dashboard generated/opened
- machine bridge locked

## 3. Release gate

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command release-gate -OpenReport
```

Expected:

- RC_READY or RC_PARTIAL
- not BLOCKED

## 4. Latest ledger

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command ledger-latest
```

Expected:

- phase is 003O1 or latest recorded run
- direct printer send false
- machine bridge LOCKED
