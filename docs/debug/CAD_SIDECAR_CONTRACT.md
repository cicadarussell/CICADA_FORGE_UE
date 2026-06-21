# CAD SIDECAR CONTRACT

## Purpose

The CAD sidecar owns exact manufacturing geometry.

Unreal, dashboard, and headless tools may orchestrate, inspect, and display, but they must not pretend mesh STL equals exact CAD.

## V0 part schema

The V0 schema supports:

- one box body
- top-face through holes
- material metadata
- manufacturing hints
- safety lock metadata

## Exact export rule

STEP export is allowed only if an exact CAD engine is available.

Current preferred exact engine:

- CadQuery

Possible future engine:

- FreeCAD Python module / OpenCascade bridge

## No-fake-STEP rule

If no exact CAD engine is available:

- report must say STEP export is blocked
- no fake STEP file
- no triangle mesh renamed as CAD
- no imaginary success state

## Fallback STL rule

Fallback ASCII STL is allowed only for simple box parts without holes/features.

If holes/cuts/features exist and no CAD engine exists:

- do not fake them
- write a blocked report
- tell the user exact engine is required

## Machine boundary

The sidecar must not:

- send printer commands
- stream G-code
- open serial ports
- call CNC/pick-and-place machines
- imply machine readiness

## Outputs

- `Saved/CICADAForge/CADIntent`
- `Saved/CICADAForge/CADExports`
- `Saved/CICADAForge/CADReports`
