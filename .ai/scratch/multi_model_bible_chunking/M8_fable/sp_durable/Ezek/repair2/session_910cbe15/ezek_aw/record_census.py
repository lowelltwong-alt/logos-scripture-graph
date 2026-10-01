#!/usr/bin/env python3
"""Land the OW-15 position and record the two receipt defects it exposed."""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
SP = EZ.parent
HERE = Path(__file__).resolve().parent
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

src = HERE / "ezek_ow15_position.v1.json"
dst = SP / "campaign" / "ezek_ow15_position.v1.json"
if dst.is_file() and sha(dst) != sha(src):
    raise SystemExit("REFUSED: exists with different bytes")
shutil.copy2(src, dst)
pos = json.loads(dst.read_text(encoding="utf-8"))

entry = {
    "id": "E13-64",
    "severity": "MEDIUM",
    "headline": "THE CENSUS IS A LOWER BOUND, NOT AN EQUALITY: nine attempt receipts carry no token figure and "
                "a summing census asserts they cost zero. Four of the nine are receipts I wrote this session.",
    "raised_by": "orchestrator (claude-opus-5), while checking the OW-15 position before launching the author "
                 "wave",
    "defect_1_absent_token_figures": {
        "what": ("9 of 143 attempt receipts have no tokens_reported. A census that sums the field and skips "
                 "what is missing returns 38,678,610 and presents it as THE census, which asserts that nine "
                 "attempts - four of them substantial Fable runs (the boss audit and the e12/e13/e14 rulings) "
                 "- cost nothing."),
        "why_it_matters": ("OW-18: implication is assertion. An absent field in a summed column asserts zero, "
                           "and the OW-15 headroom of 16,321,390 was being reported as a fact when it is an "
                           "UPPER bound."),
        "fix": ("the four receipts I authored now carry tokens_reported as an explicit UNAVAILABLE VALUE with "
                "its reason, written as a STRING so a naive summing script FAILS LOUD instead of skipping it "
                "silently - the campaign's own rule is that guards fail loud. A new census tool reports the "
                "census as a LOWER BOUND and the headroom as an UPPER BOUND, and lists every attempt whose "
                "cost is unknown."),
        "not_fixed_and_why": ("the five older receipts (2 phase0, 3 top-level rulings) were written by earlier "
                              "lanes I did not author; their bytes are left alone and the census reports them "
                              "as UNKNOWN, which is the same honesty without mutating another session's "
                              "records."),
        "standing_fix_for_future_landings": ("every landing script must record tokens_reported, or UNAVAILABLE "
                                             "with a reason. Mine did neither."),
    },
    "defect_2_wrong_attempt_id": {
        "what": ("reviews/ezek_rulings_attempt_receipts.jsonl carried three rows whose execution_ids were "
                 "correctly ezek_e12/e13/e14_ruling_a1#e1 while ALL THREE attempt_ids read "
                 "ezek_e12_ruling_a1."),
        "cause": "I built each landing script from the previous one and carried the hardcoded attempt_id "
                 "forward - the same copy-forward habit that produced ledger E-31.",
        "why_it_matters": "an attempt_id is provenance; any census or audit keyed on it would merge three "
                          "distinct controlling-agent attempts into one.",
        "fix": "the attempt_id is now DERIVED from the execution_id rather than retyped, because retyping is "
               "how the error happened. Preimages backed up beside the files.",
    },
    "two_of_my_own_measurement_failures_on_the_way": [
        ("my first census used a HARDCODED list of receipt files and returned 23,895,678 - it missed five "
         "lanes (author, writer, fixup1-3). The pinned budget tool's own note says it discovers files by "
         "recursive glob precisely 'because a hardcoded list would undercount'. I undercounted by 14.8M, and "
         "what made me look was that my figure was LOWER than the recorded census, which is impossible."),
        ("I then guessed the field name - total_tokens, tokens, usage - and got zero from every file, before "
         "reading the attachment that names it: tokens_reported. Both failures were the same mistake: "
         "inventing a shape instead of reading the one the pinned artifact declares."),
    ],
    "position": {"census_lower_bound": pos["census"]["LOWER_BOUND"],
                 "ceiling": pos["ceiling"]["value"],
                 "headroom_upper_bound": pos["headroom"]["UPPER_BOUND"],
                 "attempts_counted": pos["census"]["attempts_counted"],
                 "attempts_unknown": pos["census"]["attempts_with_no_figure"],
                 "carrier_sha256": pos["ceiling"]["carrier_sha256"],
                 "artifact": "campaign/ezek_ow15_position.v1.json", "artifact_sha256": sha(dst)},
    "launch_decision": pos["consequence_for_the_author_wave_launch"],
    "blocks_author_wave": False, "status": "DONE", "tier": "MEASURED for every figure present; the nine "
                                                           "unmeasured attempts are UNAVAILABLE",
    "opened_at": datetime.now(timezone.utc).isoformat(),
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
print(json.dumps({"appended": "E13-64", "landed": str(dst.relative_to(SP)), "sha256": sha(dst),
                  "queue_rows": len(Q.read_text(encoding="utf-8").strip().splitlines())}, indent=1))
