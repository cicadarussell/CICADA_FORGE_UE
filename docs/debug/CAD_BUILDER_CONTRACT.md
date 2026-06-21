# CAD BUILDER CONTRACT

## Purpose

The CAD builder creates safe CAD-intent JSON for common mechanical primitives.

It does not send machine commands.

## Current builders

- mounting plate
- robot plate
- enclosure blank

## Output

- `Saved/CICADAForge/CADIntent/*.part.json`
- `Saved/CICADAForge/CADReports/*.cad_report.json`
- `Saved/CICADAForge/CADReports/*.cad_report.html`
- optional `Saved/CICADAForge/CADExports/*` if exact engine exists

## Safety

Every generated part must include:

```json
{
  "direct_printer_send": false,
  "machine_bridge": "LOCKED"
}
```

## No-fake-STEP rule

If exact engine is missing, report blocked STEP.

Do not rename STL as STEP.

Do not fake holes/cuts/features.
