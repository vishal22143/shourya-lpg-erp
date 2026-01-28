from utils.bpcl_csv import read_bpcl_scheduled_list
from services.delivery_store import is_delivered

def get_pending_scheduled(csv_path):
    all_items = read_bpcl_scheduled_list(csv_path)
    return [d for d in all_items if not is_delivered(d['cashmemo'])]
