from __future__ import annotations

import argparse
import json
import math
import os
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


REPO = Path(r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE")
SAVED = REPO / "Saved" / "CICADAForge"
STL_DIR = SAVED / "STL"
REPORT_DIR = SAVED / "Reports"


Vertex = tuple[float, float, float]
Triangle = tuple[Vertex, Vertex, Vertex]


@dataclass(frozen=True)
class MeshStats:
    source: str
    triangle_count: int
    vertex_count: int
    unique_vertex_count: int
    min_xyz: Vertex
    max_xyz: Vertex
    dimensions_mm: Vertex
    surface_area_mm2: float
    volume_mm3: float
    edge_count: int
    non_manifold_edge_count: int
    boundary_edge_count: int
    quality_pass: bool
    warnings: list[str]


def parse_ascii_stl(path: Path) -> list[Triangle]:
    text = path.read_text(encoding="utf-8", errors="replace")
    matches = re.findall(
        r"vertex\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)",
        text,
    )

    vertices: list[Vertex] = [(float(x), float(y), float(z)) for x, y, z in matches]

    if len(vertices) % 3 != 0:
        raise ValueError(f"Vertex count {len(vertices)} is not divisible by 3. ASCII STL may be malformed.")

    return [
        (vertices[i], vertices[i + 1], vertices[i + 2])
        for i in range(0, len(vertices), 3)
    ]


def sub(a: Vertex, b: Vertex) -> Vertex:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a: Vertex, b: Vertex) -> Vertex:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def dot(a: Vertex, b: Vertex) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def length(a: Vertex) -> float:
    return math.sqrt(dot(a, a))


def triangle_area(t: Triangle) -> float:
    a, b, c = t
    return 0.5 * length(cross(sub(b, a), sub(c, a)))


def signed_tetra_volume(t: Triangle) -> float:
    a, b, c = t
    return dot(a, cross(b, c)) / 6.0


def canonical_vertex(v: Vertex, places: int = 6) -> Vertex:
    return (round(v[0], places), round(v[1], places), round(v[2], places))


def canonical_edge(a: Vertex, b: Vertex) -> tuple[Vertex, Vertex]:
    ca = canonical_vertex(a)
    cb = canonical_vertex(b)
    return (ca, cb) if ca <= cb else (cb, ca)


def analyze(path: Path) -> tuple[MeshStats, list[Triangle]]:
    triangles = parse_ascii_stl(path)

    if not triangles:
        raise ValueError("No triangles found in STL.")

    all_vertices = [v for tri in triangles for v in tri]
    xs = [v[0] for v in all_vertices]
    ys = [v[1] for v in all_vertices]
    zs = [v[2] for v in all_vertices]

    min_xyz = (min(xs), min(ys), min(zs))
    max_xyz = (max(xs), max(ys), max(zs))
    dims = (
        max_xyz[0] - min_xyz[0],
        max_xyz[1] - min_xyz[1],
        max_xyz[2] - min_xyz[2],
    )

    area = sum(triangle_area(t) for t in triangles)
    volume = abs(sum(signed_tetra_volume(t) for t in triangles))

    edge_counter: Counter[tuple[Vertex, Vertex]] = Counter()
    for a, b, c in triangles:
        edge_counter[canonical_edge(a, b)] += 1
        edge_counter[canonical_edge(b, c)] += 1
        edge_counter[canonical_edge(c, a)] += 1

    boundary_edges = [edge for edge, count in edge_counter.items() if count == 1]
    non_manifold_edges = [edge for edge, count in edge_counter.items() if count != 2]

    warnings: list[str] = []

    if len(triangles) < 4:
        warnings.append("Very low triangle count.")

    if any(d <= 0 for d in dims):
        warnings.append("Bounding box has zero or negative dimension.")

    if boundary_edges:
        warnings.append(f"{len(boundary_edges)} boundary edges found. Mesh may be open.")

    if len(non_manifold_edges) != 0:
        warnings.append(f"{len(non_manifold_edges)} edges are not used exactly twice.")

    if volume <= 0:
        warnings.append("Volume estimate is zero or negative.")

    quality_pass = not warnings

    stats = MeshStats(
        source=str(path),
        triangle_count=len(triangles),
        vertex_count=len(all_vertices),
        unique_vertex_count=len(set(canonical_vertex(v) for v in all_vertices)),
        min_xyz=min_xyz,
        max_xyz=max_xyz,
        dimensions_mm=dims,
        surface_area_mm2=area,
        volume_mm3=volume,
        edge_count=len(edge_counter),
        non_manifold_edge_count=len(non_manifold_edges),
        boundary_edge_count=len(boundary_edges),
        quality_pass=quality_pass,
        warnings=warnings,
    )

    return stats, triangles


