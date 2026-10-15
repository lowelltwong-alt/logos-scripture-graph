#!/usr/bin/env python3
"""Pre-launch LAUNCH-MESSAGE check (ledger E-62, 2026-09-23): a subagent is launched only with a message that carries,
itself, every piece the campaign's controls require. The brief carrying them is not enough.

WHY. Ledger OW-11-h (2026-09-11) made the owner's exception travel in every LAUNCH message, after an author lane that
followed its own global policy read the registry's Fable-5-only rule, saw no exception, and stopped. E-13 made the
research-context preamble a launch-message item; E-19 made the no-check line and the exact-path law launch-message
items. All of these were held in the orchestrator's working notes, and no tool enforced them. An audit of the
orchestrating session's own launches (2026-09-23) found 42 of 207 carrying none of the exact strings, inline or in a
message file, from 2026-09-16 on. This tool is the enforcement: write the launch message to a file, run this check,
launch only on MATCH, and pass the file's exact text as the prompt.

A MATCH requires all of the following:
  - every COMMON string below, verbatim, and every string of the AUTHORITY that covers --book;
  - one line 'BRIEF: <absolute path> sha256 <64 hex>' whose file exists at that digest;
  - that brief passing _brief_pin_check.py with MATCH (amended 2026-09-23, ledger E-62 sibling audit): the v10 delta
    lanes launched on a brief whose 4-column pin table the pin check could not read (NO_TABLE, exit 2). The pin check
    failed closed and was then not obeyed, so NO_TABLE and DRIFT are gaps here;
  - --book inside an owner's grant, and that grant not expired. Each grant names its books, its own required strings
    and the receipt whose existence ends it:
      OW-11 ("Yes: Ezekiel, then Daniel"): Ezek and Dan; expires at receipts/Dan_completion.json (Daniel's close).
      OW-36 ("Your six-book queue (Recommended)", amended 2026-10-14 additively): 1Cor, John, Rom, Rev, Heb, Matt,
        each expiring at its OWN receipts/<Book>_completion.json, with an NT research preamble (the Hebrew Bible
        preamble is false for these books).
    A book outside every grant is refused until the owner grants a new one and this table is amended under a ledger
    entry.
Exit 0 on MATCH; 1 on any gap; 2 on a usage error. Read-only.

Usage: _launch_message_check.py --book Dan --message <file>
       _launch_message_check.py --selftest"""
import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

SP = Path(__file__).resolve().parent.parent
COMMON = [
    ("ledger path to verify", "M8_fable\\ERROR_PATTERN_LEDGER.v1.md"),
    ("no-mutation statement", "never runs git, never writes a receipt and never touches the registry"),
    ("E-19 affirmative no-check line", "Never run any existence check, listing, glob or recursive search"),
    ("E-19 exact-path law", "State in your final message that you ran no listing and no glob"),
]
OW11 = [
    ("E-13 research-context preamble",
     "RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible"),
    ("OW-11 owner's answer on authority", "Yes: Ezekiel, then Daniel"),
    ("OW-11 owner's answer on recording", "M8 log only"),
    ("OW-11 authorization_ref", "lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan"),
]
OW36 = [
    ("E-13 research-context preamble (NT)",
     "RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament"),
    ("OW-36 authority heading", "AUTHORITY (OW-36"),
    ("OW-36 owner's answer", "Your six-book queue (Recommended)"),
    ("OW-36 authorization_ref", "lowell_chat_2026-10-14_m8_opus_orchestration_six_book_queue"),
]
# book -> (grant, the grant's own strings, the receipt whose existence ends the grant for that book)
AUTHORITY = {"Ezek": ("OW-11", OW11, "receipts/Dan_completion.json"),
             "Dan": ("OW-11", OW11, "receipts/Dan_completion.json")}
for _b in ("1Cor", "John", "Rom", "Rev", "Heb", "Matt"):
    AUTHORITY[_b] = ("OW-36", OW36, "receipts/%s_completion.json" % _b)
REQUIRED = COMMON + OW11                    # the OW-11 message shape, kept under its old name
EXCEPTION_BOOKS = {"Ezek", "Dan"}           # OW-11, kept under its old name
EXPIRY_RECORD = "receipts/Dan_completion.json"
BRIEF = re.compile(r"^BRIEF: (.+?) sha256 ([0-9a-f]{64})\s*$", re.M)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _brief_pin_check import check as brief_pin_check  # noqa: E402  (sp, brief) -> {verdict: MATCH|DRIFT|NO_TABLE}


def check(sp, book, text):
    grant = AUTHORITY.get(book)
    if grant is None:
        gaps = [name for name, s in COMMON if s not in text]
        gaps.append("book %s is outside every owner grant (OW-11, OW-36)" % book)
    else:
        name_, strings, expiry = grant
        gaps = [name for name, s in COMMON + strings if s not in text]
        if (sp / expiry).is_file():
            gaps.append("the %s grant for %s has expired: %s exists" % (name_, book, expiry))
    briefs = BRIEF.findall(text)
    if not briefs:
        gaps.append("no 'BRIEF: <path> sha256 <hex>' line")
    for path, digest in briefs:
        p = Path(path)
        if not p.is_file():
            gaps.append("brief missing: %s" % path)
        elif hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            gaps.append("brief drift: %s" % path)
        else:
            pins = brief_pin_check(sp, p)
            if pins["verdict"] != "MATCH":
                gaps.append("brief pin check %s: %s" % (pins["verdict"], path))
    return gaps


