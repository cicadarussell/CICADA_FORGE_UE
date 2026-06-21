from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json
import argparse


def tri(a, b, c) -> str:
    return (
        "  facet normal 0 0 0\n"
        "    outer loop\n"
        f"      vertex {a[0]:.6f} {a[1]:.6f} {a[2]:.6f}\n"
        f"      vertex {b[0]:.6f} {b[1]:.6f} {b[2]:.6f}\n"
        f"      vertex {c[0]:.6f} {c[1]:.6f} {c[2]:.6f}\n"
        "    endloop\n"
        "  endfacet\n"
    )


def build_box_stl(width: float, depth: float, height: float) -> str:
    v000 = (0.0, 0.0, 0.0)
    v100 = (width, 0.0, 0.0)
    v110 = (width, depth, 0.0)
    v010 = (0.0, depth, 0.0)
    v001 = (0.0, 0.0, height)
    v101 = (width, 0.0, height)
    v111 = (width, depth, height)
    v011 = (0.0, depth, height)

    triangles = [
        (v000, v110, v100), (v000, v010, v110),
        (v001, v101, v111), (v001, v111, v011),
        (v000, v100, v101), (v000, v101, v001),
        (v010, v011, v111), (v010, v111, v110),
        (v000, v001, v011), (v000, v011, v010),
        (v100, v110, v111), (v100, v111, v101),
    ]

    body = "".join(tri(*t) for t in triangles)
    return f"solid CICADA_Sketch_Box\n{body}endsolid CICADA_Sketch_Box\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA STL sidecar V0: generate a box STL from simple sketch parameters.")
    parser.add_argument("--width", type=float, default=80.0)
    parser.add_argument("--depth", type=float, default=40.0)
    parser.add_argument("--height", type=float, default=12.0)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    if args.width <= 0 or args.depth <= 0 or args.height <= 0:
        raise SystemExit("Dimensions must be positive.")

    repo = Path(r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE")
    out_dir = repo / "Saved" / "CICADAForge" / "STL"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = args.out or out_dir / f"CICADA_Sidecar_Box_{datetime.now().strftime('%Y%m%d_%H%M%S')}.stl"
    out_path.write_text(build_box_stl(args.width, args.depth, args.height), encoding="utf-8")

    manifest = {
        "project": "CICADA_FORGE_UE",
        "tool": "cicada_box_stl_sidecar.py",
        "direct_printer_send": False,
        "machine_bridge": "LOCKED",
        "stl_path": str(out_path),
        "box_mm": {"width": args.width, "depth": args.depth, "height": args.height},
    }
    manifest_path = out_path.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"STL: {out_path}")
    print(f"Manifest: {manifest_path}")
    print("Direct printer send: LOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
