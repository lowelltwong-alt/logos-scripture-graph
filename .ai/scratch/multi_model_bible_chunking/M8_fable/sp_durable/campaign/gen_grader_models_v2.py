#!/usr/bin/env python3
"""Write the campaign grader carrier `campaign/grader_models.v2.json`, the version that adds Daniel's close shape.

WHY A NEW VERSION. gen_grader_models.py rules that any change to the carrier is a new version, never an edit of v1
(E-44). OW-33 (2026-10-13) granted Daniel the merged-verdict close shape, which v1 does not list. v2 is v1's content,
read from v1's pinned bytes and copied unchanged, plus `book_close_shapes.Dan`. v1 and its generator are not touched, so
every pin on v1 still holds. A tool that needs Daniel's shape reads v2; a tool that needs only the grader model may
read either, since those fields are the same values.

TRANSCRIBED, NOT AUTHORED. Daniel's entry is cut from ERROR_PATTERN_LEDGER.v1.md the way v1 cuts Ezekiel's: each text is
taken by the bold lead-in that opens its paragraph in the OW-33 section, the paragraph's lines joined with single
spaces. The owner's words are the text between the first pair of double quotes in the directive paragraph. `directive`
stays "OW-26" because that is the shape's name; `granted_by` names the entry that grants it to Daniel. --check compares
the cut text and v1's copied fields, never the ledger digest, because the ledger is append-only and will grow.

usage: gen_grader_models_v2.py [--check]     --check rebuilds in memory and prints MATCH or DIFFERS
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
V1 = HERE / "grader_models.v1.json"
V1_SHA = "cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d"
OUT = HERE / "grader_models.v2.json"
OW33_HEAD = "## OWNER DIRECTIVE OW-33 (2026-10-13)"
OWNER_LEAD = "**The directive (TRANSCRIBED, owner in chat, 2026-10-13T00:12:24Z"
WEAKNESS_LEAD = "**The weakness, recorded as the owner ordered.**"


def v1_tool():
    spec = importlib.util.spec_from_file_location("gen_grader_models", HERE / "gen_grader_models.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build():
    g = v1_tool()
    v1_bytes = V1.read_bytes()
    if hashlib.sha256(v1_bytes).hexdigest() != V1_SHA:
        raise SystemExit("REFUSED: grader_models.v1.json is not the bytes this tool pins")
    v1 = json.loads(v1_bytes.decode("utf-8"))
    _, d1 = g.build()
    keys = ("downgrade_statement", "downgrade_statement_sha256", "declared_fallback_model", "ow13_grader_model")
    if not (all(v1.get(k) == d1[k] for k in keys) and v1["book_close_shapes"] == d1["book_close_shapes"]):
        raise SystemExit("REFUSED: v1 no longer transcribes the ledger; v2 will not copy it")
    raw = g.LEDGER.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    ln_o, owner_par = g.paragraph(lines, OW33_HEAD, OWNER_LEAD)
    q0 = owner_par.index('"')
    q1 = owner_par.index('"', q0 + 1)
    if owner_par.count('"') != 2:
        raise SystemExit("REFUSED: the OW-33 directive paragraph does not hold exactly one quotation")
    ln_w, weakness = g.paragraph(lines, OW33_HEAD, WEAKNESS_LEAD)
    weakness = weakness[len(WEAKNESS_LEAD):].strip()
    d = dict(v1)
    d["schema"] = "m8_grader_models.v2"
    d["written"] = "2026-10-13"
    d["supersedes"] = {"file": "campaign/grader_models.v1.json", "sha256": V1_SHA,
                       "what_changed": "book_close_shapes.Dan added (OW-33); every other value is v1's, copied unchanged"}
    shapes = dict(v1["book_close_shapes"])
    shapes["Dan"] = {
        "directive": "OW-26",
        "granted_by": "OW-33",
        "scope": "Daniel only",
        "shape": "merged-verdict close: one pair of blind lanes on the carrier's grader model, each returning postcheck "
                 "fit_to_assemble, OW-6 final check fit_to_close bound to corpus_sha256, and close-gate items 20-23",
        "transcript_audit": "OWED, NOT MET",
        "close_action": "reserved to the owner (OW-33)",
        "owner_words_transcribed": owner_par[q0 + 1:q1],
        "owner_words_line": ln_o,
        "weakness_statement": weakness,
        "weakness_statement_sha256": hashlib.sha256(weakness.encode("utf-8")).hexdigest(),
        "weakness_statement_line": ln_w,
        "source": "ERROR_PATTERN_LEDGER.v1.md",
        "source_sha256_at_transcription": hashlib.sha256(raw).hexdigest(),
    }
    d["book_close_shapes"] = shapes
    d["generator"] = "campaign/gen_grader_models_v2.py"
    return (json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8"), d


def main():
    data, d = build()
    if "--check" in sys.argv:
        if not OUT.is_file():
            print("DIFFERS (absent)")
            sys.exit(1)
        old = json.loads(OUT.read_bytes().decode("utf-8"))
        drop = ("source_sha256_at_transcription",)
        cut = lambda x: {b: {k: v for k, v in s.items() if k not in drop} for b, s in x["book_close_shapes"].items()}
        same = cut(old) == cut(d) and all(old.get(k) == v for k, v in d.items() if k != "book_close_shapes")
        print("MATCH" if same else "DIFFERS")
        sys.exit(0 if same else 1)
    if OUT.exists():
        if OUT.read_bytes() != data:
            raise SystemExit("REFUSED: %s exists with different bytes; never overwritten (E-44)" % OUT.name)
        state = "same bytes, left"
    else:
        OUT.write_bytes(data)
        state = "written"
    dan = d["book_close_shapes"]["Dan"]
    print(json.dumps({"carrier": OUT.name, "state": state, "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
                      "dan_weakness_statement_sha256": dan["weakness_statement_sha256"],
                      "dan_owner_words_chars": len(dan["owner_words_transcribed"]),
                      "dan_lines": [dan["owner_words_line"], dan["weakness_statement_line"]]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
