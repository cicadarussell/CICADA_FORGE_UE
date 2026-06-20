# DECISION 001 - UNREAL AS FORGE COCKPIT

## Decision

CICADA FORGE uses Unreal Engine as the visual cockpit and orchestration layer.

## Reason

Unreal can provide:

- real-time 3D interaction
- live viewport/digital twin
- future node/agent canvas
- camera feeds
- machine status visualisation
- evidence capture
- plugin architecture

## Boundary

Unreal is not treated as the sole manufacturing truth.

Exact CAD/CAM remains in sidecars.

## Consequence

The project architecture is split:

- Unreal = interface, control, interaction, evidence, preview
- sidecars = exact geometry, export, slicing/CAM, machine protocols

## Safety note

Machine execution remains gated and explicit.

No automatic physical machine sending in V0.
