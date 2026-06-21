# CICADA CAD FEATURES V0.2

## Hole

Through hole on top face.

## Slot

Axis-aligned rounded slot through top face.

Fields:

- x
- y
- length
- width
- angle_deg

V0.2 validates non-zero angle as not exact-exportable yet.

## Standoff

Cylindrical boss on top face.

Fields:

- x
- y
- diameter
- height
- optional pilot_hole_diameter

## Why this is enough for now

Robot plates, sensor mounts, motor mounts, and enclosure blanks usually need holes, slots, and standoffs before they need fancy surfaces.

One boring useful feature beats ten hallucinated manufacturing features. Humanity resists decorative nonsense for another day.
