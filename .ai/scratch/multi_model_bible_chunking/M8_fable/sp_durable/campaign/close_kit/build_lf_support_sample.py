#!/usr/bin/env python3
"""B-8 (close gate item 1): rebuild a book's LF-support frame from its LF primary finals and draw the deterministic
sample, every 5th row of the id-sorted frame (the Isaiah rule, as Jer/_build_lf_frame.py). Book-agnostic (TE-1).

The frame is every row an LF final marks verdict support (case folded), restricted to rows still in the corpus. The
sample is drawn here; the audit of each sampled row on the corpus bytes is the reissued lanes' duty, never this tool's.
Digits are this tool's counts. Every input is recorded with its sha256, and the corpus digest binds the sample.

usage (from SP): python -B campaign/close_kit/build_lf_support_sample.py --book 1Cor [--check]
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

SP = Path(__file__).resolve().parents[2]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def build(book):
    bk = SP / book
    corpus = bk / "rows_v1_final.jsonl"
    ids = [json.loads(s)["decision_id"] for s in corpus.read_text(encoding="utf-8").splitlines() if s.strip()]
    finals = sorted((bk / "review" / "primaries" / "finals").glob("final_LF_c*_e1.json"))
    if not finals:
        raise SystemExit("REFUSED: no LF primary finals for %s" % book)
    support, challenge, other = [], [], []
    for f in finals:
        for it in json.loads(f.read_text(encoding="utf-8"))["items"]:
            v = str(it.get("verdict", "")).lower()
            (support if v == "support" else challenge if v == "challenge" else other).append(it["row_id"])
    if other:
        raise SystemExit("REFUSED: LF verdicts other than support or challenge: %r" % other[:5])
    gone = sorted(set(support) - set(ids))
    frame = sorted(set(support) & set(ids))
    sample = frame[::5]
    return {"schema": "m8_lf_support_sample.v1", "book": book,
            "frame_object": "rows the LF primary finals mark verdict support, restricted to rows in the corpus",
            "rule": "every 5th of the id-sorted frame, starting at the first (Isaiah rule)",
            "corpus": {"path": "%s/rows_v1_final.jsonl" % book, "sha256": sha(corpus), "rows": len(ids)},
            "lf_finals": [{"path": f.relative_to(SP).as_posix(), "sha256": sha(f)} for f in finals],
            "support_verdicts": len(support), "challenge_verdicts": len(challenge), "support_rows_not_in_corpus": gone,
            "frame_size": len(frame), "sample_size": len(sample), "sample": sample, "frame": frame,
            "drawn_by": "campaign/close_kit/build_lf_support_sample.py", "tool_sha256": sha(__file__)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    doc = build(a.book)
    out = SP / a.book / "close" / "lf_support_sample.v1.json"
    text = (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    if a.check:
        print("MATCH" if out.is_file() and out.read_bytes() == text else "DIFFERS")
        return
    if out.exists() and out.read_bytes() != text:
        raise SystemExit("REFUSED: %s exists with other bytes" % out.name)
    out.write_bytes(text)
    print(json.dumps({"sha256": sha(out), **{k: doc[k] for k in ("support_verdicts", "challenge_verdicts",
                     "support_rows_not_in_corpus", "frame_size", "sample_size", "sample")}}))


if __name__ == "__main__":
    main()
