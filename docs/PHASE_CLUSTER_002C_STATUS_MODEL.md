# PHASE CLUSTER 002C - STATUS MODEL

## Build type

Mainline.

## Goal

Move the Forge shell text/state into a small status model.

This is the first step toward the UI being driven by state instead of hardcoded text scattered around Slate layout code like breadcrumbs left by a caffeinated pigeon.

## Scope

This phase adds:

- `FCICADAForgeStatusModel`
- `FCICADAForgePanelCard`
- default Phase 002C model factory
- editor UI reads project name, phase label, action stubs, workspace cards, status cards, and bottom log from the model

## Out of scope

Do not add:

- persistent project files
- real interactive buttons
- real feature graph execution
- CAD export
- sidecar HTTP calls
- live cameras
- machine commands

## Pass condition

Phase 002C passes when:

1. Unreal opens after rebuild.
2. `Window -> CICADA Forge` opens the Forge tab.
3. Tab shows:
   - `Phase 002C: status model feeds the shell`
   - `LOG: Phase 002C status model loaded.`
4. Project/workspace/status panels still appear.
5. Evidence is logged.

## Next phase after pass

Phase 002D:
Add persistent editor settings / project state stub.

Likely target:

- repo path display
- current phase display
- sidecar status enum
- machine bridge locked state enum
- evidence status enum

Still no real machine control.
