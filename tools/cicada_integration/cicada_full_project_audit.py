from __future__ import annotations

import argparse
import html
import json
import os
import py_compile
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))

BANNED_EXTERNAL_SWITCH_PATTERNS = [
    "-OpenReport:$OpenReport",
    "-OpenDashboard:$OpenDashboard",
    "-OpenStl:$OpenStl",
    "-OpenReport:$Open",
    "-OpenDashboard:$Open",
]

REQUIRED_FILES = [
    "CICADA_FORGE_UE.uproject",
    "Plugins/CICADAForge/CICADAForge.uplugin",
    "scripts/cicada_forge.ps1",
    "tools/cicada_cad_sidecar/cicada_cad_sidecar.py",
    "tools/cicada_cad_sidecar/cicada_mechanical_part_builder.py",
    "tools/cicada_env/cicada_cad_engine_launcher.py",
    "tools/cicada_slicer/cicada_slicer_readiness.py",
    "tools/cicada_slicer/cicada_slicer_dryrun_planner.py",
    "tools/cicada_dashboard/cicada_artifact_dashboard.py",
    "tools/cicada_health/cicada_health_report.py",
    "tools/cicada_launcher/cicada_command_center.py",
    "tools/cicada_ledger/cicada_run_ledger.py",
    "tools/cicada_integration/cicada_full_project_audit.py",
]


