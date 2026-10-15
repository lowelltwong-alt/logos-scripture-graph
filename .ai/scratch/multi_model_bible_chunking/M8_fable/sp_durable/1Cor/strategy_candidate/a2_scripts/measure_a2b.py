import re, sys
sys.stdout.reconfigure(encoding="utf-8")
from web_lib import load_web
web = load_web()
def key(r): c, v = r.split(":"); return (int(c), int(v))
print("verses", len(web))
for r, s in (("1:17", "For Christ sent me not to baptize"), ("4:14", "I don\u2019t write these things"),
             ("7:12", "I\u2014not the Lord\u2014"), ("14:37", "If any man thinks")):
    print(r, repr(s), "in verse:", s in web[r], "| book hits:", sorted((x for x, t in web.items() if s in t), key=key))
for pat in (r"\bknow\b", "perfect", "complete"):
    print(pat, sorted((r for r, t in web.items() if re.search(pat, t, re.I)), key=key)[:40])
for r in ("6:2", "6:3", "13:10"): print(r, web[r][:200])
