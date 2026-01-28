from services.delivery_store import mark_status

def start_trip(cashmemo, driver=None):
    mark_status(cashmemo, 'In Trip', driver)

def deliver_otp(cashmemo, driver=None):
    mark_status(cashmemo, 'Delivered (OTP)', driver)

def deliver_emergency(cashmemo, driver=None):
    mark_status(cashmemo, 'Delivered (Emergency)', driver)

def cancel_delivery(cashmemo, driver=None):
    mark_status(cashmemo, 'Cancelled', driver)
