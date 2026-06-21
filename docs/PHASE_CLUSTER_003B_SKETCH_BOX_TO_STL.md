# PHASE CLUSTER 003B - SKETCH BOX TO STL

## Build type

Mainline cumulative patch.

## Goal

Make the software useful in the first small manufacturing way:

> create a box from a sketch-like rectangle and export a real STL file.

This is not full CAD. It is not STEP. It is not a slicer. It is not direct printer sending.

It is the first real part-output proof.

## Scope

This phase adds:

- fixed sketch rectangle: 80 x 40 mm
- fixed extrude: 12 mm
- validation
- direct ASCII STL export from Unreal C++
- output folder:
  `Saved/CICADAForge/STL`
- locked print handoff manifest:
  `Saved/CICADAForge/PrintHandoff`
- export receipt:
  `Saved/CICADAForge/Receipts`
- open STL output folder button
- standalone Python STL sidecar backup/debug tool
- STL validation/inventory scripts

## Strict boundary

Allowed:

- generate STL mesh file
- generate print handoff manifest JSON
- generate receipt JSON
- open STL folder

Not allowed:

- send to printer directly
- stream G-code
- talk to serial ports
- run slicer automatically
- generate STEP
- claim exact CAD kernel support

## Pass condition

Phase 003B passes when:

1. Unreal opens after rebuild.
2. UI shows:
   `Phase 003B: sketch box to STL export pipeline is alive`
3. User clicks:
   - Create rectangle 80 x 40 mm
   - Extrude sketch 12 mm
   - Validate sketch box
   - Generate box STL
4. STL appears under:
   `Saved/CICADAForge/STL`
5. STL can be opened by a slicer or mesh viewer.
6. User clicks:
   - Prepare locked print handoff manifest
7. Manifest appears under:
   `Saved/CICADAForge/PrintHandoff`
8. No direct printer command occurs.

## Next phase after pass

Phase 003C:
Add editable dimensions and a basic STL preview/import check, then prepare slicer handoff.
