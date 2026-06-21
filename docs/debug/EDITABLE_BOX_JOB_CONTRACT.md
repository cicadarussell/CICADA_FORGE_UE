# EDITABLE BOX JOB CONTRACT

## Source of truth

Editable box jobs are JSON files.

Minimum schema:

```json
{
  "name": "custom_box",
  "box_mm": {
    "width": 80,
    "depth": 40,
    "height": 12
  },
  "material": "PLA",
  "layer_height_mm": 0.2,
  "walls": 3,
  "infill_percent": 15,
  "supports": "off",
  "direct_printer_send": false,
  "machine_bridge": "LOCKED"
}
```

## Validation

The V0 generic build volume is:

- width: 220 mm
- depth: 220 mm
- height: 250 mm

## Outputs

Runner creates:

- STL
- print handoff manifest
- receipt

## Hard safety boundary

Job runner must not:

- call serial ports
- stream G-code
- send to printer
- launch slicer CLI automatically
- claim STEP/CAD support
