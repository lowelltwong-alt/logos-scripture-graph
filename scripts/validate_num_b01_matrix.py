#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_numbers_b01_role_input_matrix import ROOT, build

ROLES = {"original_language_translation_scout", "literary_form_scout", "canonical_relations_and_premortem_scout", "second_temple_rabbinic_context_scout"}

def validate(path: Path) -> None:
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != build(): raise ValueError("matrix differs from current governed-input digests or role closure")
    if actual["book"] != "Num" or actual["candidate_only"] is not True or actual["non_authorizing"] is not True: raise ValueError("identity flags")
    if actual["contains_scripture_text"] or actual["contains_source_rows"] or actual["boundary_authority"] != "none": raise ValueError("authority/text leakage")
    rows = actual["inputs"]
    if len({r["artifact_id"] for r in rows}) != len(rows) or len({r["path"] for r in rows}) != len(rows): raise ValueError("duplicate artifact/path")
    if {r["role_id"] for r in actual["roles"]} != ROLES: raise ValueError("exact four roles required")
    for row in actual["hard_passage_forecast"]:
        if row.get("candidate_boundary") is not False or not re.fullmatch(r"Num\.\d+(?:\.\d+)?(?:-Num\.\d+(?:\.\d+)?)?", row["ref_scope"]): raise ValueError("reference-only forecast required")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--matrix", type=Path, default=ROOT / "docs/governance/NUMBERS_B01_ROLE_INPUT_MATRIX.v1.json"); args = ap.parse_args(); validate(args.matrix); print(f"Numbers B01 matrix valid: {args.matrix}")
