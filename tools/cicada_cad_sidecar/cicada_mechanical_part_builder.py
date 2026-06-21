from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))


def safe_name(name: str) -> str:
    value = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name).strip("_")
    return value or "cicada_part"


def base_part(name: str, material: str, width: float, depth: float, height: float) -> dict[str, Any]:
    return {
        "schema_version": "cicada_part_v0_2",
        "part_id": safe_name(name),
        "units": "mm",
        "material": material,
        "bodies": [
            {
                "id": "body_001",
                "type": "box",
                "width": float(width),
                "depth": float(depth),
                "height": float(height),
                "origin": [0, 0, 0],
            }
        ],
        "features": [],
        "manufacturing": {
            "process": "3d_print",
            "layer_height_mm": 0.24,
            "walls": 4,
            "infill_percent": 25,
            "supports": "off",
        },
        "safety": {
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        },
    }


def add_hole(part: dict[str, Any], hole_id: str, x: float, y: float, diameter: float) -> None:
    part["features"].append(
        {"id": hole_id, "type": "hole", "target_body": "body_001", "face": "top", "x": float(x), "y": float(y), "diameter": float(diameter), "depth": "through"}
    )


def add_slot(part: dict[str, Any], slot_id: str, x: float, y: float, length: float, width: float, angle_deg: float = 0.0) -> None:
    part["features"].append(
        {"id": slot_id, "type": "slot", "target_body": "body_001", "face": "top", "x": float(x), "y": float(y), "length": float(length), "width": float(width), "angle_deg": float(angle_deg), "depth": "through"}
    )


def add_standoff(part: dict[str, Any], standoff_id: str, x: float, y: float, diameter: float, height: float, pilot_hole_diameter: float = 0.0) -> None:
    part["features"].append(
        {"id": standoff_id, "type": "standoff", "target_body": "body_001", "face": "top", "x": float(x), "y": float(y), "diameter": float(diameter), "height": float(height), "pilot_hole_diameter": float(pilot_hole_diameter)}
    )


def mounting_plate(name: str, width: float, depth: float, height: float, hole_diameter: float, inset: float, material: str, holes: int) -> dict[str, Any]:
    part = base_part(name, material, width, depth, height)
    if holes not in (2, 4):
        raise ValueError("mounting-plate holes must be 2 or 4")

    y_mid = depth / 2.0
    add_hole(part, "hole_001", inset, y_mid, hole_diameter)
    add_hole(part, "hole_002", width - inset, y_mid, hole_diameter)

    if holes == 4:
        add_hole(part, "hole_003", inset, inset, hole_diameter)
        add_hole(part, "hole_004", width - inset, depth - inset, hole_diameter)

    part["manufacturing"]["infill_percent"] = 30
    return part


def robot_mount_plate(name: str, width: float, depth: float, height: float, rail_spacing: float, hole_diameter: float, material: str) -> dict[str, Any]:
    part = base_part(name, material, width, depth, height)

    x_left = (width - rail_spacing) / 2.0
    x_right = (width + rail_spacing) / 2.0
    y_front = depth * 0.25
    y_back = depth * 0.75

    add_hole(part, "rail_hole_001", x_left, y_front, hole_diameter)
    add_hole(part, "rail_hole_002", x_right, y_front, hole_diameter)
    add_hole(part, "rail_hole_003", x_left, y_back, hole_diameter)
    add_hole(part, "rail_hole_004", x_right, y_back, hole_diameter)

    part["manufacturing"]["infill_percent"] = 40
    return part


def enclosure_blank(name: str, width: float, depth: float, height: float, hole_diameter: float, inset: float, material: str) -> dict[str, Any]:
    part = base_part(name, material, width, depth, height)

    add_hole(part, "corner_hole_001", inset, inset, hole_diameter)
    add_hole(part, "corner_hole_002", width - inset, inset, hole_diameter)
    add_hole(part, "corner_hole_003", inset, depth - inset, hole_diameter)
    add_hole(part, "corner_hole_004", width - inset, depth - inset, hole_diameter)

    part["manufacturing"]["infill_percent"] = 20
    return part


def sensor_plate(name: str, width: float, depth: float, height: float, material: str) -> dict[str, Any]:
    part = base_part(name, material, width, depth, height)

    add_slot(part, "mount_slot_001", width * 0.30, depth * 0.25, 24, 5)
    add_slot(part, "mount_slot_002", width * 0.70, depth * 0.25, 24, 5)
    add_slot(part, "strap_slot_001", width * 0.30, depth * 0.75, 30, 4)
    add_slot(part, "strap_slot_002", width * 0.70, depth * 0.75, 30, 4)
    add_standoff(part, "sensor_standoff_001", width * 0.40, depth * 0.50, 8, 6, 2.4)
    add_standoff(part, "sensor_standoff_002", width * 0.60, depth * 0.50, 8, 6, 2.4)

    part["manufacturing"]["infill_percent"] = 35
    return part


