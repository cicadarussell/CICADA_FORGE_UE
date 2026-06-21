from __future__ import annotations

import argparse
import html
import importlib.util
import json
import math
import os
import platform
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))


class CadSidecarError(RuntimeError):
    pass


@dataclass(frozen=True)
class CadEngineState:
    cadquery_available: bool
    freecad_available: bool
    selected_engine: str
    exact_step_available: bool
    notes: list[str]


class CicadaCadSidecar:
    def __init__(self, repo: Path = DEFAULT_REPO) -> None:
        self.repo = repo
        self.saved = repo / "Saved" / "CICADAForge"
        self.parts_dir = repo / "examples" / "cad_parts"
        self.schema_path = repo / "tools" / "cicada_cad_sidecar" / "schemas" / "cicada_part_schema_v0_1.json"
        self.export_dir = self.saved / "CADExports"
        self.report_dir = self.saved / "CADReports"
        self.intent_dir = self.saved / "CADIntent"

    def engine_state(self, preferred: str = "auto") -> CadEngineState:
        cadquery_available = importlib.util.find_spec("cadquery") is not None
        freecad_available = importlib.util.find_spec("FreeCAD") is not None

        notes: list[str] = []

        if cadquery_available:
            notes.append("CadQuery module detected: exact STEP/STL export path can be attempted.")
        else:
            notes.append("CadQuery module not detected.")

        if freecad_available:
            notes.append("FreeCAD module detected: FreeCAD bridge can be developed/used later.")
        else:
            notes.append("FreeCAD module not detected in current Python environment.")

        if preferred == "cadquery" and not cadquery_available:
            selected = "none"
            notes.append("Requested CadQuery but it is unavailable.")
        elif preferred == "freecad" and not freecad_available:
            selected = "none"
            notes.append("Requested FreeCAD but it is unavailable.")
        elif preferred == "cadquery" and cadquery_available:
            selected = "cadquery"
        elif preferred == "freecad" and freecad_available:
            selected = "freecad"
            notes.append("FreeCAD detected, but 003I does not yet implement full FreeCAD export. CadQuery is the primary V0 exact exporter.")
        elif cadquery_available:
            selected = "cadquery"
        elif freecad_available:
            selected = "freecad-detected-not-implemented"
        else:
            selected = "none"

        exact_step = selected == "cadquery"

        return CadEngineState(
            cadquery_available=cadquery_available,
            freecad_available=freecad_available,
            selected_engine=selected,
            exact_step_available=exact_step,
            notes=notes,
        )

    def load_part(self, part_path: Path) -> dict[str, Any]:
        if not part_path.exists():
            raise FileNotFoundError(f"Missing part file: {part_path}")
        return json.loads(part_path.read_text(encoding="utf-8"))

    def validate_part(self, part: dict[str, Any]) -> list[str]:
        errors: list[str] = []

        if part.get("schema_version") != "cicada_part_v0_1":
            errors.append("schema_version must be cicada_part_v0_1.")

        if part.get("units") != "mm":
            errors.append("units must be mm.")

        bodies = part.get("bodies")
        if not isinstance(bodies, list) or len(bodies) != 1:
            errors.append("V0 supports exactly one body.")
            return errors

        body = bodies[0]
        if body.get("type") != "box":
            errors.append("V0 supports only body type box.")
            return errors

        for key in ["width", "depth", "height"]:
            try:
                value = float(body[key])
                if value <= 0:
                    errors.append(f"body.{key} must be positive.")
            except Exception:
                errors.append(f"body.{key} must be numeric.")

        width = float(body.get("width", 0) or 0)
        depth = float(body.get("depth", 0) or 0)
        height = float(body.get("height", 0) or 0)

        if width > 220 or depth > 220 or height > 250:
            errors.append("V0 generic printer fit check failed: body exceeds 220 x 220 x 250 mm.")

        features = part.get("features", [])
        if not isinstance(features, list):
            errors.append("features must be a list.")
            return errors

        for idx, feature in enumerate(features):
            ftype = feature.get("type")
            if ftype != "hole":
                errors.append(f"features[{idx}] unsupported type: {ftype}. V0 supports hole only.")
                continue

            if feature.get("face") != "top":
                errors.append(f"features[{idx}] face must be top in V0.")

            try:
                x = float(feature["x"])
                y = float(feature["y"])
                diameter = float(feature["diameter"])
            except Exception:
                errors.append(f"features[{idx}] x/y/diameter must be numeric.")
                continue

            if diameter <= 0:
                errors.append(f"features[{idx}] diameter must be positive.")
                continue

            radius = diameter / 2.0
            if not (radius <= x <= width - radius and radius <= y <= depth - radius):
                errors.append(f"features[{idx}] hole centre/radius is outside the box top face.")

            depth_mode = feature.get("depth", "through")
            if depth_mode != "through":
                try:
                    d = float(depth_mode)
                    if d <= 0:
                        errors.append(f"features[{idx}] depth must be through or positive number.")
                except Exception:
                    errors.append(f"features[{idx}] depth must be through or numeric.")

        safety = part.get("safety", {})
        if safety.get("direct_printer_send") is not False:
            errors.append("safety.direct_printer_send must be false.")

        if str(safety.get("machine_bridge", "")).upper() != "LOCKED":
            errors.append("safety.machine_bridge must be LOCKED.")

        return errors

    def derived_stats(self, part: dict[str, Any]) -> dict[str, Any]:
        body = part["bodies"][0]
        width = float(body["width"])
        depth = float(body["depth"])
        height = float(body["height"])

        holes = [f for f in part.get("features", []) if f.get("type") == "hole"]
        hole_area = 0.0
        for hole in holes:
            diameter = float(hole["diameter"])
            hole_area += math.pi * (diameter / 2.0) ** 2

        gross_volume = width * depth * height
        through_hole_volume = hole_area * height
        estimated_volume = max(gross_volume - through_hole_volume, 0.0)

        return {
            "width_mm": width,
            "depth_mm": depth,
            "height_mm": height,
            "gross_volume_mm3": gross_volume,
            "estimated_hole_removed_volume_mm3": through_hole_volume,
            "estimated_net_volume_mm3": estimated_volume,
            "top_area_mm2": width * depth,
            "hole_count": len(holes),
            "fits_generic_220x220x250": width <= 220 and depth <= 220 and height <= 250,
        }

    def svg_preview(self, part: dict[str, Any]) -> str:
        body = part["bodies"][0]
        width = float(body["width"])
        depth = float(body["depth"])

        scale = min(500 / max(width, 1), 280 / max(depth, 1))
        ox, oy = 70, 60
        w, d = width * scale, depth * scale

        holes_svg = []
        for feature in part.get("features", []):
            if feature.get("type") == "hole":
                cx = ox + float(feature["x"]) * scale
                cy = oy + float(feature["y"]) * scale
                r = float(feature["diameter"]) * scale / 2.0
                holes_svg.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="none" stroke="#111" stroke-width="2"/>')
                holes_svg.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="2.2" fill="#111"/>')

        return f"""
<svg viewBox="0 0 660 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CICADA CAD top preview">
  <style>
    .label {{ fill:#eaeaea; font:14px system-ui, sans-serif; }}
    .dim {{ fill:#aaa; font:12px system-ui, sans-serif; }}
  </style>
  <rect x="0" y="0" width="660" height="420" fill="#050505"/>
  <rect x="{ox:.2f}" y="{oy:.2f}" width="{w:.2f}" height="{d:.2f}" fill="#f2f2f2" stroke="#111" stroke-width="2"/>
  {''.join(holes_svg)}
  <text class="label" x="30" y="30">{html.escape(str(part.get("part_id", "part")))}</text>
  <text class="dim" x="{ox:.2f}" y="{oy + d + 26:.2f}">{width:.2f} mm x {depth:.2f} mm top view</text>
</svg>
"""

    def generate_cadquery(self, part: dict[str, Any], step_path: Path, stl_path: Path | None = None) -> dict[str, str]:
        import cadquery as cq  # type: ignore
        from cadquery import exporters  # type: ignore

        body = part["bodies"][0]
        width = float(body["width"])
        depth = float(body["depth"])
        height = float(body["height"])

        result = cq.Workplane("XY").box(width, depth, height, centered=(False, False, False))

        holes = [f for f in part.get("features", []) if f.get("type") == "hole"]
        if holes:
            points = []
            for hole in holes:
                points.append((float(hole["x"]) - width / 2.0, float(hole["y"]) - depth / 2.0))
            # On the top face, make through holes.
            # V0 assumes all hole features are through holes on top face.
            first_diameter = float(holes[0]["diameter"])
            same = all(abs(float(h["diameter"]) - first_diameter) < 1e-6 for h in holes)
            if same:
                result = result.faces(">Z").workplane(centerOption="CenterOfBoundBox").pushPoints(points).hole(first_diameter)
            else:
                # Different diameters are handled one by one, because precision beats pretending.
                for hole in holes:
                    x = float(hole["x"]) - width / 2.0
                    y = float(hole["y"]) - depth / 2.0
                    result = result.faces(">Z").workplane(centerOption="CenterOfBoundBox").center(x, y).hole(float(hole["diameter"])).center(-x, -y)

        step_path.parent.mkdir(parents=True, exist_ok=True)
        exporters.export(result, str(step_path))

        outputs = {"step": str(step_path)}
        if stl_path is not None:
            stl_path.parent.mkdir(parents=True, exist_ok=True)
            exporters.export(result, str(stl_path))
            outputs["stl"] = str(stl_path)

        return outputs

    def make_report_html(self, report: dict[str, Any]) -> str:
        preview = report.get("svg_preview", "")
        raw = html.escape(json.dumps(report, indent=2))
        status = "PASS" if report.get("validation_pass") else "CHECK"
        status_cls = "good" if report.get("validation_pass") else "warn"
        exact = "YES" if report.get("exact_step_exported") else "NO"

        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CICADA CAD Sidecar Report</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ color-scheme: dark; --bg:#050505; --panel:#111; --line:#333; --text:#f5f5f5; --muted:#aaa; --good:#9fffa8; --warn:#ffd479; --bad:#ff8f8f; --cyan:#aef5ff; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:system-ui, Segoe UI, Arial, sans-serif; }}
