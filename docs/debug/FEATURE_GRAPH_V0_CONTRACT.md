# FEATURE GRAPH V0 CONTRACT

## Purpose

Feature Graph V0 records design intent before any CAD geometry exists.

It is not a visual node graph yet. It is not a CAD kernel. It is not a mesh generator.

It is a structured proof that CICADA Forge can track operations, validation state, and dry-run export state.

## Current operation types

- `Primitive.Box`
- `Primitive.Cylinder`
- `Operation.Hole`

## Current fields

Stored as simple lines in Phase 003A:

- op id
- op type
- placeholder parameters
- validation status

## Current persistence

Feature graph dry-run JSON can be written under:

`Saved/CICADAForge/FeatureGraphs`

## Hard boundaries

Phase 003A must not:

- call CAD sidecar
- export STEP/STL
- create machine instructions
- call machine bridge
- pretend geometry exists

## Future

Phase 003B should replace simple operation strings with a real schema:

- id
- type
- parameters object
- parent/target references
- validity
- errors/warnings
- created timestamp
