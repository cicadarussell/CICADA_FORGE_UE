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
- Phase 002F worked: visible selected-action state.
- Phase 002G worked: mirrored Last Action status.
- Phase 002H worked by user report: Event Log and Output Log show safe click events.
- Phase 002I was assumed passed per user instruction.
- Phase 002J worked by user report/log.
- Phase 002K worked visually by screenshot; user reported right side started overflowing.
- Current patch is Phase 002L: scrollable backend debug cockpit.

## Output-log interpretation

Noisy but non-blocking lines observed include:

- `DerivedDataCache maintenance finished`
- `EOSSDK Config Product Update Request Completed - No Change`
- Slate Roboto font lazy loading
- `aqProf.dll` missing
- `VtuneApi.dll` missing
- PIX/RenderDoc not loaded unless launched from those tools
- XGE license not activated but standalone build continues
- Android/iOS/Linux/Mac SDK not installed
- occasional audio buffer underrun when idle/under load

Important pass signals:

- `Rebuild All: 1 succeeded, 0 failed, 0 skipped`
- `LogCICADAForgeEditor: Display: CICADA Forge safe action stub clicked: ...`
- `LogCICADAForgeEditor: Display: CICADA Forge receipt dry-run save: ...`

## Engineering rules

- truth-first engineering
- no fake working claims
- no silent branch drift
- keep evidence logs
- use phase clusters
- preserve mainline project state
- machine actions must be gated

## Immediate next task

After Phase 002L is pushed, verify:
- `Config/CICADAForgeState.ini`
- `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- `docs/checklists/PHASE_002L_SMOKE_TEST.md`
- `docs/debug/UNREAL_OUTPUT_LOG_TRIAGE.md`

Then ask for:
- screenshot showing scrollable right rail no longer cutting off
- whether Backend Inspector and Backend Health are useful
- whether `Show backend map` clearly lists working/not-built/locked systems
