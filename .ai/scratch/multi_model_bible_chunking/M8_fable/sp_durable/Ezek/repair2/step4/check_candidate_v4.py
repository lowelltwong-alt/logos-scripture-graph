#!/usr/bin/env python3
"""REPAIR-2 step-4c CANDIDATE GATE, v4 - the author vocabulary batch.

What changes from v3.1, and nothing else:
  * SCOPE comes from the step-4c worklist (rows with an owed item: prose fields and refs; never signals).
  * NEW OR CHANGED ENTRIES may now carry a face qualifier and the clause 6 v2 absence tokens - the form check accepts
    '[WARRANT-onset:near]' and friends, WARRANT-absence and DISCLOSURE-absence, and allows one extra annotation word
    when a WARRANT-rival's first token is its seam pair. Whether a qualifier is TRUE is not this form check's call: the
    HARD role_tokens member in the whole-suite arm verifies every one against verse and span and fails loud.
  * COMPLETION MEASURE: after the suite, role_tokens runs on the candidate in POST phase and the gate reports the
    warrants still unqualified. That number is the batch's remaining work, reported beside the verdict.
Kept from v3.1: per-row flags judged as a DELTA against the live row, and the whole pinned suite on the candidate with
no hard member allowed to gain a flag. A selftest with fixtures that must fail gates every verdict (E-36).

usage: python check_candidate_v4.py <proposal.json> --work <dir>
       python check_candidate_v4.py --selftest
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sys.path.insert(0, str(EZ / "repair2" / "step3"))
import check_candidate_v3 as V3                                                # noqa: E402
import check_candidate_v3_1 as V31                                             # noqa: E402

V2 = V3.V2
PROSE, REFS = V3.PROSE, V3.REFS
WORKLIST = HERE / "step4c_worklist.v1.json"
TOKENS = {"WARRANT-onset", "WARRANT-close", "WARRANT-rival", "WARRANT-absence", "DISCLOSURE-absence",
          "DISCLOSURE-kq", "DISCLOSURE-mark", "DISCLOSURE-paseq", "DISCLOSURE-note", "DISCLOSURE-device", "QUOTE", "ANCHOR",
          "WARRANT-absence-over-range"}
MT_BORNE = {"DISCLOSURE-kq", "DISCLOSURE-mark", "DISCLOSURE-paseq", "DISCLOSURE-note", "DISCLOSURE-device"}
REF = r"(oshb|web):Ezek\.(\d{1,2})\.(\d{1,3})(?:-Ezek\.(\d{1,2})\.(\d{1,3}))?"
ENTRY = re.compile(r"^" + REF + r"(?: = " + REF + r")? \[([A-Za-z-]+)(?::(near|far|interior|merge))?\] (.+)$")


def check_new_entry(e):
    m = ENTRY.match(e)
    if not m:
        return ["not in the entry form '<face>:Ezek.C.V[-...][ = <face>:Ezek.C.V[-...]] [TOKEN[:near|:far|:interior]] annotation'"]
    g = m.groups()
    token, qual, note = g[10], g[11], g[12]
    probs = []
    if token not in TOKENS:
        probs.append("token [%s] is not in the clause 6 v2 vocabulary" % token)
    if qual and token not in ("WARRANT-onset", "WARRANT-close", "WARRANT-rival"):
        probs.append("a face qualifier belongs only on WARRANT-onset, WARRANT-close or WARRANT-rival")
    if qual == "merge" and token != "WARRANT-rival":
        probs.append(":merge belongs only on WARRANT-rival (#e16 C1)")
    words = note.split()
    limit = 7 if (token == "WARRANT-rival" and words and re.fullmatch(r"\d{1,2}\.\d{1,3}/\d{1,2}\.\d{1,3}", words[0])) else 6
    if not 1 <= len(words) <= limit:
        probs.append("annotation has %d words; the limit here is %d" % (len(words), limit))
    f1 = (g[0], (int(g[1]), int(g[2])), (int(g[3]), int(g[4])) if g[3] else (int(g[1]), int(g[2])))
    in_zone = V2._touches_zone(*f1) or (g[5] is not None and V2._touches_zone(
        g[5], (int(g[6]), int(g[7])), (int(g[8]), int(g[9])) if g[8] else (int(g[6]), int(g[7]))))
    if in_zone:
        if g[5] is None or g[0] != "web" or g[5] != "oshb":
            probs.append("the entry touches the ch 20/21 zone and must be DUAL, 'web:... = oshb:...'")
        elif V2.LIB.web_to_mt(*f1[1]) != (int(g[6]), int(g[7])):
            probs.append("dual pair disagrees with the offset map")
    else:
        if token in MT_BORNE and g[0] != "oshb":
            probs.append("an MT-borne device token sits on the oshb: face (X2)")
        if token == "QUOTE" and g[0] != "web":
            probs.append("a [QUOTE] sits on the web: face (X2)")
    return probs


def scope():
    wl = json.loads(WORKLIST.read_text(encoding="utf-8"))
    return {i["row"]: set(PROSE) | {REFS} for i in wl["items"] if i["status"] != "DONE"}


def selftest():
    live, sc = V2.live_rows(), scope()
    V2.check_new_entry = check_new_entry
    cases = []
    r = next(i for i in json.loads(WORKLIST.read_text(encoding="utf-8"))["items"] if i["source"] == "RT"
             and "WARRANT-rival" in i["entry"])
    rid, entry = r["row"], r["entry"]
    good = entry.replace("[WARRANT-rival]", "[WARRANT-rival:near]")
    cases.append(("a qualified rival is ACCEPTED by the form check", not check_new_entry(good) or
                  all("words" in p for p in check_new_entry(good))))
    cases.append(("a qualifier on a DISCLOSURE token is refused",
                  bool(check_new_entry("oshb:Ezek.33.20 [DISCLOSURE-mark:near] pe single-witness"))))
    cases.append(("WARRANT-absence is accepted", not check_new_entry("oshb:Ezek.40.38 [WARRANT-absence] no device here")))
    cases.append(("an unknown token is refused", bool(check_new_entry("oshb:Ezek.40.38 [WARRANT-maybe] x"))))
    cases.append(("a zone entry that is not dual is refused",
                  bool(check_new_entry("web:Ezek.21.7 [WARRANT-onset:far] preceding verse"))))
    out_row = next(x for x in live if x not in sc)
    cases.append(("a row the 4c worklist owes nothing is refused",
                  not V31.check_row(live[out_row], {"device_notes": "x"}, set())["clean"]))
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if selftest():
        raise SystemExit("REFUSED: selftest failed; no verdict computed (E-36)")
    V2.check_new_entry = check_new_entry
    V3.check_row = lambda live_row, fields, allowed: V31.check_row(live_row, fields, allowed)
    V3.scope = scope
    V3.selftest = lambda: 0
    code = V3.main()
    work = Path(sys.argv[sys.argv.index("--work") + 1])
    cand = work / "candidate_rows.jsonl"
    p = subprocess.run([sys.executable, "-B", str(EZ / "tools" / "check_role_tokens.py"), str(cand), "--phase", "post"],
                       capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONUTF8="1"))
    d = json.loads(p.stdout[p.stdout.find("{"):])
    remaining = [f for f in d["flags"] if "unqualified" in f["problem"]]
    wrong = [f for f in d["flags"] if "unqualified" not in f["problem"]]
    print(json.dumps({"COMPLETION_MEASURE": {"warrants_still_unqualified_on_the_candidate": len(remaining),
                                             "qualifier_or_token_defects_on_the_candidate": len(wrong),
                                             "defects": wrong[:20]}}, ensure_ascii=False, indent=1))
    return 1 if (code or wrong) else 0


if __name__ == "__main__":
    raise SystemExit(main())
