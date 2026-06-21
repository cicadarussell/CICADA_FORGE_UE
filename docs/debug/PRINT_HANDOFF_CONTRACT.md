# PRINT HANDOFF CONTRACT

## Current allowed path

1. Generate STL.
2. Open STL in default slicer/viewer.
3. Inspect model manually.
4. Save handoff manifest.
5. Slice manually.
6. Print manually.

## Current blocked path

CICADA Forge must not:

- send directly to printer
- stream G-code
- open serial ports
- choose printer profile automatically
- bypass slicer inspection

## Current output folders

STL:

`Saved/CICADAForge/STL`

Print handoff manifest:

`Saved/CICADAForge/PrintHandoff`

Receipts:

`Saved/CICADAForge/Receipts`

## Next future upgrade

A later phase may call a slicer CLI only after:

- STL validation passes
- slicer path is explicit
- printer profile is explicit
- user approval exists
- output G-code preview/log is created
- direct send remains separately locked
