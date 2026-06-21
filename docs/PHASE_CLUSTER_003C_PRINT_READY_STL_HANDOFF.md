# PHASE CLUSTER 003C - PRINT-READY STL HANDOFF

## Build type

Mainline cumulative patch.

## Goal

Make CICADA Forge more useful for the actual workshop:

> choose a box preset, export STL, open it in a slicer/default app, and generate a locked print handoff manifest.

This still does not directly send to a printer. That comes later, after stronger approval gates.

## Scope

This phase adds:

- print-ready presets:
  - 20 x 20 x 10 mm test block
  - 80 x 40 x 4 mm thin plate
  - 80 x 40 x 12 mm box
- validation against generic 220 x 220 x 250 mm build volume
- ASCII STL export
- default app/slicer STL launch
- richer print handoff manifest
- open STL folder button
- receipt JSON
- slicer discovery script
- latest STL opener script

## Strict boundary

Allowed:

- generate STL
- open STL with Windows default app
- generate handoff manifest
- generate receipt
- open folders

Not allowed:

- stream G-code
- touch serial ports
- send directly to printer
- claim exact CAD/STEP support
- invoke slicer CLI automatically

## Pass condition

Phase 003C passes when:

1. Unreal opens after rebuild.
2. UI shows:
   `Phase 003C: print-ready STL handoff workflow is alive`
3. User selects a preset.
4. User validates sketch + printer fit.
5. User exports STL.
6. User opens STL in default app/slicer.
7. Manifest writes under:
   `Saved/CICADAForge/PrintHandoff`
8. Direct printer send remains locked.

## Next phase after pass

Phase 003D:
Add editable dimensions using safer UI controls and generate a simple viewport/thumbnail proof. Slicer CLI integration remains separate and gated.
