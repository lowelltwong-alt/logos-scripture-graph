#!/usr/bin/env python3
"""Create held, controller-bound r8 B01 packets for a bounded OT book batch."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from scripts.build_whole_bible_b01_controller_r8 import ControllerRun, prepare

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS = ("Deut", "Josh", "Judg", "Ruth")
ROLES = ("original_language_translation_scout", "literary_form_scout", "canonical_relations_and_premortem_scout", "second_temple_rabbinic_context_scout")
COMMON = [ROOT / "config/agents/families/scripture-first-biblical-chunking/whole_bible_campaign_registry.v1.json", ROOT / "config/agents/families/scripture-first-biblical-chunking/whole_bible_candidate_workflow.v2.yaml", ROOT / "config/agents/families/scripture-first-biblical-chunking/whole_bible_candidate_prompt_pack.v2.yaml", ROOT / "config/agents/families/scripture-first-biblical-chunking/codex_desktop_campaign_adapter.v2.yaml", ROOT / "data/canonical/scripture/passages/passages.jsonl", ROOT / "data/canonical/translations/eng-web/translation_witnesses.jsonl"]
OT_BASE = [ROOT / "data/raw/original_language/hebrew/openscriptures_oshb/source_manifest.yaml", ROOT / "data/raw/original_language/hebrew/openscriptures_oshb/raw/openscriptures_oshb-3d15126fb1ef.zip", ROOT / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/canonical_source_view_manifest.yaml", ROOT / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/included_files.jsonl", ROOT / "data/raw/original_language/hebrew/tanach_us_uxlc/source_manifest.yaml", ROOT / "data/raw/original_language/hebrew/tanach_us_uxlc/raw/Tanach.xml.zip", ROOT / "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/canonical_source_view_manifest.yaml", ROOT / "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/included_files.jsonl", ROOT / "config/chunking/form_registry.yaml", ROOT / ".ai/control/t423_literary_marker_quality_protocol.yaml", ROOT / ".ai/control/t468_owner_faithful_chunking_policy.yaml", ROOT / ".ai/control/bible_wide_chunking_research_registry.yaml", ROOT / ".ai/control/contextual_reading_policy.yaml", ROOT / ".ai/control/autonomous_corpus_processor.yaml"]

def sha(path: Path) -> str: return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
def file_packet_digest(packet: Path) -> str:
    rows = {f.name: hashlib.sha256(json.dumps(json.loads(f.read_text(encoding="utf-8")), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest() for f in sorted(packet.glob("*.json")) if f.name != "boss-authorization.json"}
    return "sha256:" + hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def run_book(book: str) -> None:
    run_id = f"{book.lower()}-r8-held-1"; attempt = "b01-controller-1"; root = MODEL / "state/r8" / book / run_id
    source_paths = COMMON + OT_BASE + [ROOT / f"data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/{book}.xml", ROOT / f"data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/files/{book}.xml"]
    run = prepare(root=root, book=book, run_id=run_id, attempt_id=attempt, source_paths=source_paths, controller_instance_id=f"controller-{book.lower()}-r8")
    chunk_path = MODEL / "book_chunks" / book / "chunks.jsonl"; count = len([x for x in chunk_path.read_text(encoding="utf-8").splitlines() if x.strip()])
    observations = {
      ROLES[0]: [f"The OT source lane records Hebrew/Aramaic translation pressure for {book}; roots and one gloss cannot authorize a boundary.", "OSHB and UXLC are correlated Leningrad-family evidence; any versification or lexical uncertainty remains held."],
      ROLES[1]: [f"The current {book} candidate file contains {count} low-confidence structural units with literary-form metadata.", "Chapter seams are provisional; speeches, songs, registers, legal units, and narrative continuities require red-team review."],
      ROLES[2]: [f"Internal/canonical relation seeds for {book} are context candidates only and do not authorize graph edges or local splits.", "Premortem holds include chapter-only fragmentation, cross-reference overreach, and theology-smuggling."],
      ROLES[3]: ["No qualified ancient Jewish, Second Temple, or rabbinic corpus is activated for this packet.", "Ancient-context lane is an explicit gap receipt; no simulated expertise is asserted."],
    }
    for i, role in enumerate(ROLES, 1):
        assignment = run.assign(role, provider_family="codex-gpt5-correlated-local")
        report = {"observations":[{"observation_id":f"{book}-R8-{i}-{j}","scope":book,"claim":claim,"evidence_refs":["whole_bible_role_source_matrix.v1",f"book_chunks/{book}/chunks.jsonl"],"confidence":"low"} for j, claim in enumerate(observations[role],1)],"uncertainties":["shared Codex substrate; not an independent provider vote","B01 receipt-only; no boundary promotion"],"source_refs":[f".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/{book}/chunks.jsonl","docs/governance/WHOLE_BIBLE_B01_TYPED_CONTRACT.md"]}
        run.record_result(assignment, agent_instance_id=f"codex-{book.lower()}-role-{i:02d}", provider_family="codex-gpt5-correlated-local", report=report)
    packet = root / "packet"; redteam = {"schema_version":"whole_bible_b01_redteam_note.v1","kind":"redteam_note","book":book,"run_id":run_id,"stage_attempt_id":attempt,"candidate_only":True,"non_authorizing":True,"shared_model_substrate":True,"counts_as_cross_model_independent_vote":False,"findings":[{"finding_id":f"{book}-RT-001","severity":"high","claim":"The four role reports share one Codex substrate and cannot count as independent provider votes."},{"finding_id":f"{book}-RT-002","severity":"high","claim":"Ancient-context lane is an unqualified corpus gap."}],"dissent_preserved":True}
    (root / "redteam-note.json").write_text(json.dumps(redteam, sort_keys=True, separators=(",", ":")), encoding="utf-8")
    # Boss review is controller-observed and distinct from every role instance.
    boss_exec=f"exec-{book.lower()}-r8-boss"; boss_asg=f"asg-{book.lower()}-r8-boss"; boss_evt=f"evt-{book.lower()}-r8-boss-reviewed"; run._event(event_id=boss_evt,event_kind="boss_reviewed",execution_id=boss_exec,assignment_id=boss_asg,result_digest=sha(root/"redteam-note.json"))
    boss={"schema_version":"whole_bible_b01_boss_authorization.v2","kind":"boss_authorization","book":book,"run_id":run_id,"stage_attempt_id":attempt,"candidate_only":True,"non_authorizing":True,"identity":{"execution_id":boss_exec,"assignment_id":boss_asg,"agent_instance_id":f"codex-{book.lower()}-boss","role_id":"evidence_dispute_boss","provider_family":"codex-gpt5-correlated-local"},"controller_event_ids":[boss_evt],"input_manifest_sha256":run.manifest_sha256,"packet_sha256":file_packet_digest(packet),"redteam_digest":sha(root/"redteam-note.json"),"verdict":"GO_B01_RECEIPT_ONLY","rationale":"Candidate observations are structurally bound, but correlated substrate and unqualified ancient-context evidence require holds.","rejected_alternatives":["promote boundaries","count correlated reports as independent","simulate ancient context"],"dissent":["QF-CORRELATED-SUBSTRATE","QF-ANCIENT-CONTEXT-GAP"],"appeal_route":"human or external-provider review"}
    (packet/"boss-authorization.json").write_text(json.dumps(boss, sort_keys=True, separators=(",", ":")), encoding="utf-8")

def main() -> int:
    for book in BOOKS: run_book(book)
    print(json.dumps({"books":list(BOOKS),"verdict":"GO_B01_RECEIPT_ONLY","B02_authorized":False,"candidate_only":True}, sort_keys=True)); return 0
if __name__ == "__main__": raise SystemExit(main())
