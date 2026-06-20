# PHASE CLUSTER 002A - FORGE UI SHELL

## Build type

Mainline.

## Goal

Add the first visible CICADA Forge UI inside Unreal Editor.

This is not the final interface. This is the first living tab. A tadpole with a menu entry. Try not to bully it.

## Scope

This phase adds:

- `CICADAForgeEditor` module
- Window menu entry:
  `Window -> CICADA Forge`
- nomad tab spawner:
  `CICADAForgeMainTab`
- placeholder Forge workspace Slate tab
- smoke test checklist

## Out of scope

Do not add:

- real node graph
- CAD export
- machine controls
- sidecar HTTP
- live cameras
- asset-heavy UI art
- Comfy/Ollama/agent integration

## Pass condition

Phase 002A passes when:

1. Unreal opens after rebuild.
2. Output Log shows:
   `CICADA Forge Editor module started.`
3. Menu item appears:
   `Window -> CICADA Forge`
4. Clicking it opens a tab titled:
   `CICADA Forge`
5. Evidence is logged.

## Fail condition

Phase 002A fails if:

- plugin descriptor is invalid
- editor module does not compile
- Unreal cannot open project
- menu does not appear
- tab crashes when opened

## Evidence required

- screenshot or statement showing Unreal opened
- screenshot or statement showing the menu exists
- screenshot or statement showing the tab opens
- compile errors if not

## Next phase after pass

Phase 002B:
Replace the single placeholder tab with a structured Forge UI shell:

- left project/action rail
- centre workspace placeholder
- right evidence/status rail
- bottom log strip

No singularity confetti yet. We earn the pretty buttons.
