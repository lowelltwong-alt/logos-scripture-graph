#!/usr/bin/env python3
"""1 CORINTHIANS device inventory - the book's own structural signals, counted from Greek witness bytes. Ported in
form (not content) from Daniel's _build_device_inventory_dan.py; every difference beyond book tokens is listed in
LOGIC_CHANGES.

ORCHESTRATOR AMENDMENT 2026-10-14. Built by lane cor_p0_device_inventory_a1#e1 (sha256 7848ed06...);
the orchestrator then split the frame family at the letter's measured edges (FRAME_PAIRS / FRAME_IN_BODY_PAIRS),
after the lane's own report flagged 10:32. Nothing else changed.

WHAT THIS IS. It COUNTS recurring epistolary and argumentative formulae (topic markers, vocatives, disclosure, appeal,
citation, slogan, tradition, praise, frame, question openers) and records where they stand. It decides no boundary.
The campaign rules stand: a refrain CLOSES a unit, and a seam is assessed from BOTH sides.

EVERY COUNT IS A SKELETON MATCH. greek_lib.skeleton (through cor_lib): NFD, combining marks removed (accents,
breathings, iota subscript), casefolded, final sigma -> σ, elision marks deleted, punctuation, symbols and the SBLGNT
critical signs U+2E00-U+2E05 turned into spaces. A pattern is a sequence of skeleton WORDS, matched on word boundaries
(token equality, re-checked with greek_lib.bounded_find), never a bare substring; the substring reading is reported
beside it. Counts are of VERSES containing a form, per witness.

TWO WITNESSES, ONE LANGUAGE. Robinson-Pierpont (RP, primary) and SBLGNT (secondary), OW-31. Every pattern is
measured on both; every verse where they disagree on a hit is listed, with its cause (wording or edition punctuation).

REFS ARE WEB = GREEK. Identity on all 437 verses (web_greek_offset_map.json): numbering_face "WEB", equal to the
Greek face verse for verse. Consumers still assert the face (cor_lib.web_to_greek is range-guarded).

USAGE. Installed at SP/1Cor it reads its sibling inputs, imports tools/cor_lib.py beside them, and writes
1cor_device_inventory.json beside itself.
  --root DIR --out FILE   redirect the inputs (and the cor_lib import) and the output
  --selftest              run the synthetic self-test only (writes nothing)
It exits non-zero unless every self-assertion holds.
"""
import argparse
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = "1Cor"
INPUTS = ["1Cor_rp.txt", "1Cor_sbl.txt", "1Cor_web_clean.txt", "pmarks_1Cor.json", "web_greek_offset_map.json",
          "verse_inventory.json", "web_greek_verse_check.json", "tools/cor_lib.py",
          "../../greek_substrate/tools/greek_lib.py"]
PRODUCED_BY = {"attempt_id": "cor_p0_device_inventory_a1", "execution_id": "cor_p0_device_inventory_a1#e1",
               "model": "claude-opus-5-5", "grader_role": "grader_fallback (OW-25)",
               "statement": "a recorded downgrade, not an equivalence: this lane ran on claude-opus-5-5 under OW-25"}
STOPS = {".": "full_stop", ";": "question", ";": "question", "·": "ano_teleia", "·": "ano_teleia",
         "!": "exclamation"}
SIGLA = "⸀⸁⸂⸃⸄⸅"
SENT = ["sentence_start"]
NOT_SENT = ["verse_initial_mid_sentence", "after_comma", "after_other_punct", "internal"]
G = None  # cor_lib, bound by bind()


def bind(root):
    global G
    tools = (root / "tools").resolve()
    sys.path.insert(0, str(tools))
    import cor_lib
    if Path(cor_lib.__file__).resolve() != (tools / "cor_lib.py"):
        raise SystemExit("cor_lib imported from %s, not from %s" % (cor_lib.__file__, tools))
    G = cor_lib
    return cor_lib


def F(name, family, alts, gloss, **opt):
    return {"name": name, "family": family, "alts": alts, "gloss": gloss, **opt}


