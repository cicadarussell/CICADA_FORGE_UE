# CICADA FORGE UE MEGA MASTERPLAN

## One-line mission

Build a real-time product creation operating system inside Unreal Engine: design, simulate, validate, export, log, and eventually control manufacturing machines through gated pipelines.

## V0 alpha outcome

A human can open Unreal, create a simple parametric part through CICADA Forge UI, export real STL/STEP via sidecar, preview the result, and commit evidence.

## Long-term outcome

CICADA FORGE becomes the front-end for CICADA SINGULARITY:

- visual node canvas
- agents
- live cameras
- design tools
- CAD/CAM sidecars
- 3D printers/CNC/pick-and-place
- project memory
- automated test/evidence logs
- digital twin of machines/workshop
- safe gated manufacturing

## Architecture

### Unreal layer

Responsible for:

- UI
- viewport
- node canvas
- live visualisation
- project browser
- feature timeline
- camera feeds
- digital twin
- agent/macro orchestration
- machine cockpit
- evidence capture

### CAD sidecar

Responsible for:

- parametric feature graph to exact geometry
- STL export
- STEP export
- geometry validation
- failure reports

Potential technologies:

- CadQuery
- OpenCascade
- FreeCAD headless
- Python service

### CAM / slicer sidecar

Responsible for:

- G-code generation or import
- path preview
- layer/toolpath metadata
- machine bounds checks
- dry-run planning

Potential technologies:

- PrusaSlicer/SuperSlicer CLI
- CuraEngine
- FreeCAD Path
- custom parsers first, not full CAM first

### Machine bridge

Responsible for:

- machine status
- gated job sending
- safe acknowledgement
- logs
- dry-run mode

Potential technologies:

- OctoPrint/Moonraker APIs for 3D printers
- GRBL/FluidNC/LinuxCNC style bridge later
- serial/network protocols through a separate service

## Phase map

| Phase | Name | Goal | Completion after pass |
|---:|---|---|---:|
| 000 | Repo Bootstrap | GitHub/documentation spine | 3% |
| 001 | UE Project Skeleton | Clean UE5.8 project + plugin skeleton | 8% |
| 002 | Forge UI Shell | Browser, timeline, panels, viewport mode | 15% |
| 003 | Feature Graph V0 | JSON feature graph in Unreal | 22% |
| 004 | Primitive Tools | Box, cylinder, move, dimensions | 30% |
| 005 | CAD Sidecar V0 | feature graph to STL/STEP | 42% |
| 006 | Reimport Preview | display generated exact output in Unreal | 50% |
| 007 | Modify Tools | holes, fillets, chamfers, shell | 62% |
| 008 | Evidence Ledger | screenshots, logs, export receipts | 70% |
| 009 | Live Cameras | camera feeds and snapshots | 78% |
| 010 | Manufacturing Preview | G-code/path preview, no send | 86% |
| 011 | Machine Bridge Dry Run | machine status and gated dry-run | 94% |
| 012 | V0 Alpha Demo | bracket/enclosure from design to exported proof | 100% V0 |

## Phase 001A scope

Add only the Unreal project skeleton and plugin skeleton.

Do not add:

- Forge UI
- node canvas
- CAD generation
- live cameras
- machine bridge
- agent system
- Comfy/Ollama integration
- manufacturing send
- asset-heavy Unreal content

The goal is boring but vital: project opens, module loads, repo remains clean.

## Safety/gating rule

No machine receives job commands until:

- geometry is valid
- bounds are known
- material/tool/nozzle is known
- job preview exists
- dry run passes
- human approval is explicit
- logs are written

## Project risk register

| Risk | Severity | Mitigation |
|---|---:|---|
| Unreal mesh mistaken for manufacturing truth | High | feature graph + CAD sidecar |
| Feature sprawl | High | phase gates |
| GitHub repo becomes asset dump | High | .gitignore + LFS + docs |
| ChatGPT loses context | High | handoff/status files |
| Machine damage | High | dry-run and approval gates |
| Build breaks silently | Medium | smoke tests and evidence |
| Unreal plugin complexity | Medium | start with minimal compile target |
| Sidecar integration pain | Medium | local HTTP and strict JSON schema |

## Current locked decision

Use Unreal Engine as CICADA FORGE interface and orchestration layer.

Use sidecars for exact CAD/CAM/manufacturing output.
