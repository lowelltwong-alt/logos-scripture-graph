"""Every sentence of a book's controlling rulings that lays something on the merged lanes, so a brief cannot drop one (L-0108).

The merged briefs of 1 Corinthians were built on Daniel's shape, 18 rows a lane, although two rulings said the lanes read every
final row. Nothing compared the brief to the rulings. make_merged_lanes.py now refuses until each sentence found here is entered
in the book's merged_params under ruling_duties, by digest, with what carries it. Rounds are read in order from E1 until the
first absent file, so a later round cannot be left out by a list a person kept. Run from sp_durable:

  python -B campaign/close_kit/ruling_duties.py --book 1Cor --lower 1cor [--params 1Cor/close/merged_params.v1.json]
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

SP = Path(__file__).resolve().parents[2]
NAMES = re.compile(r"merged[- ](?:verdict )?lanes?\b|\bblind lanes?\b|\bevery final row\b", re.I)
EVERY_ROW = re.compile(r"\bevery final row\b", re.I)
SKIP_KEYS = {"attempt_id", "execution_id", "inputs_ruled_on", "evidence", "deliverables", "verification"}


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in SKIP_KEYS:
                yield from walk(v, "%s/%s" % (path, k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, "%s/%d" % (path, i))
    elif isinstance(o, str):
        yield path, o


def found(review_dir, lower):
    """One entry per distinct sentence, first round that says it."""
    out, seen, n = [], set(), 1
    while True:
        path = Path(review_dir) / ("%s_controlling_agent_rulings_E%d.v1.json" % (lower, n))
        if not path.exists():
            return out, n - 1
        for where, text in walk(json.loads(path.read_text(encoding="utf-8"))):
            for sent in re.split(r"(?<=[.;])\s+", text):
                if NAMES.search(sent):
                    sha = hashlib.sha256(sent.encode("utf-8")).hexdigest()
                    if sha not in seen:
                        seen.add(sha)
                        out.append({"round": "E%d" % n, "where": where, "sha256": sha, "text": sent})
        n += 1


def refusals(review_dir, lower, params):
    """What stops a merged brief being built: an entry missing, a stale entry, or a row duty the parameters do not carry."""
    if "read_every_row" not in params:
        return ["merged_params has no read_every_row: state it, true or false"]
    entered = {d["sha256"]: d for d in params.get("ruling_duties", [])}
    sentences, rounds = found(review_dir, lower)
    if not rounds:
        return ["no ruling file found for %s under %s" % (lower, review_dir)]
    out = ["not entered in ruling_duties: %s %s: %s" % (s["round"], s["sha256"][:12], s["text"][:150])
           for s in sentences if s["sha256"] not in entered]
    now = {s["sha256"] for s in sentences}
    out += ["ruling_duties entry matches no sentence of E1..E%d: %s" % (rounds, k[:12]) for k in entered if k not in now]
    out += ["ruling_duties entry %s has no carried_by" % k[:12] for k, d in entered.items() if not d.get("carried_by")]
    if params["read_every_row"] is not True and any(EVERY_ROW.search(s["text"]) for s in sentences):
        out.append("a ruling says the lanes read every final row and read_every_row is not true")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", required=True)
    ap.add_argument("--lower", required=True)
    ap.add_argument("--params")
    a = ap.parse_args()
    review = SP / a.book / "review"
    if a.params:
        bad = refusals(review, a.lower, json.loads((SP / a.params).read_text(encoding="utf-8")))
        print("\n".join(bad) if bad else "PASS")
        raise SystemExit(1 if bad else 0)
    sentences, rounds = found(review, a.lower)
    print(json.dumps({"rounds": rounds, "sentences": sentences}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
