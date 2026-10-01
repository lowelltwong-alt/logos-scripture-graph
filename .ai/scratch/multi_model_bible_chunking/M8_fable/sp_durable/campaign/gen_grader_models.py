#!/usr/bin/env python3
"""Write the campaign grader carrier `campaign/grader_models.v1.json` (OW-25), which close tools READ.

WHY A CARRIER. OW-25 made claude-opus-5-5 the declared fallback for every role OW-13 gave to claude-fable-5-1. It also
ruled that a close tool must not be loosened to accept any model. The tool reads the grader model from here and asserts
that the completion receipt carries the downgrade statement. So the statement lives in one place, and a close tool cannot
paraphrase it.

TRANSCRIBED, NOT AUTHORED. The owner's words, the downgrade statement and the OW-26 weakness statement are cut
byte-for-byte from ERROR_PATTERN_LEDGER.v1.md. Each is taken by the bold lead-in that opens its paragraph, and the
paragraph's lines are joined with single spaces. The ledger is append-only and will grow, so --check compares the cut
text, never the ledger digest; the digest at transcription is recorded for provenance only.

Restoring Fable, or any other change, is a NEW version of this carrier (v2), never an edit of v1 (E-44).

usage: gen_grader_models.py [--check]     --check rebuilds in memory and prints MATCH or DIFFERS
"""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
M8 = HERE.parent.parent
LEDGER = M8 / "ERROR_PATTERN_LEDGER.v1.md"
OUT = HERE / "grader_models.v1.json"

OW25_HEAD = "## OWNER DIRECTIVE OW-25 (2026-09-22)"
OW26_HEAD = "## OWNER DIRECTIVE OW-26 (2026-09-22)"
DOWNGRADE_LEAD = "**The downgrade, stated so no reader mistakes a fallback grade for an OW-13 grade.**"
WEAKNESS_LEAD = "**The weakness, stated with the choice and recorded so no reader mistakes it for three independent passes.**"
OWNER_LEAD = "**The directive (TRANSCRIBED, owner in chat, 2026-09-22):**"


def section(lines, head):
    """Lines of the ledger section that opens with `head`, up to the next '## ' heading."""
    starts = [i for i, l in enumerate(lines) if l.startswith(head)]
    if len(starts) != 1:
        raise SystemExit("REFUSED: %d ledger headings start %r; expected exactly one" % (len(starts), head))
    s = starts[0]
    e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return s + 1, lines[s:e]


def paragraph(lines, head, lead):
    """(first line number, paragraph text) of the one paragraph in `head`'s section that opens with `lead`."""
    base, sec = section(lines, head)
    hits = [i for i, l in enumerate(sec) if l.startswith(lead)]
    if len(hits) != 1:
        raise SystemExit("REFUSED: %d paragraphs in %r open with %r; expected exactly one" % (len(hits), head, lead))
    i, out = hits[0], []
    while i < len(sec) and sec[i].strip():
        out.append(sec[i].strip())
        i += 1
    return base + hits[0], " ".join(out)


def build():
    raw = LEDGER.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    ln_d, downgrade = paragraph(lines, OW25_HEAD, DOWNGRADE_LEAD)
    ln_w, weakness = paragraph(lines, OW26_HEAD, WEAKNESS_LEAD)
    ln_o, owner_par = paragraph(lines, OW25_HEAD, OWNER_LEAD)
    q0, q1 = owner_par.index('"'), owner_par.index('"', owner_par.index('"') + 1)
    owner_words = owner_par[q0 + 1:q1]
    downgrade = downgrade[len(DOWNGRADE_LEAD):].strip()
    weakness = weakness[len(WEAKNESS_LEAD):].strip()
    d = {
        "schema": "m8_grader_models.v1",
        "written": "2026-09-22",
        "ow13_grader_model": "claude-fable-5-1",
        "declared_fallback_model": "claude-opus-5-5",
        "fallback_in_force": True,
        "effective_from": "2026-09-22",
        "scope": "project-wide: every role OW-13 assigned to claude-fable-5-1, all remaining books (OW-25)",
        "authority": {
            "directive": "OW-25",
            "owner_words_transcribed": owner_words,
            "source": "ERROR_PATTERN_LEDGER.v1.md",
            "source_sha256_at_transcription": hashlib.sha256(raw).hexdigest(),
            "owner_words_line": ln_o,
            "downgrade_statement_line": ln_d,
        },
        "downgrade_statement": downgrade,
        "downgrade_statement_sha256": hashlib.sha256(downgrade.encode("utf-8")).hexdigest(),
        "receipt_rule": ("Every completion receipt written on or after effective_from while fallback_in_force is true carries "
                         "grader_fallback = {model: declared_fallback_model, statement: downgrade_statement}, the statement "
                         "byte-equal to this carrier's. A close tool reads the grader model from this carrier; it never "
                         "hard-codes the fallback and never accepts an unnamed model."),
        "book_close_shapes": {
            "Ezek": {
                "directive": "OW-26",
                "shape": "merged-verdict close: one pair of blind claude-opus-5-5 lanes, each returning postcheck "
                         "fit_to_assemble, OW-6 final check fit_to_close bound to corpus_sha256, and close-gate items 20-23",
                "transcript_audit": "OWED, NOT MET",
                "weakness_statement": weakness,
                "weakness_statement_sha256": hashlib.sha256(weakness.encode("utf-8")).hexdigest(),
                "weakness_statement_line": ln_w,
            }
        },
        "limit": ("This carrier says who grades. It does not change OW-19 (two blind non-author lanes are the floor; the "
                  "orchestrator never grades its own items), OW-22 (Ezekiel's 72,000,000 hard line) or OW-11 (closing, "
                  "publication and campaign-log appends remain the owner's act). It does not record that Fable is "
                  "permanently unavailable; the account question is recorded in OW-25 and not pursued. A book listed in "
                  "book_close_shapes used that shape; a book not listed has not been granted one."),
        "generator": "campaign/gen_grader_models.py",
    }
    return (json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8"), d


def main():
    data, d = build()
    if "--check" in sys.argv:
        if not OUT.is_file():
            print("DIFFERS (absent)")
            return
        old = json.loads(OUT.read_text(encoding="utf-8"))
        keys = ("downgrade_statement", "downgrade_statement_sha256", "declared_fallback_model", "ow13_grader_model")
        same = (all(old.get(k) == d[k] for k in keys) and old["book_close_shapes"] == d["book_close_shapes"]
                and old["authority"]["owner_words_transcribed"] == d["authority"]["owner_words_transcribed"])
        print("MATCH" if same else "DIFFERS")
        return
    if OUT.exists():
        if OUT.read_bytes() != data:
            raise SystemExit("REFUSED: %s exists with different bytes; never overwritten (E-44)" % OUT.name)
        state = "same bytes, left"
    else:
        OUT.write_bytes(data)
        state = "written"
    print(json.dumps({"carrier": OUT.name, "state": state, "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
                      "downgrade_statement_sha256": d["downgrade_statement_sha256"],
                      "weakness_statement_sha256": d["book_close_shapes"]["Ezek"]["weakness_statement_sha256"],
                      "owner_words": d["authority"]["owner_words_transcribed"],
                      "downgrade_chars": len(d["downgrade_statement"])}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
