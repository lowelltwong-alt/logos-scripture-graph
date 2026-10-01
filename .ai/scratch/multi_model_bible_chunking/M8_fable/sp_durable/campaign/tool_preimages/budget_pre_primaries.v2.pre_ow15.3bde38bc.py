"""Read-only budget measurement for the owner check-in before Ezekiel's primaries - VERSION 2.

v1 (budget_pre_primaries.py, kept unchanged with its 2026-09-11 output) carries two numbers that went stale, and GATE-E10 names this script
by name for the check-in after S4 lands, so the stale run would have been the one the owner saw:

  1. CEILING was 21,500,000. The owner's THIRD answer of 2026-09-11 raised Ezekiel's ceiling to 49,604,821 and gave Daniel its own 25M
     (ledger OW-11-n). v1 would report headroom against a ceiling that no longer binds.
  2. The corpus was repair/rows_v5_fixup2.jsonl. The chain head is now repair/rows_v6_fixup3.jsonl, and the cluster count that drives the
     primaries' component is derived from it.

Also added, because the campaign has run them since v1 and the projection should use what it measured: S3 and S4 in the distinct-check
component, and FIXUP-3 in the author-wave component. The component STRUCTURE is unchanged - same seven components, same bases - so v1's
shape can still be compared with v2's.

v1 is not edited. This prints JSON and writes nothing; every number is read from receipts or rows on disk. It is an ESTIMATE, not a
receipt, and each component states its basis.

Usage: budget_pre_primaries.v2.py [--json <out>]
"""
import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
CEILING = 49_604_821                      # owner, 2026-09-11 third answer (ledger OW-11-n); supersedes v1's 21,500,000
CEILING_SUPERSEDED = 21_500_000
DANIEL_CEILING = 25_000_000               # Daniel's own ceiling, counted from its first launch
DANIEL_VERSES_STANDARD = 357
EZ = SP / "Ezek"
ROWS = EZ / "repair" / "rows_v6_fixup3.jsonl"   # the chain head; v1 read rows_v5_fixup2.jsonl


