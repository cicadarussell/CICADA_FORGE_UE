from __future__ import annotations

import argparse
import html
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))


class SlicerDryRunPlanner:
    def __init__(self, repo: Path = DEFAULT_REPO) -> None:
        self.repo = repo
        self.saved = repo / "Saved" / "CICADAForge"
        self.stl_dir = self.saved / "STL"
        self.cad_export_dir = self.saved / "CADExports"
        self.reports = self.saved / "SlicerReports"

    def latest_stl(self) -> Path | None:
        # 003P integration fix: normal STL folder first, CADExports fallback second.
        candidates: list[Path] = []
        for folder in [self.stl_dir, self.cad_export_dir]:
            if folder.exists():
                candidates.extend([p for p in folder.glob("*.stl") if p.is_file()])
        files = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
        return files[0] if files else None


    def find_slicer(self) -> dict[str, Any]:
        checks = []
        names = [
            ("OrcaSlicer", ["orca-slicer", "OrcaSlicer"]),
            ("PrusaSlicer", ["prusa-slicer", "PrusaSlicer"]),
            ("BambuStudio", ["bambu-studio", "BambuStudio"]),
            ("Cura", ["Cura", "UltiMaker-Cura"]),
        ]
        for label, aliases in names:
            for alias in aliases:
                found = shutil.which(alias)
                checks.append({"label": label, "alias": alias, "path": found, "exists": found is not None, "source": "PATH"})
                if found:
                    return {"name": label, "path": found, "source": "PATH", "checks": checks}

        envs = [
            ("OrcaSlicer", "CICADA_ORCA_SLICER"),
            ("PrusaSlicer", "CICADA_PRUSA_SLICER"),
            ("BambuStudio", "CICADA_BAMBU_STUDIO"),
            ("Cura", "CICADA_CURA"),
        ]
        for label, env in envs:
            value = os.environ.get(env)
            if value:
                exists = Path(value).exists()
                checks.append({"label": label, "alias": env, "path": value, "exists": exists, "source": "env"})
                if exists:
                    return {"name": label, "path": value, "source": env, "checks": checks}

        # 003P integration fix: mirror readiness known-path scan.
        bases = [os.environ.get("ProgramFiles", r"C:\Program Files"), os.environ.get("LOCALAPPDATA", "")]
        known = [
            ("OrcaSlicer", r"OrcaSlicer\orca-slicer.exe"),
            ("BambuStudio", r"Bambu Studio\bambu-studio.exe"),
            ("PrusaSlicer", r"Prusa3D\PrusaSlicer\prusa-slicer.exe"),
            ("Cura", r"UltiMaker Cura\UltiMaker-Cura.exe"),
        ]
        for base in bases:
            if not base:
                continue
            for label, rel in known:
                p = Path(base) / rel
                checks.append({"label": label, "alias": label, "path": str(p), "exists": p.exists(), "source": "known_path"})
                if p.exists():
                    return {"name": label, "path": str(p), "source": "known_path", "checks": checks}

        return {"name": None, "path": None, "source": None, "checks": checks}

    def command_plan(self, slicer: dict[str, Any], stl: Path | None) -> dict[str, Any]:
        if stl is None:
            return {"ready": False, "reason": "No STL found. Generate one first.", "commands": []}

        if slicer.get("path") is None:
            return {"ready": False, "reason": "No slicer executable found. Install/configure slicer first.", "commands": []}

        path = str(slicer["path"])
        name = slicer["name"]
        stl_str = str(stl)

        # These are deliberately non-executed plan strings. No G-code is written by this phase.
        if name == "PrusaSlicer":
            commands = [
                [path, "--info", stl_str],
                [path, "--export-gcode", "--dont-arrange", "--output", "<BLOCKED_BY_003M_NO_GCODE>", stl_str],
            ]
        elif name == "OrcaSlicer":
            commands = [
                [path, "--help"],
                [path, "--slice", "0", "--output", "<BLOCKED_BY_003M_NO_GCODE>", stl_str],
            ]
        elif name == "BambuStudio":
            commands = [
                [path, "--help"],
                [path, "--slice", "0", "--output", "<BLOCKED_BY_003M_NO_GCODE>", stl_str],
            ]
        elif name == "Cura":
            commands = [
                [path, "--help"],
                [path, "slice", "-l", stl_str, "-o", "<BLOCKED_BY_003M_NO_GCODE>"],
            ]
        else:
            commands = [[path, "--help"]]

        return {
            "ready": True,
            "reason": "Slicer and STL found. Commands are plans only; not executed.",
            "commands": commands,
        }

    def plan(self) -> dict[str, Any]:
        slicer = self.find_slicer()
        stl = self.latest_stl()
        plan = self.command_plan(slicer, stl)
        data = {
            "project": "CICADA_FORGE_UE",
            "phase": "003P",
            "slicer": slicer,
            "latest_stl": str(stl) if stl else None,
            "dry_run_plan": plan,
            "executed": False,
            "gcode_generated": False,
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
            "warning": "003M only writes this dry-run plan. It does not run slicer export or create G-code.",
        }
        print(json.dumps(data, indent=2))
        return data

    def write_report(self, data: dict[str, Any], open_report: bool = False) -> dict[str, str]:
        self.reports.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = self.reports / f"slicer_dryrun_plan_{stamp}.json"
        html_path = self.reports / f"slicer_dryrun_plan_{stamp}.html"
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        html_path.write_text(self.html_report(data), encoding="utf-8")
        if open_report:
            os.startfile(html_path)
        outputs = {"json": str(json_path), "html": str(html_path)}
        print(json.dumps(outputs, indent=2))
        return outputs

    def html_report(self, data: dict[str, Any]) -> str:
        raw = html.escape(json.dumps(data, indent=2))
        ready = bool(data.get("dry_run_plan", {}).get("ready"))
        cls = "good" if ready else "warn"
        status = "PLAN READY" if ready else "NOT READY"
        commands = data.get("dry_run_plan", {}).get("commands", [])
        command_html = "".join(f"<pre>{html.escape(json.dumps(cmd, indent=2))}</pre>" for cmd in commands) or "<p class='muted'>No commands yet.</p>"
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CICADA Slicer Dry-Run Plan</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ color-scheme: dark; --bg:#050505; --panel:#111; --line:#333; --text:#f5f5f5; --muted:#aaa; --good:#9fffa8; --warn:#ffd479; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:system-ui, Segoe UI, Arial, sans-serif; }}
main {{ max-width:1120px; margin:0 auto; padding:24px; }}
.panel {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; margin:12px 0; }}
.good {{ color:var(--good); font-weight:800; }}
.warn {{ color:var(--warn); font-weight:800; }}
.muted {{ color:var(--muted); }}
pre {{ white-space:pre-wrap; word-break:break-word; background:#050505; border:1px solid #333; border-radius:12px; padding:14px; }}
</style>
</head>
<body>
<main>
<h1>CICADA SLICER DRY-RUN PLAN</h1>
<p class="muted">Plan-only. No G-code generated. No printer send. The machine bridge remains locked because we are not complete maniacs.</p>
<section class="panel"><h2>Status: <span class="{cls}">{status}</span></h2>
<p>Slicer: {html.escape(str(data.get("slicer", {}).get("name")))}</p>
<p>Latest STL: {html.escape(str(data.get("latest_stl")))}</p>
<p>Executed: false</p>
<p>G-code generated: false</p>
<p>Machine bridge: LOCKED</p>
</section>
<section class="panel"><h2>Planned commands, not executed</h2>{command_html}</section>
<section class="panel"><h2>Raw JSON</h2><pre>{raw}</pre></section>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA slicer dry-run planner. Writes plan only, never runs slicer export.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--open-report", action="store_true")
    args = parser.parse_args()

    planner = SlicerDryRunPlanner(args.repo)
    data = planner.plan()
    planner.write_report(data, open_report=args.open_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
