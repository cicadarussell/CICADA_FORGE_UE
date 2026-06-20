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
- Current patch is Phase 002C: status model feeding the shell.

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

This fixed the Phase 002B stale UI issue.

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

After Phase 002C is pushed, verify:

- `Plugins/CICADAForge/Source/CICADAForgeEditor/Public/CICADAForgeStatusModel.h`
- `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeStatusModel.cpp`
- `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- `docs/process/UNREAL_STALE_BINARY_FIX.md`
- `docs/checklists/PHASE_002C_SMOKE_TEST.md`

Then ask the user for the Unreal result.

Do not move to Phase 003 until the UI reads from the status model or the compile/layout failure is understood.
