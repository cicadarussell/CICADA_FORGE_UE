from __future__ import annotations

import argparse, html, json, os, subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_REPO = Path(os.environ.get("CICADA_FORGE_REPO", r"C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"))

class Ledger:
    def __init__(self, repo: Path = DEFAULT_REPO):
        self.repo = repo
        self.saved = repo / "Saved" / "CICADAForge"
        self.dir = self.saved / "Ledger"
        self.release_dir = self.saved / "ReleaseGates"
        self.jsonl = self.dir / "run_ledger.jsonl"
        self.latest_json = self.dir / "latest_state.json"
        self.latest_html = self.dir / "latest_state.html"

    def now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def git(self) -> dict[str, Any]:
        try:
            branch = subprocess.run(["git", "branch", "--show-current"], cwd=self.repo, capture_output=True, text=True, timeout=10)
            head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=self.repo, capture_output=True, text=True, timeout=10)
            status = subprocess.run(["git", "status", "--short"], cwd=self.repo, capture_output=True, text=True, timeout=10)
            raw_lines = [x for x in status.stdout.splitlines() if x.strip()]
            ignored_prefixes = ("?? .cicada_envs/", "?? Saved/", "?? Saved\\", "?? DerivedDataCache/")
            lines = [x for x in raw_lines if not x.startswith(ignored_prefixes)]
            return {"branch": branch.stdout.strip(), "head": head.stdout.strip(), "changed_count": len(lines), "changed_files": lines[:120], "ignored_generated_count": len(raw_lines) - len(lines)}
        except Exception as exc:
            return {"branch": None, "head": None, "changed_count": None, "error": str(exc)}

    def latest_file(self, folder: str, pattern: str) -> Path | None:
        d = self.saved / folder
        if not d.exists():
            return None
        files = sorted([p for p in d.glob(pattern) if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)
        return files[0] if files else None

    def read_json(self, p: Path | None) -> dict[str, Any] | None:
        if not p or not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            return {"_error": str(exc), "_path": str(p)}

    def artifacts(self) -> dict[str, Any]:
        specs = {
            "health": ("HealthReports", "latest_health_report.json"),
            "command_center": ("CommandCenter", "command_center.json"),
            "dashboard": ("Dashboard", "cicada_dashboard_snapshot.json"),
            "cad_report": ("CADReports", "*.cad_report.json"),
            "env_report": ("EnvReports", "*.json"),
            "slicer_report": ("SlicerReports", "*.json"),
            "stl": ("STL", "*.stl"),
            "print_manifest": ("PrintHandoff", "*.json"),
            "release_gate": ("ReleaseGates", "*.json"),
            "integration_report": ("IntegrationReports", "*.json"),
        }
        out = {}
        for k, (folder, pattern) in specs.items():
            p = (self.saved / folder / pattern) if "*" not in pattern else self.latest_file(folder, pattern)
            if p and "*" not in pattern and not p.exists():
                p = None
            out[k] = {"exists": bool(p and p.exists()), "path": str(p) if p else None, "name": p.name if p else None}
        return out

    def phase(self) -> str:
        cfg = self.repo / "Config" / "CICADAForgeState.ini"
        if not cfg.exists():
            return "unknown"
        for line in cfg.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("CurrentPhase="):
                return line.split("=", 1)[1].strip()
        return "unknown"

    def html_page(self, title: str, data: dict[str, Any]) -> str:
        raw = html.escape(json.dumps(data, indent=2))
        return f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>body{{background:#050505;color:#f5f5f5;font-family:system-ui,Segoe UI,Arial;padding:24px}}pre{{white-space:pre-wrap;background:#111;border:1px solid #333;border-radius:12px;padding:14px}}.warn{{color:#ffd479}}.good{{color:#9fffa8}}.bad{{color:#ff8f8f}}</style></head>
<body><h1>{html.escape(title)}</h1><p>Machine bridge: <b class="warn">LOCKED</b> | Direct printer send: false | G-code generated: false</p><pre>{raw}</pre></body></html>"""

    def record(self, phase: str, verdict: str, note: str, source: str) -> dict[str, Any]:
        self.dir.mkdir(parents=True, exist_ok=True)
        data = {
            "timestamp": self.now(),
            "project": "CICADA_FORGE_UE",
            "phase": phase,
            "configured_phase": self.phase(),
            "verdict": verdict,
            "note": note,
            "source": source,
            "git": self.git(),
            "artifacts": self.artifacts(),
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
            "gcode_generated": False,
        }
        with self.jsonl.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data, sort_keys=True) + "\n")
        self.latest_json.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.latest_html.write_text(self.html_page("CICADA Latest Ledger State", data), encoding="utf-8")
        print(json.dumps(data, indent=2))
        return data

    def latest(self) -> dict[str, Any]:
        if self.latest_json.exists():
            data = json.loads(self.latest_json.read_text(encoding="utf-8"))
        else:
            data = {"project": "CICADA_FORGE_UE", "phase": "none", "verdict": "NOT_RUN", "note": "No ledger entries yet.", "timestamp": self.now(), "direct_printer_send": False, "machine_bridge": "LOCKED"}
        print(json.dumps(data, indent=2))
        return data

    def release_gate(self, strict: bool, open_report: bool) -> dict[str, Any]:
        self.release_dir.mkdir(parents=True, exist_ok=True)
        artifacts = self.artifacts()
        checks = []

        required = [
            ("master wrapper", "scripts/cicada_forge.ps1"),
            ("health tool", "tools/cicada_health/cicada_health_report.py"),
            ("ledger tool", "tools/cicada_ledger/cicada_run_ledger.py"),
            ("command center", "tools/cicada_launcher/cicada_command_center.py"),
            ("CAD sidecar", "tools/cicada_cad_sidecar/cicada_cad_sidecar.py"),
            ("slicer planner", "tools/cicada_slicer/cicada_slicer_dryrun_planner.py"),
        ]
        for name, rel in required:
            p = self.repo / rel
            checks.append({"name": name, "status": "PASS" if p.exists() else "FAIL", "detail": str(p)})

        for key in ["health", "command_center", "dashboard", "cad_report", "env_report", "slicer_report", "integration_report"]:
            exists = artifacts[key]["exists"]
            checks.append({"name": f"artifact:{key}", "status": "PASS" if exists else ("FAIL" if strict else "NOT_RUN"), "detail": artifacts[key]["path"]})

        manifest = self.read_json(Path(artifacts["print_manifest"]["path"])) if artifacts["print_manifest"]["path"] else None
        if manifest:
            safe = manifest.get("direct_printer_send") is False and str(manifest.get("machine_bridge", "")).upper() == "LOCKED" and manifest.get("gcode_streaming") in (False, None)
            checks.append({"name": "manifest safety", "status": "PASS" if safe else "FAIL", "detail": artifacts["print_manifest"]["path"]})
        else:
            checks.append({"name": "manifest safety", "status": "NOT_RUN", "detail": "No manifest generated yet."})

        counts = {s: sum(1 for c in checks if c["status"] == s) for s in ["PASS", "NOT_RUN", "CHECK", "FAIL"]}
        verdict = "BLOCKED" if counts["FAIL"] else ("RC_PARTIAL" if counts["NOT_RUN"] or counts["CHECK"] else "RC_READY")
        gate = {
            "project": "CICADA_FORGE_UE",
            "phase": self.phase(),
            "timestamp": self.now(),
            "strict": strict,
            "verdict": verdict,
            "counts": counts,
            "checks": checks,
            "git": self.git(),
            "artifacts": artifacts,
            "direct_printer_send": False,
            "machine_bridge": "LOCKED",
            "gcode_generated": False,
            "note": "RC_PARTIAL is acceptable when artifacts have not been generated. BLOCKED means actual failure/safety issue.",
        }

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = self.release_dir / f"release_gate_{stamp}.json"
        html_path = self.release_dir / f"release_gate_{stamp}.html"
        latest_json = self.release_dir / "latest_release_gate.json"
        latest_html = self.release_dir / "latest_release_gate.html"
        text = json.dumps(gate, indent=2)
        page = self.html_page("CICADA Release Candidate Gate", gate)
        json_path.write_text(text, encoding="utf-8")
        html_path.write_text(page, encoding="utf-8")
        latest_json.write_text(text, encoding="utf-8")
        latest_html.write_text(page, encoding="utf-8")
        if open_report:
            os.startfile(latest_html)
        print(json.dumps({**gate, "outputs": {"json": str(json_path), "html": str(html_path), "latest_json": str(latest_json), "latest_html": str(latest_html)}}, indent=2))
        return gate

def main() -> int:
    ap = argparse.ArgumentParser(description="CICADA run ledger and release candidate gate.")
    ap.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    sub = ap.add_subparsers(dest="command", required=True)

    rec = sub.add_parser("record")
    rec.add_argument("--phase", default="003O")
    rec.add_argument("--verdict", default="RECORDED")
    rec.add_argument("--note", default="Manual run recorded.")
    rec.add_argument("--source", default="manual")

    sub.add_parser("latest")
    gate = sub.add_parser("release-gate")
    gate.add_argument("--strict", action="store_true")
    gate.add_argument("--open-report", action="store_true")
    args = ap.parse_args()

    ledger = Ledger(args.repo)
    if args.command == "record":
        ledger.record(args.phase, args.verdict, args.note, args.source)
        return 0
    if args.command == "latest":
        ledger.latest()
        return 0
    if args.command == "release-gate":
        result = ledger.release_gate(strict=args.strict, open_report=args.open_report)
        return 0 if result["verdict"] != "BLOCKED" else 2
    raise AssertionError("unhandled")

if __name__ == "__main__":
    raise SystemExit(main())
