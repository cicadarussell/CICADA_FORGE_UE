# SLICER DRY-RUN PLAN CONTRACT

## Purpose

Prepare for future slicer CLI dry-runs without generating G-code yet.

## Allowed

- find slicer executable
- find latest STL
- write candidate command plan
- write HTML/JSON report

## Forbidden

- executing export/slice command
- generating G-code
- sending to printer
- serial/network printer commands
