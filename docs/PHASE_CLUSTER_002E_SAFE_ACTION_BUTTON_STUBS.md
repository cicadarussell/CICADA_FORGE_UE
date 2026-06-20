# PHASE CLUSTER 002E - SAFE ACTION BUTTON STUBS

## Build type

Mainline.

## Goal

Turn the left-rail action labels into real clickable Slate buttons.

The buttons must be safe stubs only. They log that they were clicked. They do not create designs, open graphs, run validation, export proof, touch files, talk to sidecars, or command machines.

Tiny buttons. No teeth yet.

## Scope

This phase adds:

- Slate `SButton` action stubs
- Output Log message on click
- updated phase config
- updated evidence/checklist docs

## Out of scope

Do not add:

- real project creation
- real graph opening
- real validation
- real export
- file write actions
- CAD sidecar calls
- live camera calls
- machine commands

## Pass condition

Phase 002E passes when:

1. Unreal opens after rebuild.
2. `Window -> CICADA Forge` opens the Forge tab.
3. UI shows:
   - `Phase 002E: action button stubs are alive`
   - buttons for New design, Open feature graph, Run validation, Export proof receipt
4. Clicking buttons writes Output Log entries:
   `CICADA Forge safe action stub clicked:`
5. No machine/CAD/sidecar action occurs.

## Next phase after pass

Phase 002F:
Add selected-action UI state so button clicks visibly update a status line inside the Forge tab, not just Output Log.
