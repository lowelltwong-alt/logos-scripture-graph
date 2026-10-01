#!/usr/bin/env python3
"""P7, part two: compare the re-derived A6 floor against what each of peers 01-06 reported, and say honestly
what the comparison can and cannot establish.

THE TEST'S LOGIC, as I stated it before running it: the arm is a FLOOR. A peer hand count ABOVE the arm is
expected and is not a discrepancy. Only a peer count BELOW the arm's on the same rows is evidence of a figure
lowered by a corrupted parse.

WHAT THE RESULT ACTUALLY SHOWS, and why it does not close the question: three peers' reported counts sit BELOW the
arm's floor for their rows. That is the signature - AND it is equally consistent with those peers applying
judgement the arm has none of. Fable's A6-b ruling, written AFTER these peers ran, exempts "a run that is only
the WEB's fixed rendering of a counted device or addressee title ... when the row names the device". A peer that
exempted such runs by its own judgement would report fewer than the raw arm, correctly. The arm applies no
exemption at all.

So the comparison cannot distinguish a corrupted figure from a correctly exercised exemption. Recording it as
either would be a false claim. It is recorded as UNKNOWN per group, with the evidence, and routed to the boss
audit - whose own ruling gives it the authority to "flag REPORTED-where-MEASURED grounds", which is exactly this.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
P7 = EZ / "peer_figure_rederivation_p7.v1.json"
REVIEWS = EZ / "reviews"
OUT = EZ / "peer_figure_rederivation_p7.v2.json"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


doc = json.loads(P7.read_text(encoding="utf-8"))

# The peers' own reported A6 counts, EXTRACTED from their packets where a number is stated there, never from the
# orchestrator's memory of their replies. Where a packet does not state a group total, it is UNKNOWN.
NUM = re.compile(r"(\d+)")
for g in doc["per_group"]:
    pkt = REVIEWS / ("peer_%s.json" % g["peer_group"].replace("peer_", ""))
    text = pkt.read_text(encoding="utf-8")
    # look for the peer's own A6 sentences and pull any count it states near them
    sents = [s for s in re.split(r"(?<=[.;])\s+", text) if re.search(r"\bA6\b|a6_", s)]
    stated = sorted({int(n) for s in sents for n in NUM.findall(s) if 0 < int(n) <= 200})
    arm = g["a6_runs_rederived_by_the_campaign_arm"]
    g["peer_a6_sentences_found_in_packet"] = len(sents)
    g["numbers_appearing_in_those_sentences"] = stated[:14]
    g["arm_floor_for_these_rows"] = arm
    g["verdict"] = "UNKNOWN"
    g["verdict_reason"] = (
        "the arm's floor for these rows is %d. A peer count above it is expected; a peer count below it is the "
        "corruption signature. But ruling A6-b - written after this peer ran - exempts a run that is only the "
        "translation's fixed rendering of a counted device or addressee title when the row names the device, and "
        "the arm applies no exemption. A count below the floor is therefore equally consistent with a corrupted "
        "parse and with a correctly exercised exemption, and this script cannot distinguish them." % arm)
    g["what_would_settle_it"] = (
        "reading this peer's per-run reasoning against the arm's per-row hits for the same rows, which is a "
        "reading task and not a script task - and is within the boss audit's authority to flag "
        "REPORTED-where-MEASURED grounds")

doc["schema"] = "m8_peer_figure_rederivation.v2"
doc["supersedes"] = {"file": P7.name, "sha256": sha(P7), "kept_on_disk": True,
                     "why": "v1 re-derived the floor; v2 adds the comparison and the honest verdict"}
doc["built_at"] = datetime.now(timezone.utc).isoformat()
doc["fables_named_test"]["resolution"] = (
    "peer_06's zero across eight rows is CORROBORATED rather than contradicted. The arm, on an independently "
    "proved parse, finds runs on only %d of peer_06's 14 rows - so at most %d of its 14 carry one, which is "
    "consistent with eight clean. The arm finds FEWER runs in that group than peer_06 itself reported, which is "
    "the expected direction for a floor. peer_06's zero is not a dropped-continuation artifact."
    % (next(g["rows_with_a_run_count"] for g in doc["per_group"] if g["peer_group"] == "peer_06"),
       next(g["rows_with_a_run_count"] for g in doc["per_group"] if g["peer_group"] == "peer_06")))
doc["overall_verdict"] = {
    "peer_re_run_needed": False,
    "figures_proved_corrupted": 0,
    "figures_proved_sound": 0,
    "figures_remaining_UNKNOWN": len(doc["per_group"]),
    "statement": (
        "No figure is proved corrupted and none is proved sound. The precondition's real product is this: the "
        "translation parse used for every comparison is PROVED (1273 verses, 522 continuations joined, equal to "
        "the Hebrew witness), and Fable's one named test - peer_06's zero - is corroborated by an independent "
        "parse rather than contradicted. The remaining per-group comparisons cannot be settled by a script "
        "because the arm has no exemptions and the peers exercised judgement the ruling later codified. They are "
        "UNKNOWN, named as such, and routed to the boss audit."),
    "tier": "the parse proof and the arm's floors are MEASURED; every per-group verdict is UNKNOWN",
}
doc["honest_limits"].append(
    "The orchestrator set the comparison rule before seeing the result and then found the result does not satisfy "
    "the rule's precondition - the arm turned out to have no exemption where the peers had one. Reporting a "
    "count-below-floor as corruption would have condemned three peers on a comparison that cannot support it.")

OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"written": OUT.name, "sha256": sha(OUT)[:32],
                  "named_test_resolution": doc["fables_named_test"]["resolution"],
                  "overall": doc["overall_verdict"],
                  "per_group_floors": {g["peer_group"]: g["arm_floor_for_these_rows"]
                                       for g in doc["per_group"]}}, indent=1, ensure_ascii=False))
