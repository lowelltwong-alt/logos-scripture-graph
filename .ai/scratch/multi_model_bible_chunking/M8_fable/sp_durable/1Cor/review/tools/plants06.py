import json,sys,copy,hashlib,os,re
W=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,W)
sys.argv=["x"]
import cwo06_ref as c
SP=c.SP
rows=[json.loads(l) for l in open(SP+r"\1Cor\fixup\draft_rows_fixup2_applied.jsonl",encoding="utf-8")]
base6=c.sweep06(rows); base7=c.sweep07(rows)
print("base",len(base6),len(base7))
def R(rs,d): return next(r for r in rs if r["decision_id"]==d)
def plant(name,fn,expect):
    rs=copy.deepcopy(rows); fn(rs)
    d6=len(c.sweep06(rs))-len(base6); d7=len(c.sweep07(rs))-len(base7)
    ok=(d6,d7)==expect
    print("PLANT",name,d6,d7,"PASS" if ok else "FAIL expected %s"%(expect,)); return ok
def add(d,f,txt):
    def fn(rs): R(rs,d)[f]+=" "+txt
    return fn
def ref(d,txt):
    def fn(rs): R(rs,d)["boundary_evidence_refs"].append(txt)
    return fn
ok=[]
ok.append(plant("P1 tag-first wording",add("W1-001","strongest_rejected_alternative","rp:1Cor.9.15 Ἐγὼ δὲ οὐδενὶ ἐχρησάμην τούτων."),(1,0)))
ok.append(plant("P2 paren-before sign",add("W6-014","strongest_rejected_alternative","Οὐκ εἰμὶ ἐλεύθερος (rp:1Cor.9.1)."),(1,0)))
ok.append(plant("P3 paren-after sign",add("W5-008","boundary_rationale","rp:1Cor.10.11 (Ταῦτα δὲ) applies it."),(1,0)))
ok.append(plant("P4 double-quoted",add("W1-004","boundary_rationale",'rp:1Cor.14.13 "Διόπερ" opens.'),(1,0)))
ok.append(plant("P5 ref tag",ref("W1-001","rp:1Cor.7.12 [WARRANT-close:far] Τοῖς δὲ λοιποῖς ἐγὼ λέγω"),(1,0)))
def p6(rs):
    r=R(rs,"W1-001"); r["device_notes"]+=" sbl:1Cor.9.1-1Cor.9.3 differs."; r["boundary_rationale"]+=" Οὐκ εἰμὶ ἐλεύθερος (rp:1Cor.9.1)."
ok.append(plant("P6 range only stays open",p6,(1,0)))
def p7(rs):
    r=R(rs,"W1-001"); r["device_notes"]+=" sbl:1Cor.9.1 differs."; r["boundary_rationale"]+=" Οὐκ εἰμὶ ἐλεύθερος (rp:1Cor.9.1)."
ok.append(plant("P7 exact token clears",p7,(0,0)))
ok.append(plant("P8 unsigned shared words clear",add("W1-001","boundary_rationale","rp:1Cor.7.10 (Τοῖς δὲ γεγαμηκόσιν παραγγέλλω)."),(0,0)))
def p9(rs):
    r=R(rs,"W6-014")
    for f in("boundary_rationale","device_notes"):
        r[f]=r[f].replace("sbl:1Cor.16.24","").replace("16:24","")
    r["boundary_evidence_refs"]=[x for x in r["boundary_evidence_refs"] if "16.24" not in x]
