# PHASE 003J SMOKE TEST

## Repo audit

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003J_repo_audit.ps1"
```

## CAD full check

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-full-check -OpenReport -OpenDashboard
```

Expected:

- cad-doctor runs
- cad-validate passes
- mounting plate CAD intent is created
- robot plate CAD intent is created
- CAD reports are generated
- dashboard refreshes
- if no CadQuery: STEP is blocked honestly
- direct printer send remains false
- machine bridge remains locked

## Switch forwarding regression check

These must not throw SwitchParameter conversion errors:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-demo -OpenReport

powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-generate -Part "examples\cad_parts\mounting_plate_2holes.part.json" -OpenReport
```

## CadQuery helper

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cadquery-check
```

## Verdict

- [ ] PASS
- [ ] PARTIAL - correct if CadQuery missing but reports are honest
- [ ] FAIL
