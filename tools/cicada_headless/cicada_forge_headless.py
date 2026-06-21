from __future__ import annotations

import argparse
import html
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))


@dataclass
class CommandResult:
    label: str
    returncode: int
    stdout: str
    stderr: str


class HeadlessForge:
    def __init__(self, repo: Path = DEFAULT_REPO) -> None:
        self.repo = repo
        self.saved = repo / "Saved" / "CICADAForge"
        self.box_job_runner = repo / "tools" / "cicada_stl_sidecar" / "cicada_box_job_runner.py"
        self.stl_analyzer = repo / "tools" / "cicada_stl_sidecar" / "cicada_stl_analyzer.py"
        self.job_editor = repo / "tools" / "cicada_job_editor" / "local_box_job_editor.html"
        self.report_dir = self.saved / "RunReports"

    def rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.repo))
        except ValueError:
            return str(path)

    def run(self, label: str, args: list[str], check: bool = True) -> CommandResult:
        completed = subprocess.run(
            args,
            cwd=self.repo,
            text=True,
            capture_output=True,
            shell=False,
        )
        result = CommandResult(label, completed.returncode, completed.stdout, completed.stderr)

        if result.stdout.strip():
            print(result.stdout.rstrip())
        if result.stderr.strip():
            print(result.stderr.rstrip(), file=sys.stderr)

        if check and result.returncode != 0:
            raise RuntimeError(f"{label} failed with code {result.returncode}")

        return result

    def py(self, label: str, script: Path, extra: list[str], check: bool = True) -> CommandResult:
        if not script.exists():
            raise FileNotFoundError(f"Missing script: {script}")
        return self.run(label, [sys.executable, str(script), *extra], check=check)

    def latest(self, folder: str, pattern: str) -> Path | None:
        path = self.saved / folder
        if not path.exists():
            return None
        files = sorted(path.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        return files[0] if files else None

    def list_latest(self, folder: str, pattern: str = "*", limit: int = 8) -> list[dict[str, Any]]:
        path = self.saved / folder
        if not path.exists():
            return []
        files = sorted(path.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]
        return [
            {
                "name": p.name,
                "path": str(p),
                "size_bytes": p.stat().st_size,
                "modified": datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds"),
            }
            for p in files
            if p.is_file()
        ]

    def required_files(self) -> dict[str, str]:
        return {
            "UE project": "CICADA_FORGE_UE.uproject",
            "Plugin descriptor": "Plugins/CICADAForge/CICADAForge.uplugin",
            "Editor module": "Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp",
            "State config": "Config/CICADAForgeState.ini",
            "Box job runner": "tools/cicada_stl_sidecar/cicada_box_job_runner.py",
            "STL analyzer": "tools/cicada_stl_sidecar/cicada_stl_analyzer.py",
            "Local job editor": "tools/cicada_job_editor/local_box_job_editor.html",
            "Print handoff contract": "docs/debug/PRINT_HANDOFF_CONTRACT.md",
            "STL proof contract": "docs/debug/STL_PROOF_GATE_CONTRACT.md",
        }

    def doctor(self) -> dict[str, Any]:
        checks: list[dict[str, Any]] = []
        for name, rel in self.required_files().items():
            p = self.repo / rel
            checks.append({"name": name, "path": str(p), "exists": p.exists()})

        py_ok = sys.version_info >= (3, 9)
        slicers = self.find_slicers()

        data = {
            "project": "CICADA_FORGE_UE",
            "phase": "003G",
            "repo": str(self.repo),
            "python": sys.version,
            "python_ok": py_ok,
            "platform": platform.platform(),
            "checks": checks,
            "slicers_found": slicers,
            "latest": self.inventory(),
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }

        print(json.dumps(data, indent=2))
        return data

    def find_slicers(self) -> list[str]:
        candidates = [
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "OrcaSlicer" / "orca-slicer.exe",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "OrcaSlicer" / "orca-slicer.exe",
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Bambu Studio" / "bambu-studio.exe",
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Prusa3D" / "PrusaSlicer" / "prusa-slicer.exe",
        ]
        return [str(p) for p in candidates if p.exists()]

    def inventory(self) -> dict[str, Any]:
        folders = {
            "box_jobs": ("BoxJobs", "*.json"),
            "stl": ("STL", "*.stl"),
            "reports": ("Reports", "*.*"),
            "print_handoff": ("PrintHandoff", "*.json"),
            "receipts": ("Receipts", "*.json"),
            "run_reports": ("RunReports", "*.*"),
        }
        return {
            key: self.list_latest(folder, pattern)
            for key, (folder, pattern) in folders.items()
        }

    def custom_box(
        self,
        name: str,
        width: float,
        depth: float,
        height: float,
        material: str,
        layer_height: float,
        walls: int,
        infill: int,
        supports: str,
        open_report: bool = False,
        open_stl: bool = False,
    ) -> dict[str, Any]:
        job_dir = self.saved / "BoxJobs"
        job_dir.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name).strip("_") or "custom_box"
        job_path = job_dir / f"{safe_name}.json"

        self.py(
            "create job",
            self.box_job_runner,
            [
                "init",
                "--name", name,
                "--width", str(width),
                "--depth", str(depth),
                "--height", str(height),
                "--material", material,
                "--layer-height", str(layer_height),
                "--walls", str(walls),
                "--infill", str(infill),
                "--supports", supports,
                "--out", str(job_path),
            ],
        )

        run_args = ["run", str(job_path)]
        if open_stl:
            run_args.append("--open")
        self.py("run job", self.box_job_runner, run_args)

        quality = self.py("quality gate", self.stl_analyzer, ["--quality-gate"])
        report_args = ["--report"]
        if open_report:
            report_args.append("--open-report")
        report = self.py("write report", self.stl_analyzer, report_args)

        result = {
            "job_path": str(job_path),
            "quality_gate_returncode": quality.returncode,
            "report_returncode": report.returncode,
            "latest": self.inventory(),
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }
        return result

    def manifest_check(self) -> dict[str, Any]:
        latest_manifest = self.latest("PrintHandoff", "*.json")
        if latest_manifest is None:
            raise FileNotFoundError("No print handoff manifest found.")

        data = json.loads(latest_manifest.read_text(encoding="utf-8"))
        direct = data.get("direct_printer_send")
        gcode = data.get("gcode_streaming")
        machine = str(data.get("machine_bridge", "")).upper()

        ok = direct is False and (gcode is False or gcode is None) and machine == "LOCKED"
        result = {
            "manifest": str(latest_manifest),
            "direct_printer_send": direct,
            "gcode_streaming": gcode,
            "machine_bridge": machine,
            "pass": ok,
        }
        print(json.dumps(result, indent=2))

        if not ok:
            raise RuntimeError("Manifest safety check failed.")

        return result

    def write_run_report(self, title: str, data: dict[str, Any], open_report: bool = False) -> dict[str, str]:
        self.report_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = self.report_dir / f"{title}_{stamp}.json"
        html_path = self.report_dir / f"{title}_{stamp}.html"

        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        html_text = self.make_run_report_html(title, data)
        html_path.write_text(html_text, encoding="utf-8")

        if open_report:
            os.startfile(html_path)

        outputs = {"json": str(json_path), "html": str(html_path)}
        print(json.dumps(outputs, indent=2))
        return outputs

    def make_run_report_html(self, title: str, data: dict[str, Any]) -> str:
        raw = html.escape(json.dumps(data, indent=2))
        now = datetime.now().isoformat(timespec="seconds")
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CICADA Forge Run Report</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ color-scheme: dark; --bg:#050505; --panel:#111; --line:#333; --text:#f5f5f5; --muted:#aaa; --good:#9fffa8; }}
body {{ margin:0; font-family:system-ui, Segoe UI, Arial, sans-serif; background:var(--bg); color:var(--text); }}
main {{ max-width:1180px; margin:0 auto; padding:24px; }}
.panel {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; margin:12px 0; }}
h1 {{ margin:0 0 8px; }}
.sub {{ color:var(--muted); }}
.good {{ color:var(--good); font-weight:700; }}
pre {{ white-space:pre-wrap; word-break:break-word; background:#050505; border:1px solid #333; border-radius:12px; padding:14px; }}
</style>
</head>
<body>
<main>
<h1>CICADA FORGE HEADLESS RUN REPORT</h1>
<p class="sub">Generated {now}. No Unreal launch required. Direct printer send remains <span class="good">LOCKED</span>, because the machine does not get a tiny crown.</p>
<section class="panel">
<h2>{html.escape(title)}</h2>
<pre>{raw}</pre>
</section>
</main>
</body>
</html>
"""

    def full_check(self, open_report: bool = False) -> dict[str, Any]:
        doctor = self.doctor()
        pipeline = self.custom_box(
            name="headless_full_check_box",
            width=80,
            depth=40,
            height=12,
            material="PLA",
            layer_height=0.20,
            walls=3,
            infill=15,
            supports="off",
            open_report=False,
            open_stl=False,
        )
        manifest = self.manifest_check()
        inventory = self.inventory()

        data = {
            "project": "CICADA_FORGE_UE",
            "phase": "003G",
            "verdict": "PASS",
            "doctor": doctor,
            "pipeline": pipeline,
            "manifest_check": manifest,
            "inventory": inventory,
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }

        self.write_run_report("phase003G_full_check", data, open_report=open_report)
        return data


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA Forge headless control tower. No Unreal launch required.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor")
    sub.add_parser("inventory")
    sub.add_parser("manifest-check")

    demo = sub.add_parser("demo")
    demo.add_argument("--open-report", action="store_true")
    demo.add_argument("--open-stl", action="store_true")

    custom = sub.add_parser("custom-box")
    custom.add_argument("--name", default="custom_box")
    custom.add_argument("--width", type=float, required=True)
    custom.add_argument("--depth", type=float, required=True)
    custom.add_argument("--height", type=float, required=True)
    custom.add_argument("--material", default="PLA")
    custom.add_argument("--layer-height", type=float, default=0.20)
    custom.add_argument("--walls", type=int, default=3)
    custom.add_argument("--infill", type=int, default=15)
    custom.add_argument("--supports", default="off")
    custom.add_argument("--open-report", action="store_true")
    custom.add_argument("--open-stl", action="store_true")

    analyze = sub.add_parser("analyze")
    analyze.add_argument("--report", action="store_true")
    analyze.add_argument("--open-report", action="store_true")
    analyze.add_argument("--quality-gate", action="store_true")

    report = sub.add_parser("run-report")
    report.add_argument("--open", action="store_true")

    full = sub.add_parser("full-check")
    full.add_argument("--open-report", action="store_true")

    args = parser.parse_args()
    forge = HeadlessForge(args.repo)

    if args.command == "doctor":
        forge.doctor()
        return 0

    if args.command == "inventory":
        print(json.dumps(forge.inventory(), indent=2))
        return 0

    if args.command == "manifest-check":
        forge.manifest_check()
        return 0

    if args.command == "demo":
        result = forge.custom_box(
            name="headless_demo_box",
            width=80,
            depth=40,
            height=12,
            material="PLA",
            layer_height=0.20,
            walls=3,
            infill=15,
            supports="off",
            open_report=args.open_report,
            open_stl=args.open_stl,
        )
        forge.write_run_report("phase003G_demo", result, open_report=args.open_report)
        return 0

    if args.command == "custom-box":
        result = forge.custom_box(
            name=args.name,
            width=args.width,
            depth=args.depth,
            height=args.height,
            material=args.material,
            layer_height=args.layer_height,
            walls=args.walls,
            infill=args.infill,
            supports=args.supports,
            open_report=args.open_report,
            open_stl=args.open_stl,
        )
        forge.write_run_report("phase003G_custom_box", result, open_report=args.open_report)
        return 0

    if args.command == "analyze":
        extra = []
        if args.quality_gate:
            extra.append("--quality-gate")
        if args.report:
            extra.append("--report")
        if args.open_report:
            extra.append("--open-report")
        forge.py("analyze latest STL", forge.stl_analyzer, extra)
        return 0

    if args.command == "run-report":
        data = {
            "project": "CICADA_FORGE_UE",
            "phase": "003G",
            "doctor": forge.doctor(),
            "manifest_check": forge.manifest_check() if forge.latest("PrintHandoff", "*.json") else "no manifest yet",
            "inventory": forge.inventory(),
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }
        forge.write_run_report("phase003G_status", data, open_report=args.open)
        return 0

    if args.command == "full-check":
        forge.full_check(open_report=args.open_report)
        return 0

    raise AssertionError("Unhandled command")


if __name__ == "__main__":
    raise SystemExit(main())