# ---------------------------------------------------------------- formulae (skeleton words; alternatives listed)
FORMULAE = [
    # topic markers
    F("peri_de", "topic_marker", ["περι δε"], "περὶ δέ 'now concerning', any position"),
    F("peri_de_ton", "topic_marker", ["περι δε των"], "περὶ δὲ τῶν 'now concerning the ...', any position"),
    F("peri_de_topic_marker", "topic_marker", ["περι δε"],
      "περὶ δέ at a sentence start (verse-initial after a stop, or after . ; · within the verse): the topic-marker reading",
      positions=SENT),
    F("peri_de_internal", "topic_marker", ["περι δε"], "περὶ δέ NOT at a sentence start (inside a clause)",
      positions=NOT_SENT),
    F("peri_sentence_start_bare", "topic_marker", ["περι"], "bare περί (not περὶ δέ) at a sentence start",
      positions=SENT, exclude_followed=["περι δε"]),
    F("peri_any", "topic_marker", ["περι"], "περί, any position (frequency control)"),
    # vocatives
    F("adelphoi", "vocative", ["αδελφοι"], "ἀδελφοί, any case reading (nominative and vocative share the form)"),
    F("adelphoi_no_article", "vocative", ["αδελφοι"],
      "ἀδελφοί not preceded by the article οἱ in the verse (the vocative reading; a heuristic)", not_preceded_by=["οι"]),
    F("adelphoi_mou", "vocative", ["αδελφοι μου"], "ἀδελφοί μου"),
    F("adelphoi_mou_agapetoi", "vocative", ["αδελφοι μου αγαπητοι"], "ἀδελφοί μου ἀγαπητοί"),
    F("agapetoi", "vocative", ["αγαπητοι"], "ἀγαπητοί, any position"),
    F("agapetoi_mou", "vocative", ["αγαπητοι μου"], "ἀγαπητοί μου"),
    # disclosure
    F("ou_thelo_agnoein", "disclosure", ["ου θελω υμασ αγνοειν", "ου θελω δε υμασ αγνοειν", "ου θελω γαρ υμασ αγνοειν"],
      "οὐ θέλω (δὲ / γὰρ) ὑμᾶς ἀγνοεῖν 'I do not want you to be ignorant'"),
    F("gnorizo_hymin", "disclosure", ["γνωριζω υμιν", "γνωριζω δε υμιν", "γνωριζω γαρ υμιν"],
      "γνωρίζω (δὲ / γὰρ) ὑμῖν 'I make known to you'"),
    F("thelo_de_hymas_eidenai", "disclosure", ["θελω δε υμασ ειδεναι"], "θέλω δὲ ὑμᾶς εἰδέναι 'I want you to know'"),
    F("thelo_de_hymas_wider", "disclosure_control", ["θελω δε υμασ", "θελω δε παντασ υμασ"],
      "θέλω δὲ (πάντας) ὑμᾶς + any infinitive: a wider wish form, NOT counted in the disclosure family"),
    # appeal
    F("parakalo", "appeal", ["παρακαλω"], "παρακαλῶ, any position"),
    F("parakalo_hymas", "appeal", ["παρακαλω υμασ", "παρακαλω δε υμασ", "παρακαλω ουν υμασ"],
      "παρακαλῶ (δὲ / οὖν) ὑμᾶς 'I appeal to you'"),
    F("parakalo_de_hymas", "appeal", ["παρακαλω δε υμασ"], "παρακαλῶ δὲ ὑμᾶς"),
    # rhetorical
    F("ouk_oidate", "rhetorical", ["ουκ οιδατε"], "οὐκ οἴδατε 'do you not know'"),
    F("ouk_oidate_hoti", "rhetorical", ["ουκ οιδατε οτι"], "οὐκ οἴδατε ὅτι"),
    F("e_ouk_oidate", "rhetorical", ["η ουκ οιδατε"], "ἢ οὐκ οἴδατε 'or do you not know'"),
    # citation
    F("gegraptai", "citation", ["γεγραπται"], "γέγραπται 'it is written', any form of introduction"),
    F("kathos_gegraptai", "citation", ["καθωσ γεγραπται"], "καθὼς γέγραπται"),
    F("gegraptai_gar", "citation", ["γεγραπται γαρ"], "γέγραπται γάρ"),
    F("legei", "citation", ["λεγει"], "λέγει 'he/it says', any subject (frequency control)"),
    F("ho_nomos_legei", "citation", ["ο νομοσ λεγει"], "ὁ νόμος λέγει 'the law says'"),
    F("legei_kyrios", "citation", ["λεγει κυριοσ"], "λέγει κύριος 'says the Lord'"),
    # slogan
    F("panta_moi_exestin", "slogan", ["παντα μοι εξεστιν"], "πάντα μοι ἔξεστιν 'all things are lawful for me'"),
    F("panta_exestin", "slogan", ["παντα εξεστιν"], "πάντα ἔξεστιν (without μοι)"),
    F("exestin_any", "slogan", ["εξεστιν"], "ἔξεστιν, any position"),
    F("ou_panta_sympherei", "slogan", ["ου παντα συμφερει"], "the reply οὐ πάντα συμφέρει"),
    # tradition
    F("parelabon", "tradition", ["παρελαβον"], "παρέλαβον 'I received'"),
    F("parelabete", "tradition", ["παρελαβετε"], "παρελάβετε 'you received'"),
    F("paredoka", "tradition", ["παρεδωκα"], "παρέδωκα 'I delivered'"),
    F("paradoseis", "tradition", ["παραδοσεισ"], "παραδόσεις 'traditions'"),
    # praise
    F("epaino", "praise", ["επαινω"], "ἐπαινῶ 'I praise', any position (includes the denial)"),
    F("ouk_epaino", "praise", ["ουκ επαινω"], "οὐκ ἐπαινῶ 'I do not praise'"),
    F("epaino_de_hymas", "praise", ["επαινω δε υμασ"], "ἐπαινῶ δὲ ὑμᾶς"),
    F("epaineso", "praise", ["επαινεσω"], "ἐπαινέσω 'shall I praise'"),
    # epistolary frame
    F("prescript_paulos", "frame", ["παυλοσ κλητοσ αποστολοσ"], "prescript Παῦλος κλητὸς ἀπόστολος"),
    F("adscript_church_of_god", "frame", ["τη εκκλησια του θεου"], "adscript τῇ ἐκκλησίᾳ τοῦ θεοῦ"),
    F("grace_peace_greeting", "frame", ["χαρισ υμιν και ειρηνη"], "salutation χάρις ὑμῖν καὶ εἰρήνη"),
    F("eucharisto", "frame", ["ευχαριστω"], "εὐχαριστῶ 'I give thanks', any position"),
    F("eucharisto_to_theo", "frame", ["ευχαριστω τω θεω"], "εὐχαριστῶ τῷ θεῷ"),
    F("greet_third_person", "frame", ["ασπαζεται", "ασπαζονται"], "ἀσπάζεται / ἀσπάζονται 'greets / greet'"),
    F("greet_imperative", "frame", ["ασπασασθε"], "ἀσπάσασθε 'greet'"),
    F("greeting_own_hand", "frame", ["ο ασπασμοσ τη εμη χειρι"], "ὁ ἀσπασμὸς τῇ ἐμῇ χειρί 'the greeting in my own hand'"),
    F("grace_benediction", "frame", ["η χαρισ του κυριου"], "benediction ἡ χάρις τοῦ κυρίου"),
    F("love_closing", "frame", ["η αγαπη μου"], "ἡ ἀγάπη μου 'my love'"),
    F("maranatha", "frame", ["μαραν αθα", "μαρανα θα", "μαραναθα"], "Aramaic μαρὰν ἀθά in Greek letters, all divisions"),
    F("amen", "frame", ["αμην"], "ἀμήν"),
    F("ego_paulos", "frame", ["εγω παυλοσ"], "ἐγὼ Παῦλος (first-person self-naming; Daniel's 'I, Daniel' analogue)"),
    # question openers
    F("ti_oun", "question", ["τι ουν"], "τί οὖν"),
    F("ti_oun_estin", "question", ["τι ουν εστιν"], "τί οὖν ἐστιν"),
    F("ti_oun_eroumen", "question", ["τι ουν ερουμεν"], "τί οὖν ἐροῦμεν (tried; a Romans form)"),
    F("ti_gar", "question", ["τι γαρ"], "τί γάρ"),
    F("me_genoito", "question", ["μη γενοιτο"], "μὴ γένοιτο"),
    # other markers
    F("touto_de_phemi", "other_marker", ["τουτο δε φημι"], "τοῦτο δέ φημι 'this I say'"),
    F("touto_de_lego", "other_marker", ["τουτο δε λεγω"], "τοῦτο δὲ λέγω"),
    F("idou", "other_marker", ["ιδου"], "ἰδού 'behold' (Daniel's behold analogue)"),
    F("charis_to_theo", "other_marker", ["τω δε θεω χαρισ"], "thanks ascription τῷ δὲ θεῷ χάρις"),
    # measurements for the Daniel crosswalk (date family)
    F("year_word", "date_family_control", ["ετοσ", "ετουσ", "ετει", "ετη", "ετων", "ετεσι", "ετεσιν"], "year noun ἔτος, any form"),
    F("month_word", "date_family_control", ["μην", "μηνοσ", "μηνι", "μηνα", "μηνεσ", "μηνασ", "μηνων"], "month noun μήν, any form"),
    F("day_word", "date_family_control", ["ημερα", "ημερασ", "ημεραν", "ημεραι", "ημερων", "ημεραισ"], "day noun ἡμέρα, any form"),
    F("first_of_the_week", "date_family_control", ["μιαν σαββατου", "μιαν σαββατων"], "κατὰ μίαν σαββάτου 'the first day of the week'"),
    F("pentecost", "date_family_control", ["πεντηκοστησ", "πεντηκοστη"], "πεντηκοστή 'Pentecost'"),
    F("pascha", "date_family_control", ["πασχα"], "πάσχα 'Passover'"),
]

# onset-candidate families for citation_sweep_constants: {FAMILY: formula names}; pairs = union of RP verse lists
CONST_FAMILIES = [
    ("TOPIC_MARKER", ["peri_de_topic_marker"]),
    ("BARE_PERI_SENTENCE_START", ["peri_sentence_start_bare"]),
    ("DISCLOSURE", ["ou_thelo_agnoein", "gnorizo_hymin", "thelo_de_hymas_eidenai"]),
    ("APPEAL", ["parakalo_hymas"]),
    ("TRADITION", ["parelabon", "parelabete", "paredoka", "paradoseis"]),
    ("PRAISE", ["epaino", "epaineso"]),
    ("SLOGAN", ["panta_moi_exestin", "panta_exestin"]),
    ("FRAME", ["prescript_paulos", "adscript_church_of_god", "grace_peace_greeting", "greet_third_person",
               "greet_imperative", "greeting_own_hand", "grace_benediction"]),
    ("THANKSGIVING", ["eucharisto_to_theo"]),
]