ok.append(plant("P9 site listing removed",p9,(0,1)))
def p10(rs): R(rs,"W1-007")["observed_substrate_signals"].append("SBL variant sites at 2:7, 2:9, 2:11, 2:13 and 2:15")
ok.append(plant("P10 OSS listing clears",p10,(0,-5)))
print("plants",sum(ok),"of",len(ok))
print("sha",hashlib.sha256(open(W+r"\cwo06_ref.py","rb").read()).hexdigest())
RP,SBL=c.RP,c.SBL
F="""r1.4 Εὐχαριστῶ τῷ θεῷ μου πάντοτε|r1.26 τὴν κλῆσιν ὑμῶν|r3.4 οὐχὶ σαρκικοί ἐστε|s3.4 ⸂οὐκ ἄνθρωποί⸃ ἐστε|s3.1 ⸀σαρκίνοις|s3.1 ⸂λαλῆσαι ὑμῖν⸃|r3.5 Τίς οὖν ἐστιν|s3.5 τί οὖν|r3.12 Εἰ δέ τις|r3.14 εἴ τινος|r3.15 εἴ τινος|r3.17 εἴ τις|r3.18 εἴ τις|r4.1 ἡμᾶς|r4.3 Ἐμοὶ|r4.3 ἀνακριθῶ|r4.3 ἀνακρίνω|r4.4 ἀνακρίνων|r4.5 κρίνετε|r4.6 ὑπὲρ ὃ γέγραπται φρονεῖν|s4.6 Μὴ ὑπὲρ ⸀ἃ ⸀γέγραπται|r5.6 Οὐ καλὸν τὸ καύχημα ὑμῶν|r5.13 ἐξαρεῖτε|s5.13 ⸀ἐξάρατε|r5.13 κρινεῖ|s5.13 ⸀κρίνει|r6.1 ἀδίκων|r6.7 ἀδικεῖσθε|r6.8 ἀδικεῖτε|r6.9 ἄδικοι|r6.19 Ἢ οὐκ οἴδατε|s7.1 ⸀ἐγράψατε|r6.16 φησίν|r7.8 ὡς κἀγώ|r7.7 ὡς καὶ ἐμαυτόν|r7.8 καλὸν|r7.1 Καλὸν|r7.11 καὶ ἄνδρα γυναῖκα μὴ ἀφιέναι|s7.12 ⸂λέγω ἐγώ⸃|r7.15 κέκληκεν|r7.17 κέκληκεν|r7.34 Μεμέρισται|s7.34 ⸀καὶ μεμέρισται|s7.34 ⸂ἡ ἄγαμος|s7.35 ⸀σύμφορον|s7.38 ⸀γαμίζων|s7.38 ⸂τὴν παρθένον ἑαυτοῦ⸃|s7.38 ⸀ποιήσει|s7.39 Γυνὴ ⸀δέδεται|r9.24 πάντες μὲν τρέχουσιν, εἷς δὲ λαμβάνει|r10.5 Ἀλλ’ οὐκ ἐν τοῖς πλείοσιν|r9.27 ἀδόκιμος γένωμαι|r9.26 Ἐγὼ τοίνυν|s9.23 ⸀πάντα δὲ ποιῶ|s10.1 ⸀γὰρ|r10.1 Οὐ θέλω δὲ|r10.1 ἀγνοεῖν|r12.1 ἀγνοεῖν|s10.11 ⸀δὲ|s9.15 ⸂οὐ κέχρημαι οὐδενὶ⸃|s9.3 ⸂ἐστιν αὕτη⸃|r9.1 Οὐκ εἰμὶ ἀπόστολος|s9.1 Οὐκ εἰμὶ ⸂ἐλεύθερος|s9.18 ⸀μού|s10.23 ⸀Πάντα ἔξεστιν|s11.2 Ἐπαινῶ δὲ ⸀ὑμᾶς|r11.2 ἀδελφοί|s11.3 ⸀τοῦ|s11.5 ⸀αὐτῆς|s11.7 ⸀ἡ|s11.15 ⸀δέδοται|s11.19 ⸀καὶ|s11.25 ⸀ἐὰν|s11.31 εἰ ⸀δὲ|s11.32 ⸀ὑπὸ|s11.34 ⸀εἴ τις|r11.11 Πλὴν|r11.12 Ὥσπερ γὰρ|r11.8 γυνὴ ἐξ ἀνδρός|r11.12 ἡ γυνὴ ἐκ τοῦ ἀνδρός|r11.9 διὰ τὸν ἄνδρα|r11.12 διὰ τῆς γυναικός|r11.13 ὑμῖν|r11.13 ἀκατακάλυπτον|r11.5 ἀκατακαλύπτῳ|r12.8 κατὰ τὸ αὐτὸ πνεῦμα|r12.9 ἐν τῷ αὐτῷ πνεύματι|s12.9 ⸀ἑνὶ πνεύματι|r12.11 πάντα δὲ ταῦτα|r12.21 Οὐ δύναται δὲ ὁ ὀφθαλμὸς εἰπεῖν τῇ χειρί|r12.13 ἐν ἑνὶ πνεύματι|s12.28 ⸀ἔπειτα|r12.31 Ζηλοῦτε|r14.1 ζηλοῦτε|r14.39 ζηλοῦτε|s13.8 ⸀πίπτει|r14.6 Νυνὶ δέ, ἀδελφοί|s14.6 ⸀Νῦν δέ|r14.9 Οὕτως καὶ ὑμεῖς|r14.12 Οὕτως καὶ ὑμεῖς|s14.13 ⸀Διὸ|s14.28 ⸀διερμηνευτής|r14.35 γυναιξὶν|s14.35 γυναικὶ|r14.34 ἀλλ’ ὑποτάσσεσθαι|s14.34 ἀλλὰ ⸀ὑποτασσέσθωσαν|r14.28 σιγάτω|r14.30 σιγάτω|r14.34 σιγάτωσαν|r14.32 ὑποτάσσεται|r15.29 ποιήσουσιν|r15.29 βαπτίζονται|r15.31 ὑμετέραν|r15.15 νεκροὶ οὐκ ἐγείρονται|r15.16 νεκροὶ οὐκ ἐγείρονται|r15.29 νεκροὶ οὐκ ἐγείρονται|r15.32 νεκροὶ οὐκ ἐγείρονται|r15.50 Τοῦτο δέ φημι, ἀδελφοί, ὅτι|r15.50 φθορὰ|r15.50 ἀφθαρσίαν|r16.2 ἔλθω|r16.3 παραγένωμαι|r16.3 πέμψω|r16.4 κἀμὲ πορεύεσθαι|r16.5 Ἐλεύσομαι|r16.6 πορεύωμαι|r16.1 λογίας|r16.2 λογίαι|r16.3 χάριν|r16.11 ἐκδέχομαι γὰρ αὐτὸν μετὰ τῶν ἀδελφῶν|r16.12 μετὰ τῶν ἀδελφῶν|r16.12 ἵνα ἔλθῃ|r16.12 θέλημα|r16.12 πρὸς ὑμᾶς|r16.14 Πάντα ὑμῶν ἐν ἀγάπῃ γινέσθω|r14.26 Πάντα πρὸς οἰκοδομὴν γενέσθω|r14.40 Πάντα εὐσχημόνως καὶ κατὰ τάξιν γινέσθω|s16.17 ὅτι τὸ ⸀ὑμέτερον ὑστέρημα|r16.17 Φουρτουνάτου|s16.17 Φορτουνάτου|r16.20 Ἀσπάσασθε ἀλλήλους|r16.16 τοῖς τοιούτοις|r16.18 τοὺς τοιούτους|r16.15 Στεφανᾶ|r16.17 Στεφανᾶ|s16.19 ⸀Πρίσκα|r16.19 Πρίσκιλλα|r16.23 Ἡ χάρις|r16.24 Ἡ ἀγάπη μου|r16.24 μετὰ πάντων ὑμῶν|s16.22 ⸀κύριον"""
bad=[]
for x in F.split("|"):
    v,s=x.split(" ",1); w,vv=v[0],"1Cor."+v[1:]
    if s not in (RP if w=="r" else SBL).get(vv,""): bad.append(x)
print("facts",len(F.split("|")),"failed",len(bad)); print(bad)
for k in ("1Cor.3.14","1Cor.3.15","1Cor.7.34","1Cor.11.9","1Cor.14.40","1Cor.16.1","1Cor.16.2"):
    print(k,"R",RP[k][:150]); print(k,"S",SBL[k][:150])
print("13.7 diff","1Cor.13.7" in c.DIFF, "13.7 site","1Cor.13.7" in c.SITES)
import unicodedata
nw=[(v) for v in RP if any(t in c.toks(RP[v]) for t in c.toks("σῶμα σώματος σώματι σώματα μέλη μέλος"))]
print([v[5:] for v in nw if v.startswith("1Cor.12.")][:8])
