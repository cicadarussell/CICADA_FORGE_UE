# HEADLESS CONTROL TOWER CONTRACT

## Purpose

The headless control tower exists so the CICADA Forge pipeline can be tested without opening Unreal Engine.

## Allowed actions

- check files
- generate local box jobs
- generate STL
- generate manifest
- generate receipt
- analyze STL
- generate reports
- open reports/STLs through Windows file association
- inventory artifacts

## Forbidden actions

- direct printer send
- serial ports
- G-code streaming
- machine bridge calls
- slicer CLI automation unless later explicitly gated
- pretending exact CAD/STEP exists

## Output folders

- `Saved/CICADAForge/BoxJobs`
- `Saved/CICADAForge/STL`
- `Saved/CICADAForge/Reports`
- `Saved/CICADAForge/RunReports`
- `Saved/CICADAForge/PrintHandoff`
- `Saved/CICADAForge/Receipts`

## Pass condition

`full-check` passes only when:

- required files exist
- box job runs
- STL is generated
- quality gate passes
- report is generated
- print manifest confirms:
  - `direct_printer_send: false`
  - `machine_bridge: LOCKED`

## Why this matters

Unreal should become the cockpit, not the only test environment.

Headless tools keep the engineering loop fast and measurable.