def jl(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def toks(rs):
    return [r["tokens_reported"] for r in rs if isinstance(r.get("tokens_reported"), int)]


def stat(rs):
    t = toks(rs)
    return {"n": len(t), "sum": sum(t), "mean": (sum(t) // len(t)) if t else 0, "max": max(t) if t else 0}


def book_total(book):
    return sum(sum(toks(jl(fp))) for fp in (SP / book).rglob("*_attempt_receipts.jsonl"))


def verse_total(book):
    p = SP / book / "verse_inventory.json"
    if not p.is_file():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    for k in ("total_verses", "verses_total", "total", "web_total"):
        if isinstance(d.get(k), int):
            return d[k]
    for k in ("chapters", "per_chapter", "web_per_chapter", "verses_per_chapter"):
        v = d.get(k)
        if isinstance(v, dict) and v and all(isinstance(x, int) for x in v.values()):
            return sum(v.values())
        if isinstance(v, list) and v and all(isinstance(x, int) for x in v):
            return sum(v)
    return None


ap = argparse.ArgumentParser()
ap.add_argument("--json")
a = ap.parse_args()
if not ROWS.is_file():
    raise SystemExit("ABORT: the chain head %s does not exist" % ROWS)

census = book_total("Ezek")
rows = jl(ROWS)
parts = Counter(r["writer_part"] for r in rows)
clusters = sum(math.ceil(n / 8) for n in parts.values())
rul = jl(EZ / "ezek_rulings_attempt_receipts.jsonl")


def by_prefix(p):
    return stat([r for r in rul if str(r.get("attempt_id", "")).startswith(p)])


ctl = by_prefix("ezek_controlling_rulings")
s1 = by_prefix("ezek_author_wave_spot_review_s1")
s2 = by_prefix("ezek_fixup_wave_review_s2")
s3 = by_prefix("ezek_fixup2_wave_review_s3")
s4 = by_prefix("ezek_fixup3_wave_review_s4")
aw = stat(jl(EZ / "author" / "ezek_author_attempt_receipts.jsonl"))
fx2 = stat(jl(EZ / "fixup2" / "ezek_author_fixup_attempt_receipts.jsonl"))
fx3 = stat(jl(EZ / "fixup3" / "ezek_author_fixup_attempt_receipts.jsonl"))
pr = stat(jl(SP / "Lam" / "reviews" / "lam_pr_attempt_receipts.jsonl"))
peer = stat(jl(SP / "Lam" / "reviews" / "lam_peer_attempt_receipts.jsonl"))
jspot = stat(jl(SP / "Jer" / "spot" / "jer_spot_attempt_receipts.jsonl"))
jmicro = stat(jl(SP / "Jer" / "spot" / "jer_micro_attempt_receipts.jsonl"))
jfin = stat(jl(SP / "Jer" / "postcheck" / "jer_finalize_attempt_receipts.jsonl"))

half = math.ceil(clusters / 2)
checks = [x["sum"] for x in (s1, s2, s3, s4) if x["n"]]
waves = [x["sum"] for x in (fx2, fx3) if x["n"]]
comp = [
    ("primaries LF+OL", 2 * clusters * pr["mean"], 2 * clusters * pr["max"],
     "2 x %d clusters (rows_v6_fixup3) x Lam PR mean %s..max %s" % (clusters, pr["mean"], pr["max"])),
    ("peer round", half * peer["mean"], 2 * half * peer["max"],
     "%d peer orders x Lam peer mean %s; high runs each twice at max %s" % (half, peer["mean"], peer["max"])),
    ("boss rulings", 3 * ctl["mean"], 6 * ctl["mean"], "3..6 x Ezekiel controlling-agent mean %s" % ctl["mean"]),
    ("author wave on the remedies", min(waves), aw["sum"],
     "smallest Ezekiel fix-up wave total (FIXUP-2 %s, FIXUP-3 %s)..author-wave total %s" % (fx2["sum"], fx3["sum"], aw["sum"])),
    ("second-generation distinct check", min(checks), max(checks),
     "smallest..largest measured Ezekiel distinct check (S1 %s, S2 %s, S3 %s, S4 %s)" % (s1["sum"], s2["sum"], s3["sum"], s4["sum"])),
    ("spot wave + OW-6b second Fable review", jspot["sum"], jspot["sum"] + jmicro["sum"], "Jer spot..Jer spot + micro"),
    ("postcheck + final checks", jfin["sum"], 2 * jfin["sum"], "Jer finalize x 1..2"),
]
low, high = sum(c[1] for c in comp), sum(c[2] for c in comp)
lam_t, jer_t = book_total("Lam"), book_total("Jer")
lam_v, jer_v = verse_total("Lam"), verse_total("Jer")
dan = None
if lam_v and jer_v:
    rates = sorted([lam_t / lam_v, jer_t / jer_v])
    dan = {"verses_standard_web_not_staged": DANIEL_VERSES_STANDARD, "per_verse_rates": [round(x) for x in rates],
           "low": round(DANIEL_VERSES_STANDARD * rates[0]), "high": round(DANIEL_VERSES_STANDARD * rates[1]),
           "own_ceiling": DANIEL_CEILING,
           "basis": "Lam %s tokens / %s verses and Jer %s tokens / %s verses (receipts totals / verse inventories)"
                    % (lam_t, lam_v, jer_t, jer_v)}
out = {
    "schema": "m8_budget_projection.v2", "book": "Ezek",
    "changed_since_v1": [
        "ceiling %s -> %s (owner's third answer of 2026-09-11, ledger OW-11-n; v1's figure no longer binds)"
        % (format(CEILING_SUPERSEDED, ","), format(CEILING, ",")),
        "corpus repair/rows_v5_fixup2.jsonl -> repair/rows_v6_fixup3.jsonl (the chain head; the cluster count derives from it)",
        "the distinct-check component now spans every measured Ezekiel check (S1..S4), not S2..S1",
        "the author-wave component now spans FIXUP-2 and FIXUP-3, not FIXUP-2 alone",
        "Daniel's own 25M ceiling is stated beside its bracket",
        "v1 and its 2026-09-11 output are kept unchanged",
    ],
    "census_now": census, "ceiling": CEILING, "headroom": CEILING - census,
    "ezek_rows": len(rows), "rows_by_part": dict(sorted(parts.items())), "clusters_le8_within_parts": clusters,
    "measured": {"lam_pr": pr, "lam_peer": peer, "ezek_controlling": ctl, "ezek_s1": s1, "ezek_s2": s2, "ezek_s3": s3, "ezek_s4": s4,
                 "ezek_author_wave": aw, "ezek_fixup2": fx2, "ezek_fixup3": fx3, "jer_spot": jspot, "jer_micro": jmicro,
                 "jer_finalize": jfin},
    "projection_to_ezekiel_close": [{"component": c[0], "low": c[1], "high": c[2], "basis": c[3]} for c in comp],
    "projection_total": {"low": low, "high": high},
    "projected_ezekiel_total_at_close": {"low": census + low, "high": census + high},
    "crosses_the_ceiling": {"low": census + low > CEILING, "high": census + high > CEILING},
    "owner_check_in_required_before_the_primaries": census + high > CEILING,
    "daniel_bracket": dan or "UNAVAILABLE: a closed book's verse inventory could not be read",
    "limit": ("estimate from measured means and maxima of comparable lanes; not a receipt; fix-up rounds beyond one author wave are not "
              "included, and S4's own cost is counted only once its receipt lands"),
}
if a.json:
    Path(a.json).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(out, ensure_ascii=False, indent=1))