# the orchestrator's reading candidates (classified, not trusted)
CANDIDATES = [
    ("peri_de", "περὶ δέ", ["7.1", "7.25", "8.1", "12.1", "16.1", "16.12"],
     ["peri_de", "peri_de_topic_marker", "peri_de_ton"], ["concerning", "Concerning", "about"]),
    ("parakalo", "παρακαλῶ", ["1.10", "4.16", "16.15"], ["parakalo", "parakalo_hymas"], ["beg", "urge", "exhort"]),
    ("slogan", "πάντα μοι ἔξεστιν", ["6.12", "10.23"], ["panta_moi_exestin", "panta_exestin"], ["lawful"]),
    ("tradition", "παρέλαβον / παρέδωκα", ["11.2", "11.23", "15.1", "15.3"],
     ["parelabon", "parelabete", "paredoka", "paradoseis"], ["delivered", "received", "traditions", "instructions"]),
    ("praise", "ἐπαινῶ", ["11.2", "11.17", "11.22"], ["epaino", "ouk_epaino", "epaineso"], ["praise"]),
    ("frame", "the frame", ["1.1", "1.2", "1.3", "1.4", "16.19", "16.20", "16.21", "16.23"],
     ["prescript_paulos", "adscript_church_of_god", "grace_peace_greeting", "eucharisto", "eucharisto_to_theo",
      "greet_third_person", "greet_imperative", "greeting_own_hand", "grace_benediction", "love_closing", "amen"],
     ["Paul", "assembly", "Grace", "grace", "thank", "greet", "greeting", "Amen"]),
]


# ---------------------------------------------------------------- the measuring core (used by selftest too)
def vk(s):
    c, v = s.split(".")[-2:]
    return (int(c), int(v))


def ref(k):
    return "%s.%d.%d" % (BOOK, k[0], k[1])


def _is_word(ch):
    return unicodedata.category(ch)[0] in "LMN" or ch in G.g.ELISION


def tokenize(raw):
    """[{sk, s, e, sep}]: skeleton words with their raw span and the raw separator text before them."""
    ws, i, n, last = [], 0, len(raw), 0
    while i < n:
        if _is_word(raw[i]):
            j = i
            while j < n and _is_word(raw[j]):
                j += 1
            sk = G.skeleton(raw[i:j])
            if sk:
                for part in sk.split():
                    ws.append({"sk": part, "s": i, "e": j, "sep": raw[last:i]})
                last = j
            i = j
        else:
            i += 1
    return ws


def end_class(raw):
    t = raw.rstrip()
    while t and (t[-1] in SIGLA or t[-1] in "”\"')]" or t[-1].isspace()):
        t = t[:-1]
    return "stop" if t and t[-1] in STOPS else "no_stop"


def position(ws, i, prev):
    if i == 0:
        return "sentence_start" if prev in ("book_start", "stop") else "verse_initial_mid_sentence"
    sep = ws[i]["sep"]
    if any(c in STOPS for c in sep):
        return "sentence_start"
    if "," in sep:
        return "after_comma"
    if any(unicodedata.category(c)[0] == "P" and c not in SIGLA for c in sep):
        return "after_other_punct"
    return "internal"


def prepare(texts):
    order = sorted(texts)
    prep, prev = {}, "book_start"
    for k in order:
        ws = tokenize(texts[k])
        prep[k] = {"ws": ws, "sk": G.skeleton(texts[k]), "prev": prev,
                   "pos": [position(ws, i, prev) for i in range(len(ws))]}
        prev = end_class(texts[k])
    return order, prep


def match(p, spec):
    sks = [w["sk"] for w in p["ws"]]
    out = []
    for i in range(len(sks)):
        for alt in spec["alts"]:
            a = alt.split()
            if sks[i:i + len(a)] != a:
                continue
            if spec.get("positions") and p["pos"][i] not in spec["positions"]:
                continue
            if spec.get("not_preceded_by") and i > 0 and sks[i - 1] in spec["not_preceded_by"]:
                continue
            if any(sks[i:i + len(x.split())] == x.split() for x in spec.get("exclude_followed", ())):
                continue
            out.append((i, i + len(a), alt))
            break
    return out


def sign_blind(raw):
    """the skeleton WITHOUT turning signs and punctuation into spaces: what a sign would break"""
    d = unicodedata.normalize("NFD", raw)
    d = "".join(c for c in d if unicodedata.category(c) != "Mn").casefold().replace("ς", "σ")
    return " ".join(d.split())


def run_formula(spec, texts, order, prep):
    verses, positions, quotes, matched, signed = [], {}, {}, {}, []
    for k in order:
        h = match(prep[k], spec)
        if not h:
            continue
        r = ref(k)
        verses.append(r)
        ws = prep[k]["ws"]
        positions[r] = [prep[k]["pos"][i] for i, _, _ in h]
        i, j, alt = h[0]
        q = texts[k][ws[i]["s"]:ws[j - 1]["e"]]
        quotes[r] = q
        matched[r] = sorted({a for _, _, a in h})
        if any(c in SIGLA for c in q):
            signed.append({"verse": r, "quote": q, "found_if_signs_kept": alt in sign_blind(texts[k])})
    sub = [ref(k) for k in order if any(a in prep[k]["sk"] for a in spec["alts"])]
    bnd = [ref(k) for k in order if any(G.bounded_in(a, prep[k]["sk"], False) for a in spec["alts"])]
    return {"verses": verses, "positions": positions, "quotes": quotes, "matched": matched, "signed": signed,
            "substring": sub, "bounded_unconstrained": bnd}


def evaluate(wit, diff_verses):
    """wit = {'rp': {k: raw}, 'sbl': {k: raw}} -> {name: entry}, {name: {w: run}}"""
    prepd = {w: prepare(t) for w, t in wit.items()}
    runs, out = {}, {}
    for spec in FORMULAE:
        rr = {w: run_formula(spec, wit[w], *prepd[w]) for w in ("rp", "sbl")}
        runs[spec["name"]] = rr
        a, b = set(rr["rp"]["verses"]), set(rr["sbl"]["verses"])
        dis = []
        for r in sorted(a ^ b, key=vk):
            dis.append({"verse": r, "rp": r in a, "sbl": r in b,
                        "rp_quote": rr["rp"]["quotes"].get(r), "sbl_quote": rr["sbl"]["quotes"].get(r),
                        "cause": ("wording (RP and SBLGNT skeletons differ in this verse)" if r in diff_verses else
                                  "position class only (same skeleton; the editions punctuate differently)")})
        cons = {k: spec[k] for k in ("positions", "not_preceded_by", "exclude_followed") if spec.get(k)}
        e = {"family": spec["family"], "gloss": spec["gloss"], "pattern": spec["alts"],
             "constraints": cons or None,
             "count_rp": len(rr["rp"]["verses"]), "verses_rp": rr["rp"]["verses"],
             "count_sbl": len(rr["sbl"]["verses"]), "verses_sbl": rr["sbl"]["verses"],
             "witness_disagreements": dis,
             "positions_rp": rr["rp"]["positions"], "positions_sbl": rr["sbl"]["positions"],
             "quotes_rp": rr["rp"]["quotes"], "quotes_sbl": rr["sbl"]["quotes"]}
        srd = {}
        for w in ("rp", "sbl"):
            only = sorted(set(rr[w]["substring"]) - set(rr[w]["bounded_unconstrained"]), key=vk)
            srd[w] = {"substring_count": len(rr[w]["substring"]),
                      "word_bounded_unconstrained_count": len(rr[w]["bounded_unconstrained"]),
                      "substring_only_verses": only}
        e["substring_reading"] = srd
        if rr["sbl"]["signed"]:
            e["sbl_hits_with_a_critical_sign_inside"] = rr["sbl"]["signed"]
        out[spec["name"]] = e
    return out, runs, prepd


