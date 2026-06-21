# SKETCH TO STL CONTRACT

## Purpose

Phase 003B provides the first useful manufacturing artifact from CICADA Forge:

- sketch-like rectangle
- extrude
- validate
- generate STL
- prepare locked print handoff manifest

## Current dimensions

- width: 80 mm
- depth: 40 mm
- height: 12 mm

## Output

STL:

`Saved/CICADAForge/STL`

Print handoff manifest:

`Saved/CICADAForge/PrintHandoff`

Receipt:

`Saved/CICADAForge/Receipts`

## Hard limits

This is STL mesh export only.

It is not:

- STEP
- exact CAD B-rep
- slicer integration
- printer control
- G-code generation
- serial communication

## Safety rule

Direct printer send remains locked.

Manual workflow:

1. export STL
2. open STL in slicer
3. inspect model
4. choose printer/material/profile
5. slice manually
6. print manually
