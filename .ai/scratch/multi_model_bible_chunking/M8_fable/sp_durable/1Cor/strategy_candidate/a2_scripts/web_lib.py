"""Load 1Cor_web_clean.txt (chapter headers '===== 1COR C =====', verse lines '[v] N text', other lines skipped)."""
import re
SP = "C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable/1Cor/"
def load_web():
    out, c = {}, None
    for l in open(SP + "1Cor_web_clean.txt", encoding="utf-8").read().splitlines():
        m = re.match(r"^=+ 1COR (\d+) =+$", l)
        if m: c = int(m.group(1)); continue
        m = re.match(r"^\[v\] (\d+) (.*)$", l)
        if m: out["%d:%s" % (c, m.group(1))] = m.group(2)
    return out
