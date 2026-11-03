"""Derive the E5 launch-message template from the E4 message bytes, so the required lines stay byte-identical."""
from pathlib import Path
HERE = Path(__file__).resolve().parent
SP = HERE.parents[2]
src = (SP / "1Cor/review/primaries/messages/launch_message_CTL_E4.txt").read_text(encoding="utf-8")
out = []
for line in src.split("\n"):
    if line.startswith("BRIEF: "):
        line = "BRIEF: @@BRIEF@@ sha256 @@BRIEF_SHA@@"
    elif line.startswith("EFFICIENCY-OUT: "):
        line = line.replace("cor_ctl4", "cor_ctl5")
    out.append(line)
t = "\n".join(out)
if "cor_ctl4" in t or "BRIEF_E4" in t:
    raise SystemExit("REFUSED: E4 reference survives")
(HERE / "launch_message_E5.template.txt").write_bytes(t.encode("utf-8"))
print("template", len(t))
