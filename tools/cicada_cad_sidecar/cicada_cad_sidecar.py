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
SUPPORTED_SCHEMAS = {"cicada_part_v0_1", "cicada_part_v0_2"}


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
        self.schema_path = repo / "tools" / "cicada_cad_sidecar" / "schemas" / "cicada_part_schema_v0_2.json"
        self.export_dir = self.saved / "CADExports"
        self.report_dir = self.saved / "CADReports"
        self.intent_dir = self.saved / "CADIntent"

    def engine_state(self, preferred: str = "auto") -> CadEngineState:
        # No fake STEP: STEP export is allowed only when an exact CAD engine actually exists.
        cadquery_available = importlib.util.find_spec("cadquery") is not None
        freecad_available = importlib.util.find_spec("FreeCAD") is not None

        notes: list[str] = []
        notes.append("CadQuery module detected: exact STEP/STL export path can be attempted." if cadquery_available else "CadQuery module not detected.")
        notes.append("FreeCAD module detected: FreeCAD bridge can be developed/used later." if freecad_available else "FreeCAD module not detected in current Python environment.")

        if preferred == "none":
            selected = "none"
            notes.append("Exact CAD export deliberately disabled by --engine none.")
        elif preferred == "cadquery" and cadquery_available:
            selected = "cadquery"
        elif preferred == "cadquery":
            selected = "none"
            notes.append("Requested CadQuery but it is unavailable.")
        elif preferred == "freecad" and freecad_available:
            selected = "freecad-detected-not-implemented"
            notes.append("FreeCAD detected, but 003K still uses CadQuery as the implemented exact exporter.")
        elif preferred == "freecad":
            selected = "none"
            notes.append("Requested FreeCAD but it is unavailable.")
        elif cadquery_available:
            selected = "cadquery"
        elif freecad_available:
            selected = "freecad-detected-not-implemented"
        else:
            selected = "none"

        return CadEngineState(
            cadquery_available=cadquery_available,
            freecad_available=freecad_available,
            selected_engine=selected,
            exact_step_available=(selected == "cadquery"),
            notes=notes,
        )

    def load_part(self, part_path: Path) -> dict[str, Any]:
        if not part_path.exists():
            raise FileNotFoundError(f"Missing part file: {part_path}")
        return json.loads(part_path.read_text(encoding="utf-8"))

    def _num(self, obj: dict[str, Any], key: str, errors: list[str], prefix: str, positive: bool = False) -> float:
        try:
            value = float(obj[key])
            if positive and value <= 0:
                errors.append(f"{prefix}.{key} must be positive.")
            return value
        except Exception:
            errors.append(f"{prefix}.{key} must be numeric.")
            return 0.0

    def validate_part(self, part: dict[str, Any]) -> list[str]:
        errors: list[str] = []

        if part.get("schema_version") not in SUPPORTED_SCHEMAS:
            errors.append(f"schema_version must be one of {sorted(SUPPORTED_SCHEMAS)}.")

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

        width = self._num(body, "width", errors, "body", positive=True)
        depth = self._num(body, "depth", errors, "body", positive=True)
        height = self._num(body, "height", errors, "body", positive=True)

        if width > 220 or depth > 220 or height > 250:
            errors.append("V0 generic printer fit check failed: body exceeds 220 x 220 x 250 mm.")

        features = part.get("features", [])
        if not isinstance(features, list):
            errors.append("features must be a list.")
            return errors

        for idx, feature in enumerate(features):
            prefix = f"features[{idx}]"
            ftype = feature.get("type")
            if ftype not in {"hole", "slot", "standoff"}:
                errors.append(f"{prefix} unsupported type: {ftype}. V0.2 supports hole, slot, standoff.")
                continue

            if feature.get("face") != "top":
                errors.append(f"{prefix}.face must be top in V0.2.")

            x = self._num(feature, "x", errors, prefix)
            y = self._num(feature, "y", errors, prefix)

            if ftype == "hole":
                diameter = self._num(feature, "diameter", errors, prefix, positive=True)
                radius = diameter / 2.0
                if not (radius <= x <= width - radius and radius <= y <= depth - radius):
                    errors.append(f"{prefix} hole centre/radius is outside the box top face.")
                depth_mode = feature.get("depth", "through")
                if depth_mode != "through":
                    try:
                        if float(depth_mode) <= 0:
                            errors.append(f"{prefix}.depth must be through or positive number.")
                    except Exception:
                        errors.append(f"{prefix}.depth must be through or numeric.")

            if ftype == "slot":
                length = self._num(feature, "length", errors, prefix, positive=True)
                slot_width = self._num(feature, "width", errors, prefix, positive=True)
                if length < slot_width:
                    errors.append(f"{prefix}.length must be >= width for a slot.")
                angle = float(feature.get("angle_deg", 0) or 0)
                if abs(angle) > 1e-6:
                    errors.append(f"{prefix}.angle_deg other than 0 is recorded but not manufacturable in V0.2 exact export.")
                if not (length / 2.0 <= x <= width - length / 2.0 and slot_width / 2.0 <= y <= depth - slot_width / 2.0):
                    errors.append(f"{prefix} slot extents are outside the box top face.")

            if ftype == "standoff":
                diameter = self._num(feature, "diameter", errors, prefix, positive=True)
                standoff_height = self._num(feature, "height", errors, prefix, positive=True)
                radius = diameter / 2.0
                if not (radius <= x <= width - radius and radius <= y <= depth - radius):
                    errors.append(f"{prefix} standoff centre/radius is outside the box top face.")
                pilot = feature.get("pilot_hole_diameter", 0)
                if pilot not in (None, "", 0, 0.0):
                    try:
                        pilot_value = float(pilot)
                        if pilot_value <= 0 or pilot_value >= diameter:
                            errors.append(f"{prefix}.pilot_hole_diameter must be positive and smaller than standoff diameter.")
                    except Exception:
                        errors.append(f"{prefix}.pilot_hole_diameter must be numeric if supplied.")
                if height + standoff_height > 250:
                    errors.append(f"{prefix} total part height exceeds 250 mm generic V0 check.")

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

        removed_volume = 0.0
        added_volume = 0.0
        counts = {"hole": 0, "slot": 0, "standoff": 0}

        for feature in part.get("features", []):
            ftype = feature.get("type")
            if ftype in counts:
                counts[ftype] += 1

            if ftype == "hole":
                diameter = float(feature["diameter"])
                removed_volume += math.pi * (diameter / 2.0) ** 2 * height

            if ftype == "slot":
                length = float(feature["length"])
                slot_width = float(feature["width"])
                straight_length = max(length - slot_width, 0.0)
                slot_area = straight_length * slot_width + math.pi * (slot_width / 2.0) ** 2
                removed_volume += slot_area * height

            if ftype == "standoff":
                diameter = float(feature["diameter"])
                standoff_height = float(feature["height"])
                added_volume += math.pi * (diameter / 2.0) ** 2 * standoff_height
                pilot = feature.get("pilot_hole_diameter", 0)
                if pilot not in (None, "", 0, 0.0):
                    pilot_d = float(pilot)
                    removed_volume += math.pi * (pilot_d / 2.0) ** 2 * (height + standoff_height)

        gross_volume = width * depth * height
        estimated_volume = max(gross_volume - removed_volume + added_volume, 0.0)

        return {
            "width_mm": width,
            "depth_mm": depth,
            "height_mm": height,
            "gross_volume_mm3": gross_volume,
            "estimated_removed_volume_mm3": removed_volume,
            "estimated_added_volume_mm3": added_volume,
            "estimated_net_volume_mm3": estimated_volume,
            "top_area_mm2": width * depth,
            "feature_counts": counts,
            "fits_generic_220x220x250": width <= 220 and depth <= 220 and height <= 250,
        }

    def svg_preview(self, part: dict[str, Any]) -> str:
        body = part["bodies"][0]
        width = float(body["width"])
        depth = float(body["depth"])
        scale = min(500 / max(width, 1), 280 / max(depth, 1))
        ox, oy = 70, 70
        w, d = width * scale, depth * scale

        feature_svg = []
        for feature in part.get("features", []):
            ftype = feature.get("type")
            x = ox + float(feature.get("x", 0)) * scale
            y = oy + float(feature.get("y", 0)) * scale

            if ftype == "hole":
                r = float(feature["diameter"]) * scale / 2.0
                feature_svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="none" stroke="#111" stroke-width="2"/>')
                feature_svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.2" fill="#111"/>')

            if ftype == "slot":
                length = float(feature["length"]) * scale
                sw = float(feature["width"]) * scale
                rx = sw / 2.0
                feature_svg.append(f'<rect x="{x-length/2:.2f}" y="{y-sw/2:.2f}" width="{length:.2f}" height="{sw:.2f}" rx="{rx:.2f}" ry="{rx:.2f}" fill="none" stroke="#111" stroke-width="2"/>')

            if ftype == "standoff":
                r = float(feature["diameter"]) * scale / 2.0
                feature_svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="none" stroke="#111" stroke-width="2"/>')
                feature_svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r*0.55:.2f}" fill="none" stroke="#666" stroke-width="1.5"/>')

        return f"""
<svg viewBox="0 0 660 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CICADA CAD top preview">
  <style>
    .label {{ fill:#eaeaea; font:14px system-ui, sans-serif; }}
    .dim {{ fill:#aaa; font:12px system-ui, sans-serif; }}
  </style>
  <rect x="0" y="0" width="660" height="430" fill="#050505"/>
  <rect x="{ox:.2f}" y="{oy:.2f}" width="{w:.2f}" height="{d:.2f}" fill="#f2f2f2" stroke="#111" stroke-width="2"/>
  {''.join(feature_svg)}
  <text class="label" x="30" y="35">{html.escape(str(part.get("part_id", "part")))}</text>
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

        for feature in part.get("features", []):
            ftype = feature.get("type")
            x = float(feature.get("x", 0)) - width / 2.0
            y = float(feature.get("y", 0)) - depth / 2.0

            if ftype == "hole":
                result = result.faces(">Z").workplane(centerOption="CenterOfBoundBox").center(x, y).hole(float(feature["diameter"])).center(-x, -y)

            if ftype == "slot":
                # Axis-aligned V0.2 slots only. Angled slots are validated as non-exportable for now.
                length = float(feature["length"])
                slot_width = float(feature["width"])
                result = result.faces(">Z").workplane(centerOption="CenterOfBoundBox").center(x, y).slot2D(length, slot_width).cutThruAll().center(-x, -y)

            if ftype == "standoff":
                diameter = float(feature["diameter"])
                standoff_height = float(feature["height"])
                post = cq.Workplane("XY").workplane(offset=height).center(float(feature["x"]), float(feature["y"])).circle(diameter / 2.0).extrude(standoff_height)
                result = result.union(post)

                pilot = feature.get("pilot_hole_diameter", 0)
                if pilot not in (None, "", 0, 0.0):
                    result = result.faces(">Z").workplane(centerOption="CenterOfBoundBox").center(x, y).hole(float(pilot)).center(-x, -y)

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
:root {{ color-scheme: dark; --bg:#050505; --panel:#111; --line:#333; --text:#f5f5f5; --muted:#aaa; --good:#9fffa8; --warn:#ffd479; --bad:#ff8f8f; }}
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
<p class="muted">V0.2 feature-intent report. Direct machine control remains locked, because metal and motors are not vibes.</p>
<div class="grid">
<section class="panel"><h2>Preview</h2>{preview}</section>
<section class="panel">
<h2>Gate: <span class="{status_cls}">{status}</span></h2>
<table>
<tr><td>Part</td><td>{html.escape(str(report.get("part_id")))}</td></tr>
<tr><td>Engine selected</td><td>{html.escape(str(report.get("engine", {}).get("selected_engine")))}</td></tr>
<tr><td>Exact STEP exported</td><td>{exact}</td></tr>
<tr><td>STEP path</td><td>{html.escape(str(report.get("outputs", {}).get("step", "not exported")))}</td></tr>
<tr><td>Export block reason</td><td>{html.escape(str(report.get("export_block_reason", "")))}</td></tr>
<tr><td>Machine bridge</td><td>LOCKED</td></tr>
<tr><td>Direct printer send</td><td>false</td></tr>
</table>
</section>
</div>
<section class="panel"><h2>Validation</h2><pre>{html.escape(json.dumps(report.get("validation", {}), indent=2))}</pre></section>
<section class="panel"><h2>Derived stats</h2><pre>{html.escape(json.dumps(report.get("derived", {}), indent=2))}</pre></section>
<section class="panel"><h2>Raw report JSON</h2><pre>{raw}</pre></section>
</main>
</body>
</html>
"""

    def fallback_box_stl(self, part: dict[str, Any], out_path: Path) -> str:
        # Fallback mesh output is intentionally limited to a plain box with no features.
        # If holes/slots/standoffs exist, do not fake them.
        if part.get("features"):
            return ""

        body = part["bodies"][0]
        width = float(body["width"])
        depth = float(body["depth"])
        height = float(body["height"])

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

        v000 = (0.0, 0.0, 0.0); v100 = (width, 0.0, 0.0); v110 = (width, depth, 0.0); v010 = (0.0, depth, 0.0)
        v001 = (0.0, 0.0, height); v101 = (width, 0.0, height); v111 = (width, depth, height); v011 = (0.0, depth, height)
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
            outputs["fallback_stl"] = fallback if fallback else "not generated because features exist; refusing to fake holes/slots/standoffs without CAD engine"

        intent_path = self.intent_dir / f"{safe}_{stamp}.intent.json"
        intent_path.write_text(json.dumps(part, indent=2), encoding="utf-8")
        outputs["intent"] = str(intent_path)

        report = {
            "project": "CICADA_FORGE_UE",
            "phase": "003K",
            "part_id": part_id,
            "source": str(part_path),
            "validation_pass": validation_pass,
            "validation": {"errors": errors, "no_fake_step_rule": True},
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
            "phase": "003K",
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
            "phase": "003K",
            "repo": str(self.repo),
            "python": sys.version,
            "platform": platform.platform(),
            "schema_exists": self.schema_path.exists(),
            "example_parts": [str(p) for p in sorted(self.parts_dir.glob("*.part.json"))],
            "supported_schemas": sorted(SUPPORTED_SCHEMAS),
            "supported_features": ["box", "hole", "slot", "standoff"],
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
    parser = argparse.ArgumentParser(description="CICADA CAD sidecar V0.2. Exact-geometry contract, validation, reports, optional CadQuery export.")
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
        payload = {"part": str(args.part), "pass": len(errors) == 0, "errors": errors, "direct_printer_send": False, "machine_bridge": "LOCKED"}
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