# ---------------------------------------------------------------- selftest over synthetic lines
def selftest():
    rp = {
        (1, 1): "Οὐ θέλω δὲ ὑμᾶς ἀγνοεῖν, ἀδελφοί, ὅτι οἱ ἀδελφοὶ τοῦ κυρίου ἦλθον.",
        (1, 2): "καὶ οἱ ἀδελφοὶ τοῦ κυρίου ἔγραψαν περὶ δὲ τούτου οὐδέν.",
        (1, 3): "Περὶ δὲ τῶν παρθένων ἐπιταγὴν οὐκ ἔχω, ἀντιλέγει δὲ οὐδείς,",
        (1, 4): "περὶ τῆς βρώσεως οὖν τῶν εἰδωλοθύτων οἴδαμεν. Περὶ δὲ τῆς λογίας ἀκούω.",
        (1, 5): "Περὶ τῆς βρώσεως οὖν οἴδαμεν.",
        (1, 6): "Πάντα μοι ἔξεστιν, ἀλλ’ οὐ πάντα συμφέρει.",
        (1, 7): "Περὶ δὲ τῶν πνευματικῶν, ἀδελφοί, οὐ θέλω ὑμᾶς ἀγνοεῖν.",
        (1, 8): "Παρακαλῶ δὲ ὑμᾶς, ἀδελφοί, γνωρίζω δὲ ὑμῖν τὸ εὐαγγέλιον.",
    }
    sbl = dict(rp)
    sbl[(1, 6)] = "Πάντα ἔξεστιν, ἀλλ’ οὐ πάντα συμφέρει."
    sbl[(1, 7)] = "Περὶ ⸀δὲ τῶν πνευματικῶν, ἀδελφοί, οὐ θέλω ὑμᾶς ἀγνοεῖν."
    diff = {ref(k) for k in rp if G.skeleton(rp[k]) != G.skeleton(sbl[k])}
    out, runs, prepd = evaluate({"rp": rp, "sbl": sbl}, diff)
    V = lambda n, w="rp": out[n]["verses_" + w]
    R = lambda *vs: ["1Cor.1.%d" % v for v in vs]
    tok_ok = all([w["sk"] for w in prepd[x][1][k]["ws"]] == G.skeleton(t[k]).split()
                 for x, t in (("rp", rp), ("sbl", sbl)) for k in t)
    sg = out["peri_de_topic_marker"].get("sbl_hits_with_a_critical_sign_inside", [])
    quotes_ok = all(G.collate(q, (rp if w == "rp" else sbl)[vk(r)]) == "byte"
                    for e in out.values() for w in ("rp", "sbl") for r, q in e["quotes_" + w].items())
    res = [
        ("tokenisation equals greek_lib.skeleton(verse).split() (elision ἀλλ’ and the sign ⸀ included)", tok_ok),
        ("περὶ δέ topic marker: sentence-start hits only (1.3 after a stop, 1.4 after '.', 1.7)",
         V("peri_de_topic_marker") == R(3, 4, 7)),
        ("περὶ δέ that is not one: inside a clause (1.2) is peri_de_internal, not a topic marker",
         V("peri_de_internal") == R(2) and V("peri_de") == R(2, 3, 4, 7)),
        ("περὶ δὲ τῶν counted (1.3, 1.7)", V("peri_de_ton") == R(3, 7)),
        ("bare περί at a sentence start (1.5); verse-initial after a comma is not one (1.4 word 1)",
         V("peri_sentence_start_bare") == R(5) and prepd["rp"][1][(1, 4)]["pos"][0] == "verse_initial_mid_sentence"),
        ("vocative ἀδελφοί: 'οἱ ἀδελφοί' alone (1.2) is excluded by the article rule",
         V("adelphoi") == R(1, 2, 7, 8) and V("adelphoi_no_article") == R(1, 7, 8)),
        ("disclosure formula οὐ θέλω (δὲ) ὑμᾶς ἀγνοεῖν (1.1, 1.7) and γνωρίζω δὲ ὑμῖν (1.8)",
         V("ou_thelo_agnoein") == R(1, 7) and V("gnorizo_hymin") == R(8)),
        ("appeal παρακαλῶ δὲ ὑμᾶς (1.8)", V("parakalo_hymas") == R(8)),
        ("SBLGNT critical sign inside a pattern: the skeleton match still hits 1.7, a sign-kept reading would not",
         "1Cor.1.7" in V("peri_de_topic_marker", "sbl") and len(sg) == 1 and sg[0]["verse"] == "1Cor.1.7"
         and sg[0]["found_if_signs_kept"] is False and "⸀" in sg[0]["quote"]),
        ("RP/SBLGNT pair where only one witness hits: πάντα μοι ἔξεστιν RP-only, πάντα ἔξεστιν SBL-only, both disclosed",
         V("panta_moi_exestin") == R(6) and V("panta_moi_exestin", "sbl") == [] and V("panta_exestin", "sbl") == R(6)
         and [d["verse"] for d in out["panta_moi_exestin"]["witness_disagreements"]] == R(6)
         and out["panta_moi_exestin"]["witness_disagreements"][0]["cause"].startswith("wording")),
        ("elided ἀλλ’ does not break 'οὐ πάντα συμφέρει' (both witnesses)",
         V("ou_panta_sympherei") == R(6) and V("ou_panta_sympherei", "sbl") == R(6)),
        ("substring vs word-bounded: λέγει inside ἀντιλέγει is substring-only (1.3), bounded count 0",
         V("legei") == [] and out["legei"]["substring_reading"]["rp"]["substring_only_verses"] == R(3)),
        ("every synthetic Greek quotation collates at tier byte in its witness", quotes_ok),
    ]
    return res


# ---------------------------------------------------------------- web text
def parse_web(raw):
    verses, cont, ch, cur = {}, 0, 0, None
    for line in raw.split("\n"):
        if line.startswith("===== 1COR ") and line.endswith(" ====="):
            ch, cur = int(line.split()[2]), None
            continue
        if line.startswith("[v] "):
            n, text = line[4:].split(" ", 1)
            cur = (ch, int(n))
            verses[cur] = [text]
            continue
        if line.strip() and line.strip() != "¶" and cur is not None:
            verses[cur].append(line)
            cont += 1
    return verses, cont


def web_slice(segments, kws, pad=25):
    for kw in kws:
        for seg in segments:
            i = seg.find(kw)
            if i >= 0:
                lo = seg.rfind(" ", 0, max(0, i - pad)) + 1 if i > pad else 0
                hi = seg.find(" ", i + len(kw) + pad)
                return seg[lo:hi if hi >= 0 else len(seg)], kw
    seg = segments[0]
    hi = seg.find(" ", 50)
    return seg[:hi if hi >= 0 else len(seg)], None


