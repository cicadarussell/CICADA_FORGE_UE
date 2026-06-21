# CICADA CAD SIDECAR V0

## What it is

A local exact-geometry boundary for CICADA Forge.

It validates mechanical part intent and, when an exact CAD engine is available, exports exact CAD files.

## V0 supported part

- one rectangular box body
- optional through holes on top face
- material and manufacturing hints
- safety lock metadata

## Engine behaviour

| Engine state | Behaviour |
|---|---|
| CadQuery available | attempts STEP/STL export |
| CadQuery missing | writes report and blocks STEP |
| FreeCAD module available | reported, not primary exporter yet |
| no CAD engine | validates intent and writes blocked report |

## Why this matters

STL is triangles.

STEP is exact CAD.

The sidecar prevents the project from quietly confusing the two, which is how engineering projects turn into decorative lying.
