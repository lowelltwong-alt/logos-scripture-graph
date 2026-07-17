"""Build a self-contained, offline human review workbench."""

from __future__ import annotations

import base64
import json
from pathlib import Path

from .contracts import ContractError, load_json, verify_run_artifacts


def build_review(run_dir: Path, output: Path, *, confidential_mode: bool = False) -> Path:
    run = load_json(run_dir / "run.json")
    verify_run_artifacts(run_dir, run)
    sources = [p for p in run_dir.glob("source.*") if p.is_file()]
    if len(sources) != 1 or sources[0].suffix.lower() not in {".png", ".jpg", ".jpeg", ".svg"}:
        raise ContractError("run directory requires exactly one supported page image")
    source = sources[0]
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}[source.suffix.lower()]
    payload = {"run": run, "imageUri": f"data:{mime};base64,{base64.b64encode(source.read_bytes()).decode()}",
               "confidentialMode": confidential_mode}
    encoded = base64.b64encode(json.dumps(payload, ensure_ascii=False).encode()).decode()
    template = (Path(__file__).parent / "web" / "review.html").read_text(encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template.replace("__REVIEW_PAYLOAD_B64__", encoded), encoding="utf-8", newline="\n")
    return output
