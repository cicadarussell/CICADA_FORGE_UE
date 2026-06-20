# Architecture Overview

## Core model

CICADA FORGE UE is split into four layers:

1. Unreal Engine Forge Layer
2. Exact CAD/CAM Sidecars
3. Machine Bridge Services
4. Project Memory / Evidence Ledger

## Data flow

User/Agent action in Unreal
→ structured feature/event JSON
→ validation
→ sidecar execution
→ exported artifact
→ reimport/preview in Unreal
→ evidence log
→ optional gated machine action

## Primary file types

| File | Purpose |
|---|---|
| `.cforge.json` | CICADA Forge project feature graph |
| `.uasset` / `.umap` | Unreal assets/maps |
| `.step` | exact CAD exchange |
| `.stl` | mesh export for printing |
| `.gcode` | manufacturing job |
| `.receipt.json` | evidence/job receipt |
| `.log` | sidecar/system logs |

## Boundary

Unreal previews geometry.
Sidecars create manufacturing truth.