# ---------------------------------------------------------------- main
def build(root):
    bind(root)
    raw = {n: (root / n).read_bytes() for n in INPUTS}
    inputs = {n: hashlib.sha256(b).hexdigest() for n, b in raw.items()}
    J = lambda n: json.loads(raw[n].decode("utf-8"))
    pm, omap, vinv, vchk = J("pmarks_1Cor.json"), J("web_greek_offset_map.json"), J("verse_inventory.json"), \
        J("web_greek_verse_check.json")
    wit = {}
    for w, n in (("rp", "1Cor_rp.txt"), ("sbl", "1Cor_sbl.txt")):
        d = {}
        for line in raw[n].decode("utf-8").splitlines():
            key, text = line.split("\t", 1)
            d[vk(key)] = text
            assert key.split(".")[0] == BOOK
        wit[w] = d
    wtext = raw["1Cor_web_clean.txt"].decode("utf-8")
    web, cont_lines = parse_web(wtext)
    A = []

    # totals, numbering, faces
    def per_ch(keys):
        return {str(c): sum(1 for k in keys if k[0] == c) for c in sorted({k[0] for k in keys})}
    pc = {w: per_ch(list(wit[w])) for w in ("rp", "sbl")}
    pc["web"] = per_ch(list(web))
    A.append(("16 chapters and 437 verses in each of RP, SBLGNT and WEB",
              all(len(pc[w]) == 16 and sum(pc[w].values()) == 437 for w in pc)))
    A.append(("per-chapter counts of RP, SBLGNT and WEB are equal and equal verse_inventory.json and "
              "web_greek_verse_check.json",
              pc["rp"] == pc["sbl"] == pc["web"] == {str(c): n for c, n in vinv["chapters"].items()}
              and all(vchk["per_chapter"][c] == {"web": n, "rp": n, "sbl": n} for c, n in pc["rp"].items())))
    A.append(("numbering is identity: offset map identity_throughout, no zones, verse_inventory numbering_face WEB, "
              "and the three witnesses carry the same verse keys",
              omap["identity_throughout"] is True and omap["zones"] == [] and vinv["numbering_face"] == "WEB"
              and set(wit["rp"]) == set(wit["sbl"]) == set(web)
              and all(G.web_to_greek(*k) == k for k in web)))
    order = sorted(wit["rp"])
    diff = sorted((ref(k) for k in order if G.skeleton(wit["rp"][k]) != G.skeleton(wit["sbl"][k])), key=vk)
    A.append(("RP/SBLGNT wording differs (after greek_lib.skeleton) in 218 verses, equal to pmarks rp_sbl_differences",
              len(diff) == 218 and diff == sorted(pm["rp_sbl_differences"], key=vk)))
    sign_verses = sorted((ref(k) for k in order if any(c in SIGLA for c in wit["sbl"][k])), key=vk)
    n_signs = sum(1 for k in order for c in wit["sbl"][k] if c in SIGLA)
    pm_signs = sum(sum(v.values()) for v in pm["sbl_variant_sites"].values())
    A.append(("SBLGNT carries 419 critical signs over 220 verses, equal to pmarks sbl_variant_sites",
              n_signs == 419 and len(sign_verses) == 220 and pm_signs == 419
              and sign_verses == sorted(pm["sbl_variant_sites"], key=vk)))
    A.append(("RP carries no critical sign and no pilcrow (removed and recorded in pmarks)",
              not any(c in SIGLA or c == "¶" for t in wit["rp"].values() for c in t)))
    hebrew = sum(1 for w in ("rp", "sbl") for t in wit[w].values() for c in t if "֐" <= c <= "׿")
    A.append(("no Hebrew-block character in either Greek witness (Daniel's Hebrew/Aramaic patterns cannot apply)",
              hebrew == 0))

    formulae, runs, prepd = evaluate(wit, set(diff))
    A.append(("skeleton tokenisation equals greek_lib.skeleton(verse).split() in every verse of both witnesses",
              all([x["sk"] for x in prepd[w][1][k]["ws"]] == G.skeleton(wit[w][k]).split()
                  for w in ("rp", "sbl") for k in order)))

    # paragraph marks
    rpp, wpp = pm["rp_paragraph_starts"], pm["web_paragraph_starts"]
    ov = sorted(set(rpp) & set(wpp), key=vk)
    paragraph_marks = {
        "gloss": ("edition paragraphing from pmarks_1Cor.json: RP pilcrows (removed from 1Cor_rp.txt) and WEB paragraph "
                  "starts. Evidence, never a driver (E-23)."),
        "rp_pilcrow": {"count": len(rpp), "verses": rpp},
        "web_paragraph_start": {"count": len(wpp), "verses": wpp},
        "web_paragraph_midverse": pm["web_paragraph_midverse"],
        "overlap": {"count": len(ov), "verses": ov},
        "rp_only": {"count": len(set(rpp) - set(wpp)), "verses": sorted(set(rpp) - set(wpp), key=vk)},
        "web_only": {"count": len(set(wpp) - set(rpp)), "verses": sorted(set(wpp) - set(rpp), key=vk)},
    }
    A.append(("RP pilcrows 35, WEB paragraph starts 87, overlap 31", (len(rpp), len(wpp), len(ov)) == (35, 87, 31)))
    for e in formulae.values():
        e["paragraph_overlay"] = {"rp_hits_on_rp_pilcrow": sum(1 for r in e["verses_rp"] if r in set(rpp)),
                                  "rp_hits_on_web_paragraph_start": sum(1 for r in e["verses_rp"] if r in set(wpp))}

    # constants
    csc = {"face": "WEB",
           "face_equals_greek": True,
           "face_basis": ("Daniel's citation_sweep.py compares its calendar pairs on the MT face: DATELINE_PAIRS, "
                          "CAL_DATE_PAIRS and CAL_NO_ONSET are MT pairs (lines 303-308), and the onset arm converts a "
                          "WEB span with web_to_mt before the membership test (lines 389-393). In 1 Corinthians "
                          "cor_lib.web_to_mt is web_to_greek, identity on all 437 verses, so these pairs are on the "
                          "WEB face and equal the Greek (RP and SBLGNT) face verse for verse; a consumer still "
                          "converts through the range-guarded function."),
           "pairs_taken_from": "the RP (primary) verse lists; any SBLGNT-only hit is listed separately",
           "family_members": {f: m for f, m in CONST_FAMILIES}}
    for fam, members in CONST_FAMILIES:
        a = sorted({r for m in members for r in formulae[m]["verses_rp"]}, key=vk)
        b = sorted({r for m in members for r in formulae[m]["verses_sbl"]} - set(a), key=vk)
        csc[fam + "_PAIRS"] = [list(vk(r)) for r in a]
        csc[fam + "_SBL_ONLY_PAIRS"] = [list(vk(r)) for r in b]
    csc["DEVICE_NO_ONSET"] = []
    # ORCHESTRATOR AMENDMENT 2026-10-14 (lane D's own report flagged 1Cor.10.32): the frame formulae also occur inside
    # the body (the adscript form at 10:32 stands inside a clause), so FRAME_PAIRS keeps only the hits on the letter's
    # edges and FRAME_IN_BODY_PAIRS lists the rest. The edges are measured from this inventory, never typed: the
    # opening runs up to (not including) the first APPEAL pair, the body-opening appeal; the closing runs from the first
    # frame-formula hit in the last chapter that carries one.
    _fr = [tuple(p) for p in csc["FRAME_PAIRS"]]
    _open_end = min(tuple(p) for p in csc["APPEAL_PAIRS"])
    _last_ch = max(c for c, _ in _fr)
    _close_start = min(p for p in _fr if p[0] == _last_ch)
    csc["FRAME_PAIRS"] = [list(p) for p in _fr if p < _open_end or p >= _close_start]
    csc["FRAME_IN_BODY_PAIRS"] = [list(p) for p in _fr if _open_end <= p < _close_start]
    csc["FRAME_edges"] = {"opening_before": list(_open_end), "closing_from": list(_close_start)}
    csc["FRAME_edges_statement"] = (
        "FRAME_PAIRS = frame-formula RP hits before the first APPEAL pair or at/after the first frame-formula hit of "
        "the last chapter that has one; FRAME_IN_BODY_PAIRS = the other frame-formula RP hits. An orchestrator "
        "amendment of the lane's builder, named for the Fable end review.")
    A.append(("FRAME_PAIRS and FRAME_IN_BODY_PAIRS partition the frame family's RP hits at the measured edges",
              all(tuple(p) < _open_end or tuple(p) >= _close_start for p in csc["FRAME_PAIRS"])
              and all(_open_end <= tuple(p) < _close_start for p in csc["FRAME_IN_BODY_PAIRS"])
              and sorted(csc["FRAME_PAIRS"] + csc["FRAME_IN_BODY_PAIRS"]) == [list(p) for p in _fr]))
    csc["DEVICE_NO_ONSET_statement"] = (
        "empty: no 1 Corinthians ruling restricts onsets at any device. Daniel's CAL_NO_ONSET was also empty and "
        "Ezekiel's came from that book's own ruling; neither carries over. These constants record facts only "
        "(which verses carry which form), never an onset rule.")
    A.append(("citation_sweep constants equal the union of their families' RP verse lists (FRAME with FRAME_IN_BODY); SBL-only lists are "
              "disjoint from them; DEVICE_NO_ONSET is empty",
              all(sorted(csc[f + "_PAIRS"] + csc.get(f + "_IN_BODY_PAIRS", [])) == [list(vk(r)) for r in sorted({r for m in ms for r in formulae[m]["verses_rp"]},
                                                                     key=vk)]
                  and not ({tuple(p) for p in csc[f + "_PAIRS"]} & {tuple(p) for p in csc[f + "_SBL_ONLY_PAIRS"]})
                  for f, ms in CONST_FAMILIES) and csc["DEVICE_NO_ONSET"] == []))

    # reading candidates
    web_quotes = []
    cands = []
    for fam, label, vs, members, kws in CANDIDATES:
        listed = ["1Cor." + v for v in vs]
        hit_union = sorted({r for m in members for w in ("rp", "sbl") for r in formulae[m]["verses_" + w]}, key=vk)
        for r, off in [(x, False) for x in listed] + [(x, True) for x in hit_union if x not in listed]:
            hr = [m for m in members if r in formulae[m]["verses_rp"]]
            hs = [m for m in members if r in formulae[m]["verses_sbl"]]
            cls = ("present_both_witnesses" if hr and hs else "present_rp_only" if hr else
                   "present_sbl_only" if hs else "absent_both_witnesses")
            sl, kw = web_slice(web[vk(r)], kws)
            web_quotes.append(sl)
            cands.append({"family": fam, "candidate": label, "verse": r, "on_orchestrator_list": not off,
                          "class": cls, "formulae_hit_rp": hr, "formulae_hit_sbl": hs,
                          "positions_rp": {m: formulae[m]["positions_rp"][r] for m in hr},
                          "quote_rp": formulae[hr[0]]["quotes_rp"][r] if hr else None,
                          "quote_sbl": formulae[hs[0]]["quotes_sbl"][r] if hs else None,
                          "rp_pilcrow": r in rpp, "web_paragraph_start": r in wpp,
                          "rp_sbl_wording_differs": r in set(diff),
                          "web_evidence": sl, "web_keyword": kw})
    A.append(("every listed reading candidate is classified, and every off-list family hit is classified",
              all(any(c["verse"] == "1Cor." + v and c["family"] == f for c in cands)
                  for f, _, vs, _, _ in CANDIDATES for v in vs)))

    # formula-level checks
    rset = {w: {ref(k) for k in wit[w]} for w in ("rp", "sbl")}
    bound_ok, quote_ok, dis_ok, sign_ok = True, True, True, True
    for n, e in formulae.items():
        for w in ("rp", "sbl"):
            for r in e["verses_" + w]:
                k = vk(r)
                bound_ok &= all(G.bounded_in(a, prepd[w][1][k]["sk"], False) for a in runs[n][w]["matched"][r])
                quote_ok &= G.collate(e["quotes_" + w][r], wit[w][k]) == "byte"
        dis_ok &= [d["verse"] for d in e["witness_disagreements"]] == sorted(
            set(e["verses_rp"]) ^ set(e["verses_sbl"]), key=vk)
        for s in e.get("sbl_hits_with_a_critical_sign_inside", []):
            sign_ok &= s["verse"] in e["verses_sbl"] and any(c in SIGLA for c in s["quote"])
    for c in cands:
        for w in ("rp", "sbl"):
            q = c["quote_" + w]
            if q is not None:
                quote_ok &= G.collate(q, wit[w][vk(c["verse"])]) == "byte"
    A.append(("every hit of every pattern is found word-bounded (greek_lib.bounded_find) in its witness's skeleton",
              bound_ok))
    A.append(("every Greek quotation is found by cor_lib.collate at tier byte in its witness", quote_ok))
    A.append(("every formula's witness_disagreements equal the symmetric difference of its RP and SBLGNT lists",
              dis_ok))
    A.append(("every SBLGNT hit whose span carries a critical sign is still found by the skeleton match", sign_ok))

    sign_hits = sorted({(s["verse"], n, s["found_if_signs_kept"]) for n, e in formulae.items()
                        for s in e.get("sbl_hits_with_a_critical_sign_inside", [])})
    totals = {"verses": len(order), "chapters": 16, "verses_per_chapter": pc["rp"],
              "rp_sbl_differing_verses": len(diff),
              "sbl_critical_signs": {"signs": n_signs, "verses": len(sign_verses)},
              "sbl_hits_with_a_sign_inside_the_span": {
                  "count": len(sign_hits),
                  "would_be_missed_if_signs_were_kept": sum(1 for x in sign_hits if not x[2])},
              "hebrew_block_characters_in_greek_witnesses": hebrew}
    position_census = {}
    for w in ("rp", "sbl"):
        cc = {}
        for k in order:
            for p in prepd[w][1][k]["pos"]:
                cc[p] = cc.get(p, 0) + 1
        position_census[w] = dict(sorted(cc.items()))

    out = {
        "book": BOOK,
        "produced_by": PRODUCED_BY,
        "witness": {"primary": "Robinson-Pierpont Byzantine Textform (RP), 1Cor_rp.txt",
                    "secondary": "SBLGNT, 1Cor_sbl.txt (inline critical signs U+2E00-U+2E05 kept)",
                    "english_face": "World English Bible (WEB), 1Cor_web_clean.txt",
                    "ruling": "OW-31: Byzantine primary, SBLGNT secondary; neither is preferred here"},
        "numbering": ("identity: WEB = RP = SBLGNT verse for verse on all 437 verses in 16 chapters "
                      "(web_greek_offset_map.json identity_throughout true, zones empty). There is no numbering zone."),
        "numbering_face": "WEB",
        "numbering_face_obligation_on_consumers": (
            "every ref here is on the WEB face, which equals the Greek face verse for verse (identity). "
            "verse_inventory.json beside it declares the WEB face too. A consumer still asserts the face it expects "
            "before verse arithmetic and maps through cor_lib.web_to_greek, which is range-guarded."),
        "method": ("word-bounded skeleton match. Each verse of each witness is tokenised into greek_lib.skeleton words "
                   "(NFD, combining marks removed, casefold, final sigma to σ, elision deleted; punctuation and the "
                   "SBLGNT signs become separators); the token list is asserted equal to skeleton(verse).split(). A "
                   "pattern is a list of alternative skeleton word sequences, matched by token equality and re-checked "
                   "with greek_lib.bounded_find. Position classes come from the raw separators: sentence_start "
                   "(verse-initial after a verse ending in . ; · or the book start, or after . ; · within the verse), "
                   "verse_initial_mid_sentence, after_comma, after_other_punct, internal. Punctuation is each "
                   "EDITION's, so position classes are per witness. Counts are of VERSES containing a form, per "
                   "witness. The substring reading is reported per formula."),
        "inputs": inputs,
        "web_format": {"verse_lines": len(web), "continuation_lines": cont_lines,
                       "verses_with_continuation_lines": sum(1 for v in web.values() if len(v) > 1),
                       "note": ("1Cor_web_clean.txt has one '[v] N' line per verse plus paragraph and poetry "
                                "continuation lines; every WEB quotation is sliced from a single line and asserted "
                                "byte-exact in the file")},
        "totals": totals,
        "position_census": position_census,
        "formulae": formulae,
        "paragraph_marks": paragraph_marks,
        "citation_sweep_constants": csc,
        "reading_candidates": cands,
        "how_these_are_used": [
            "RULE: these are EVIDENCE, not a verdict. No boundary is set by a count alone; edition punctuation, "
            "edition paragraphing and translation formatting never drive one (E-23).",
            "RULE: a refrain CLOSES a unit, so a closing formula (grace benediction, ἀμήν, a doxology) belongs to "
            "the unit BEFORE it.",
            "RULE: a seam is assessed from BOTH sides; an onset-only diagnosis is incomplete until the adjacent "
            "unit's close is weighed from bytes.",
            "RULE: refs are WEB = Greek (identity); assert the face anyway before comparing.",
            "RULE: quote RP (primary); where RP and SBLGNT disagree on a hit, disclose both and argue from neither "
            "alone. A disagreement whose cause is 'position class only' is an edition-punctuation fact, not a "
            "textual variant.",
            "RULE: a sentence_start position rests on the edition's punctuation; it is evidence about the edition, "
            "not about the author.",
            "HYPOTHESIS to test: a sentence-initial περὶ δέ opens a topic section; weigh each against the close of "
            "the section before it, and weigh a mid-clause περὶ δέ separately.",
            "HYPOTHESIS to test: disclosure (οὐ θέλω ὑμᾶς ἀγνοεῖν, γνωρίζω ὑμῖν) and appeal (παρακαλῶ ὑμᾶς) "
            "formulae open units; test each from both sides.",
            "HYPOTHESIS to test: the vocative ἀδελφοί marks a turn or an appeal, but it is too frequent to set a "
            "boundary alone; the skeleton cannot separate vocative from nominative.",
            "HYPOTHESIS to test: citation formulae (γέγραπται, λέγει) and rhetorical οὐκ οἴδατε introduce support "
            "inside a unit and are weak boundary signals.",
            "HYPOTHESIS to test: the epistolary frame (prescript, salutation, thanksgiving, greetings, benediction) "
            "brackets the body; the thanksgiving verb also stands outside the frame, so the verb alone does not "
            "mark it.",
            "HYPOTHESIS to test: question openers (τί οὖν, τί γάρ, μὴ γένοιτο) step an argument within a unit.",
        ],
        "dan_key_crosswalk": None,
        "for_fable_end_review": None,
        "attribution": {
            "greek": ("Greek witnesses: Robinson-Pierpont Byzantine Textform (Unlicense), primary; SBLGNT (CC BY 4.0), "
                      "secondary; their attribution terms travel with any quotation"),
            "english": "World English Bible (WEB); its attribution terms travel with any quotation",
        },
    }
    fz = {n: (e["count_rp"], e["count_sbl"]) for n, e in formulae.items()}
    out["dan_key_crosswalk"] = crosswalk(fz, omap, hebrew, formulae)
    out["for_fable_end_review"] = fable_items(formulae, cands, totals, position_census)
    out["for_fable_end_review"].insert(len(out["for_fable_end_review"]) - 1, {
        "item": "frame edges (orchestrator amendment)",
        "measurement": "FRAME_PAIRS %s; FRAME_IN_BODY_PAIRS %s; edges %s" % (
            csc["FRAME_PAIRS"], csc["FRAME_IN_BODY_PAIRS"], csc["FRAME_edges"]),
        "question": "are the opening (before the first appeal) and closing (from the first closing frame hit) edges the right frame extent for an onset family?"})

    # ---- remaining self-assertions over the finished output
    listed = {"rp": set(), "sbl": set()}

    def walk(o):
        ok = True
        if isinstance(o, dict):
            for w in ("rp", "sbl"):
                if "count_" + w in o and "verses_" + w in o:
                    vs = o["verses_" + w]
                    ok &= o["count_" + w] == len(vs) and len(set(vs)) == len(vs)
                    listed[w].update(vs)
            if "count" in o and "verses" in o:
                ok &= o["count"] == len(o["verses"]) and len(set(o["verses"])) == len(o["verses"])
                listed["rp"].update(o["verses"])
            for v in o.values():
                ok &= walk(v)
        elif isinstance(o, list):
            for v in o:
                ok &= walk(v)
        return ok
    A.append(("every count equals the length of its verse list (and no list repeats a verse)", walk(out)))
    A.append(("every verse listed exists in the witness it is listed for",
              listed["rp"] <= rset["rp"] and listed["sbl"] <= rset["sbl"] and len(listed["rp"]) > 0
              and all(c["verse"] in rset["rp"] for c in cands)))
    A.append(("every WEB quotation is found byte-exact in 1Cor_web_clean.txt",
              all(q and q in wtext for q in web_quotes)))
    out["self_assertions"] = [{"assertion": n, "holds": bool(ok)} for n, ok in A]
    return out, A