def selftest():
    with tempfile.TemporaryDirectory() as td:
        sp = Path(td)
        (sp / "In.txt").write_bytes(b"input\n")
        in_sha = hashlib.sha256(b"input\n").hexdigest()
        brief = sp / "B.md"
        brief.write_bytes(("| `SP\\In.txt` | `%s` |\n" % in_sha).encode("utf-8"))
        digest = hashlib.sha256(brief.read_bytes()).hexdigest()
        tail = "\nBRIEF: %s sha256 %s\n" % (brief, digest)
        good = "\n".join(s for _, s in REQUIRED) + tail
        good_nt = "\n".join(s for _, s in COMMON + OW36) + tail
        assert digest in good
        # the v10 shape: a 4-column pin table that _brief_pin_check.py reads as NO_TABLE
        wide = sp / "W.md"
        wide.write_bytes(("| `SP\\In.txt` | `%s` | 1 | input |\n" % in_sha).encode("utf-8"))
        wide_msg = good.replace(str(brief), str(wide)).replace(digest, hashlib.sha256(wide.read_bytes()).hexdigest())
        # a brief whose pinned input has drifted
        stale = sp / "S.md"
        stale.write_bytes(("| `SP\\In.txt` | `%s` |\n" % ("0" * 64)).encode("utf-8"))
        stale_msg = good.replace(str(brief), str(stale)).replace(digest, hashlib.sha256(stale.read_bytes()).hexdigest())
        cases = [("full message", good, "Dan", 0)]
        for name, s in REQUIRED:
            cases.append(("without " + name, good.replace(s, ""), "Dan", 1))
        cases += [("brief pin check NO_TABLE (4-column table)", wide_msg, "Dan", 1),
                  ("brief pin check DRIFT", stale_msg, "Dan", 1),
                  ("wrong brief digest", good.replace(digest, "0" * 64), "Dan", 1),
                  ("no BRIEF line", "\n".join(s for _, s in REQUIRED), "Dan", 1),
                  ("book outside every grant", good, "Gen", 1),
                  ("book outside every grant, NT shape", good_nt, "Mark", 1),
                  # OW-36 (2026-10-14): each queue book MATCHes only on the NT shape
                  ("1Cor full NT message", good_nt, "1Cor", 0),
                  ("Matt full NT message", good_nt, "Matt", 0),
                  ("1Cor on the OW-11 message", good, "1Cor", 1),
                  ("Dan on the OW-36 message", good_nt, "Dan", 1),
                  ("1Cor NT shape with the Hebrew Bible preamble",
                   good_nt.replace(OW36[0][1], OW11[0][1]), "1Cor", 1)]
        for name, s in COMMON + OW36:
            cases.append(("1Cor without " + name, good_nt.replace(s, ""), "1Cor", 1))
        fails = []
        for label, text, book, want in cases:
            got = 1 if check(sp, book, text) else 0
            if got != want:
                fails.append(label)
        stages = [(EXPIRY_RECORD, [("exception expired at Daniel's close", "Dan", good, 1),
                                   ("Ezekiel also expired at Daniel's close", "Ezek", good, 1),
                                   ("1Cor unaffected by Daniel's close", "1Cor", good_nt, 0)]),
                  ("receipts/1Cor_completion.json", [("1Cor expired at its own close", "1Cor", good_nt, 1),
                                                     ("John unaffected by 1Cor's close", "John", good_nt, 0)])]
        (sp / "receipts").mkdir()
        n = len(cases)
        for receipt, late in stages:      # each receipt is written before its own stage only
            (sp / receipt).write_text("{}", encoding="utf-8")
            for label, book, text, want in late:
                got = 1 if check(sp, book, text) else 0
                if got != want:
                    fails.append(label)
            n += len(late)
    print(json.dumps({"selftest": "PASS" if not fails else "FAIL", "cases": n, "fails": fails}))
    return 0 if not fails else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--book")
    ap.add_argument("--message")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.book and a.message):
        ap.print_usage()
        return 2
    raw = Path(a.message).read_bytes()
    gaps = check(SP, a.book, raw.decode("utf-8"))
    from m8_execution_efficiency import check_launch
    gaps.extend(check_launch(SP.parent, raw.decode("utf-8"),
                            [p for p, h in BRIEF.findall(raw.decode("utf-8"))]))
    print(json.dumps({"verdict": "MATCH" if not gaps else "REFUSED", "gaps": gaps, "book": a.book,
                      "message_sha256": hashlib.sha256(raw).hexdigest()}, ensure_ascii=False))
    return 0 if not gaps else 1


if __name__ == "__main__":
    raise SystemExit(main())
