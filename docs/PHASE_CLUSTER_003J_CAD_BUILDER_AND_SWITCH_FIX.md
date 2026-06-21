# PHASE CLUSTER 003J - CAD BUILDER AND POWERSHELL SWITCH FIX

## Build type

Mainline cumulative patch.

## Why this phase exists

The latest PowerShell feedback proved:

- Phase 003I audit passed.
- CAD doctor works.
- CAD example validation works.
- Dashboard still works.
- CadQuery and FreeCAD are not currently detected in the active Python environment.
- `cad-demo -OpenReport` and `cad-generate -OpenReport` failed because the master PowerShell wrapper forwarded switches badly.

So Phase 003J fixes the wrapper bug and adds more useful CAD-side work.

## Added

- Fixes `scripts/cicada_forge.ps1` so switch parameters are forwarded as real switches.
- Adds mechanical part builder:
  `tools/cicada_cad_sidecar/cicada_mechanical_part_builder.py`
- Adds CAD builder scripts:
  - `scripts/cad/cicada_cad_make_mounting_plate.ps1`
  - `scripts/cad/cicada_cad_make_robot_plate.ps1`
  - `scripts/cad/cicada_cad_make_enclosure_blank.ps1`
  - `scripts/cad/cicada_cad_full_check.ps1`
- Adds CadQuery setup helper:
  `scripts/cad/cicada_cadquery_setup_helper.ps1`
- Adds headless CAD full-check wrapper.
- Fixes `--engine none` behaviour so it genuinely disables exact export.
- Adds literal No fake STEP marker to the sidecar so audit stops whining like a printer at 2am.

## Main commands

CAD full check:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-full-check -OpenReport -OpenDashboard
```

Build a mounting plate:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-build-mounting-plate -Name "test_plate" -Width 100 -Depth 40 -Height 6 -Material PETG -HoleDiameter 5 -Inset 12 -Holes 2 -OpenReport
```

Build a robot plate:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-build-robot-plate -Name "robot_plate" -Width 120 -Depth 70 -Height 8 -RailSpacing 60 -HoleDiameter 4.2 -OpenReport
```

CadQuery check:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cadquery-check
```

## Correct partial pass

If CadQuery is missing, exact STEP export should be blocked honestly.

That is not failure.

Failure would be pretending STEP was created.
