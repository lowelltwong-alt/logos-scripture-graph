#!/usr/bin/env python3
"""Second-pass device probe: byte-verify the surprising first-pass counts
before pinning inventory assertions (E-05 discipline)."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
POINTS = re.compile(r"[֑-ׇ]")
FINALS = str.maketrans("ךםןףץ", "כמנפצ")


def skel(s):
    return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("־", " ").translate(FINALS)


SK = {}
for line in (SPBOOK / "Jer_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        ref, text = line.split("\t", 1)
        SK[ref.split(".", 1)[1]] = skel(text)
TOK = {k: v.split() for k, v in SK.items()}
key = lambda k: tuple(map(int, k.split(".")))

out = {}
# (a) the one koh-amar without YHWH immediately after
ka = [k for k in SK if " כה אמר " in f" {SK[k]} " or SK[k].startswith("כה אמר")]
ka_y = [k for k in SK if " כה אמר יהוה " in f" {SK[k]} " or SK[k].startswith("כה אמר יהוה")]
out["koh_amar_without_yhwh"] = [
    {"ref": k, "text": SK[k][:120]} for k in sorted(set(ka) - set(ka_y), key=key)]

# (b) hoy full list with openings
hoy = sorted((k for k in TOK if "הוי" in TOK[k]), key=key)
out["hoy_sites"] = [{"ref": k, "opening": " ".join(TOK[k][:6])} for k in hoy]

# (c) Shiloh: any token containing שלו / שילו / שלה with prefixes
shilo_hits = {}
for k in sorted(SK, key=key):
    for t in TOK[k]:
        base = re.sub(r"^[והבלכמש]{0,2}", "", t)
        if base in ("שלו", "שילו", "שלה", "שילה"):
            shilo_hits.setdefault(k, []).append(t)
out["shiloh_candidate_tokens"] = shilo_hits

# (d) every token beginning נבוכד or נבכד (all spellings of the king)
neb = {}
for k in sorted(SK, key=key):
    for t in TOK[k]:
        base = re.sub(r"^[והבלכמש]{0,2}", "", t)
        if base.startswith("נבוכד") or base.startswith("נבכד"):
            neb.setdefault(base, []).append(k)
out["nebuchad_spellings"] = {sp: {"verses": len(set(v)), "sites": sorted(set(v), key=key)}
                            for sp, v in neb.items()}

# (e) date-header candidates: verses containing בשנת (construct) or בשנה
dates = {}
for k in sorted(SK, key=key):
    hits = [t for t in TOK[k] if t in ("בשנת", "בשנה", "ובשנת", "ובשנה")]
    if hits:
        dates[k] = {"tokens": hits, "initial": TOK[k][0] in ("בשנת", "בשנה", "ויהי", "ובשנת"),
                    "opening": " ".join(TOK[k][:5])}
out["date_candidates"] = dates

# (f) neum without YHWH immediately after
nm = sorted((k for k in TOK if "נאמ" in TOK[k]), key=key)
nm_y = [k for k in SK if " נאמ יהוה " in f" {SK[k]} " or SK[k].startswith("נאמ יהוה")]
out["neum_without_yhwh"] = [
    {"ref": k, "ctx": SK[k][max(0, SK[k].find("נאמ") - 30):SK[k].find("נאמ") + 40]}
    for k in sorted(set(nm) - set(nm_y), key=key)]

# (g) the non-initial vayehi-debar-YHWH site
vy = [k for k in SK if " ויהי דבר יהוה " in f" {SK[k]} " or SK[k].startswith("ויהי דבר יהוה")]
out["vayehi_non_initial"] = [
    {"ref": k, "opening": " ".join(TOK[k][:6])} for k in sorted(vy, key=key)
    if not SK[k].startswith("ויהי דבר יהוה")]

# (h) OAN lamed-initial candidate list with tokens
oan = []
for k in sorted(SK, key=key):
    c = int(k.split(".")[0])
    if 46 <= c <= 51 and TOK[k] and TOK[k][0].startswith("ל") and len(TOK[k][0]) >= 4:
        oan.append({"ref": k, "first": TOK[k][0]})
out["oan_lamed_initial"] = oan

print(json.dumps(out, ensure_ascii=False, indent=1))
