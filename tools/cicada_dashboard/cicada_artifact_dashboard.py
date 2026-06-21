from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))


@dataclass
class Artifact:
    kind: str
    path: Path
    size_bytes: int
    modified: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "name": self.path.name,
            "path": str(self.path),
            "size_bytes": self.size_bytes,
            "modified": self.modified,
        }


class CicadaDashboard:
    def __init__(self, repo: Path = DEFAULT_REPO) -> None:
        self.repo = repo
        self.saved = repo / "Saved" / "CICADAForge"
        self.dashboard_dir = self.saved / "Dashboard"
        self.artifact_specs = {
            "BoxJobs": ("BoxJobs", "*.json"),
            "STL": ("STL", "*.stl"),
            "Reports": ("Reports", "*.*"),
            "RunReports": ("RunReports", "*.*"),
            "PrintHandoff": ("PrintHandoff", "*.json"),
            "Receipts": ("Receipts", "*.json"),
            "FeatureGraphs": ("FeatureGraphs", "*.json"),
            "CADIntent": ("CADIntent", "*.json"),
            "CADExports": ("CADExports", "*.*"),
            "CADReports": ("CADReports", "*.*"),
            "EnvReports": ("EnvReports", "*.*"),
            "SlicerReports": ("SlicerReports", "*.*"),
            "HealthReports": ("HealthReports", "*.*"),
            "CommandCenter": ("CommandCenter", "*.*"),
            "Launchers": ("Launchers", "*.ps1"),
            "Ledger": ("Ledger", "*.*"),
            "ReleaseGates": ("ReleaseGates", "*.*"),
            "IntegrationReports": ("IntegrationReports", "*.*"),
        }

    def artifact_list(self, kind: str, folder: str, pattern: str, limit: int = 12) -> list[Artifact]:
        base = self.saved / folder
        if not base.exists():
            return []

        files = sorted(
            [p for p in base.glob(pattern) if p.is_file()],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )[:limit]

        return [
            Artifact(
                kind=kind,
                path=p,
                size_bytes=p.stat().st_size,
                modified=datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds"),
            )
            for p in files
        ]

    def inventory(self) -> dict[str, list[dict[str, Any]]]:
        return {
            kind: [a.to_dict() for a in self.artifact_list(kind, folder, pattern)]
            for kind, (folder, pattern) in self.artifact_specs.items()
        }

    def latest_file(self, folder: str, pattern: str) -> Path | None:
        files = self.artifact_list(folder, folder, pattern, limit=1)
        return files[0].path if files else None

    def read_json_safe(self, path: Path | None) -> dict[str, Any] | None:
        if path is None or not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            return {"_error": str(exc), "_path": str(path)}

    def git_status(self) -> dict[str, Any]:
        try:
            completed = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.repo,
                text=True,
                capture_output=True,
                shell=False,
                timeout=12,
            )
            raw_lines = [line for line in completed.stdout.splitlines() if line.strip()]
            ignored_prefixes = ("?? .cicada_envs/", "?? Saved/", "?? Saved\\", "?? DerivedDataCache/")
            lines = [line for line in raw_lines if not line.startswith(ignored_prefixes)]
            return {
                "returncode": completed.returncode,
                "changed_count": len(lines),
                "lines": lines[:120],
                "ignored_generated_count": len(raw_lines) - len(lines),
                "stderr": completed.stderr.strip(),
            }
        except Exception as exc:
            return {"returncode": -1, "changed_count": None, "lines": [], "stderr": str(exc)}

    def phase_state(self) -> dict[str, Any]:
        config = self.repo / "Config" / "CICADAForgeState.ini"
        text = config.read_text(encoding="utf-8", errors="replace") if config.exists() else ""
        def find(key: str) -> str:
            m = re.search(rf"^{re.escape(key)}=(.*)$", text, flags=re.MULTILINE)
            return m.group(1).strip() if m else "unknown"
        return {
            "CurrentPhase": find("CurrentPhase"),
            "EvidenceState": find("EvidenceState"),
            "CadSidecarState": find("CadSidecarState"),
            "MachineBridgeState": find("MachineBridgeState"),
            "bMachineCommandsLocked": find("bMachineCommandsLocked"),
        }

    def safety_summary(self) -> dict[str, Any]:
        latest_manifest = self.latest_file("PrintHandoff", "*.json")
        manifest = self.read_json_safe(latest_manifest)

        direct_ok = None
        machine_ok = None
        gcode_ok = None

        if isinstance(manifest, dict):
            direct_ok = manifest.get("direct_printer_send") is False
            machine_ok = str(manifest.get("machine_bridge", "")).upper() == "LOCKED"
            gcode = manifest.get("gcode_streaming")
            gcode_ok = gcode is False or gcode is None

        return {
            "latest_manifest": str(latest_manifest) if latest_manifest else None,
            "direct_printer_send_false": direct_ok,
            "machine_bridge_locked": machine_ok,
            "gcode_streaming_false_or_absent": gcode_ok,
            "safe_to_continue_headless": all(v is True for v in [direct_ok, machine_ok, gcode_ok]) if manifest else False,
        }

    def capability_matrix(self) -> list[dict[str, str]]:
        return [
            {"capability": "Unreal cockpit", "status": "built", "notes": "Still useful, but no longer required for every check"},
            {"capability": "Headless doctor/full-check", "status": "built", "notes": "Phase 003G"},
            {"capability": "Local dashboard", "status": "built", "notes": "Phase 003H"},
            {"capability": "Editable box jobs", "status": "built", "notes": "JSON source-of-truth"},
            {"capability": "STL generation", "status": "built", "notes": "ASCII STL boxes"},
            {"capability": "STL analysis/report", "status": "built", "notes": "Quality gate + HTML report"},
            {"capability": "Manual print manifest", "status": "built", "notes": "Direct send false"},
            {"capability": "CAD/STEP sidecar contract", "status": "built", "notes": "003I exact-geometry boundary"},
            {"capability": "Exact STEP export", "status": "engine-dependent", "notes": "CadQuery required; no fake STEP if missing"},
            {"capability": "CadQuery env readiness", "status": "built", "notes": "003L reports/venv plan"},
            {"capability": "Slicer readiness", "status": "built", "notes": "003L report-only; no G-code"},
            {"capability": "CAD engine launcher", "status": "built", "notes": "003M prefers .cicada_envs/cadquery"},
            {"capability": "Slicer dry-run planner", "status": "built", "notes": "003M plan-only; no G-code"},
            {"capability": "Passive health report", "status": "built", "notes": "003N not-run-aware diagnostics"},
            {"capability": "Command center", "status": "built", "notes": "003N launcher scripts and command page"},
            {"capability": "Run ledger", "status": "built", "notes": "003O latest-good/run history"},
            {"capability": "Release candidate gate", "status": "built", "notes": "003O RC_READY/RC_PARTIAL/BLOCKED"},
            {"capability": "Slicer CLI", "status": "not built", "notes": "Later, dry-run only first"},
            {"capability": "Direct printer bridge", "status": "locked", "notes": "Correctly locked"},
        ]

    def recommended_next_command(self) -> str:
        return (
            r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" '
            r'-Command phase003P-full-check -OpenReport -OpenDashboard'
        )

    def command_cards(self) -> list[dict[str, str]]:
        return [
            {
                "title": "003P full integration check",
                "command": r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command phase003P-full-check -OpenReport -OpenDashboard'
            },
            {
                "title": "Full project audit",
                "command": r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command full-project-audit -OpenReport'
            },
            {
                "title": "Release gate",
                "command": r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command release-gate -OpenReport'
            },
            {
                "title": "Ledger latest",
                "command": r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command ledger-latest'
            },
            {
                "title": "CAD full check",
                "command": r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command cad-full-check -OpenReport -OpenDashboard'
            },
            {
                "title": "Slicer dry-run plan",
                "command": r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command slicer-dryrun-plan -OpenReport'
            },
            {
                "title": "Open dashboard",
                "command": r'powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard'
            },
        ]

    def build_snapshot(self) -> dict[str, Any]:
        latest_report = self.latest_file("Reports", "*.json")
        latest_run_report = self.latest_file("RunReports", "*.json")
        latest_manifest = self.latest_file("PrintHandoff", "*.json")
        latest_receipt = self.latest_file("Receipts", "*.json")
        latest_job = self.latest_file("BoxJobs", "*.json")

        phase_state = self.phase_state()
        current_phase = str(phase_state.get("CurrentPhase", "unknown"))
        phase_code_match = re.search(r"Phase\s+([0-9A-Z]+)", current_phase)
        phase_code = phase_code_match.group(1) if phase_code_match else "current"

        snapshot = {
            "project": "CICADA_FORGE_UE",
            "phase": phase_code,
            "generated": datetime.now().isoformat(timespec="seconds"),
            "repo": str(self.repo),
            "phase_state": phase_state,
            "safety": self.safety_summary(),
            "git": self.git_status(),
            "capability_matrix": self.capability_matrix(),
            "recommended_next_command": self.recommended_next_command(),
            "command_cards": self.command_cards(),
            "latest_json": {
                "latest_report": self.read_json_safe(latest_report),
                "latest_run_report": self.read_json_safe(latest_run_report),
                "latest_manifest": self.read_json_safe(latest_manifest),
                "latest_receipt": self.read_json_safe(latest_receipt),
                "latest_job": self.read_json_safe(latest_job),
            },
            "inventory": self.inventory(),
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
        }
        return snapshot

    def esc(self, value: Any) -> str:
        return html.escape(str(value))

    def status_class(self, status: str) -> str:
        s = status.lower()
        if s in {"built", "pass", "true", "ok"}:
            return "good"
        if s in {"locked"}:
            return "warn"
        if "not built" in s or "fail" in s:
            return "bad"
        return "muted"

    def table_artifacts(self, title: str, items: list[dict[str, Any]]) -> str:
        rows = []
        if not items:
            rows.append('<tr><td colspan="4" class="muted">None yet</td></tr>')
        for item in items:
            p = Path(item["path"])
            file_url = p.as_uri() if p.exists() else ""
            open_link = f'<a href="{self.esc(file_url)}">open</a>' if file_url else ""
            rows.append(
                "<tr>"
                f"<td>{self.esc(item['modified'])}</td>"
                f"<td>{self.esc(item['name'])}</td>"
                f"<td>{self.esc(item['size_bytes'])}</td>"
                f"<td>{open_link}</td>"
                "</tr>"
            )
        return f"""
<section class="panel">
<h2>{self.esc(title)}</h2>
<table>
<thead><tr><th>Modified</th><th>Name</th><th>Bytes</th><th>Open</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</section>
"""

    def render_html(self, snapshot: dict[str, Any]) -> str:
        phase = snapshot["phase_state"]
        safety = snapshot["safety"]
        git = snapshot["git"]
        inventory = snapshot["inventory"]

        safety_pass = safety.get("safe_to_continue_headless") is True
        safety_text = "PASS" if safety_pass else "CHECK"
        safety_cls = "good" if safety_pass else "warn"

        capability_rows = []
        for row in snapshot["capability_matrix"]:
            cls = self.status_class(row["status"])
            capability_rows.append(
                "<tr>"
                f"<td>{self.esc(row['capability'])}</td>"
                f'<td class="{cls}">{self.esc(row["status"])}</td>'
                f"<td>{self.esc(row['notes'])}</td>"
                "</tr>"
            )

        artifact_sections = "\n".join(
            self.table_artifacts(title, items)
            for title, items in inventory.items()
        )

        raw_json = self.esc(json.dumps(snapshot, indent=2))

        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CICADA Forge Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{
  color-scheme: dark;
  --bg:#050505; --panel:#111; --line:#333; --text:#f5f5f5; --muted:#aaa;
  --good:#9fffa8; --warn:#ffd479; --bad:#ff8f8f; --cyan:#aef5ff;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:system-ui, Segoe UI, Arial, sans-serif; }}
main {{ max-width:1320px; margin:0 auto; padding:24px; }}
h1 {{ margin:0 0 8px; letter-spacing:.04em; }}
h2 {{ margin:0 0 12px; }}
a {{ color:var(--cyan); }}
.grid {{ display:grid; grid-template-columns: 1.2fr .8fr; gap:16px; }}
.cards {{ display:grid; grid-template-columns: repeat(4, minmax(160px, 1fr)); gap:12px; margin:18px 0; }}
.card, .panel {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; }}
.big {{ font-size:28px; font-weight:800; }}
.muted {{ color:var(--muted); }}
.good {{ color:var(--good); font-weight:700; }}
.warn {{ color:var(--warn); font-weight:700; }}
.bad {{ color:var(--bad); font-weight:700; }}
table {{ width:100%; border-collapse:collapse; }}
th, td {{ text-align:left; border-bottom:1px solid #2b2b2b; padding:8px; vertical-align:top; }}
th {{ color:var(--muted); font-weight:600; }}
pre {{ white-space:pre-wrap; word-break:break-word; background:#050505; border:1px solid #333; border-radius:12px; padding:14px; max-height:520px; overflow:auto; }}
code {{ color:var(--cyan); }}
@media (max-width: 980px) {{ .grid, .cards {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body>
<main>
<h1>CICADA FORGE CONTROL ROOM</h1>
<p class="muted">Generated {self.esc(snapshot["generated"])}. Local dashboard only. It does not control machines, because apparently we are still pretending consequences exist.</p>

<div class="cards">
  <div class="card"><div class="muted">Phase</div><div class="big">{self.esc(snapshot.get("phase"))}</div></div>
  <div class="card"><div class="muted">Safety</div><div class="big {safety_cls}">{safety_text}</div></div>
  <div class="card"><div class="muted">Git changed files</div><div class="big">{self.esc(git.get("changed_count"))}</div></div>
  <div class="card"><div class="muted">Machine bridge</div><div class="big warn">LOCKED</div></div>
</div>

<div class="grid">
<section class="panel">
<h2>Current State</h2>
<table>
<tr><th>Key</th><th>Value</th></tr>
<tr><td>Current phase</td><td>{self.esc(phase.get("CurrentPhase"))}</td></tr>
<tr><td>Evidence</td><td>{self.esc(phase.get("EvidenceState"))}</td></tr>
<tr><td>CAD sidecar</td><td>{self.esc(phase.get("CadSidecarState"))}</td></tr>
<tr><td>Machine bridge</td><td>{self.esc(phase.get("MachineBridgeState"))}</td></tr>
<tr><td>Machine commands locked</td><td>{self.esc(phase.get("bMachineCommandsLocked"))}</td></tr>
<tr><td>Latest manifest</td><td>{self.esc(safety.get("latest_manifest"))}</td></tr>
<tr><td>direct_printer_send false</td><td>{self.esc(safety.get("direct_printer_send_false"))}</td></tr>
<tr><td>gcode false/absent</td><td>{self.esc(safety.get("gcode_streaming_false_or_absent"))}</td></tr>
</table>
</section>

<section class="panel">
<h2>Next Useful Command</h2>
<p>Run the headless full check, generate proof, and open a report:</p>
<pre>{self.esc(snapshot["recommended_next_command"])}</pre>
<p class="muted">Do this instead of opening Unreal for every little check. Unreal can have a nap. It has earned nothing, but still.</p>
</section>
</div>

<section class="panel" style="margin-top:16px;">
<h2>Command Cards</h2>
<p class="muted">Copy/paste commands. Browser does not run them directly, because that would be local automation with clown shoes.</p>
<div class="cards">
{''.join('<div class="card"><div class="muted">' + self.esc(card["title"]) + '</div><pre>' + self.esc(card["command"]) + '</pre></div>' for card in snapshot.get("command_cards", []))}
</div>
</section>

<section class="panel" style="margin-top:16px;">
<h2>Capability Matrix</h2>
<table>
<thead><tr><th>Capability</th><th>Status</th><th>Notes</th></tr></thead>
<tbody>{''.join(capability_rows)}</tbody>
</table>
</section>

<div class="grid" style="margin-top:16px;">
{artifact_sections}
</div>

<section class="panel" style="margin-top:16px;">
<h2>Git Status</h2>
<pre>{self.esc(chr(10).join(git.get("lines", [])) or "clean or unavailable")}</pre>
</section>

<section class="panel" style="margin-top:16px;">
<h2>Raw Snapshot JSON</h2>
<pre>{raw_json}</pre>
</section>
</main>
</body>
</html>
"""

    def generate(self, open_dashboard: bool = False) -> dict[str, str]:
        self.dashboard_dir.mkdir(parents=True, exist_ok=True)
        snapshot = self.build_snapshot()

        json_path = self.dashboard_dir / "cicada_dashboard_snapshot.json"
        html_path = self.dashboard_dir / "index.html"

        json_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
        html_path.write_text(self.render_html(snapshot), encoding="utf-8")

        if open_dashboard:
            os.startfile(html_path)

        outputs = {
            "dashboard_json": str(json_path),
            "dashboard_html": str(html_path),
            "direct_printer_send": "LOCKED_FALSE",
        }
        print(json.dumps(outputs, indent=2))
        return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA local artifact dashboard generator.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--open", action="store_true")
    args = parser.parse_args()

    dashboard = CicadaDashboard(args.repo)
    dashboard.generate(open_dashboard=args.open)
    print("Machine bridge: LOCKED")
    print("Direct printer send: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
