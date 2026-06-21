# COMMAND CENTER CONTRACT

## Purpose

Provide a local command catalog and generated launcher scripts.

## Safety

The command center may launch checks, reports, dashboards, and builders.

It must not:

- generate G-code
- send to printer
- call serial ports
- contact CNC/pick-and-place/robot machine bridge

## Outputs

- `Saved/CICADAForge/CommandCenter/index.html`
- `Saved/CICADAForge/CommandCenter/command_center.json`
- `Saved/CICADAForge/Launchers/*.ps1`
