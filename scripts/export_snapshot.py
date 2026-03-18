from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from project.monitoring.service import build_demo_snapshot


def main() -> None:
    snapshot = build_demo_snapshot()
    output_path = ROOT / "artifacts" / "monitoring_snapshot.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(asdict(snapshot), indent=2), encoding="utf-8")
    print(f"Wrote monitoring snapshot to {output_path}")


if __name__ == "__main__":
    main()
