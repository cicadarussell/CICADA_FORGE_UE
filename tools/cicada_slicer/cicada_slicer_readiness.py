from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))


@dataclass
class SlicerCandidate:
    name: str
    path: str
    source: str
    exists: bool


class CicadaSlicerReadiness:
    def __init__(self, repo: Path = DEFAULT_REPO) -> None:
        self.repo = repo
        self.saved = repo / "Saved" / "CICADAForge"
        self.reports = self.saved / "SlicerReports"
        self.stl_dir = self.saved / "STL"
        self.cad_export_dir = self.saved / "CADExports"

    def candidates(self) -> list[SlicerCandidate]:
        candidates: list[SlicerCandidate] = []

        path_names = ["orca-slicer", "OrcaSlicer", "prusa-slicer", "PrusaSlicer", "bambu-studio", "BambuStudio", "Cura", "UltiMaker-Cura"]
        for name in path_names:
            found = shutil.which(name)
            if found:
                candidates.append(SlicerCandidate(name=name, path=found, source="PATH", exists=True))

        envs = {
            "CICADA_ORCA_SLICER": "OrcaSlicer",
            "CICADA_PRUSA_SLICER": "PrusaSlicer",
            "CICADA_BAMBU_STUDIO": "BambuStudio",
            "CICADA_CURA": "Cura",
        }
        for env, name in envs.items():
            value = os.environ.get(env)
            if value:
                p = Path(value)
                candidates.append(SlicerCandidate(name=name, path=str(p), source=env, exists=p.exists()))

        program_files = [os.environ.get("ProgramFiles", r"C:\Program Files"), os.environ.get("LOCALAPPDATA", "")]
        known = [
            ("OrcaSlicer", r"OrcaSlicer\orca-slicer.exe"),
            ("BambuStudio", r"Bambu Studio\bambu-studio.exe"),
            ("PrusaSlicer", r"Prusa3D\PrusaSlicer\prusa-slicer.exe"),
            ("Cura", r"UltiMaker Cura\UltiMaker-Cura.exe"),
        ]
        for base in program_files:
            if not base:
                continue
            for name, rel in known:
                p = Path(base) / rel
                candidates.append(SlicerCandidate(name=name, path=str(p), source="known_path", exists=p.exists()))

        # de-dupe by path
        seen = set()
        unique = []
        for c in candidates:
            key = c.path.lower()
            if key not in seen:
                seen.add(key)
                unique.append(c)
        return unique

    def latest_stl(self) -> Path | None:
        # 003P integration fix: normal STL folder first, CADExports fallback second.
        candidates: list[Path] = []
        for folder in [self.stl_dir, self.cad_export_dir]:
            if folder.exists():
                candidates.extend([p for p in folder.glob("*.stl") if p.is_file()])
        files = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
        return files[0] if files else None

    def version_probe(self, candidate: SlicerCandidate) -> dict[str, Any]:
        if not candidate.exists:
            return {"attempted": False, "reason": "path missing"}
        try:
            completed = subprocess.run([candidate.path, "--version"], capture_output=True, text=True, timeout=10)
            return {
                "attempted": True,
                "returncode": completed.returncode,
                "stdout": completed.stdout.strip()[:1000],
                "stderr": completed.stderr.strip()[:1000],
            }
        except Exception as exc:
            return {"attempted": True, "error": str(exc)}

    def readiness(self, probe_versions: bool = False) -> dict[str, Any]:
        candidates = self.candidates()
        latest_stl = self.latest_stl()
        found = [c for c in candidates if c.exists]

        data = {
            "project": "CICADA_FORGE_UE",
            "phase": "003P",
            "slicer_candidates": [
                {
                    "name": c.name,
                    "path": c.path,
                    "source": c.source,
                    "exists": c.exists,
                    "version_probe": self.version_probe(c) if probe_versions and c.exists else None,
                }
                for c in candidates
            ],
            "slicer_found": len(found) > 0,
            "latest_stl": str(latest_stl) if latest_stl else None,
            "safe_dry_run_possible": len(found) > 0 and latest_stl is not None,
            "dry_run_plan_only": True,
            "gcode_generated": False,
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
            "recommended_next": "Install/configure a slicer and keep using manual inspection. Slicer CLI dry-run can come later, still no printer send.",
        }
        print(json.dumps(data, indent=2))
        return data

    def write_report(self, data: dict[str, Any], open_report: bool = False) -> dict[str, str]:
        self.reports.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = self.reports / f"slicer_readiness_{stamp}.json"
        html_path = self.reports / f"slicer_readiness_{stamp}.html"
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        html_path.write_text(self.html_report(data), encoding="utf-8")

        if open_report:
            os.startfile(html_path)

        outputs = {"json": str(json_path), "html": str(html_path)}
        print(json.dumps(outputs, indent=2))
        return outputs

    def html_report(self, data: dict[str, Any]) -> str:
        status = "READY-ISH" if data.get("safe_dry_run_possible") else "NOT READY"
        cls = "good" if data.get("safe_dry_run_possible") else "warn"
        rows = []
        for c in data.get("slicer_candidates", []):
            rows.append(
                "<tr>"
                f"<td>{html.escape(str(c.get('name')))}</td>"
                f"<td>{html.escape(str(c.get('exists')))}</td>"
                f"<td>{html.escape(str(c.get('source')))}</td>"
                f"<td>{html.escape(str(c.get('path')))}</td>"
                "</tr>"
            )
        raw = html.escape(json.dumps(data, indent=2))
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CICADA Slicer Readiness</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ color-scheme: dark; --bg:#050505; --panel:#111; --line:#333; --text:#f5f5f5; --muted:#aaa; --good:#9fffa8; --warn:#ffd479; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:system-ui, Segoe UI, Arial, sans-serif; }}
main {{ max-width:1120px; margin:0 auto; padding:24px; }}
.panel {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; margin:12px 0; }}
.good {{ color:var(--good); font-weight:800; }}
.warn {{ color:var(--warn); font-weight:800; }}
.muted {{ color:var(--muted); }}
table {{ width:100%; border-collapse:collapse; }}
td, th {{ border-bottom:1px solid #2b2b2b; padding:8px; text-align:left; }}
pre {{ white-space:pre-wrap; word-break:break-word; background:#050505; border:1px solid #333; border-radius:12px; padding:14px; }}
</style>
</head>
<body>
<main>
<h1>CICADA SLICER READINESS</h1>
<p class="muted">Report-only. No G-code generation. No printer send. The plastic dragon remains chained.</p>
<section class="panel">
<h2>Status: <span class="{cls}">{status}</span></h2>
<table>
<tr><td>Latest STL</td><td>{html.escape(str(data.get("latest_stl")))}</td></tr>
<tr><td>Slicer found</td><td>{html.escape(str(data.get("slicer_found")))}</td></tr>
<tr><td>Safe dry-run possible</td><td>{html.escape(str(data.get("safe_dry_run_possible")))}</td></tr>
<tr><td>G-code generated</td><td>false</td></tr>
<tr><td>Direct printer send</td><td>false</td></tr>
<tr><td>Machine bridge</td><td>LOCKED</td></tr>
</table>
</section>
<section class="panel">
<h2>Slicer candidates</h2>
<table><thead><tr><th>Name</th><th>Exists</th><th>Source</th><th>Path</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
</section>
<section class="panel"><h2>Raw JSON</h2><pre>{raw}</pre></section>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA slicer readiness reporter. No G-code. No printer send.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--open-report", action="store_true")
    parser.add_argument("--probe-versions", action="store_true")
    args = parser.parse_args()

    tool = CicadaSlicerReadiness(args.repo)
    data = tool.readiness(probe_versions=args.probe_versions)
    tool.write_report(data, open_report=args.open_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
