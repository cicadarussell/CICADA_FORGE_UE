# PHASE CLUSTER 003I - CAD SIDECAR CONTRACT AND EXACT-GEOMETRY BOUNDARY

## Build type

Mainline cumulative patch.

## Why this phase exists

The headless STL/job/report/dashboard path is working.

The next dangerous failure mode would be pretending triangle meshes are exact CAD. So Phase 003I creates the truth boundary:

> Unreal/dashboard/headless pipeline may orchestrate, but exact manufacturing geometry belongs to a CAD sidecar.

## Added

- CAD sidecar tool:
  `tools/cicada_cad_sidecar/cicada_cad_sidecar.py`
- part schema:
  `tools/cicada_cad_sidecar/schemas/cicada_part_schema_v0_1.json`
- example CAD parts:
  - `examples/cad_parts/simple_box.part.json`
  - `examples/cad_parts/mounting_plate_2holes.part.json`
  - `examples/cad_parts/electronics_enclosure_blank.part.json`
- CAD scripts:
  - `scripts/cad/cicada_cad_doctor.ps1`
  - `scripts/cad/cicada_cad_validate_examples.ps1`
  - `scripts/cad/cicada_cad_generate_part.ps1`
  - `scripts/cad/cicada_cad_demo.ps1`
- quick check:
  `scripts/diagnostics/cicada_cad_sidecar_quick_check.ps1`
- dashboard now tracks:
  - CADIntent
  - CADExports
  - CADReports
- master wrapper supports:
  - `cad-doctor`
  - `cad-validate`
  - `cad-demo`
  - `cad-generate`

## Critical truth rule

If CadQuery/FreeCAD exact engine is missing, the sidecar does not fake STEP.

It writes a report saying STEP is blocked.

For plain box-only parts, it may generate fallback STL, but not fake holes/cuts/features.

## Main commands

Doctor:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-doctor
```

Demo:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-demo -OpenReport
```

Generate a specific part:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-generate -Part "examples\cad_parts\mounting_plate_2holes.part.json" -OpenReport
```

## Still locked

- direct printer send
- G-code streaming
- serial ports
- slicer CLI automation
- CNC/pick-and-place commands
- robot machine bridge

## Next phase

Phase 003J should add one of:

1. CadQuery environment setup helper and install verifier.
2. A stronger bracket/enclosure feature schema.
3. Dashboard command launcher/buttons.
4. Unreal button that calls CAD sidecar doctor/demo.

Do not add direct printer sending.
