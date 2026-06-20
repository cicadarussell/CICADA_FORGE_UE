# CICADA FORGE UE

Unreal Engine based CICADA FORGE / CICADA SINGULARITY project.

## Mission

Build a real-time product creation operating system inside Unreal Engine: design, simulate, validate, export, log, and eventually control manufacturing machines through gated pipelines.

## Core thesis

Unreal Engine is the visual forge, node workspace, live camera hub, agent cockpit, evidence logger, simulation layer, and machine-control command centre.

Exact manufacturing truth stays in sidecar systems:

- CAD sidecar for parametric solid generation
- CAM/slicer sidecar for G-code/toolpath generation
- machine bridge for gated communication with printers/CNC/robots
- run ledger for proof, logs, screenshots, and failure evidence

This repo is not a random Unreal project folder dump. It is the source-of-truth spine for a multi-month build.

## Current status

Phase Cluster 001A: UE5.8 project file and CICADAForge plugin skeleton.

Progress estimate after extraction and commit: 6 percent.

Phase 001 is not fully passed until the project opens in Unreal 5.8 and the plugin skeleton compiles/loads.

## Truth-first boundary

Unreal geometry is excellent for interaction, preview, simulation, and workflow control.

It is not the only manufacturing source of truth.

CICADA FORGE stores design intent as structured feature data, then sidecar CAD/CAM systems create exact export files.

## First proof target

Inside Unreal:

1. Open CICADA Forge workspace.
2. Create a parametric mounting bracket feature graph.
3. Send feature graph to sidecar.
4. Generate STL/STEP.
5. Reimport/display output.
6. Save evidence log.

No blind machine sending in V0.

## Phase 001A install

Extract the Phase 001 patch ZIP into the repo root:

`C:\CICADA\CICADA_APPS\CICADA_FORGE_UE`

Then commit and push with GitHub Desktop:

`Phase 001A: Add UE project and CICADAForge plugin skeleton`

Then double-click:

`CICADA_FORGE_UE.uproject`

If Unreal asks to rebuild modules, allow it once. If it fails, capture the error and do not keep clicking random buttons like a desperate ape at a vending machine.
