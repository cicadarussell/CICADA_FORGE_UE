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

## Current phase

Phase Cluster 001A.

This patch adds the first Unreal project file and a minimal C++ plugin skeleton named `CICADAForge`.

## Immediate next task for future assistant

Verify these files exist in GitHub:

- `CICADA_FORGE_UE.uproject`
- `Plugins/CICADAForge/CICADAForge.uplugin`
- `Plugins/CICADAForge/Source/CICADAForge/CICADAForge.Build.cs`
- `Plugins/CICADAForge/Source/CICADAForge/Public/CICADAForgeModule.h`
- `Plugins/CICADAForge/Source/CICADAForge/Private/CICADAForgeModule.cpp`
- `docs/checklists/PHASE_001_SMOKE_TEST.md`
- `docs/evidence/EVIDENCE_LOG.md`

Then ask the user for the Unreal open/build result.

Do not start Phase 002 until Phase 001 smoke test passes or the failure is understood.
