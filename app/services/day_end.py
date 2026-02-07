from datetime import date

def run_day_end(db):
    return {
        "date": str(date.today()),
        "status": "DAY_END_OK",
        "note": "Stock aggregation temporarily disabled",
        "sections": []
    }
