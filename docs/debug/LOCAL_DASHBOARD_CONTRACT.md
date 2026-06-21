# LOCAL DASHBOARD CONTRACT

## Purpose

The dashboard is a local read/report view over CICADA Forge artifacts.

It exists to reduce the need to open Unreal for every check.

## Allowed

- inventory local artifacts
- read JSON reports/manifests/receipts/jobs
- display latest files
- show safety flags
- show Git status
- generate local HTML
- open local HTML in browser

## Forbidden

- direct printer send
- serial ports
- G-code streaming
- slicer CLI automation
- machine bridge calls
- pretending CAD/STEP sidecar exists

## Output

- `Saved/CICADAForge/Dashboard/index.html`
- `Saved/CICADAForge/Dashboard/cicada_dashboard_snapshot.json`

## Safety requirements

Dashboard snapshot must include:

- `direct_printer_send: false`
- `machine_bridge: LOCKED`

The dashboard is informational only.
