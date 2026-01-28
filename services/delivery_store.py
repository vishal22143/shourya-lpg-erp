import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path('data/deliveries.json')

def _load():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def is_delivered(cashmemo):
    data = _load()
    return cashmemo in data and data[cashmemo]['status'].startswith('Delivered')

def mark_status(cashmemo, status, driver=None, gps=None):
    data = _load()
    data[cashmemo] = {
        'status': status,
        'driver': driver,
        'gps': gps,
        'timestamp': datetime.now().isoformat()
    }
    _save(data)

def get_all():
    return _load()