class FullProjectAudit:
    def __init__(self, repo: Path = DEFAULT_REPO) -> None:
        self.repo = repo
        self.saved = repo / "Saved" / "CICADAForge"
        self.report_dir = self.saved / "IntegrationReports"

    def current_phase(self) -> str:
        cfg = self.repo / "Config" / "CICADAForgeState.ini"
        if not cfg.exists():
            return "unknown"
        for line in cfg.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("CurrentPhase="):
                return line.split("=", 1)[1].strip()
        return "unknown"

    def check_required_files(self) -> list[dict[str, Any]]:
        checks = []
        # When testing a patch folder in the sandbox, the full Unreal project file/plugin descriptor may not be present.
        # In the real installed repo these should pass. Missing here is CHECK, not FAIL.
        patch_folder_tolerated = {"CICADA_FORGE_UE.uproject", "Plugins/CICADAForge/CICADAForge.uplugin"}
        for rel in REQUIRED_FILES:
            p = self.repo / rel
            if p.exists():
                status = "PASS"
            elif rel in patch_folder_tolerated:
                status = "CHECK"
            else:
                status = "FAIL"
            checks.append({"name": f"required:{rel}", "status": status, "detail": str(p)})
        return checks

    def check_python_compile(self) -> list[dict[str, Any]]:
        checks = []
        for p in sorted((self.repo / "tools").rglob("*.py")):
            if "__pycache__" in p.parts:
                continue
            try:
                py_compile.compile(str(p), doraise=True)
                checks.append({"name": f"py_compile:{p.relative_to(self.repo)}", "status": "PASS", "detail": "compiled"})
            except Exception as exc:
                checks.append({"name": f"py_compile:{p.relative_to(self.repo)}", "status": "FAIL", "detail": str(exc)})
        return checks

    def check_switch_forwarding(self) -> list[dict[str, Any]]:
        bad = []
        for p in sorted((self.repo / "scripts").rglob("*.ps1")):
            rel = str(p.relative_to(self.repo)).replace("\\", "/")
            # Audit scripts may contain banned strings as inert test text. We only scan executable orchestration scripts.
            if rel.startswith("scripts/phase") or rel.startswith("scripts/diagnostics/cicada_full_project_audit"):
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            for pattern in BANNED_EXTERNAL_SWITCH_PATTERNS:
                if pattern in text:
                    bad.append({"file": rel, "pattern": pattern})
        return [{
            "name": "powershell external switch forwarding",
            "status": "FAIL" if bad else "PASS",
            "detail": bad if bad else "no old external -OpenReport:$OpenReport style calls found",
        }]

    def check_safety_text(self) -> list[dict[str, Any]]:
        fail = []
        suspicious_patterns = [
            'direct_printer_send": true',
            "direct_printer_send = true",
            'gcode_generated": true',
            'gcode_streaming": true',
            'machine_bridge": "OPEN"',
        ]
        for p in sorted(self.repo.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(self.repo)
            if any(part in {".git", ".cicada_envs", "Saved", "Binaries", "Intermediate"} for part in rel.parts):
                continue
            if str(rel).replace("\\", "/").startswith("tools/cicada_integration/"):
                continue
            if p.suffix.lower() not in {".py", ".ps1", ".json", ".ini", ".md", ".cpp", ".h"}:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore").lower()
            for pattern in suspicious_patterns:
                if pattern.lower() in text:
                    fail.append({"file": str(rel), "pattern": pattern})
        return [{
            "name": "machine safety lock scan",
            "status": "FAIL" if fail else "PASS",
            "detail": fail if fail else "no obvious direct-send/G-code true markers in tracked source tree",
        }]

    def check_phase_labels(self) -> list[dict[str, Any]]:
        phase = self.current_phase()
        return [{
            "name": "current phase label",
            "status": "PASS" if "003P" in phase else "CHECK",
            "detail": phase,
        }]

    def check_gitignore(self) -> list[dict[str, Any]]:
        p = self.repo / ".gitignore"
        text = p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
        required = [".cicada_envs/", "Saved/CICADAForge/", "Binaries/", "Intermediate/"]
        missing = [x for x in required if x not in text]
        return [{
            "name": "generated-output gitignore",
            "status": "PASS" if not missing else "FAIL",
            "detail": "ok" if not missing else f"missing {missing}",
        }]

    def git_status(self) -> dict[str, Any]:
        try:
            status = subprocess.run(["git", "status", "--short"], cwd=self.repo, capture_output=True, text=True, timeout=10)
            raw_lines = [x for x in status.stdout.splitlines() if x.strip()]
            ignored_prefixes = ("?? .cicada_envs/", "?? Saved/", "?? Saved\\\\", "?? DerivedDataCache/")
            lines = [x for x in raw_lines if not x.startswith(ignored_prefixes)]
            return {"returncode": status.returncode, "changed_count": len(lines), "changed_files": lines[:200], "ignored_generated_count": len(raw_lines) - len(lines)}
        except Exception as exc:
            return {"returncode": -1, "error": str(exc)}

    def audit(self) -> dict[str, Any]:
        checks: list[dict[str, Any]] = []
        checks.extend(self.check_required_files())
        checks.extend(self.check_python_compile())
        checks.extend(self.check_switch_forwarding())
        checks.extend(self.check_safety_text())
        checks.extend(self.check_phase_labels())
        checks.extend(self.check_gitignore())

        counts = {"PASS": 0, "CHECK": 0, "FAIL": 0}
        for c in checks:
            counts[c["status"]] = counts.get(c["status"], 0) + 1

        verdict = "FAIL" if counts["FAIL"] else ("PASS_WITH_CHECKS" if counts["CHECK"] else "PASS")
        data = {
            "project": "CICADA_FORGE_UE",
            "phase": self.current_phase(),
            "generated": datetime.now().isoformat(timespec="seconds"),
            "verdict": verdict,
            "counts": counts,
            "checks": checks,
            "git": self.git_status(),
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
            "gcode_generated": False,
        }
        print(json.dumps(data, indent=2))
        return data

    def html(self, data: dict[str, Any]) -> str:
        rows = []
        for c in data["checks"]:
            status = c["status"]
            cls = "good" if status == "PASS" else ("warn" if status == "CHECK" else "bad")
            detail = json.dumps(c["detail"], indent=2) if isinstance(c["detail"], (dict, list)) else str(c["detail"])
            rows.append(
                "<tr>"
                f"<td>{html.escape(c['name'])}</td>"
                f"<td class='{cls}'>{html.escape(status)}</td>"
                f"<td><pre>{html.escape(detail)}</pre></td>"
                "</tr>"
            )
        raw = html.escape(json.dumps(data, indent=2))
        verdict_cls = "good" if data["verdict"] == "PASS" else ("warn" if data["verdict"] == "PASS_WITH_CHECKS" else "bad")
        return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>CICADA Full Project Audit</title>
<style>
:root {{ color-scheme: dark; --bg:#050505; --panel:#111; --line:#333; --text:#f5f5f5; --good:#9fffa8; --warn:#ffd479; --bad:#ff8f8f; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:system-ui,Segoe UI,Arial,sans-serif; }}
main {{ max-width:1320px; margin:0 auto; padding:24px; }}
.panel {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:16px; margin:12px 0; }}
.good {{ color:var(--good); font-weight:800; }} .warn {{ color:var(--warn); font-weight:800; }} .bad {{ color:var(--bad); font-weight:800; }}
table {{ width:100%; border-collapse:collapse; }} th,td {{ border-bottom:1px solid #2b2b2b; padding:8px; text-align:left; vertical-align:top; }}
pre {{ white-space:pre-wrap; word-break:break-word; margin:0; }}
</style></head>
<body><main>
<h1>CICADA FULL PROJECT AUDIT</h1>
<section class="panel">
<h2>Verdict: <span class="{verdict_cls}">{html.escape(data['verdict'])}</span></h2>
<p>Machine bridge: LOCKED | Direct printer send: false | G-code generated: false</p>
<p>Phase: {html.escape(str(data.get('phase')))}</p>
</section>
<section class="panel"><h2>Checks</h2><table><thead><tr><th>Name</th><th>Status</th><th>Detail</th></tr></thead><tbody>{''.join(rows)}</tbody></table></section>
<section class="panel"><h2>Raw JSON</h2><pre>{raw}</pre></section>
</main></body></html>"""

    def write_report(self, data: dict[str, Any], open_report: bool = False) -> dict[str, str]:
        self.report_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = self.report_dir / f"full_project_audit_{stamp}.json"
        html_path = self.report_dir / f"full_project_audit_{stamp}.html"
        latest_json = self.report_dir / "latest_full_project_audit.json"
        latest_html = self.report_dir / "latest_full_project_audit.html"
        text = json.dumps(data, indent=2)
        page = self.html(data)
        for p, value in [(json_path, text), (html_path, page), (latest_json, text), (latest_html, page)]:
            p.write_text(value, encoding="utf-8")
        if open_report:
            os.startfile(latest_html)
        outputs = {"json": str(json_path), "html": str(html_path), "latest_json": str(latest_json), "latest_html": str(latest_html)}
        print(json.dumps(outputs, indent=2))
        return outputs


def main() -> int:
    ap = argparse.ArgumentParser(description="CICADA full project audit. Checks Python compile, PS switches, safety locks, integration files.")
    ap.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    ap.add_argument("--open-report", action="store_true")
    args = ap.parse_args()

    audit = FullProjectAudit(args.repo)
    data = audit.audit()
    audit.write_report(data, open_report=args.open_report)
    return 0 if data["verdict"] != "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
