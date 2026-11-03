"""Regression test for L-0108: a merged brief may not be built while a ruling's duty on the lanes is unentered.

Builds a private review folder of two rulings under a temporary directory and proves each refusal, then a pass. Writes nothing in
the tree. Run from anywhere: python -B campaign/close_kit/_test_ruling_duties.py
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ruling_duties as rd

DUTY = "The two blind merged lanes read every final row under their own gates."
OTHER = "The merged lanes' verdicts go to the close record."
LATER = "A reissued merged lane reads each changed row whole."


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def entry(s):
    return {"sha256": sha(s), "carried_by": "test"}


def write(folder, n, sentences):
    body = {"attempt_id": "x", "rulings": [{"id": "R%d" % n, "decision": " ".join(sentences), "evidence": [DUTY + " in evidence, not a duty"]}]}
    (folder / ("9xx_controlling_agent_rulings_E%d.v1.json" % n)).write_text(json.dumps(body), encoding="utf-8")


def main():
    fails = []

    def expect(name, got, want):
        if bool(got) != want:
            fails.append("%s: got %r" % (name, got))

    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        expect("no rulings at all", rd.refusals(folder, "9xx", {"read_every_row": True}), True)
        write(folder, 1, ["Nothing here binds anyone."])
        write(folder, 2, [DUTY, OTHER])
        expect("read_every_row not stated", rd.refusals(folder, "9xx", {"ruling_duties": [entry(DUTY), entry(OTHER)]}), True)
        expect("duties not entered", rd.refusals(folder, "9xx", {"read_every_row": True}), True)
        expect("one duty missing", rd.refusals(folder, "9xx", {"read_every_row": True, "ruling_duties": [entry(OTHER)]}), True)
        expect("row duty against false", rd.refusals(folder, "9xx", {"read_every_row": False, "ruling_duties": [entry(DUTY), entry(OTHER)]}), True)
        expect("no carried_by", rd.refusals(folder, "9xx", {"read_every_row": True, "ruling_duties": [{"sha256": sha(DUTY)}, entry(OTHER)]}), True)
        expect("stale entry", rd.refusals(folder, "9xx", {"read_every_row": True, "ruling_duties": [entry(DUTY), entry(OTHER), entry("gone")]}), True)
        clean = {"read_every_row": True, "ruling_duties": [entry(DUTY), entry(OTHER)]}
        expect("clean", rd.refusals(folder, "9xx", clean), False)
        write(folder, 3, [LATER])
        expect("a later round adds a duty", rd.refusals(folder, "9xx", clean), True)
        if len(rd.found(folder, "9xx")[0]) != 3:
            fails.append("evidence strings must not count as duties")
    print("\n".join(fails) if fails else "PASS 10 of 10")
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
