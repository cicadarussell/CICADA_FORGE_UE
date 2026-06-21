from __future__ import annotations

import argparse
import html
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))


@dataclass
class Check:
    name: str
    status: str
    detail: str
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "detail": self.detail,
            "path": self.path,
        }


class CicadaHealthReport:
    def __init__(self, repo: Path = DEFAULT_REPO, strict: bool = False) -> None:
        self.repo = repo
        self.strict = strict
        self.saved = repo / "Saved" / "CICADAForge"
        self.reports = self.saved / "HealthReports"

    def latest(self, rel: str, pattern: str) -> Path | None:
        folder = self.saved / rel
        if not folder.exists():
            return None
        files = sorted([p for p in folder.glob(pattern) if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)
        return files[0] if files else None

    def file_check(self, name: str, rel: str, required: bool = True) -> Check:
        path = self.repo / rel
        if path.exists():
            return Check(name, "PASS", "present", str(path))
        if required and self.strict:
            return Check(name, "FAIL", "missing required file in strict mode", str(path))
        if required:
            return Check(name, "CHECK", "missing in passive mode; expected if testing a patch folder rather than full repo", str(path))
        return Check(name, "NOT_RUN", "missing", str(path))

    def artifact_check(self, name: str, folder: str, pattern: str, required: bool = False) -> Check:
        found = self.latest(folder, pattern)
        if found:
            return Check(name, "PASS", f"latest artifact: {found.name}", str(found))
        status = "FAIL" if required and self.strict else "NOT_RUN"
        return Check(name, status, f"no artifact yet under Saved/CICADAForge/{folder}", str(self.saved / folder))

    def read_json(self, path: Path | None) -> dict[str, Any] | None:
        if not path or not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            return {"_error": str(exc), "_path": str(path)}

    def safety_checks(self) -> list[Check]:
        checks: list[Check] = []
        manifest = self.latest("PrintHandoff", "*.json")
        manifest_json = self.read_json(manifest)

        if not manifest_json:
            checks.append(Check("print manifest safety", "NOT_RUN", "no print handoff manifest yet", str(self.saved / "PrintHandoff")))
            return checks

        checks.append(Check(
            "direct printer send false",
            "PASS" if manifest_json.get("direct_printer_send") is False else "FAIL",
            f"direct_printer_send={manifest_json.get('direct_printer_send')}",
            str(manifest),
        ))
        checks.append(Check(
            "machine bridge locked",
            "PASS" if str(manifest_json.get("machine_bridge", "")).upper() == "LOCKED" else "FAIL",
            f"machine_bridge={manifest_json.get('machine_bridge')}",
            str(manifest),
        ))
        checks.append(Check(
            "gcode streaming false/absent",
            "PASS" if manifest_json.get("gcode_streaming") in (False, None) else "FAIL",
            f"gcode_streaming={manifest_json.get('gcode_streaming')}",
            str(manifest),
        ))
        return checks

    def report(self) -> dict[str, Any]:
        checks: list[Check] = []

        required_files = [
            ("UE project", "CICADA_FORGE_UE.uproject"),
            ("plugin descriptor", "Plugins/CICADAForge/CICADAForge.uplugin"),
            ("master wrapper", "scripts/cicada_forge.ps1"),
            ("dashboard generator", "tools/cicada_dashboard/cicada_artifact_dashboard.py"),
            ("headless control tower", "tools/cicada_headless/cicada_forge_headless.py"),
            ("CAD sidecar", "tools/cicada_cad_sidecar/cicada_cad_sidecar.py"),
            ("CAD engine launcher", "tools/cicada_env/cicada_cad_engine_launcher.py"),
            ("slicer dry-run planner", "tools/cicada_slicer/cicada_slicer_dryrun_planner.py"),
            ("command center", "tools/cicada_launcher/cicada_command_center.py"),
        ]
        for name, rel in required_files:
            checks.append(self.file_check(name, rel, required=True))

        artifact_specs = [
            ("box jobs", "BoxJobs", "*.json"),
            ("STLs", "STL", "*.stl"),
            ("STL reports", "Reports", "*.*"),
            ("run reports", "RunReports", "*.*"),
            ("dashboard", "Dashboard", "index.html"),
            ("CAD intent", "CADIntent", "*.json"),
            ("CAD reports", "CADReports", "*.json"),
            ("CAD exports", "CADExports", "*.*"),
            ("env reports", "EnvReports", "*.json"),
            ("slicer reports", "SlicerReports", "*.json"),
            ("health reports", "HealthReports", "*.json"),
            ("command center", "CommandCenter", "index.html"),
            ("launchers", "Launchers", "*.ps1"),
        ]
        for name, folder, pattern in artifact_specs:
            checks.append(self.artifact_check(name, folder, pattern, required=False))

        checks.extend(self.safety_checks())

        counts = {"PASS": 0, "NOT_RUN": 0, "CHECK": 0, "FAIL": 0}
        for check in checks:
            counts[check.status] = counts.get(check.status, 0) + 1

        verdict = "FAIL" if counts["FAIL"] else ("PASS" if counts["NOT_RUN"] == 0 else "PASS_WITH_NOT_RUN")
        score = max(0, round(100 * counts["PASS"] / max(len(checks), 1)))

        data = {
            "project": "CICADA_FORGE_UE",
            "phase": "003N",
            "generated": datetime.now().isoformat(timespec="seconds"),
            "mode": "strict" if self.strict else "passive",
            "verdict": verdict,
            "score_percent": score,
            "counts": counts,
            "checks": [c.to_dict() for c in checks],
            "note": "Missing artifacts are NOT_RUN in passive mode. This avoids treating 'not generated yet' as failure.",
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
            "gcode_generated": False,
        }
        print(json.dumps(data, indent=2))
        return data

    def write_report(self, data: dict[str, Any], open_report: bool = False) -> dict[str, str]:
        self.reports.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = self.reports / f"health_report_{stamp}.json"
        html_path = self.reports / f"health_report_{stamp}.html"
        latest_json = self.reports / "latest_health_report.json"
        latest_html = self.reports / "latest_health_report.html"

        json_text = json.dumps(data, indent=2)
        html_text = self.html_report(data)

        json_path.write_text(json_text, encoding="utf-8")
        html_path.write_text(html_text, encoding="utf-8")
        latest_json.write_text(json_text, encoding="utf-8")
        latest_html.write_text(html_text, encoding="utf-8")

        if open_report:
            os.startfile(latest_html)

        outputs = {
            "json": str(json_path),
            "html": str(html_path),
            "latest_json": str(latest_json),
            "latest_html": str(latest_html),
        }
        print(json.dumps(outputs, indent=2))
        return outputs

    def html_report(self, data: dict[str, Any]) -> str:
        verdict = data.get("verdict")
        cls = "good" if str(verdict).startswith("PASS") else "bad"
        rows = []
        for check in data.get("checks", []):
            status = str(check.get("status"))
            status_cls = "good" if status == "PASS" else ("warn" if status in ("NOT_RUN", "CHECK") else "bad")
            rows.append(
                "<tr>"
                f"<td>{html.escape(str(check.get('name')))}</td>"
                f'<td class="{status_cls}">{html.escape(status)}</td>'
                f"<td>{html.escape(str(check.get('detail')))}</td>"
                f"<td>{html.escape(str(check.get('path')))}</td>"
                "</tr>"
            )

        raw = html.escape(json.dumps(data, indent=2))
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CICADA Health Report</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ color-scheme: dark; --bg:#050505; --panel:#111; --line:#333; --text:#f5f5f5; --muted:#aaa; --good:#9fffa8; --warn:#ffd479; --bad:#ff8f8f; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:system-ui, Segoe UI, Arial, sans-serif; }}
main {{ max-width:1280px; margin:0 auto; padding:24px; }}
.panel {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; margin:12px 0; }}
.good {{ color:var(--good); font-weight:800; }}
.warn {{ color:var(--warn); font-weight:800; }}
.bad {{ color:var(--bad); font-weight:800; }}
.muted {{ color:var(--muted); }}
table {{ width:100%; border-collapse:collapse; }}
td, th {{ border-bottom:1px solid #2b2b2b; padding:8px; text-align:left; vertical-align:top; }}
pre {{ white-space:pre-wrap; word-break:break-word; background:#050505; border:1px solid #333; border-radius:12px; padding:14px; }}
</style>
</head>
<body>
<main>
<h1>CICADA PASSIVE HEALTH REPORT</h1>
<p class="muted">Missing outputs are NOT_RUN unless strict mode is used. Finally, diagnostics that know the difference between “broken” and “you did not press the button,” a distinction humanity has fought hard to ignore.</p>
<section class="panel">
<h2>Verdict: <span class="{cls}">{html.escape(str(verdict))}</span></h2>
<p>Score: {html.escape(str(data.get("score_percent")))}%</p>
<p>Mode: {html.escape(str(data.get("mode")))}</p>
<p>Direct printer send: false</p>
<p>Machine bridge: LOCKED</p>
</section>
<section class="panel">
<h2>Checks</h2>
<table>
<thead><tr><th>Name</th><th>Status</th><th>Detail</th><th>Path</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</section>
<section class="panel"><h2>Raw JSON</h2><pre>{raw}</pre></section>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="CICADA passive health report. Missing artifacts are NOT_RUN unless strict mode is enabled.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--open-report", action="store_true")
    args = parser.parse_args()

    tool = CicadaHealthReport(args.repo, strict=args.strict)
    data = tool.report()
    tool.write_report(data, open_report=args.open_report)

    return 0 if data["verdict"] != "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
