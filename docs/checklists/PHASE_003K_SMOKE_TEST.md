# PHASE 003K SMOKE TEST

## Repo audit

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003K_repo_audit.ps1"
```

## CAD full check

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-full-check -OpenReport -OpenDashboard
```

Expected:

- CAD doctor runs
- examples validate
- sample CAD parts are generated
- reports are generated
- dashboard refreshes
- direct printer send remains false
- machine bridge remains locked
- if CadQuery missing: STEP blocked honestly

## Build specific richer parts

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-build-sensor-plate -Name "robot_sensor_plate_test" -OpenReport
```

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-build-motor-mount -Name "motor_mount_test" -OpenReport
```

## Compare examples

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-compare -PartA "examples\cad_parts\mounting_plate_2holes.part.json" -PartB "examples\cad_parts\robot_sensor_plate_v02.part.json"
```

## Verdict

- [ ] PASS
- [ ] PARTIAL - correct if CadQuery missing but reports are honest
- [ ] FAIL
