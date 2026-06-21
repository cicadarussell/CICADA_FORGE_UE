from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


REPO = Path(r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE")
SAVED = REPO / "Saved" / "CICADAForge"
STL_DIR = SAVED / "STL"
MANIFEST_DIR = SAVED / "PrintHandoff"
RECEIPT_DIR = SAVED / "Receipts"
JOB_DIR = SAVED / "BoxJobs"

GENERIC_PRINTER_VOLUME = {
    "width": 220.0,
    "depth": 220.0,
    "height": 250.0,
}


@dataclass(frozen=True)
class BoxJob:
    name: str
    width_mm: float
    depth_mm: float
    height_mm: float
    material: str = "PLA"
    layer_height_mm: float = 0.20
    walls: int = 3
    infill_percent: int = 15
    supports: str = "off"
    note: str = ""


def safe_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name).strip("_") or "CICADA_Box"


def load_job(path: Path) -> BoxJob:
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    box = data.get("box_mm", data)

    job = BoxJob(
        name=str(data.get("name", path.stem)),
        width_mm=float(box["width"]),
        depth_mm=float(box["depth"]),
        height_mm=float(box["height"]),
        material=str(data.get("material", "PLA")),
        layer_height_mm=float(data.get("layer_height_mm", 0.20)),
        walls=int(data.get("walls", 3)),
        infill_percent=int(data.get("infill_percent", 15)),
        supports=str(data.get("supports", "off")),
        note=str(data.get("note", "")),
    )

    validate_job(job)
    return job


def validate_job(job: BoxJob) -> None:
    if min(job.width_mm, job.depth_mm, job.height_mm) <= 0:
        raise ValueError("All box dimensions must be positive.")

    if job.width_mm > GENERIC_PRINTER_VOLUME["width"] or job.depth_mm > GENERIC_PRINTER_VOLUME["depth"] or job.height_mm > GENERIC_PRINTER_VOLUME["height"]:
        raise ValueError("Box exceeds generic 220 x 220 x 250 mm build volume.")

    if job.layer_height_mm <= 0:
        raise ValueError("Layer height must be positive.")

    if job.walls < 1:
        raise ValueError("Walls must be at least 1.")

    if not 0 <= job.infill_percent <= 100:
        raise ValueError("Infill percent must be 0 to 100.")


def tri(a: tuple[float, float, float], b: tuple[float, float, float], c: tuple[float, float, float]) -> str:
    return (
        "  facet normal 0 0 0\n"
        "    outer loop\n"
        f"      vertex {a[0]:.6f} {a[1]:.6f} {a[2]:.6f}\n"
        f"      vertex {b[0]:.6f} {b[1]:.6f} {b[2]:.6f}\n"
        f"      vertex {c[0]:.6f} {c[1]:.6f} {c[2]:.6f}\n"
        "    endloop\n"
        "  endfacet\n"
    )


def build_box_stl(job: BoxJob) -> str:
    w, d, h = job.width_mm, job.depth_mm, job.height_mm
    v000 = (0.0, 0.0, 0.0)
    v100 = (w, 0.0, 0.0)
    v110 = (w, d, 0.0)
    v010 = (0.0, d, 0.0)
    v001 = (0.0, 0.0, h)
    v101 = (w, 0.0, h)
    v111 = (w, d, h)
    v011 = (0.0, d, h)

    triangles = [
        (v000, v110, v100), (v000, v010, v110),
        (v001, v101, v111), (v001, v111, v011),
        (v000, v100, v101), (v000, v101, v001),
        (v010, v011, v111), (v010, v111, v110),
        (v000, v001, v011), (v000, v011, v010),
        (v100, v110, v111), (v100, v111, v101),
    ]

    solid_name = safe_name(job.name)
    return f"solid {solid_name}\n" + "".join(tri(*t) for t in triangles) + f"endsolid {solid_name}\n"


