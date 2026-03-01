#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shourya Bharatgas Services — LPG ERP System
BPCL Distributor: 187618 | Jaysinghpur, Kolhapur
Author: Shourya ERP v5
Run: python app.py
"""
import os
from flask import Flask, render_template_string, session

app = Flask(__name__)
app.secret_key = "ShBhERP2026$SecretKey@Kolhapur"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload

# ── Initialize DB ──────────────────────────────────────────────
from db import init_db
with app.app_context():
    init_db()

# ── Register all route modules ─────────────────────────────────
from routes1 import register_routes_1
from routes2 import register_routes_delivery
from routes3 import register_routes_godown, register_routes_bda
from routes4 import register_routes_wages, register_routes_accounting, register_routes_bpcl_dayend
from routes5 import register_routes_users, register_routes_settings, register_routes_chat

register_routes_1(app)
register_routes_delivery(app)
register_routes_godown(app)
register_routes_bda(app)
register_routes_wages(app)
register_routes_accounting(app)
register_routes_bpcl_dayend(app)
register_routes_users(app)
register_routes_settings(app)
register_routes_chat(app)

# ── Template globals ───────────────────────────────────────────
@app.context_processor
def inject_globals():
    return dict(session=session)

if __name__ == "__main__":
    print("=" * 55)
    print("  Shourya Bharatgas ERP — Starting...")
    print("  Open: http://localhost:5000")
    print("  Mobile: http://<your-ip>:5000")
    print("  Default PIN: 1234 (must change on first login)")
    print("=" * 55)
    app.run(host="0.0.0.0", port=5000, debug=True)
