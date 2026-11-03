#!/usr/bin/env python3
"""Transcribe the conditions of the 1 Corinthians boss audit from the controlling rulings; nothing is reworded.

1 Corinthians' rulings name no `gate.boss_conditions`, as Daniel's E9-E12 did. Its standing conditions are the
`gate.s2_conditions` that E4 and E5 word. PICKS names each one taken, in ruling order; the rest are left out for a stated
reason: E1-E3 word the same subjects and E4 or E5 re-word them, and a pick's slot number is its place in the ruling's
list. The picks are the orchestrator's selection, recorded as such; the text is TRANSCRIBED.

usage: boss_1cor.py [--check]     --check rebuilds in memory and prints MATCH or DIFFERS
"""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
OUT = HERE / "boss_conditions_effective.v2.json"  # v1 was built before E6 landed and is kept, never reused
# (ruling, 1-based slot). E4 slots 2-4 are re-worded by E5 slots 4 and 6. E5 slot 8 and E4 slots 1 and 13 bind a lane's
# form and the launch cap, E5 slot 1 is that lane's scope; none is a statement about the rows.
PICKS = (("E4", 5), ("E4", 6), ("E4", 7), ("E4", 8), ("E4", 9), ("E4", 10), ("E4", 11), ("E4", 12),
         ("E5", 2), ("E5", 3), ("E5", 4), ("E5", 5), ("E5", 6), ("E5", 7),
         ("E6", 1), ("E6", 2), ("E6", 4))
LEFT_OUT = {
    "E1-E3": "same subjects, re-worded by E4 or E5",
    "E4 slots 2-4": "re-worded by E5 slots 4 and 6",
    "E4 slots 1, 13; E5 slots 1, 8": "bind a checking lane's form or the launch cap, not the rows",
    "E6 slots 3, 5, 6": "bind how S6's record is read, what later lanes do, and how a later clause is worded, not the rows",
}
READ_WITH = {("E5", 4): "E6 slot 2 and ruling R6-S6-01 construe this condition's second clause; the construction is the controlling agent's, INFERRED, and routed to the end review."}


def build():
    files, conds = {}, []
    for e, slot in PICKS:
        name = "1cor_controlling_agent_rulings_%s.v1.json" % e
        raw = (REVIEW / name).read_bytes()
        files[e] = {"ruling": e, "path": "sp_durable/1Cor/review/" + name, "sha256": hashlib.sha256(raw).hexdigest()}
        text = json.loads(raw.decode("utf-8"))["gate"]["s2_conditions"][slot - 1]
        conds.append({"id": "B%d" % (len(conds) + 1), "text": text, "source": e, "slot": slot})
        if (e, slot) in READ_WITH:
            conds[-1]["read_with"] = READ_WITH[(e, slot)]
    d = {"schema": "1cor_boss_conditions_effective.v2", "book": "1Cor",
         "what": "the standing conditions of the rulings, each as the latest ruling that words it leaves it",
         "tier": "TRANSCRIBED by boss_1cor.py from the ruling files; nothing reworded. The selection is the orchestrator's",
         "left_out": LEFT_OUT, "ruling_files": list(files.values()), "conditions": conds}
    return (json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8"), d


def main():
    data, d = build()
    if "--check" in sys.argv:
        same = OUT.is_file() and OUT.read_bytes() == data
        print("MATCH" if same else "DIFFERS")
        sys.exit(0 if same else 1)
    if OUT.exists() and OUT.read_bytes() != data:
        raise SystemExit("REFUSED: %s exists with different bytes" % OUT.name)
    OUT.write_bytes(data)
    print(json.dumps({"conditions": len(d["conditions"]), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}))


if __name__ == "__main__":
    main()
