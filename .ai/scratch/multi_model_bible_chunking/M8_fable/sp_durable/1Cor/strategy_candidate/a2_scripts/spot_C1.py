"""Orchestrator spot check of C1 DEF-01 (synerchesthai verses) and DEF-10 (4-token run calibration) on RP bytes."""
import re
import sys
import unicodedata
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
RP = "C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable/1Cor/1Cor_rp.txt"
rows = [l.split("\t", 1) for l in open(RP, encoding="utf-8").read().splitlines() if l.strip()]


def strip(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()


hits = [r[0][5:].replace(".", ":") for r in rows if re.search(r"συνερχ|συνελθ|συνηλθ|συνεληλυθ", strip(r[1]))]
print("synerchesthai verses:", hits)
for name, tok in (("whitespace", lambda t: t.split()),
                  ("letters only", lambda t: re.findall(r"\w+", t)),
                  ("stripped letters", lambda t: re.findall(r"\w+", strip(t)))):
    where = defaultdict(set)
    for ref, t in rows:
        w = tok(t)
        for i in range(len(w) - 3):
            where[tuple(w[i:i + 4])].add(ref)
    print(name, "distinct", len(where), "recur>1 verse", sum(1 for v in where.values() if len(v) > 1))
