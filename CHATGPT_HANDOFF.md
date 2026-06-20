# CHATGPT HANDOFF

This file is the short context handoff for any future ChatGPT/Codex/agent session.

## Project identity

CICADA FORGE UE is the Unreal Engine based CICADA SINGULARITY build.

The user wants Unreal Engine to become the main design/coding/machine-control forge:

- design inside Unreal
- build software systems inside Unreal
- use live cameras
- orchestrate CAD/CAM/slicers/machines
- later add agents/macros
- preserve full project continuity through GitHub

## Current architecture decision

Unreal is the interface and operating environment.

Sidecars handle exact manufacturing:

- CAD sidecar for STEP/STL exact geometry
- CAM/slicer sidecar for G-code/toolpaths
- machine bridge for printers/CNC/robotics
- evidence logger for screenshots/logs/build proofs

## Current proven state

User reported that Phase 001A worked.

Phase 001A added and pushed:

- `CICADA_FORGE_UE.uproject`
- `Plugins/CICADAForge/CICADAForge.uplugin`
- minimal `CICADAForge` runtime C++ module
- Phase 001 smoke test docs

The next normal technical build is Phase 002A: Forge UI Shell skeleton.

## Standing CICADA app development workflow

Use this pattern for this repo and future CICADA apps:

1. ChatGPT gives a ZIP download link at the top.
2. ChatGPT gives completion percentages.
3. User downloads ZIP.
4. User runs a PowerShell extractor into the local repo root.
5. User commits and pushes through GitHub Desktop.
6. ChatGPT reads GitHub and verifies.
7. User asks for next phase cluster.
8. Repeat.

This is the default structure until direct repo write automation is available.

## Engineering rules

Use truth-first engineering:

- separate facts, assumptions, speculation, unknowns
- no fake working claims
- no silent branch drift
- no rebuilding from scratch when patching one layer
- keep evidence logs
- use phase clusters
- always preserve mainline project state
- machine actions must be gated

## V0 alpha goal

Open Unreal and use CICADA Forge to create a simple bracket/enclosure feature graph, export STL/STEP through a sidecar, reimport/display it, and record evidence.

## Immediate next task for future assistant

Verify Phase 001B exists, then begin Phase 002A.

Phase 002A should add the smallest useful Forge UI shell, not the whole singularity dressed as a spreadsheet demon.
