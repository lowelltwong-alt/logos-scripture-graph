import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path
w = json.loads((Path(__file__).resolve().parent.parent / "work_orders.json").read_text(encoding="utf-8"))
for d in w["boss_docket"]:
    txt = str(d.get("remedy") or d.get("question"))
    print(f"{d.get('cluster')}/{d.get('row_id')} [{d.get('ruling')}/{d.get('severity')}]:")
    print("  " + txt[:420].replace("\n", " "))
    print()
