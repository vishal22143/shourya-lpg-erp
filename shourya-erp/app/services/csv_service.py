import csv
import io
from sqlalchemy.orm import Session
from app.models.models import DeliveryPool, DeliveryStatus
from datetime import date


def import_csv(db: Session, file_content: bytes, erp_date: date, uploaded_by: int) -> dict:
    """
    Import BPCL delivery CSV.
    Rules:
    - Already DELIVERED entries are never overwritten
    - Duplicate consumer_no on same date = flagged is_duplicate=True
    - Can be uploaded multiple times safely
    """
    content = file_content.decode("utf-8-sig")  # handle BOM
    reader = csv.DictReader(io.StringIO(content))

    imported = 0
    skipped_delivered = 0
    duplicates = 0

    # Get consumer numbers already delivered today
    delivered_nos = {
        r.consumer_no for r in
        db.query(DeliveryPool).filter(
            DeliveryPool.erp_date == erp_date,
            DeliveryPool.status.in_([DeliveryStatus.DELIVERED, DeliveryStatus.DELIVERED_EMERGENCY])
        ).all()
    }

    # Get all existing consumer numbers for today (for duplicate detection)
    existing = {
        r.consumer_no: r for r in
        db.query(DeliveryPool).filter(DeliveryPool.erp_date == erp_date).all()
    }

    for row in reader:
        # Normalize column names (BPCL CSV has varied headers)
        consumer_no   = str(row.get("Consumer No", row.get("ConsumerNo", row.get("CONSUMER_NO", "")))).strip()
        consumer_name = str(row.get("Consumer Name", row.get("Name", row.get("CONSUMER_NAME", "")))).strip()
        address       = str(row.get("Address", row.get("ADDRESS", ""))).strip()
        mobile        = str(row.get("Mobile", row.get("MOBILE", row.get("Mobile No", "")))).strip()
        area          = str(row.get("Area", row.get("AREA", row.get("Route", "")))).strip()
        booking_type  = str(row.get("Booking Type", row.get("BookingType", "REGULAR"))).strip()
        product_code  = str(row.get("Product Code", row.get("ProductCode", "5350"))).strip()

        if not consumer_no:
            continue

        # Never overwrite a delivered entry
        if consumer_no in delivered_nos:
            skipped_delivered += 1
            continue

        if consumer_no in existing:
            # Update non-delivered existing record
            rec = existing[consumer_no]
            rec.consumer_name = consumer_name or rec.consumer_name
            rec.address       = address or rec.address
            rec.mobile        = mobile or rec.mobile
            rec.area          = area or rec.area
            rec.booking_type  = booking_type
            duplicates += 1
        else:
            rec = DeliveryPool(
                erp_date=erp_date,
                consumer_no=consumer_no,
                consumer_name=consumer_name,
                address=address,
                mobile=mobile,
                area=area,
                booking_type=booking_type,
                product_code=product_code or "5350",
                status=DeliveryStatus.SCHEDULED,
            )
            db.add(rec)
            imported += 1

    db.commit()
    return {
        "imported": imported,
        "updated": duplicates,
        "skipped_delivered": skipped_delivered,
        "total_today": db.query(DeliveryPool).filter(DeliveryPool.erp_date == erp_date).count()
    }


def get_deliveries_for_trip(db: Session, erp_date: date, area: str = None):
    q = db.query(DeliveryPool).filter(
        DeliveryPool.erp_date == erp_date,
        DeliveryPool.status == DeliveryStatus.SCHEDULED
    )
    if area:
        q = q.filter(DeliveryPool.area == area)
    return q.all()
