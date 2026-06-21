# SLICER READINESS CONTRACT

## Purpose

Detect slicer readiness without generating G-code or sending anything to a printer.

## Allowed

- find slicer executables
- report latest STL
- write readiness report
- optionally probe slicer version

## Forbidden

- generating G-code
- sending to printer
- serial ports
- network printer commands
- modifying printer profiles

## Reports

`Saved/CICADAForge/SlicerReports`