def slotted_motor_mount(name: str, width: float, depth: float, height: float, material: str, slot_length: float, slot_width: float, hole_diameter: float) -> dict[str, Any]:
    part = base_part(name, material, width, depth, height)

    add_slot(part, "adjust_slot_001", width * 0.32, depth * 0.50, slot_length, slot_width)
    add_slot(part, "adjust_slot_002", width * 0.68, depth * 0.50, slot_length, slot_width)
    add_hole(part, "locator_hole_001", width * 0.50, depth * 0.25, hole_diameter)
    add_hole(part, "locator_hole_002", width * 0.50, depth * 0.75, hole_diameter)

    part["manufacturing"]["infill_percent"] = 45
    return part


def write_part(repo: Path, part: dict[str, Any], out: Path | None) -> Path:
    if out is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = repo / "Saved" / "CICADAForge" / "CADIntent"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{safe_name(part['part_id'])}_{stamp}.part.json"
    else:
        out.parent.mkdir(parents=True, exist_ok=True)

    out.write_text(json.dumps(part, indent=2), encoding="utf-8")
    print(f"CAD intent: {out}")
    print("Direct printer send: LOCKED")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA CAD mechanical part builder. Writes safe part-intent JSON only.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    sub = parser.add_subparsers(dest="command", required=True)

    mp = sub.add_parser("mounting-plate")
    mp.add_argument("--name", default="mounting_plate")
    mp.add_argument("--width", type=float, default=100)
    mp.add_argument("--depth", type=float, default=40)
    mp.add_argument("--height", type=float, default=6)
    mp.add_argument("--hole-diameter", type=float, default=5)
    mp.add_argument("--inset", type=float, default=12)
    mp.add_argument("--holes", type=int, choices=[2, 4], default=2)
    mp.add_argument("--material", default="PETG")
    mp.add_argument("--out", type=Path)

    rp = sub.add_parser("robot-plate")
    rp.add_argument("--name", default="robot_mount_plate")
    rp.add_argument("--width", type=float, default=120)
    rp.add_argument("--depth", type=float, default=70)
    rp.add_argument("--height", type=float, default=8)
    rp.add_argument("--rail-spacing", type=float, default=60)
    rp.add_argument("--hole-diameter", type=float, default=4.2)
    rp.add_argument("--material", default="PETG")
    rp.add_argument("--out", type=Path)

    enc = sub.add_parser("enclosure-blank")
    enc.add_argument("--name", default="electronics_enclosure_blank")
    enc.add_argument("--width", type=float, default=120)
    enc.add_argument("--depth", type=float, default=70)
    enc.add_argument("--height", type=float, default=28)
    enc.add_argument("--hole-diameter", type=float, default=3.4)
    enc.add_argument("--inset", type=float, default=12)
    enc.add_argument("--material", default="PETG")
    enc.add_argument("--out", type=Path)

    sp = sub.add_parser("sensor-plate")
    sp.add_argument("--name", default="robot_sensor_plate")
    sp.add_argument("--width", type=float, default=120)
    sp.add_argument("--depth", type=float, default=70)
    sp.add_argument("--height", type=float, default=6)
    sp.add_argument("--material", default="PETG")
    sp.add_argument("--out", type=Path)

    sm = sub.add_parser("slotted-motor-mount")
    sm.add_argument("--name", default="slotted_motor_mount")
    sm.add_argument("--width", type=float, default=100)
    sm.add_argument("--depth", type=float, default=60)
    sm.add_argument("--height", type=float, default=8)
    sm.add_argument("--material", default="PETG")
    sm.add_argument("--slot-length", type=float, default=28)
    sm.add_argument("--slot-width", type=float, default=5.2)
    sm.add_argument("--hole-diameter", type=float, default=4.2)
    sm.add_argument("--out", type=Path)

    args = parser.parse_args()

    if args.command == "mounting-plate":
        part = mounting_plate(args.name, args.width, args.depth, args.height, args.hole_diameter, args.inset, args.material, args.holes)
    elif args.command == "robot-plate":
        part = robot_mount_plate(args.name, args.width, args.depth, args.height, args.rail_spacing, args.hole_diameter, args.material)
    elif args.command == "enclosure-blank":
        part = enclosure_blank(args.name, args.width, args.depth, args.height, args.hole_diameter, args.inset, args.material)
    elif args.command == "sensor-plate":
        part = sensor_plate(args.name, args.width, args.depth, args.height, args.material)
    elif args.command == "slotted-motor-mount":
        part = slotted_motor_mount(args.name, args.width, args.depth, args.height, args.material, args.slot_length, args.slot_width, args.hole_diameter)
    else:
        raise AssertionError("Unhandled command")

    write_part(args.repo, part, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
