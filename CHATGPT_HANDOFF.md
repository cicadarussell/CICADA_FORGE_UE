# CHATGPT HANDOFF

This file is the short context handoff for any future ChatGPT/Codex/agent session.

## Project identity

CICADA FORGE UE is the Unreal Engine based CICADA SINGULARITY build.

## Current architecture decision

Unreal is the interface and operating environment.

Sidecars handle exact manufacturing:

- CAD sidecar for STEP/STL exact geometry
- CAM/slicer sidecar for G-code/toolpaths
- machine bridge for printers/CNC/robotics
- evidence logger for screenshots/logs/build proofs

## Current proven state

- Phase 001A worked by user report.
- Phase 001B locked the reusable ZIP-to-GitHub app workflow.
- Phase 002A worked by user screenshot: first Forge tab.
- Phase 002B worked by user screenshot: structured cockpit shell.
- Phase 002C worked by user screenshot: status model fed the shell.
- Phase 002D worked by user screenshot: persistent project state fed the shell.
- Phase 002E worked by user report: four buttons clicked and logged safe stub actions.
- Phase 002F is current in GitHub and added visible selected-action state.
- Current patch is Phase 002G: mirrored Last Action status card.

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

## Standing Unreal stale-binary fix

If GitHub/local source shows a newer phase but Unreal still displays old UI text:

1. Close Unreal fully.
2. Delete root/plugin `Binaries`, `Intermediate`, and root `Saved`.
3. Reopen `.uproject`.
4. Allow one rebuild.
5. Re-test the tab.

## Current issue fixed in Phase 002G

The user output log showed:

```text
ImportText (ProjectID): Missing opening parenthesis
LoadConfig ... import failed for ProjectID
```

Phase 002G changes `Config/DefaultGame.ini` from brace GUID format to Unreal struct-style `ProjectID=(A=...,B=...,C=...,D=...)`.

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

After Phase 002G is pushed, verify:

- `Config/DefaultGame.ini`
- `Config/CICADAForgeState.ini`
- `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- `docs/checklists/PHASE_002G_SMOKE_TEST.md`

Then ask the user for:
- screenshot showing right-rail Last Action update
- whether Output Log still has safe stub click logs
- whether ProjectID import warning is gone

Do not move to Phase 002H until Last Action mirror works.
