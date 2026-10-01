#!/usr/bin/env python3
"""O4's UNION: the re-run's in-window unmirrored citations UNITED with the peers' hand-named in-window verses.

WHAT MATTERS HERE IS THE RESIDUE, not the union's size. #e14 O4 says the peers' 47 are "largely already inside"
the member's citations. "Largely" is not a basis to install from, so this script measures the containment exactly
and names every peer verse that NO member citation covers. Those verses - if any - are the class the member
still cannot see, and they are the only part of the peers' work the union actually adds.

HOW THE PEERS' SET IS EXTRACTED, disclosed because the extraction is mine and not the ruling's. Each peer item
carries flags_answered entries of class A4_unmirrored_reference_convention, each with an argued_but_unmirrored
verse list and a ruling. A verse counts as HAND-NAMED IN-WINDOW when the peer did not rule it a false positive
AND it lies in the row's A4 window as the fixed member computes that window. The peers also name verses in free
text; those are collected separately and reported, never silently merged, because a verse mentioned in prose is
not the same evidence as a verse on a ruled flag.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
sys.path.insert(0, str(EZ / "tools"))
from check_refs_mirror import a4_window                                    # noqa: E402
from ezek_lib import expand_ref_token                                      # noqa: E402

HERE = Path(__file__).resolve().parent
RUN = json.loads((HERE / "refs_mirror_citation_run2.json").read_text(encoding="utf-8"))
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
rows = {r["decision_id"]: r for r in
        (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())
        if isinstance(r, dict) and "decision_id" in r}

VTOK = re.compile(r"Ezek\.(\d+)\.(\d+)")
windows = {}
for rid, r in rows.items():
    own = set(expand_ref_token(str(r.get("span", "")).replace("web:", "")))
    win, _ = a4_window(own)
    windows[rid] = (win, own)

# ---- the member's citations, and the set of verses any citation COVERS
member_cov = {}
for i in RUN["worklist_citations"]:
    member_cov.setdefault(i["decision_id"], set()).update(
        tuple(map(int, VTOK.match(v).groups())) for v in i["verses_web"])

# ---- the peers' hand-named in-window verses
peers = {}
on_ruled_flag, in_free_text, false_positive_only = {}, {}, {}
for n in range(1, 12):
    p = EZ / "reviews" / ("peer_%02d.json" % n)
    d = json.loads(p.read_text(encoding="utf-8"))
    # SHAPE, MEASURED: peer packets are NOT uniform - some carry items as a dict keyed by row_id and some as a
    # list of records with a row_id field. A reader that assumes one shape silently drops every peer using the
    # other, which is how a "0 findings" result gets manufactured.
    raw = d.get("items") or {}
    if isinstance(raw, dict):
        pairs = list(raw.items())
    else:
        pairs = [(str(x.get("row_id") or x.get("row") or "?"), x) for x in raw if isinstance(x, dict)]
    for rid, it in pairs:
        win, own = windows.get(rid, (set(), set()))
        for e in (it.get("flags_answered") or []):
            if not isinstance(e, dict):
                continue
            if "A4" not in str(e.get("class", "")) and "unmirrored" not in str(e.get("class", "")):
                continue
            ruling = str(e.get("ruling", "")).lower()
            verses = set()
            for v in (e.get("argued_but_unmirrored") or []):
                m = VTOK.match(str(v))
                if m:
                    verses.add((int(m.group(1)), int(m.group(2))))
            inwin = {v for v in verses if v in win}
            if not inwin:
                continue
            if "false_positive" in ruling:
                false_positive_only.setdefault(rid, set()).update(inwin)
            else:
                on_ruled_flag.setdefault(rid, set()).update(inwin)
        # free-text namings, kept separate on purpose
        blob = " ".join(str(v) for k, v in it.items() if isinstance(v, str))
        for m in VTOK.finditer(blob):
            v = (int(m.group(1)), int(m.group(2)))
            if v in win:
                in_free_text.setdefault(rid, set()).add(v)

peer_named = {rid: set(vs) for rid, vs in on_ruled_flag.items()}
peer_total = sum(len(v) for v in peer_named.values())

# ---- containment: which peer verses does NO member citation cover?
residue = {}
covered_n = 0
for rid, vs in peer_named.items():
    cov = member_cov.get(rid, set())
    miss = sorted(vs - cov)
    covered_n += len(vs) - len(miss)
    if miss:
        residue[rid] = ["Ezek.%d.%d" % v for v in miss]

ft_residue = {}
for rid, vs in in_free_text.items():
    cov = member_cov.get(rid, set()) | peer_named.get(rid, set())
    miss = sorted(vs - cov)
    if miss:
        ft_residue[rid] = ["Ezek.%d.%d" % v for v in miss]

out = {
    "schema": "ezek_o4_union.v1",
    "order": "#e14 O4: worklist basis for A4 = the re-run's in-window unmirrored CITATIONS united with the "
             "peers' hand-named in-window verses (the 47, largely already inside)",
    "member_side": {
        "worklist_citations": len(RUN["worklist_citations"]),
        "rows": RUN["counts"]["rows_with_any_worklist_citation"],
        "in_span_plus_mixed": RUN["counts"]["in_span_citations"] + RUN["counts"][
            "mixed_span_and_seam_citations"],
        "at_seam": RUN["counts"]["at_seam_single_citations"] + RUN["counts"]["seam_touching_range_citations"],
    },
    "peer_side": {
        "extraction": ("verses on peer flags_answered entries of the A4 class that the peer did NOT rule a "
                       "false positive, restricted to the row's A4 window as the fixed member computes it; "
                       "peer packets carry items as either a dict or a list and BOTH shapes are read"),
        "hand_named_in_window_verses": peer_total,
        "rows": len(peer_named),
        "the_rulings_figure": 47,
        "agreement": ("EXACT" if peer_total == 47 else
                      "my extraction yields %d against the ruling's 47 - the difference is disclosed and the "
                      "union is taken over the EXTRACTED set, which is the larger evidence base where it is "
                      "larger" % peer_total),
        "verses_the_peers_ruled_FALSE_POSITIVE_and_are_therefore_not_in_the_union":
            sum(len(v) for v in false_positive_only.values()),
    },
    "containment_MEASURED": {
        "peer_verses_covered_by_a_member_citation": covered_n,
        "peer_verses_NOT_covered_by_any_member_citation": sum(len(v) for v in residue.values()),
        "the_residue_by_row": residue,
        "what_the_residue_means": ("these are the verses the peers named that the member's rule does not reach "
                                   "even after the citation fix - the only part of the peers' A4 work the union "
                                   "genuinely adds. Each becomes its own worklist item attributed to the peer, "
                                   "so its provenance is the peer's reading and not a tool's output."),
    },
    "free_text_namings_kept_separate": {
        "why": ("a verse a peer mentions in prose is not the same evidence as a verse on a ruled flag, so these "
                "are reported and NOT merged into the union. They are handed to the author as context."),
        "rows_with_free_text_verses_outside_both_sets": len(ft_residue),
        "count": sum(len(v) for v in ft_residue.values()),
    },
    "inputs": {"rows_sha256": hashlib.sha256(ROWS.read_bytes()).hexdigest(),
               "member_sha256": hashlib.sha256((EZ / "tools" / "check_refs_mirror.py").read_bytes()).hexdigest()},
    "tier": "MEASURED; the peer-side extraction rule is the orchestrator's and is stated in full",
}
(HERE / "o4_union.v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                       encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("member_side", "peer_side", "containment_MEASURED",
                                      "free_text_namings_kept_separate")}, indent=1, ensure_ascii=False))
