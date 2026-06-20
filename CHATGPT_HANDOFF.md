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

## Why

The user likes the Unreal route because it can become:
- a live visual node/agent workspace
- a 3D digital twin of the workshop
- a software maker
- a product forge
- a machine command cockpit
- a future CICADA macro/agent environment

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

## Immediate next phase

Phase Cluster 001:
Create UE5.8 project cleanly, commit only source/config/docs/plugin skeleton, add .gitignore/.gitattributes, then add CICADAForge plugin skeleton.
