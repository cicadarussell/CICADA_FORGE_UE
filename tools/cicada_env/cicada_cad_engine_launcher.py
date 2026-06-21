from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))


class CadEngineLauncher:
    def __init__(self, repo: Path = DEFAULT_REPO) -> None:
        self.repo = repo
        self.sidecar = repo / "tools" / "cicada_cad_sidecar" / "cicada_cad_sidecar.py"
        self.venv = repo / ".cicada_envs" / "cadquery"
        self.saved = repo / "Saved" / "CICADAForge"
        self.reports = self.saved / "EnvReports"

    def venv_python(self) -> Path:
        if os.name == "nt":
            return self.venv / "Scripts" / "python.exe"
        return self.venv / "bin" / "python"

    def probe_python(self, python_exe: Path | str) -> dict[str, Any]:
        code = (
            "import importlib.util, sys, json; "
            "print(json.dumps({"
            "'executable': sys.executable, "
            "'version': sys.version, "
            "'cadquery': importlib.util.find_spec('cadquery') is not None, "
            "'FreeCAD': importlib.util.find_spec('FreeCAD') is not None"
            "}))"
        )
        try:
            completed = subprocess.run([str(python_exe), "-c", code], capture_output=True, text=True, timeout=20)
            data = json.loads(completed.stdout.strip()) if completed.returncode == 0 and completed.stdout.strip() else {}
            return {"returncode": completed.returncode, "data": data, "stderr": completed.stderr.strip()}
        except Exception as exc:
            return {"returncode": -1, "data": {}, "stderr": str(exc)}

    def engine_plan(self) -> dict[str, Any]:
        current_probe = self.probe_python(sys.executable)
        venv_py = self.venv_python()
        venv_probe = self.probe_python(venv_py) if venv_py.exists() else {"returncode": None, "data": {}, "stderr": "venv python missing"}

        if venv_probe.get("data", {}).get("cadquery") is True:
            selected = str(venv_py)
            reason = "isolated .cicada_envs/cadquery Python has CadQuery"
        elif current_probe.get("data", {}).get("cadquery") is True:
            selected = sys.executable
            reason = "current Python has CadQuery"
        else:
            selected = sys.executable
            reason = "no CadQuery engine found; sidecar will validate/report and block exact STEP honestly"

        return {
            "project": "CICADA_FORGE_UE",
            "phase": "003M",
            "repo": str(self.repo),
            "selected_python": selected,
            "selected_reason": reason,
            "current_python": current_probe,
            "venv_python": str(venv_py),
            "venv_probe": venv_probe,
            "sidecar": str(self.sidecar),
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }

    def write_plan_report(self, data: dict[str, Any]) -> dict[str, str]:
        self.reports.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.reports / f"cad_engine_launcher_{stamp}.json"
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return {"report_json": str(path)}

    def run_generate(self, part: Path, engine: str, open_report: bool = False) -> int:
        plan = self.engine_plan()
        outputs = self.write_plan_report(plan)
        print(json.dumps({**plan, "launcher_report": outputs}, indent=2))

        selected_python = plan["selected_python"]

        # If selected Python has CadQuery, use engine auto/cadquery. Otherwise force engine none so the report is honest.
        has_cadquery = (
            plan.get("venv_probe", {}).get("data", {}).get("cadquery") is True
            or plan.get("current_python", {}).get("data", {}).get("cadquery") is True
        )
        actual_engine = engine
        if engine == "auto" and not has_cadquery:
            actual_engine = "none"

        cmd = [selected_python, str(self.sidecar), "--repo", str(self.repo), "generate", str(part), "--engine", actual_engine]
        if open_report:
            cmd.append("--open-report")

        print("CAD ENGINE LAUNCHER COMMAND:")
        print(json.dumps(cmd, indent=2))

        completed = subprocess.run(cmd, cwd=self.repo)
        return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA CAD engine launcher. Prefers isolated CadQuery venv if available.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor")

    generate = sub.add_parser("generate")
    generate.add_argument("part", type=Path)
    generate.add_argument("--engine", choices=["auto", "cadquery", "freecad", "none"], default="auto")
    generate.add_argument("--open-report", action="store_true")

    args = parser.parse_args()
    launcher = CadEngineLauncher(args.repo)

    if args.command == "doctor":
        data = launcher.engine_plan()
        outputs = launcher.write_plan_report(data)
        print(json.dumps({**data, "launcher_report": outputs}, indent=2))
        return 0

    if args.command == "generate":
        return launcher.run_generate(args.part, engine=args.engine, open_report=args.open_report)

    raise AssertionError("Unhandled command")


if __name__ == "__main__":
    raise SystemExit(main())