def latest_stl() -> Path:
    files = sorted(STL_DIR.glob("*.stl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError(f"No STL files found in {STL_DIR}")
    return files[0]


def stats_to_dict(stats: MeshStats) -> dict:
    return {
        "source": stats.source,
        "triangle_count": stats.triangle_count,
        "vertex_count": stats.vertex_count,
        "unique_vertex_count": stats.unique_vertex_count,
        "min_xyz": list(stats.min_xyz),
        "max_xyz": list(stats.max_xyz),
        "dimensions_mm": {
            "x": stats.dimensions_mm[0],
            "y": stats.dimensions_mm[1],
            "z": stats.dimensions_mm[2],
        },
        "surface_area_mm2": stats.surface_area_mm2,
        "volume_mm3": stats.volume_mm3,
        "edge_count": stats.edge_count,
        "non_manifold_edge_count": stats.non_manifold_edge_count,
        "boundary_edge_count": stats.boundary_edge_count,
        "quality_pass": stats.quality_pass,
        "warnings": stats.warnings,
        "direct_printer_send": False,
        "machine_bridge": "LOCKED",
    }


def make_svg_preview(stats: MeshStats) -> str:
    w, d, h = stats.dimensions_mm
    if w <= 0 or d <= 0 or h <= 0:
        w, d, h = 80, 40, 12

    scale = min(300 / max(w, d, 1), 160 / max(h + d * 0.4, 1))
    sx, sy, sz = w * scale, d * scale, h * scale

    x0, y0 = 80, 210
    dx, dy = d * scale * 0.45, d * scale * 0.28

    # simple isometric-ish box points
    p1 = (x0, y0)
    p2 = (x0 + sx, y0)
    p3 = (x0 + sx + dx, y0 - dy)
    p4 = (x0 + dx, y0 - dy)
    p5 = (p1[0], p1[1] - sz)
    p6 = (p2[0], p2[1] - sz)
    p7 = (p3[0], p3[1] - sz)
    p8 = (p4[0], p4[1] - sz)

    def poly(points: list[tuple[float, float]], klass: str) -> str:
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        return f'<polygon class="{klass}" points="{pts}"/>'

    return f"""
<svg viewBox="0 0 460 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="STL box preview">
  <style>
    .face1 {{ fill: #ffffff; opacity: 0.92; }}
    .face2 {{ fill: #d7d7d7; opacity: 0.92; }}
    .face3 {{ fill: #a8a8a8; opacity: 0.92; }}
    .edge {{ stroke: #111; stroke-width: 1.8; fill: none; }}
    .txt {{ fill: #eaeaea; font: 13px system-ui, sans-serif; }}
  </style>
  <rect x="0" y="0" width="460" height="260" fill="#050505"/>
  {poly([p5, p6, p7, p8], "face1")}
  {poly([p2, p3, p7, p6], "face2")}
  {poly([p1, p2, p6, p5], "face3")}
  {poly([p1, p2, p3, p4], "edge")}
  {poly([p5, p6, p7, p8], "edge")}
  <line class="edge" x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p5[0]:.1f}" y2="{p5[1]:.1f}"/>
  <line class="edge" x1="{p2[0]:.1f}" y1="{p2[1]:.1f}" x2="{p6[0]:.1f}" y2="{p6[1]:.1f}"/>
  <line class="edge" x1="{p3[0]:.1f}" y1="{p3[1]:.1f}" x2="{p7[0]:.1f}" y2="{p7[1]:.1f}"/>
  <line class="edge" x1="{p4[0]:.1f}" y1="{p4[1]:.1f}" x2="{p8[0]:.1f}" y2="{p8[1]:.1f}"/>
  <text class="txt" x="20" y="235">{w:.2f} x {d:.2f} x {h:.2f} mm</text>
</svg>
"""


def make_html_report(stats: MeshStats) -> str:
    data = stats_to_dict(stats)
    warning_html = "".join(f"<li>{w}</li>" for w in stats.warnings) or "<li>None</li>"
    status = "PASS" if stats.quality_pass else "CHECK"
    status_class = "good" if stats.quality_pass else "warn"
    svg = make_svg_preview(stats)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CICADA STL Report</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ color-scheme: dark; --bg:#050505; --panel:#111; --line:#333; --text:#f4f4f4; --muted:#aaa; --good:#9fffa8; --warn:#ffd479; --bad:#ff8f8f; }}
body {{ margin:0; font-family:system-ui, Segoe UI, Arial, sans-serif; background:var(--bg); color:var(--text); }}
main {{ max-width:1100px; margin:0 auto; padding:24px; }}
.grid {{ display:grid; grid-template-columns: 1fr 1fr; gap:16px; }}
.panel {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; }}
h1 {{ margin:0 0 6px; }}
.sub {{ color:var(--muted); margin:0 0 18px; }}
.good {{ color:var(--good); }}
.warn {{ color:var(--warn); }}
.bad {{ color:var(--bad); }}
table {{ width:100%; border-collapse:collapse; }}
td {{ border-bottom:1px solid #2b2b2b; padding:8px; vertical-align:top; }}
td:first-child {{ color:var(--muted); width:45%; }}
pre {{ white-space:pre-wrap; background:#050505; border:1px solid #333; border-radius:10px; padding:12px; }}
@media (max-width: 850px) {{ .grid {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<main>
<h1>CICADA STL REPORT</h1>
<p class="sub">Mesh proof before slicer automation. Direct printer send remains locked, because hot plastic deserves paperwork.</p>

<div class="grid">
  <section class="panel">
    <h2>Preview</h2>
    {svg}
  </section>
  <section class="panel">
    <h2>Quality Gate: <span class="{status_class}">{status}</span></h2>
    <table>
      <tr><td>Source</td><td>{stats.source}</td></tr>
      <tr><td>Triangles</td><td>{stats.triangle_count}</td></tr>
      <tr><td>Vertices</td><td>{stats.vertex_count}</td></tr>
      <tr><td>Unique vertices</td><td>{stats.unique_vertex_count}</td></tr>
      <tr><td>Dimensions mm</td><td>{stats.dimensions_mm[0]:.3f} x {stats.dimensions_mm[1]:.3f} x {stats.dimensions_mm[2]:.3f}</td></tr>
      <tr><td>Surface area mm²</td><td>{stats.surface_area_mm2:.3f}</td></tr>
      <tr><td>Volume mm³</td><td>{stats.volume_mm3:.3f}</td></tr>
      <tr><td>Edges</td><td>{stats.edge_count}</td></tr>
      <tr><td>Boundary edges</td><td>{stats.boundary_edge_count}</td></tr>
      <tr><td>Non-manifold edges</td><td>{stats.non_manifold_edge_count}</td></tr>
      <tr><td>Direct printer send</td><td>false</td></tr>
      <tr><td>Machine bridge</td><td>LOCKED</td></tr>
    </table>
  </section>
</div>

<section class="panel" style="margin-top:16px;">
  <h2>Warnings</h2>
  <ul>{warning_html}</ul>
</section>

<section class="panel" style="margin-top:16px;">
  <h2>Raw stats JSON</h2>
  <pre>{json.dumps(data, indent=2)}</pre>
</section>
</main>
</body>
</html>
"""


def write_report(stats: MeshStats, open_report: bool = False) -> dict[str, str]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    source_name = Path(stats.source).stem
    base = f"{source_name}_report_{stamp}"

    json_path = REPORT_DIR / f"{base}.json"
    html_path = REPORT_DIR / f"{base}.html"

    json_path.write_text(json.dumps(stats_to_dict(stats), indent=2), encoding="utf-8")
    html_path.write_text(make_html_report(stats), encoding="utf-8")

    if open_report:
        os.startfile(html_path)

    return {"json": str(json_path), "html": str(html_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA STL analyzer/report generator.")
    parser.add_argument("stl", nargs="?", type=Path, help="STL path. If omitted, uses latest Saved/CICADAForge/STL/*.stl")
    parser.add_argument("--report", action="store_true", help="Write JSON + HTML report.")
    parser.add_argument("--open-report", action="store_true", help="Open HTML report after writing.")
    parser.add_argument("--quality-gate", action="store_true", help="Exit non-zero if mesh quality gate fails.")
    args = parser.parse_args()

    stl = args.stl or latest_stl()
    stats, _triangles = analyze(stl)

    print(json.dumps(stats_to_dict(stats), indent=2))

    if args.report or args.open_report:
        outputs = write_report(stats, open_report=args.open_report)
        print(f"Report JSON: {outputs['json']}")
        print(f"Report HTML: {outputs['html']}")

    print("Direct printer send: LOCKED")

    if args.quality_gate and not stats.quality_pass:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
