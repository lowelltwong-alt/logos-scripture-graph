#!/usr/bin/env python3
"""Record a held, candidate-only Numbers role packet through the r8 controller."""
from __future__ import annotations
import json
from pathlib import Path
from scripts.build_whole_bible_b01_controller_r8 import ControllerRun, prepare

ROOT = Path(__file__).resolve().parents[1]
RUN_ROOT = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/Num/num-r8-20260722b"
MATRIX = ROOT / "docs/governance/NUMBERS_B01_ROLE_INPUT_MATRIX.v1.json"

def main() -> int:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    paths = [ROOT / row["path"] for row in matrix["inputs"]]
    run = prepare(root=RUN_ROOT, book="Num", run_id="num-r8-20260722b", attempt_id="b01-controller-1", source_paths=paths)
    reports = {
      "original_language_translation_scout": ("agent-num-ol-r8", ["OSHB/UXLC lineage is correlated and requires explicit WEB/MT crosswalk before any source attachment.", "Translation pressures are evidence for preserving context, not boundary authority."]),
      "literary_form_scout": ("agent-num-lit-r8", ["Numbers alternates registers, law, narrative, itinerary, embedded song, and oracle cycles.", "The 18 reviewed form zones are candidate parent frames; chapter boundaries are insufficient by themselves."]),
      "canonical_relations_and_premortem_scout": ("agent-num-can-r8", ["Internal relation candidates include wilderness retellings, oracle callbacks, and refuge-law parallels.", "Cross-references and later uses must remain context candidates and cannot authorize local boundaries."]),
      "second_temple_rabbinic_context_scout": ("agent-num-ancient-r8", ["No qualified ancient Jewish, Second Temple, or rabbinic corpus is pinned for this run.", "Ancient-context observations therefore remain an explicit gap and no simulated expertise is asserted."]),
    }
    for role, (agent, observations) in reports.items():
        assignment = run.assign(role)
        run.record_result(assignment, agent_instance_id=agent, report={
            "observations": [{"observation_id": f"{role}-obs-{i+1}", "scope": "Num", "claim": claim, "evidence_refs": ["NUMBERS_B01_ROLE_INPUT_MATRIX.v1", "form_inventory.json", "source_gap_register.json"], "confidence": "low"} for i, claim in enumerate(observations)],
            "uncertainties": ["four-role packet is one correlated Codex substrate", "B01 remains receipt-only and no boundary is promoted"],
            "source_refs": ["docs/governance/NUMBERS_B01_ROLE_INPUT_MATRIX.v1.json", ".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Num/form_inventory.json", ".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Num/source_gap_register.json"]
        })
    print(run.packet_dir)
    return 0
if __name__ == "__main__": raise SystemExit(main())