main {{ max-width:1180px; margin:0 auto; padding:24px; }}
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
.panel {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; margin:12px 0; }}
.good {{ color:var(--good); font-weight:700; }}
.warn {{ color:var(--warn); font-weight:700; }}
.bad {{ color:var(--bad); font-weight:700; }}
.muted {{ color:var(--muted); }}
table {{ width:100%; border-collapse:collapse; }}
td {{ border-bottom:1px solid #2b2b2b; padding:8px; vertical-align:top; }}
td:first-child {{ color:var(--muted); width:42%; }}
pre {{ white-space:pre-wrap; word-break:break-word; background:#050505; border:1px solid #333; border-radius:12px; padding:14px; max-height:620px; overflow:auto; }}
@media (max-width:900px) {{ .grid {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body>
<main>
<h1>CICADA CAD SIDECAR REPORT</h1>
<p class="muted">Exact-geometry boundary report. Direct machine control remains locked. The goblin may calculate; it may not touch motors.</p>

<div class="grid">
<section class="panel">
<h2>Preview</h2>
{preview}
</section>

<section class="panel">
<h2>Gate: <span class="{status_cls}">{status}</span></h2>
<table>
<tr><td>Part</td><td>{html.escape(str(report.get("part_id")))}</td></tr>
<tr><td>Engine selected</td><td>{html.escape(str(report.get("engine", {}).get("selected_engine")))}</td></tr>
<tr><td>Exact STEP exported</td><td>{exact}</td></tr>
<tr><td>STEP path</td><td>{html.escape(str(report.get("outputs", {}).get("step", "not exported")))}</td></tr>
<tr><td>Fallback STL path</td><td>{html.escape(str(report.get("outputs", {}).get("fallback_stl", report.get("outputs", {}).get("stl", "not exported"))))}</td></tr>
<tr><td>Machine bridge</td><td>LOCKED</td></tr>
<tr><td>Direct printer send</td><td>false</td></tr>
</table>
</section>
</div>

<section class="panel">
<h2>Validation</h2>
<pre>{html.escape(json.dumps(report.get("validation", {}), indent=2))}</pre>
</section>

<section class="panel">
<h2>Derived stats</h2>
<pre>{html.escape(json.dumps(report.get("derived", {}), indent=2))}</pre>
</section>

<section class="panel">
<h2>Raw report JSON</h2>
<pre>{raw}</pre>
</section>
</main>
</body>
</html>
"""

    def fallback_box_stl(self, part: dict[str, Any], out_path: Path) -> str:
        # Fallback mesh output is intentionally limited to a plain box with no holes.
        # If holes exist, do not fake them: write no fallback STL.
        if part.get("features"):
            return ""

        body = part["bodies"][0]
        width = float(body["width"])
        depth = float(body["depth"])
        height = float(body["height"])

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

        text = "solid CICADA_CAD_Fallback_Box\n" + "".join(tri(*t) for t in triangles) + "endsolid CICADA_CAD_Fallback_Box\n"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        return str(out_path)

    def generate(self, part_path: Path, engine: str = "auto", open_report: bool = False) -> dict[str, Any]:
        part = self.load_part(part_path)
        errors = self.validate_part(part)
        engine_state = self.engine_state(preferred=engine)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        part_id = str(part.get("part_id", part_path.stem))
        safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in part_id).strip("_") or "part"

        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.intent_dir.mkdir(parents=True, exist_ok=True)

        outputs: dict[str, str] = {}
        exact_step_exported = False
        export_block_reason = ""

        validation_pass = len(errors) == 0

        if validation_pass and engine_state.selected_engine == "cadquery":
            step_path = self.export_dir / f"{safe}_{stamp}.step"
            stl_path = self.export_dir / f"{safe}_{stamp}.stl"
            try:
                outputs.update(self.generate_cadquery(part, step_path, stl_path))
                exact_step_exported = "step" in outputs
            except Exception as exc:
                export_block_reason = f"CadQuery export failed: {exc}"
        elif validation_pass:
            export_block_reason = "Exact STEP export blocked: no implemented exact CAD engine available in this Python environment."
            fallback_stl_path = self.export_dir / f"{safe}_{stamp}.fallback_box.stl"
            fallback = self.fallback_box_stl(part, fallback_stl_path)
            if fallback:
                outputs["fallback_stl"] = fallback
            else:
                outputs["fallback_stl"] = "not generated because features exist; refusing to fake holes/cuts without CAD engine"

        intent_path = self.intent_dir / f"{safe}_{stamp}.intent.json"
        intent_path.write_text(json.dumps(part, indent=2), encoding="utf-8")
        outputs["intent"] = str(intent_path)

        report = {
            "project": "CICADA_FORGE_UE",
            "phase": "003I",
            "part_id": part_id,
            "source": str(part_path),
            "validation_pass": validation_pass,
            "validation": {
                "errors": errors,
                "no_fake_step_rule": True,
            },
            "engine": {
                "cadquery_available": engine_state.cadquery_available,
                "freecad_available": engine_state.freecad_available,
                "selected_engine": engine_state.selected_engine,
                "exact_step_available": engine_state.exact_step_available,
                "notes": engine_state.notes,
            },
            "derived": self.derived_stats(part) if validation_pass else {},
            "outputs": outputs,
            "exact_step_exported": exact_step_exported,
            "export_block_reason": export_block_reason,
            "svg_preview": self.svg_preview(part) if validation_pass else "",
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
            "gcode_streaming": False,
            "created": stamp,
        }

        report_json = self.report_dir / f"{safe}_{stamp}.cad_report.json"
        report_html = self.report_dir / f"{safe}_{stamp}.cad_report.html"
        report["outputs"]["report_json"] = str(report_json)
        report["outputs"]["report_html"] = str(report_html)

        report_json.write_text(json.dumps({k: v for k, v in report.items() if k != "svg_preview"}, indent=2), encoding="utf-8")
        report_html.write_text(self.make_report_html(report), encoding="utf-8")

        if open_report:
            os.startfile(report_html)

        return report

    def validate_examples(self) -> dict[str, Any]:
        results = []
        for path in sorted(self.parts_dir.glob("*.part.json")):
            part = self.load_part(path)
            errors = self.validate_part(part)
            results.append({"path": str(path), "pass": len(errors) == 0, "errors": errors})

        payload = {
            "project": "CICADA_FORGE_UE",
            "phase": "003I",
            "examples_checked": len(results),
            "all_pass": all(r["pass"] for r in results),
            "results": results,
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }
        print(json.dumps(payload, indent=2))
        return payload

    def doctor(self) -> dict[str, Any]:
        engine = self.engine_state()
        payload = {
            "project": "CICADA_FORGE_UE",
            "phase": "003I",
            "repo": str(self.repo),
            "python": sys.version,
            "platform": platform.platform(),
            "schema_exists": self.schema_path.exists(),
            "example_parts": [str(p) for p in sorted(self.parts_dir.glob("*.part.json"))],
            "cadquery_available": engine.cadquery_available,
            "freecad_available": engine.freecad_available,
            "selected_engine": engine.selected_engine,
            "exact_step_available": engine.exact_step_available,
            "notes": engine.notes,
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }
        print(json.dumps(payload, indent=2))
        return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA CAD sidecar V0. Exact-geometry contract, validation, reports, optional CadQuery export.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor")

    validate = sub.add_parser("validate")
    validate.add_argument("part", type=Path)

    sub.add_parser("validate-examples")

    generate = sub.add_parser("generate")
    generate.add_argument("part", type=Path)
    generate.add_argument("--engine", choices=["auto", "cadquery", "freecad", "none"], default="auto")
    generate.add_argument("--open-report", action="store_true")

    args = parser.parse_args()
    sidecar = CicadaCadSidecar(args.repo)

    if args.command == "doctor":
        sidecar.doctor()
        return 0

    if args.command == "validate":
        part = sidecar.load_part(args.part)
        errors = sidecar.validate_part(part)
        payload = {
            "part": str(args.part),
            "pass": len(errors) == 0,
            "errors": errors,
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }
        print(json.dumps(payload, indent=2))
        return 0 if len(errors) == 0 else 2

    if args.command == "validate-examples":
        payload = sidecar.validate_examples()
        return 0 if payload["all_pass"] else 2

    if args.command == "generate":
        report = sidecar.generate(args.part, engine=args.engine, open_report=args.open_report)
        print(json.dumps({k: v for k, v in report.items() if k != "svg_preview"}, indent=2))
        return 0 if report["validation_pass"] else 2

    raise AssertionError("Unhandled command")


if __name__ == "__main__":
    raise SystemExit(main())
