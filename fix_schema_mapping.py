"""
ONE-TIME SCHEMA ALIGNMENT FIX
- Uses existing DB tables
- No table creation
- No migrations
- Shell-safe
"""

from pathlib import Path

ROOT = Path(__file__).parent

# 1) Fix ORM table name (map legacy name to existing table)
model_candidates = [
    ROOT / "app" / "models" / "stock_movement.py",
    ROOT / "app" / "models" / "stock_movements.py",
    ROOT / "app" / "models" / "movement.py",
]

for p in model_candidates:
    if p.exists():
        txt = p.read_text()
        if "stock_movements" in txt:
            txt = txt.replace("stock_movements", "godown_events")
            p.write_text(txt)
            print(f"UPDATED ORM TABLE IN: {p}")
        else:
            print(f"NO CHANGE NEEDED IN: {p}")

# 2) Fix day-end service queries
service = ROOT / "app" / "services" / "day_end.py"
if service.exists():
    txt = service.read_text()
    if "stock_movements" in txt:
        txt = txt.replace("stock_movements", "godown_events")
        service.write_text(txt)
        print("UPDATED day_end SERVICE")
    else:
        print("day_end SERVICE OK")
else:
    print("day_end SERVICE NOT FOUND")

print("SCHEMA ALIGNMENT COMPLETE")
