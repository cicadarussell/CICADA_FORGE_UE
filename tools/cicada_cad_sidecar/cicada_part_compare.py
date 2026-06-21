from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def feature_key(feature: dict[str, Any]) -> str:
    return f"{feature.get('type')}::{feature.get('id')}"


def compare(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    a_body = a["bodies"][0]
    b_body = b["bodies"][0]

    dims = {}
    for key in ["width", "depth", "height"]:
        dims[key] = {
            "a": a_body.get(key),
            "b": b_body.get(key),
            "delta": float(b_body.get(key, 0)) - float(a_body.get(key, 0)),
        }

    a_features = {feature_key(f): f for f in a.get("features", [])}
    b_features = {feature_key(f): f for f in b.get("features", [])}

    added = sorted(set(b_features) - set(a_features))
    removed = sorted(set(a_features) - set(b_features))
    common = sorted(set(a_features) & set(b_features))

    changed = []
    for key in common:
        if a_features[key] != b_features[key]:
            changed.append(key)

    return {
        "part_a": a.get("part_id"),
        "part_b": b.get("part_id"),
        "dimension_delta": dims,
        "feature_counts": {
            "a": len(a_features),
            "b": len(b_features),
            "delta": len(b_features) - len(a_features),
        },
        "features_added": added,
        "features_removed": removed,
        "features_changed": changed,
        "direct_printer_send": False,
        "machine_bridge": "LOCKED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two CICADA CAD part-intent JSON files.")
    parser.add_argument("part_a", type=Path)
    parser.add_argument("part_b", type=Path)
    args = parser.parse_args()

    result = compare(load(args.part_a), load(args.part_b))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
