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

- Phase 001A worked by user report.
- Root `.uproject` exists.
- `CICADAForge` runtime module exists.
- Phase 001B locked the reusable ZIP-to-GitHub app workflow.
- Phase 002A worked by user screenshot: Unreal opened the CICADA Forge tab and showed `Phase 002A: Forge UI shell is alive.`
- Phase 002B worked by user screenshot: Unreal opened the structured cockpit shell with project/workspace/status/log panels.
- Phase 002C worked by user screenshot: status model fed the UI shell.
- Current patch is Phase 002D: persistent project state stub.

## Standing CICADA app development workflow

Use this pattern for this repo and future CICADA apps:

1. ChatGPT gives a ZIP download link at the top.
2. ChatGPT gives completion percentages.
3. User downloads ZIP.
4. User runs a PowerShell extractor into the local repo root.
5. Installer includes stale Unreal binary clean when C++ changes are likely.
6. User commits and pushes through GitHub Desktop.
7. ChatGPT reads GitHub and verifies.
8. User asks for next phase cluster.
9. Repeat.

This is the default structure until direct repo write automation is available.

## Standing Unreal stale-binary fix

If GitHub/local source shows a newer phase but Unreal still displays old UI text:

1. Close Unreal fully.
2. Delete:
   - root `Binaries`
   - root `Intermediate`
   - root `Saved`
   - plugin `Plugins/CICADAForge/Binaries`
   - plugin `Plugins/CICADAForge/Intermediate`
3. Reopen `.uproject`.
4. Allow one rebuild.
5. Re-test the tab.

This fixed the Phase 002B stale UI issue and was also required after Phase 002C.

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

## Immediate next task for future assistant

After Phase 002D is pushed, verify:

- `Config/CICADAForgeState.ini`
- `Plugins/CICADAForge/Source/CICADAForgeEditor/Public/CICADAForgeProjectState.h`
- `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeProjectState.cpp`
- `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeStatusModel.cpp`
- `docs/checklists/PHASE_002D_SMOKE_TEST.md`

Then ask the user for the Unreal result.

Do not move to Phase 002E until persistent project state appears in the UI or the compile/config failure is understood.
