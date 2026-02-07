from pathlib import Path

ROOT = Path(__file__).parent / "app"
changed = []

for py in ROOT.rglob("*.py"):
    txt = py.read_text(encoding="utf-8", errors="ignore")
    if "stock_movements" in txt:
        txt2 = txt.replace("stock_movements", "godown_events")
        py.write_text(txt2, encoding="utf-8")
        changed.append(str(py))

print("FILES UPDATED:")
for c in changed:
    print(" -", c)

if not changed:
    print("NO FILES NEEDED CHANGES")
