# PHASE CLUSTER 003F - STL PREVIEW AND QUALITY GATE

## Build type

Mainline cumulative patch.

## Why this phase exists

The project now generates editable box jobs and STLs.

The next engineering gate is not direct printer control. It is proving the STL is sane before it touches a slicer workflow.

Phase 003F adds STL analysis, quality gate, JSON stats, and an HTML preview report.

## Added

- STL analyzer:
  `tools/cicada_stl_sidecar/cicada_stl_analyzer.py`
- latest STL analyzer script:
  `scripts/diagnostics/cicada_analyze_latest_stl.ps1`
- latest STL report generator:
  `scripts/diagnostics/cicada_generate_latest_stl_report.ps1`
- quality gate:
  `scripts/diagnostics/cicada_stl_quality_gate.ps1`
- open latest report:
  `scripts/open_latest_stl_report.ps1`
- full one-shot custom box -> STL -> quality gate -> report:
  `scripts/new_run_analyze_box_job.ps1`
- updated artifact inventory to include Reports
- STL proof contract docs
- tracker update

## Report contents

The generated HTML report includes:

- source STL path
- triangle count
- vertex count
- unique vertex count
- bounding box
- dimensions
- surface area estimate
- volume estimate
- edge count
- boundary edge count
- non-manifold edge count
- quality pass/check verdict
- simple SVG preview

## Useful one-shot command

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\new_run_analyze_box_job.ps1" -Name "demo_box" -Width 80 -Depth 40 -Height 12 -OpenReport
```

## Still locked

- direct printer send
- G-code streaming
- serial ports
- slicer CLI automation
- CAD/STEP sidecar

## Next phase

Phase 003G should start the CAD sidecar contract or add a simple preview/report button in Unreal. Still no direct printer control.
