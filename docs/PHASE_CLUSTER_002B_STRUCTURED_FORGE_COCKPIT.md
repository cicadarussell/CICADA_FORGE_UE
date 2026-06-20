# PHASE CLUSTER 002B - STRUCTURED FORGE COCKPIT

## Build type

Mainline.

## Goal

Upgrade the first CICADA Forge editor tab from a text placeholder into a structured cockpit shell.

This is still not a real app. It is the first useful skeleton of the app shape. Skeletons first. Muscles later. Lasers much later, despite humanity's tragic instincts.

## Scope

This phase adds:

- left project/action rail
- centre workspace section
- right evidence/status rail
- bottom log strip
- explicit machine/CAD lock notes

## Out of scope

Do not add:

- real buttons
- persistent data
- feature graph execution
- CAD export
- sidecar HTTP calls
- live cameras
- machine commands
- generated assets

## Pass condition

Phase 002B passes when:

1. Unreal opens after rebuild.
2. `Window -> CICADA Forge` opens the Forge tab.
3. Tab shows:
   - `PROJECT`
   - `FORGE WORKSPACE`
   - `STATUS`
   - `LOG: Phase 002B shell loaded.`
4. Evidence is logged.

## Fail condition

Phase 002B fails if:

- Unreal cannot compile the editor module
- tab cannot open
- layout crashes
- the previous Phase 002A tab disappears

## Next phase after pass

Phase 002C:
Add a small in-memory status model feeding the UI labels instead of hardcoded text.

That prepares the way for real project status, sidecar status, evidence status, and phase gates.
