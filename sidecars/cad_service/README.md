# CAD Sidecar

This service will receive `.cforge.json` feature graphs and generate exact CAD outputs.

Planned outputs:
- STL
- STEP
- validation report JSON
- preview mesh metadata

Potential backend:
- CadQuery
- OpenCascade
- FreeCAD headless

V0 endpoint idea:
- `POST /build`
- input: feature graph JSON
- output: receipt JSON + paths to STL/STEP
