"""measure_w3b: counts on the pinned 1 Corinthians witnesses (RP and SBLGNT) for rows W3-004 and W3-005.
Greek targets are taken by token position from the witness bytes, never typed. Prints counts and verse lists."""
import os, unicodedata
SP = r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable"
def load(n):
    d = {}
    for l in open(os.path.join(SP, "1Cor", n), encoding="utf-8"):
        if "\t" in l:
            k, t = l.rstrip("\n").split("\t", 1)
            d[k] = t
    return d
RP, SBL = load("1Cor_rp.txt"), load("1Cor_sbl.txt")
def sk(tok):
    s = unicodedata.normalize("NFD", tok).casefold().replace("\u03c2", "\u03c3")
    return "".join(c for c in s if "\u03b1" <= c <= "\u03c9")
def toks(t):
    return [x for x in (sk(w) for w in t.split()) if x]
def key(k):
    _, c, v = k.split(".")
    return int(c), int(v)
ou, thelo, agnoein = (sk(RP["1Cor.10.1"].split()[i]) for i in (0, 1, 4))
ouk, oidate = (sk(RP["1Cor.9.24"].split()[i]) for i in (0, 1))
pantes = sk(RP["1Cor.10.1"].split()[10])
for name, W in (("RP", RP), ("SBL", SBL)):
    bare, inf, appeal_book, appeal_range, pan = [], [], [], [], {}
    for k, t in W.items():
        ts = toks(t)
        pairs = list(zip(ts, ts[1:]))
        if (ou, thelo) in pairs:
            bare.append(k)
            if agnoein in ts:
                inf.append(k)
        if (ouk, oidate) in pairs:
            appeal_book.append(k)
            if key("1Cor.8.1") <= key(k) <= key("1Cor.11.1"):
                appeal_range.append(k)
        if k in ("1Cor.10.1", "1Cor.10.2", "1Cor.10.3", "1Cor.10.4", "1Cor.10.5"):
            pan[k] = ts.count(pantes)
    print(name, "bare_neg_verb", len(bare), bare)
    print(name, "with_infinitive", len(inf), inf)
    print(name, "appeal_book", len(appeal_book), "appeal_8.1-11.1", len(appeal_range), appeal_range)
    print(name, "pantes_10.1-5", pan)
