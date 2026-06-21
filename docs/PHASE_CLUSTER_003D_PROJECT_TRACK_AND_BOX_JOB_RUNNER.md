# PHASE CLUSTER 003D - PROJECT TRACK + BOX JOB RUNNER

## Build type

Mainline cumulative patch.

## Why this phase exists

The project was drifting toward "lots of UI" without enough hard proof that useful manufacturing output is organised and repeatable.

Phase 003D keeps the project on track:

1. keep STL output as the near-term useful proof
2. keep direct printer send locked
3. add repeatable JSON box jobs
4. add a runner that generates STL + manifest + receipt outside Unreal too
5. document what is working, what is next, and what must not be faked

## Added

- JSON box job runner:
  `tools/cicada_stl_sidecar/cicada_box_job_runner.py`
- example jobs:
  - `test_block_20x20x10.json`
  - `thin_plate_80x40x4.json`
  - `box_80x40x12.json`
  - `large_safe_plate_180x120x6.json`
- run one job:
  `scripts/run_box_job.ps1`
- run all jobs:
  `scripts/run_all_box_jobs.ps1`
- validate job files:
  `scripts/diagnostics/cicada_validate_box_job_files.ps1`
- project on-track check:
  `scripts/diagnostics/cicada_project_on_track_check.ps1`
- roadmap/tracker:
  `docs/roadmap/CICADA_FORGE_TRACKER_003D.md`

## Useful result

A user can now generate multiple simple box STLs and print-handoff manifests from repeatable JSON job files.

## Still locked

- direct printer send
- G-code streaming
- serial ports
- slicer CLI automation
- CAD/STEP sidecar

## Next phase

Phase 003E should add editable dimensions in Unreal or a simple local UI for box dimensions. Do not jump to direct printer control yet.
