# PHASE CLUSTER 002D - PERSISTENT PROJECT STATE

## Build type

Mainline.

## Goal

Make the Forge UI read project state from a persistent config file.

This is not yet a full project browser. It is the first persistent state seam. Tiny, boring, vital. The software equivalent of remembering where it lives, which is more than some enterprise tools manage.

## Scope

This phase adds:

- `Config/CICADAForgeState.ini`
- `FCICADAForgeProjectState`
- config loading with `GConfig`
- status model built from loaded project state
- Project State status card
- updated evidence/handoff/status docs
- stale-binary clean folded into installer guidance

## Out of scope

Do not add:

- editor settings UI
- saving config from Unreal
- real project browser
- feature graph execution
- CAD export
- sidecar HTTP calls
- live cameras
- machine commands

## Pass condition

Phase 002D passes when:

1. Unreal opens after rebuild.
2. `Window -> CICADA Forge` opens the Forge tab.
3. Tab shows:
   - `Phase 002D: persistent project state feeds the shell`
   - `Project State`
   - `Repo: C:\CICADA\CICADA_APPS\CICADA_FORGE_UE`
   - `LOG: Phase 002D persistent project state loaded.`
4. Evidence is logged.

## Next phase after pass

Phase 002E:
Add minimal UI command stubs as real clickable Slate buttons, still locked/no-op except logging text.

Goal: buttons exist and report selected action without doing dangerous work.
