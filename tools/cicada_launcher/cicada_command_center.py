from __future__ import annotations

import argparse
import html
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))


class CommandCenter:
    def __init__(self, repo: Path = DEFAULT_REPO) -> None:
        self.repo = repo
        self.saved = repo / "Saved" / "CICADAForge"
        self.center = self.saved / "CommandCenter"
        self.launchers = self.saved / "Launchers"

    def command(self, title: str, command: str, group: str, note: str) -> dict[str, str]:
        return {"title": title, "command": command, "group": group, "note": note}

    def commands(self) -> list[dict[str, str]]:
        base = r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1"'
        return [
            self.command("003O full check", f"{base} -Command phase003O-full-check -OpenReport", "main", "Health, command center, 003M check, ledger, release gate, dashboard."),
            self.command("Release gate", f"{base} -Command release-gate -OpenReport", "main", "RC_READY / RC_PARTIAL / BLOCKED."),
            self.command("Ledger latest", f"{base} -Command ledger-latest", "main", "Show latest recorded run state."),
            self.command("Passive health report", f"{base} -Command health-report -OpenReport", "main", "Not-run-aware diagnostics."),
            self.command("Open dashboard", f"{base} -Command dashboard -OpenDashboard", "main", "Artifact control room."),
            self.command("Command center", f"{base} -Command command-center -OpenReport", "main", "Regenerate this page."),

            self.command("CAD full check", f"{base} -Command cad-full-check -OpenReport -OpenDashboard", "cad", "Generate CAD reports/sample parts."),
            self.command("CAD engine doctor", f"{base} -Command cad-engine-doctor -OpenReport", "cad", "Pick current Python vs .cicada_envs/cadquery."),
            self.command("Sensor plate", f'{base} -Command cad-build-sensor-plate -Name "robot_sensor_plate" -OpenReport', "cad", "Slots and standoffs."),
            self.command("Motor mount", f'{base} -Command cad-build-motor-mount -Name "slotted_motor_mount" -OpenReport', "cad", "Slotted motor mount intent."),

            self.command("Env doctor", f"{base} -Command env-doctor -OpenReport", "environment", "Python/CadQuery readiness."),
            self.command("Create CadQuery venv", f"{base} -Command env-create-cadquery", "environment", "Creates venv only, no install."),
            self.command("Install CadQuery", f"{base} -Command env-install-cadquery", "environment", "Explicit install only."),

            self.command("Slicer readiness", f"{base} -Command slicer-readiness -OpenReport", "slicer", "Find slicer/STL. No G-code."),
            self.command("Slicer dry-run plan", f"{base} -Command slicer-dryrun-plan -OpenReport", "slicer", "Writes plan only. Does not execute."),
        ]

    def launcher_filename(self, title: str) -> str:
        safe = "".join(ch if ch.isalnum() else "_" for ch in title).strip("_")
        return f"{safe}.ps1"

    def write_launchers(self, commands: list[dict[str, str]]) -> list[dict[str, str]]:
        self.launchers.mkdir(parents=True, exist_ok=True)
        outputs = []
        for item in commands:
            path = self.launchers / self.launcher_filename(item["title"])
            content = (
                f"# CICADA launcher: {item['title']}\n"
                f"# {item['note']}\n"
                f"{item['command']}\n"
            )
            path.write_text(content, encoding="utf-8")
            outputs.append({"title": item["title"], "path": str(path)})
        return outputs

    def generate(self, open_report: bool = False) -> dict[str, Any]:
        self.center.mkdir(parents=True, exist_ok=True)
        commands = self.commands()
        launchers = self.write_launchers(commands)

        snapshot = {
            "project": "CICADA_FORGE_UE",
            "phase": "003N",
            "generated": datetime.now().isoformat(timespec="seconds"),
            "commands": commands,
            "launchers": launchers,
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
            "gcode_generated": False,
        }

        json_path = self.center / "command_center.json"
        html_path = self.center / "index.html"
        json_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
        html_path.write_text(self.html(snapshot), encoding="utf-8")

        if open_report:
            os.startfile(html_path)

        outputs = {"json": str(json_path), "html": str(html_path), "launchers": launchers}
        print(json.dumps(outputs, indent=2))
        return outputs

    def html(self, snapshot: dict[str, Any]) -> str:
        groups = {}
        for cmd in snapshot["commands"]:
            groups.setdefault(cmd["group"], []).append(cmd)

        sections = []
        for group, commands in groups.items():
            cards = []
            for cmd in commands:
                cards.append(
                    "<div class='card'>"
                    f"<h3>{html.escape(cmd['title'])}</h3>"
                    f"<p class='muted'>{html.escape(cmd['note'])}</p>"
                    f"<pre>{html.escape(cmd['command'])}</pre>"
                    "</div>"
                )
            sections.append(f"<section class='panel'><h2>{html.escape(group.upper())}</h2><div class='grid'>{''.join(cards)}</div></section>")

        raw = html.escape(json.dumps(snapshot, indent=2))
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CICADA Command Center</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ color-scheme: dark; --bg:#050505; --panel:#111; --line:#333; --text:#f5f5f5; --muted:#aaa; --cyan:#aef5ff; --warn:#ffd479; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:system-ui, Segoe UI, Arial, sans-serif; }}
main {{ max-width:1320px; margin:0 auto; padding:24px; }}
.panel, .card {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; margin:12px 0; }}
.grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:12px; }}
.muted {{ color:var(--muted); }}
.warn {{ color:var(--warn); font-weight:800; }}
pre {{ white-space:pre-wrap; word-break:break-word; background:#050505; border:1px solid #333; border-radius:12px; padding:12px; }}
</style>
</head>
<body>
<main>
<h1>CICADA COMMAND CENTER</h1>
<p class="muted">Copy/paste command center and generated launcher scripts. Browser buttons are not executing PowerShell, because web security exists to stop exactly that nonsense.</p>
<p class="warn">Machine bridge: LOCKED | G-code generated: false | Direct printer send: false</p>
{''.join(sections)}
<section class="panel"><h2>Raw JSON</h2><pre>{raw}</pre></section>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CICADA command center and launcher scripts.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--open-report", action="store_true")
    args = parser.parse_args()

    CommandCenter(args.repo).generate(open_report=args.open_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