def create_job_file(
    name: str,
    width: float,
    depth: float,
    height: float,
    material: str,
    layer_height: float,
    walls: int,
    infill: int,
    supports: str,
    note: str,
    out: Path | None = None,
) -> Path:
    job = BoxJob(
        name=name,
        width_mm=width,
        depth_mm=depth,
        height_mm=height,
        material=material,
        layer_height_mm=layer_height,
        walls=walls,
        infill_percent=infill,
        supports=supports,
        note=note,
    )
    validate_job(job)

    JOB_DIR.mkdir(parents=True, exist_ok=True)
    out_path = out or (JOB_DIR / f"{safe_name(name)}.json")

    payload = {
        "name": job.name,
        "box_mm": {
            "width": job.width_mm,
            "depth": job.depth_mm,
            "height": job.height_mm,
        },
        "material": job.material,
        "layer_height_mm": job.layer_height_mm,
        "walls": job.walls,
        "infill_percent": job.infill_percent,
        "supports": job.supports,
        "note": job.note,
        "direct_printer_send": False,
        "machine_bridge": "LOCKED",
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path


def job_summary(job: BoxJob) -> dict[str, Any]:
    volume_mm3 = job.width_mm * job.depth_mm * job.height_mm
    top_area_mm2 = job.width_mm * job.depth_mm
    fits = (
        job.width_mm <= GENERIC_PRINTER_VOLUME["width"]
        and job.depth_mm <= GENERIC_PRINTER_VOLUME["depth"]
        and job.height_mm <= GENERIC_PRINTER_VOLUME["height"]
    )
    return {
        "name": job.name,
        "box_mm": {
            "width": job.width_mm,
            "depth": job.depth_mm,
            "height": job.height_mm,
        },
        "volume_mm3": volume_mm3,
        "top_area_mm2": top_area_mm2,
        "fits_generic_220x220x250": fits,
        "material": job.material,
        "layer_height_mm": job.layer_height_mm,
        "walls": job.walls,
        "infill_percent": job.infill_percent,
        "supports": job.supports,
        "direct_printer_send": False,
        "machine_bridge": "LOCKED",
    }


def write_outputs(job: BoxJob, open_stl: bool = False) -> dict[str, str]:
    validate_job(job)

    STL_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{safe_name(job.name)}_{job.width_mm:.0f}x{job.depth_mm:.0f}x{job.height_mm:.0f}_{stamp}"

    stl_path = STL_DIR / f"{base}.stl"
    manifest_path = MANIFEST_DIR / f"{base}.print_handoff.json"
    receipt_path = RECEIPT_DIR / f"{base}.receipt.json"

    stl_path.write_text(build_box_stl(job), encoding="utf-8")

    manifest = {
        "project": "CICADA_FORGE_UE",
        "phase": "003E",
        "job_name": job.name,
        "stl_path": str(stl_path),
        "direct_printer_send": False,
        "gcode_streaming": False,
        "machine_bridge": "LOCKED",
        "manual_next_step": "Open STL in slicer, inspect, slice manually, print manually.",
        "box_mm": {
            "width": job.width_mm,
            "depth": job.depth_mm,
            "height": job.height_mm,
        },
        "derived": job_summary(job),
        "suggested_slicer_settings": {
            "material": job.material,
            "layer_height_mm": job.layer_height_mm,
            "walls": job.walls,
            "infill_percent": job.infill_percent,
            "supports": job.supports,
        },
        "note": job.note,
    }

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    receipt = {
        "project": "CICADA_FORGE_UE",
        "phase": "003E",
        "job_name": job.name,
        "stl_path": str(stl_path),
        "manifest_path": str(manifest_path),
        "direct_printer_send": False,
        "machine_bridge": "LOCKED",
        "created": stamp,
    }

    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")

    if open_stl:
        os.startfile(stl_path)

    return {
        "stl": str(stl_path),
        "manifest": str(manifest_path),
        "receipt": str(receipt_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA editable box job runner. Generates STL + locked print handoff manifest from JSON.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create an editable box job JSON file.")
    init.add_argument("--name", default="custom_box")
    init.add_argument("--width", type=float, required=True)
    init.add_argument("--depth", type=float, required=True)
    init.add_argument("--height", type=float, required=True)
    init.add_argument("--material", default="PLA")
    init.add_argument("--layer-height", type=float, default=0.20)
    init.add_argument("--walls", type=int, default=3)
    init.add_argument("--infill", type=int, default=15)
    init.add_argument("--supports", default="off")
    init.add_argument("--note", default="")
    init.add_argument("--out", type=Path, default=None)

    run = sub.add_parser("run", help="Run a box job JSON file.")
    run.add_argument("job", type=Path)
    run.add_argument("--open", action="store_true")

    summary = sub.add_parser("summary", help="Summarise and validate a box job JSON file.")
    summary.add_argument("job", type=Path)

    args = parser.parse_args()

    if args.command == "init":
        out_path = create_job_file(
            name=args.name,
            width=args.width,
            depth=args.depth,
            height=args.height,
            material=args.material,
            layer_height=args.layer_height,
            walls=args.walls,
            infill=args.infill,
            supports=args.supports,
            note=args.note,
            out=args.out,
        )
        print(f"Created job: {out_path}")
        print("Direct printer send: LOCKED")
        return 0

    if args.command == "summary":
        job = load_job(args.job)
        print(json.dumps(job_summary(job), indent=2))
        return 0

    if args.command == "run":
        job = load_job(args.job)
        outputs = write_outputs(job, open_stl=args.open)

        print("CICADA BOX JOB COMPLETE")
        print(f"Job: {job.name}")
        print(f"STL: {outputs['stl']}")
        print(f"Manifest: {outputs['manifest']}")
        print(f"Receipt: {outputs['receipt']}")
        print("Direct printer send: LOCKED")
        return 0

    raise AssertionError("Unhandled command")


if __name__ == "__main__":
    raise SystemExit(main())
