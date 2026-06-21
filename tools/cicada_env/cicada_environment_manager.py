from __future__ import annotations

import argparse
import html
import importlib.util
import json
import os
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))


class CicadaEnvManager:
    def __init__(self, repo: Path = DEFAULT_REPO) -> None:
        self.repo = repo
        self.saved = repo / "Saved" / "CICADAForge"
        self.env_root = repo / ".cicada_envs"
        self.cad_env = self.env_root / "cadquery"
        self.reports = self.saved / "EnvReports"

    def current_python(self) -> dict[str, Any]:
        return {
            "executable": sys.executable,
            "version": sys.version,
            "version_info": list(sys.version_info[:3]),
            "platform": platform.platform(),
            "cadquery_available_here": importlib.util.find_spec("cadquery") is not None,
            "freecad_available_here": importlib.util.find_spec("FreeCAD") is not None,
        }

    def venv_python(self, venv: Path) -> Path:
        if os.name == "nt":
            return venv / "Scripts" / "python.exe"
        return venv / "bin" / "python"

    def cad_venv_state(self) -> dict[str, Any]:
        py = self.venv_python(self.cad_env)
        state: dict[str, Any] = {
            "venv_path": str(self.cad_env),
            "venv_exists": self.cad_env.exists(),
            "python": str(py),
            "python_exists": py.exists(),
            "cadquery_available_in_venv": False,
            "probe_returncode": None,
            "probe_stdout": "",
            "probe_stderr": "",
        }

        if py.exists():
            probe = (
                "import importlib.util, sys; "
                "print('python=' + sys.executable); "
                "print('version=' + sys.version.replace(chr(10), ' ')); "
                "print('cadquery=' + str(importlib.util.find_spec('cadquery') is not None)); "
                "print('freecad=' + str(importlib.util.find_spec('FreeCAD') is not None))"
            )
            completed = subprocess.run([str(py), "-c", probe], capture_output=True, text=True, timeout=20)
            state["probe_returncode"] = completed.returncode
            state["probe_stdout"] = completed.stdout.strip()
            state["probe_stderr"] = completed.stderr.strip()
            state["cadquery_available_in_venv"] = "cadquery=True" in completed.stdout

        return state

    def doctor(self) -> dict[str, Any]:
        data = {
            "project": "CICADA_FORGE_UE",
            "phase": "003L",
            "repo": str(self.repo),
            "current_python": self.current_python(),
            "cadquery_venv": self.cad_venv_state(),
            "recommended": {
                "create_venv": r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\env\cicada_env_create_cadquery_venv.ps1"',
                "install_cadquery": r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\env\cicada_env_install_cadquery.ps1"',
                "recheck": r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\env\cicada_env_doctor.ps1" -OpenReport'
            },
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }
        print(json.dumps(data, indent=2))
        return data

    def write_report(self, data: dict[str, Any], title: str = "cicada_env_report", open_report: bool = False) -> dict[str, str]:
        self.reports.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = self.reports / f"{title}_{stamp}.json"
        html_path = self.reports / f"{title}_{stamp}.html"

        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        html_path.write_text(self.html_report(data), encoding="utf-8")

        if open_report:
            os.startfile(html_path)

        output = {"json": str(json_path), "html": str(html_path)}
        print(json.dumps(output, indent=2))
        return output

    def html_report(self, data: dict[str, Any]) -> str:
        raw = html.escape(json.dumps(data, indent=2))
        current = data.get("current_python", {})
        venv = data.get("cadquery_venv", {})
        venv_ok = bool(venv.get("cadquery_available_in_venv"))
        current_ok = bool(current.get("cadquery_available_here"))
        status = "READY" if (venv_ok or current_ok) else "MISSING"
        cls = "good" if status == "READY" else "warn"

        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CICADA Environment Report</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ color-scheme: dark; --bg:#050505; --panel:#111; --line:#333; --text:#f5f5f5; --muted:#aaa; --good:#9fffa8; --warn:#ffd479; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:system-ui, Segoe UI, Arial, sans-serif; }}
main {{ max-width:1100px; margin:0 auto; padding:24px; }}
.panel {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; margin:12px 0; }}
.good {{ color:var(--good); font-weight:800; }}
.warn {{ color:var(--warn); font-weight:800; }}
.muted {{ color:var(--muted); }}
pre {{ white-space:pre-wrap; word-break:break-word; background:#050505; border:1px solid #333; border-radius:12px; padding:14px; }}
td {{ border-bottom:1px solid #2b2b2b; padding:8px; }}
table {{ width:100%; border-collapse:collapse; }}
</style>
</head>
<body>
<main>
<h1>CICADA ENVIRONMENT REPORT</h1>
<p class="muted">CadQuery/FreeCAD readiness report. No installs happen unless you explicitly run the install script, because accidental CAD kernels are how laptops become tiny heaters.</p>
<section class="panel">
<h2>CAD Engine Status: <span class="{cls}">{status}</span></h2>
<table>
<tr><td>Current Python</td><td>{html.escape(str(current.get("executable")))}</td></tr>
<tr><td>CadQuery in current Python</td><td>{html.escape(str(current_ok))}</td></tr>
<tr><td>CadQuery venv path</td><td>{html.escape(str(venv.get("venv_path")))}</td></tr>
<tr><td>Venv exists</td><td>{html.escape(str(venv.get("venv_exists")))}</td></tr>
<tr><td>CadQuery in venv</td><td>{html.escape(str(venv_ok))}</td></tr>
</table>
</section>
<section class="panel">
<h2>Recommended commands</h2>
<pre>{html.escape(json.dumps(data.get("recommended", {}), indent=2))}</pre>
</section>
<section class="panel">
<h2>Raw JSON</h2>
<pre>{raw}</pre>
</section>
</main>
</body>
</html>
"""

    def create_venv_plan(self) -> dict[str, Any]:
        return {
            "project": "CICADA_FORGE_UE",
            "phase": "003L",
            "venv_path": str(self.cad_env),
            "create_command": [sys.executable, "-m", "venv", str(self.cad_env)],
            "install_command": [str(self.venv_python(self.cad_env)), "-m", "pip", "install", "--upgrade", "pip", "cadquery"],
            "automatic_install": False,
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA environment manager. Reports/creates optional CAD engine environment.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    sub = parser.add_subparsers(dest="command", required=True)
    doctor = sub.add_parser("doctor")
    doctor.add_argument("--open-report", action="store_true")
    sub.add_parser("plan")
    args = parser.parse_args()

    manager = CicadaEnvManager(args.repo)

    if args.command == "doctor":
        data = manager.doctor()
        manager.write_report(data, open_report=args.open_report)
        return 0

    if args.command == "plan":
        data = manager.create_venv_plan()
        print(json.dumps(data, indent=2))
        return 0

    raise AssertionError("Unhandled command")


if __name__ == "__main__":
    raise SystemExit(main())
