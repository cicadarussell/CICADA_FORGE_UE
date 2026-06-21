# STL PROOF GATE CONTRACT

## Purpose

Before slicer automation or printer bridge work, the STL file must be measurable and inspectable.

## Current checks

The STL analyzer checks:

- ASCII STL vertex parsing
- triangle count
- vertex count
- unique vertex count
- bounding box
- dimensions
- surface area
- volume
- edge usage
- boundary edges
- non-manifold edges

## Quality pass

A V0 STL quality pass requires:

- at least one triangle
- positive dimensions
- positive volume estimate
- no boundary edges
- every edge used exactly twice

## Current report output

Reports are written to:

`Saved/CICADAForge/Reports`

## Safety boundary

The quality gate does not send prints.

It only says whether the STL appears sane enough for manual slicer inspection.

## Future upgrades

Later gates should add:

- binary STL parsing
- unit metadata checks
- slicer CLI dry-run
- G-code stats
- preview thumbnails from actual mesh
- printer profile compatibility