def crosswalk(fz, omap, hebrew, formulae):
    c = lambda n: "RP %d / SBLGNT %d" % fz[n]
    top = [
        ("book", "book", "same role; value '1Cor'"),
        ("produced_by", "produced_by", "same role and shape"),
        ("witness", "witness", "TWO witnesses (RP primary, SBLGNT secondary, OW-31) and the WEB face, not one"),
        ("numbering", "numbering", "same role; identity, measured: web_greek_offset_map.json identity_throughout="
                                   f"{omap['identity_throughout']}, zones={len(omap['zones'])}"),
        ("numbering_face", "numbering_face", "'WEB' (equal to the Greek face), not Daniel's 'MT'"),
        ("numbering_face_obligation_on_consumers", "numbering_face_obligation_on_consumers", "same role"),
        ("method", "method", "Greek skeleton words matched word-bounded, with position classes; not Hebrew regex"),
        ("inputs", "inputs", "same role ({path: sha256})"),
        ("web_format", "web_format", "same role"),
        ("totals", "totals", "same role; adds rp_sbl_differing_verses and the SBLGNT sign census; no language split"),
        ("datelines", None, f"no 1 Corinthians counterpart: the year noun ἔτος measures {c('year_word')} verses; "
                            "the letter carries no regnal or calendar dateline"),
        ("year_word_but_not_a_dateline", "formulae.year_word", f"kept as a measured control ({c('year_word')})"),
        ("calendar_dates_not_datelines", None,
         f"no month+day date: month noun {c('month_word')}; the calendar REFERENCES are kept as controls "
         f"(first_of_the_week {c('first_of_the_week')}, pentecost {c('pentecost')}, pascha {c('pascha')}) and are "
         "named for the Fable end review, not made constants"),
        ("month_or_day_word_not_a_date", "formulae.day_word / formulae.month_word",
         f"day noun {c('day_word')}, month noun {c('month_word')}; recorded as controls"),
        ("month_or_day_substring_artifacts", "formulae.*.substring_reading",
         "generalised: every formula reports its substring count and its substring-only verses"),
        ("date_family_patterns", None, "no date family; every formula carries its own pattern"),
        ("formulae", "formulae", "per formula: pattern (skeleton word sequences), count_rp/verses_rp, "
                                 "count_sbl/verses_sbl, witness_disagreements, positions, quotes; no language field"),
        ("language_switches", None, f"single language (Koine Greek); Hebrew-block characters measured {hebrew}. "
                                    f"The Aramaic μαρὰν ἀθά stands in Greek letters (maranatha {c('maranatha')}); "
                                    "named for the Fable end review, not a switch"),
        ("citation_sweep_constants", "citation_sweep_constants",
         "DATELINE_PAIRS / CAL_DATE_PAIRS / CAL_NO_ONSET are replaced by <FAMILY>_PAIRS, <FAMILY>_SBL_ONLY_PAIRS, FRAME_IN_BODY_PAIRS and "
         "DEVICE_NO_ONSET (empty); face WEB = Greek"),
        ("how_these_are_used", "how_these_are_used", "same role; rules separated from hypotheses to test"),
        ("ezek_key_crosswalk", "dan_key_crosswalk", "same role, one book on"),
        ("for_fable_end_review", "for_fable_end_review", "same role"),
        ("attribution", "attribution", "keys greek / english, not hebrew_aramaic / english"),
        ("self_assertions", "self_assertions", "same role and shape"),
        (None, "paragraph_marks", "new: RP pilcrows and WEB paragraph starts with their overlap (Daniel had none)"),
        (None, "position_census", "new: per-witness count of words in each position class"),
        (None, "reading_candidates", "new: the orchestrator's reading candidates, classified from bytes"),
    ]
    fam = [
        ("ezek_* (Ezekiel's eleven, run on Daniel's Hebrew)", None,
         f"not run: Hebrew-script patterns cannot occur in a Greek witness (Hebrew-block characters {hebrew})"),
        ("first-person report (i_daniel_*, i_nebuchadnezzar_aram)", "ego_paulos / prescript_paulos",
         f"ἐγὼ Παῦλος {c('ego_paulos')}; the prescript {c('prescript_paulos')}"),
        ("vision formulae (i_saw_*, vision nouns, behold_*)", "idou",
         f"no vision report; ἰδού {c('idou')} kept as the 'behold' analogue"),
        ("speech introductions (answered_and_said_*, and_he_said_*, court greeting, decree)",
         "citation family (gegraptai, legei, ho_nomos_legei)",
         f"an analogue, not an equivalent: γέγραπται {c('gegraptai')}, λέγει {c('legei')}"),
        ("doxologies and ascriptions (blessed_*, everlasting_*, most_high, recognition refrain)",
         "frame family (grace_benediction, amen) / charis_to_theo",
         f"benediction {c('grace_benediction')}, ἀμήν {c('amen')}, τῷ δὲ θεῷ χάρις {c('charis_to_theo')}"),
        ("transitions (at_that_time_*, vayehi_heb, then_aram, after_this_aram)", "topic_marker / question families",
         f"περὶ δέ at a sentence start {c('peri_de_topic_marker')}; τί οὖν {c('ti_oun')}"),
        ("address and direction (son_of_man_*, fear_not_heb, set_face_heb)", "vocative family",
         f"ἀδελφοί (no article) {c('adelphoi_no_article')}; ἀγαπητοί {c('agapetoi')}"),
    ]
    fields = [
        ("language", None, "one language"), ("pattern", "pattern", "skeleton word sequences, not a regex"),
        ("count", "count_rp / count_sbl", "per witness"), ("verses_mt", "verses_rp / verses_sbl", "WEB = Greek refs"),
        ("cross_language_hits", "witness_disagreements", "the cross-witness comparison replaces the cross-language one"),
    ]
    return {"top_level": [{"dan_key": a, "cor_key": b, "reason": r} for a, b, r in top],
            "formula_families": [{"dan_family": a, "cor_key": b, "reason": r} for a, b, r in fam],
            "formula_entry_fields": [{"dan_field": a, "cor_field": b, "reason": r} for a, b, r in fields]}


def fable_items(formulae, cands, totals, pc):
    f = formulae
    pos_dis = sorted({d["verse"] for e in f.values() for d in e["witness_disagreements"]
                      if d["cause"].startswith("position")}, key=vk)
    word_dis = sorted({d["verse"] for e in f.values() for d in e["witness_disagreements"]
                       if d["cause"].startswith("wording")}, key=vk)
    return [
        {"item": "sentence-start rests on edition punctuation",
         "measurement": (f"περὶ δέ any position RP {f['peri_de']['count_rp']}, at a sentence start RP "
                         f"{f['peri_de_topic_marker']['count_rp']} / SBLGNT {f['peri_de_topic_marker']['count_sbl']}, "
                         f"inside a clause RP {f['peri_de_internal']['count_rp']}; position-only witness "
                         f"disagreements over all formulae fall in {len(pos_dis)} verses: {pos_dis}"),
         "question": "is an edition's punctuation an acceptable basis for the topic-marker class, or must position "
                     "be read from syntax?"},
        {"item": "vocative versus nominative ἀδελφοί",
         "measurement": (f"ἀδελφοί any reading RP {f['adelphoi']['count_rp']}, without a preceding article RP "
                         f"{f['adelphoi_no_article']['count_rp']}"),
         "question": "is the article rule an adequate vocative test for a constant, or should the vocative family "
                     "stay evidence only?"},
        {"item": "witness disagreements on a hit",
         "measurement": f"wording-caused disagreements over all formulae fall in {len(word_dis)} verses: {word_dis}",
         "question": "does an RP-only or SBLGNT-only form count for an onset family? (pairs are taken from RP; "
                     "SBLGNT-only hits are listed apart)"},
        {"item": "calendar references in the closing chapter",
         "measurement": (f"first_of_the_week {f['first_of_the_week']['verses_rp']}, pentecost "
                         f"{f['pentecost']['verses_rp']}, pascha {f['pascha']['verses_rp']}; no month+day date"),
         "question": "are these a calendar class for a DEVICE arm, or plain evidence?"},
        {"item": "Aramaic phrase in Greek letters",
         "measurement": f"maranatha RP {f['maranatha']['verses_rp']}, SBLGNT {f['maranatha']['verses_sbl']}",
         "question": "is a transliterated Aramaic acclamation a language-switch class, or a frame formula?"},
        {"item": "thanksgiving verb outside the frame",
         "measurement": f"εὐχαριστῶ RP {f['eucharisto']['verses_rp']}",
         "question": "does THANKSGIVING_PAIRS belong with FRAME_PAIRS, given hits outside the opening?"},
        {"item": "model downgrade",
         "measurement": "this inventory was built and self-checked on claude-opus-5-5 as grader_fallback (OW-25)",
         "question": "the Fable end review is the first non-Opus check of these constants"},
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE))
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    root = Path(a.root).resolve()
    if a.selftest:
        bind(root)
        res = selftest()
        for n, ok in res:
            print(("PASS " if ok else "FAIL ") + n)
        return 0 if all(ok for _, ok in res) else 1
    out, A = build(root)
    data = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    dest = Path(a.out) if a.out else root / "1cor_device_inventory.json"
    dest.write_bytes(data.encode("utf-8"))
    for n, ok in A:
        print(("PASS " if ok else "FAIL ") + n)
    print("sha256", hashlib.sha256(data.encode("utf-8")).hexdigest())
    return 0 if all(ok for _, ok in A) else 1


if __name__ == "__main__":
    sys.exit(main())
