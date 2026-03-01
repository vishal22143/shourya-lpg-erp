#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes Part 1: Auth + Dashboard + Office — Shourya Bharatgas ERP"""
from flask import request, redirect, session, jsonify, make_response, flash
import csv, io, json, os, datetime

from db import (get_db, hpin, today, now_ts, this_month,
                add_stock, stock_bal, full_stock, add_cash, cash_summary,
                advance_balance, accessory_bal, cyl_price, gsetting,
                BDA_MAP, VEHICLES, WAGE_URBAN, WAGE_RURAL, WAGE_PAIR)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def d(*a,**k):
        if "uid" not in session: return redirect("/login")
        return f(*a,**k)
    return d

def roles(*rlist):
    from functools import wraps
    def dec(f):
        @wraps(f)
        def d(*a,**k):
            if session.get("role") not in rlist:
                flash("Access denied","danger"); return redirect("/dashboard")
            return f(*a,**k)
        return d
    return dec

def register_routes_1(app):
    from templates import BASE, LOGIN_PAGE, CHANGE_PIN_PAGE
    from flask import render_template_string

    def R(tpl, **ctx):
        ctx.setdefault("active","")
        full = BASE.replace("{% block body %}{% endblock %}",tpl)\
                   .replace("{% block scripts %}{% endblock %}",ctx.pop("scripts",""))
        return render_template_string(full, **ctx)

    # ── AUTH ────────────────────────────────────────────────────
    @app.route("/")
    def index():
        return redirect("/dashboard" if "uid" in session else "/login")

    @app.route("/login", methods=["GET","POST"])
    def login():
        error=""
        if request.method=="POST":
            mob = request.form.get("mobile","").strip()
            pin = request.form.get("pin","").strip()
            c   = get_db()
            u   = c.execute("SELECT * FROM users WHERE mobile=? AND is_active=1",(mob,)).fetchone()
            c.close()
            if u and u["pin_hash"]==hpin(pin):
                session.update(uid=u["id"],role=u["role"],name=u["name"],bda_id=u["bda_id"])
                return redirect("/change-pin" if u["must_change_pin"] else "/dashboard")
            error="❌ चुकीचा मोबाईल किंवा PIN / Wrong mobile or PIN"
        return render_template_string(LOGIN_PAGE, error=error)

    @app.route("/change-pin", methods=["GET","POST"])
    @login_required
    def change_pin():
        error=""
        if request.method=="POST":
            p1,p2 = request.form.get("pin1",""),request.form.get("pin2","")
            if p1!=p2: error="PINs जुळत नाहीत / PINs don't match"
            elif len(p1)<4: error="PIN किमान 4 अंक हवेत"
            else:
                c=get_db()
                c.execute("UPDATE users SET pin_hash=?,must_change_pin=0 WHERE id=?",(hpin(p1),session["uid"]))
                c.commit(); c.close()
                flash("✅ PIN बदलला!","success")
                return redirect("/dashboard")
        return R(CHANGE_PIN_PAGE, error=error)

    @app.route("/logout")
    def logout():
        session.clear(); return redirect("/login")

    # ── DASHBOARD ───────────────────────────────────────────────
    @app.route("/dashboard")
    @login_required
    def dashboard():
        role=session["role"]; t=today(); conn=get_db()
        if role in ["owner","manager","accountant"]:
            return _owner_dash(conn,t,R)
        elif role in ["office"]:
            return _office_dash(conn,t,R)
        elif role in ["delivery","loader","driver"]:
            conn.close(); return redirect("/delivery")
        elif role=="bda":
            conn.close(); return redirect("/bda")
        else:
            conn.close()
            return R("<div class='card'><p>Welcome {{ name }}</p></div>",
                     active="dashboard",name=session.get("name",""))

    def _owner_dash(conn, t, R):
        stock   = full_stock(conn)
        cs      = cash_summary(conn, t)
        tot_d   = conn.execute("SELECT COUNT(*) FROM delivery_pool WHERE date=?",(t,)).fetchone()[0]
        done_d  = conn.execute("SELECT COUNT(*) FROM delivery_pool WHERE date=? AND status IN ('delivered','emergency','spot')",(t,)).fetchone()[0]
        trips   = conn.execute("""SELECT t.*,u.name dm FROM trips t
            JOIN users u ON t.delivery_man_id=u.id WHERE t.date=? ORDER BY t.created_at""",(t,)).fetchall()
        bde     = conn.execute("SELECT * FROM bpcl_day_end WHERE date=?",(t,)).fetchone()
        day     = conn.execute("SELECT * FROM erp_days WHERE date=?",(t,)).fetchone()
        cash_d  = conn.execute("""SELECT entry_type,
            SUM(CASE WHEN direction='in' THEN amount ELSE -amount END) tot
            FROM cash_ledger WHERE date=? GROUP BY entry_type ORDER BY tot DESC""",(t,)).fetchall()
        conn.close()

        TPL = """
<div class="dsb">
  <div class="dsbi"><div class="v">📅 {{ t }}</div><div class="l">तारीख</div></div>
  <div class="dsbi">
    {% if bde %}
      {% if bde.status=='ok' %}<div class="v sok">✅ OK</div>
      {% elif bde.status=='difference' %}<div class="v ser">❌ Difference</div>
      {% else %}<div class="v swn">⏳ Pending</div>{% endif %}
    {% else %}<div class="v swn">⏳ Day End Pending</div>{% endif %}
    <div class="l">BPCL Status</div>
  </div>
  <div class="dsbi"><div class="v">{{ done_d }}/{{ tot_d }}</div><div class="l">Deliveries</div></div>
  <div class="dsbi"><div class="v sok">₹{{ '{:,.0f}'.format(cs.in) }}</div><div class="l">Cash In</div></div>
  <div class="dsbi"><div class="v">₹{{ '{:,.0f}'.format(cs.net) }}</div><div class="l">Net</div></div>
  {% if day and day.is_locked %}<div class="dsbi"><div class="v ser">🔒 Locked</div><div class="l">Day End</div></div>{% endif %}
</div>

<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>📦 14.2 kg साठा / Stock Summary</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    <div class="sgrid">
      <div class="sc"><div class="sn">{{ stock.godown.filled }}</div><div class="sk">गोदाम भरलेले<br>Godown Filled</div></div>
      <div class="sc em"><div class="sn">{{ stock.godown.empty }}</div><div class="sk">गोदाम रिकामे<br>Godown Empty</div></div>
      <div class="sc" style="background:linear-gradient(135deg,#1a5276,#2471a3)"><div class="sn">{{ stock.office.filled }}</div><div class="sk">ऑफिस भरलेले<br>Office Filled</div></div>
      <div class="sc em" style="background:linear-gradient(135deg,#512e5f,#7d3c98)"><div class="sn">{{ stock.office.empty }}</div><div class="sk">ऑफिस रिकामे</div></div>
      {% for bid,bi in bda_map.items() %}
      {% set bl='bda_'+bid|string %}
      <div class="sc" style="background:linear-gradient(135deg,#1e4d2b,#196f3d);font-size:11px">
        <div class="sn" style="font-size:22px">{{ stock.get(bl,{'filled':0,'empty':0}).filled }}/{{ stock.get(bl,{'filled':0,'empty':0}).empty }}</div>
        <div class="sk">{{ bi.village }}<br>भरलेले/रिकामे</div>
      </div>
      {% endfor %}
    </div>
    <div style="margin-top:12px;background:#f0f4f8;border-radius:8px;padding:12px;display:flex;gap:20px;flex-wrap:wrap">
      <div><strong style="font-size:22px">{{ stock.TOTAL.filled }}</strong><br><small>एकूण भरलेले</small></div>
      <div><strong style="font-size:22px">{{ stock.TOTAL.empty }}</strong><br><small>एकूण रिकामे</small></div>
      <div><strong style="font-size:22px">{{ stock.TOTAL.filled+stock.TOTAL.empty }}</strong><br><small>Grand Total</small></div>
    </div>
    <div style="margin-top:8px">
      <a href="/godown" class="btn bo btn-sm">🏭 Godown Details</a>
      <a href="/godown/adjust" class="btn bo btn-sm">📝 Manual Adjust</a>
    </div>
  </div>
</div>

<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>🚚 आजचे Delivery Men / Trips</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    {% for trip in trips %}
    <div style="border:2px solid {% if trip.status=='open' %}#f0ad4e{% else %}#28a745{% endif %};
      border-radius:9px;padding:12px;margin-bottom:9px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
        <div><strong>{{ trip.dm }}</strong>
          <span class="badge {% if trip.status=='open' %}by{% else %}bg{% endif %}">{{ trip.status.upper() }}</span>
          <span class="badge bb">Trip {{ trip.trip_number }}</span>
        </div>
        <a href="/delivery/trip/{{ trip.id }}" class="btn bp btn-sm">▶ Open</a>
      </div>
      <div class="g4">
        <div class="sb" style="padding:8px"><div class="sv" style="font-size:15px">{{ trip.opening_filled }}</div><div class="sl">Opening</div></div>
        <div class="sb g" style="padding:8px"><div class="sv g" style="font-size:15px">{{ trip.total_delivered }}</div><div class="sl">Delivered</div></div>
        <div class="sb" style="padding:8px"><div class="sv" style="font-size:15px">₹{{ '{:,.0f}'.format(trip.cash_collected) }}</div><div class="sl">Cash</div></div>
        <div class="sb" style="padding:8px"><div class="sv" style="font-size:15px">₹{{ '{:,.0f}'.format(trip.online_collected) }}</div><div class="sl">Online</div></div>
      </div>
    </div>
    {% else %}
    <p style="text-align:center;color:var(--mu);padding:20px">आज कोणतीही ट्रिप नाही</p>
    {% endfor %}
  </div>
</div>

<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>💰 Cash Register / रोख नोंद</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <div class="cbig">
      <div class="sl" style="font-size:12px">आजचे एकूण रोख / Today Cash In</div>
      <div class="cam">₹{{ '{:,.0f}'.format(cs.in) }}</div>
      <div style="font-size:13px;opacity:.8;margin-top:6px">
        Out: ₹{{ '{:,.0f}'.format(cs.out) }} &nbsp;|&nbsp; Net: ₹{{ '{:,.0f}'.format(cs.net) }}
      </div>
    </div>
    <div class="tw"><table>
      <tr><th>प्रकार / Type</th><th>रक्कम</th></tr>
      {% for row in cash_d %}
      <tr><td>{{ row.entry_type }}</td><td>₹{{ '{:,.0f}'.format(row.tot) }}</td></tr>
      {% endfor %}
    </table></div>
  </div>
</div>

<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>📊 BPCL Day End / तुलना</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    {% if bde %}
    <div class="cmp">
      <div class="cmpr"><div>Item</div><div>ERP</div><div>BPCL SAP</div></div>
      <div class="cmpr"><div>Opening Filled</div><div>{{ bde.erp_open_filled }}</div><div>{{ bde.bpcl_open_filled }}</div></div>
      <div class="cmpr"><div>Received</div><div>—</div><div>{{ bde.bpcl_received }}</div></div>
      <div class="cmpr"><div>Closing Filled</div>
        <div class="{{ 'der' if bde.diff_filled else 'dok' }}">{{ bde.erp_close_filled }}</div>
        <div>{{ bde.bpcl_close_filled }}</div>
      </div>
    </div>
    {% if bde.diff_filled or bde.diff_empty %}
    <div class="al ald" style="margin-top:10px">❌ Mismatch: Filled={{ bde.diff_filled }}, Empty={{ bde.diff_empty }}</div>
    {% else %}
    <div class="al als" style="margin-top:10px">✅ ERP ↔ BPCL SAP — All OK!</div>
    {% endif %}
    {% else %}
    <div class="al alw">⏳ BPCL Day End नाही.
      <a href="/bpcl-dayend" class="btn bp btn-sm" style="margin-left:8px">Enter Now</a>
    </div>
    {% endif %}
    {% if session.role in ['owner','manager'] %}
    <form action="/office/lock-day" method="post" style="margin-top:10px"
      onsubmit="return confirm('Day End Lock करायचा? बदल होणार नाही!')">
      <button type="submit" class="btn bd btn-sm">🔒 Day End Lock करा</button>
    </form>
    {% endif %}
  </div>
</div>"""
        return R(TPL, active="dashboard", t=t, stock=stock, cs=cs,
                 tot_d=tot_d, done_d=done_d, trips=trips, bde=bde, day=day,
                 cash_d=cash_d, bda_map=BDA_MAP)

    def _office_dash(conn, t, R):
        stock = full_stock(conn); cs = cash_summary(conn,t)
        ms    = conn.execute("SELECT * FROM office_morning_stock WHERE date=?",(t,)).fetchone()
        conn.close()
        TPL = """
<div class="g4">
  <div class="sb g"><div class="sv">{{ stock.office.filled }}</div><div class="sl">ऑफिस भरलेले</div></div>
  <div class="sb"><div class="sv">{{ stock.office.empty }}</div><div class="sl">ऑफिस रिकामे</div></div>
  <div class="sb o"><div class="sv o">₹{{ '{:,.0f}'.format(cs.net) }}</div><div class="sl">आजचे रोख</div></div>
  <div class="sb"><div class="sv">{{ stock.godown.filled }}</div><div class="sl">गोदाम भरलेले</div></div>
</div>
<div style="margin-top:14px;display:flex;gap:10px;flex-wrap:wrap">
  <a href="/office" class="btn bp">🏪 Office Panel</a>
  <a href="/delivery" class="btn bs">🚚 Delivery</a>
  <a href="/godown" class="btn bo">🏭 Godown</a>
</div>"""
        return R(TPL, active="dashboard", stock=stock, cs=cs, ms=ms)

    # ── OFFICE ──────────────────────────────────────────────────
    @app.route("/office")
    @login_required
    @roles("owner","manager","office","accountant")
    def office():
        t=today(); conn=get_db()
        ms    = conn.execute("SELECT * FROM office_morning_stock WHERE date=?",(t,)).fetchone()
        sales = conn.execute("SELECT * FROM office_sales WHERE date=? ORDER BY created_at DESC",(t,)).fetchall()
        stock = full_stock(conn)
        cs    = cash_summary(conn,t)
        bb    = accessory_bal(conn,"blue_book")
        sp    = accessory_bal(conn,"suraksha_pipe")
        dpr   = accessory_bal(conn,"dpr")
        delivs= conn.execute("SELECT * FROM users WHERE role='delivery' AND is_active=1 ORDER BY name").fetchall()
        price = cyl_price()
        conn.close()

        TPL = """
<div class="card">
  <div class="ch"><div class="ct">🏪 ऑफिस पॅनेल <small>Office Operations</small></div></div>
  <div class="g4">
    <div class="sb g"><div class="sv">{{ stock.office.filled }}</div><div class="sl">14.2 kg भरलेले</div></div>
    <div class="sb"><div class="sv">{{ stock.office.empty }}</div><div class="sl">14.2 kg रिकामे</div></div>
    <div class="sb o"><div class="sv o">₹{{ '{:,.0f}'.format(cs.net) }}</div><div class="sl">निव्वळ रोख</div></div>
    <div class="sb p"><div class="sv" style="font-size:18px">{{ bb }}/{{ sp }}/{{ dpr }}</div><div class="sl">BB/SP/DPR</div></div>
  </div>
</div>

<!-- MORNING STOCK -->
<div class="ex">
  <div class="exh {% if not ms %}op{% endif %}" onclick="xToggle(this)">
    <h3>🌅 सकाळचा साठा / Morning Opening Stock</h3><span class="ar">▼</span>
  </div>
  <div class="exb {% if not ms %}sh{% endif %}">
    {% if ms %}
    <div class="al als">✅ साठा नोंदवला — {{ ms.created_at[11:16] }}</div>
    <div class="g4">
      <div class="sb"><div class="sv">{{ ms.f_142 }}</div><div class="sl">14.2 Filled</div></div>
      <div class="sb"><div class="sv">{{ ms.e_142 }}</div><div class="sl">14.2 Empty</div></div>
      <div class="sb"><div class="sv">{{ ms.f_5kg }}</div><div class="sl">5kg Filled</div></div>
      <div class="sb"><div class="sv">{{ ms.e_5kg }}</div><div class="sl">5kg Empty</div></div>
    </div>
    {% else %}
    <form method="post" action="/office/morning-stock">
      <div class="g4">
        <div class="fg"><label>14.2 kg भरलेले</label><input type="number" name="f_142" value="0" min="0"></div>
        <div class="fg"><label>14.2 kg रिकामे</label><input type="number" name="e_142" value="0" min="0"></div>
        <div class="fg"><label>5 kg भरलेले</label><input type="number" name="f_5kg" value="0" min="0"></div>
        <div class="fg"><label>5 kg रिकामे</label><input type="number" name="e_5kg" value="0" min="0"></div>
        <div class="fg"><label>Blue Books</label><input type="number" name="blue_books" value="{{ bb }}" min="0"></div>
        <div class="fg"><label>Suraksha Pipes</label><input type="number" name="suraksha_pipes" value="{{ sp }}" min="0"></div>
        <div class="fg"><label>DPR (Good)</label><input type="number" name="dpr_good" value="{{ dpr }}" min="0"></div>
      </div>
      <button type="submit" class="btn bs">✅ साठा जतन करा</button>
    </form>
    {% endif %}
  </div>
</div>

<!-- CSV UPLOAD -->
<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>📁 BPCL CSV अपलोड / Upload Delivery List</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    <form method="post" action="/office/upload-csv" enctype="multipart/form-data">
      <div class="fg"><label>BPCL Cash Memo CSV</label><input type="file" name="csv_file" accept=".csv" required></div>
      <div class="al ali">CSV अनेक वेळा upload करता येतो. Delivered customers पुन्हा pending होत नाहीत.</div>
      <button type="submit" class="btn bp">📤 Upload करा</button>
    </form>
  </div>
</div>

<!-- CYLINDER SALE -->
<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>🔴 ऑफिस सिलेंडर विक्री / Cylinder Sale</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    <form method="post" action="/office/cylinder-sale">
      <div class="g3">
        <div class="fg"><label>संख्या / Qty</label><input type="number" name="qty" value="1" min="1" required></div>
        <div class="fg"><label>किंमत ₹</label><input type="number" name="price" value="{{ price }}" step="0.01" required></div>
        <div class="fg"><label>Consumer No.</label><input type="text" name="consumer_no" placeholder="Optional"></div>
      </div>
      <div class="fg">
        <label>पेमेंट पद्धत / Payment Mode</label>
        <input type="hidden" name="payment_mode" id="cs_pm" value="cash">
        <div class="pm-row">
          <button type="button" class="pm ac" data-mode="cash" onclick="selPay(this,'cs')">💵 Cash</button>
          <button type="button" class="pm" data-mode="qr" onclick="selPay(this,'cs')">📱 QR Code</button>
          <button type="button" class="pm" data-mode="gpay" onclick="selPay(this,'cs')">🟢 GPay</button>
          <button type="button" class="pm" data-mode="paytm" onclick="selPay(this,'cs')">🔵 Paytm</button>
          <button type="button" class="pm" data-mode="advance" onclick="selPay(this,'cs')">💳 BPCL Advance</button>
          <button type="button" class="pm" data-mode="partial" onclick="selPay(this,'cs')">½ Partial</button>
        </div>
        <div id="cs_cd" style="display:none" class="fg"><label>Cash Amount ₹</label><input type="number" name="cash_amount" step="0.01" placeholder="Cash portion"></div>
        <div id="cs_od" style="display:none" class="fg"><label>Online Amount ₹</label><input type="number" name="online_amount" step="0.01" placeholder="Online portion"></div>
      </div>
      <div class="dc">
        <strong>🪙 नोट मोजणी / Note Count</strong>
        {% for d in [500,200,100,50,20,10] %}
        <div class="dc-row">
          <label>₹{{ d }}</label>
          <input type="number" name="d{{ d }}" id="cs_{{ d }}" value="0" min="0" oninput="denom('cs')">
          <span id="cs_s{{ d }}">₹0</span>
        </div>
        {% endfor %}
        <div class="dc-row"><label>Coins</label><input type="number" name="d_coins" id="cs_coins" value="0" step="0.5" oninput="denom('cs')"><span></span></div>
        <div class="dc-tot"><span>एकूण / Total</span><span id="cs_tot">₹0</span></div>
      </div>
      <div class="fg" style="margin-top:10px"><label>Notes</label><input type="text" name="notes" placeholder="Optional"></div>
      <button type="submit" class="btn bs" style="margin-top:6px">✅ विक्री नोंदवा</button>
    </form>
  </div>
</div>

<!-- ADDITIONAL SALES -->
<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>➕ अतिरिक्त विक्री / Additional Sales</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <form method="post" action="/office/additional-sale">
      <div class="g3">
        <div class="fg"><label>प्रकार / Type</label>
          <select name="sale_type" onchange="updAddPrice(this)">
            <option value="sv" data-price="4000">SV — Subscription Voucher (₹4000)</option>
            <option value="blue_book" data-price="60">Blue Book (₹60)</option>
            <option value="suraksha" data-price="190">Suraksha Pipe (₹190)</option>
            <option value="dpr_paid" data-price="150">DPR — Paid (₹150)</option>
            <option value="dpr_free" data-price="0">DPR — Free</option>
            <option value="5kg" data-price="{{ price }}">5 kg Cylinder</option>
            <option value="name_change" data-price="100">Name Change (+₹100 cash IN)</option>
            <option value="termination" data-price="0">Termination Voucher (cash OUT to customer)</option>
          </select>
        </div>
        <div class="fg"><label>संख्या / Qty</label><input type="number" name="qty" value="1" min="1"></div>
        <div class="fg"><label>किंमत ₹</label><input type="number" name="price" id="add_price" value="4000" step="0.01"></div>
        <div class="fg"><label>Consumer No.</label><input type="text" name="consumer_no" placeholder="Optional"></div>
        <div class="fg"><label>Payment</label>
          <select name="payment_mode">
            <option value="cash">Cash</option><option value="qr">QR</option>
            <option value="gpay">GPay</option><option value="paytm">Paytm</option>
          </select>
        </div>
        <div class="fg"><label>Notes</label><input type="text" name="notes"></div>
      </div>
      <button type="submit" class="btn bp">✅ नोंदवा</button>
    </form>
  </div>
</div>

<!-- STOCK TRANSFER TO DELIVERY MAN -->
<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>🔄 Stock Transfer / ऑफिस → Delivery Man</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <div class="al ali">Note: Transfer = NO wages. Wages only for deliveries to customers.</div>
    <form method="post" action="/office/stock-transfer">
      <div class="g3">
        <div class="fg"><label>डिलिव्हरी मॅन</label>
          <select name="delivery_man_id" required>
            <option value="">Select...</option>
            {% for d in delivs %}<option value="{{ d.id }}">{{ d.name }}</option>{% endfor %}
          </select>
        </div>
        <div class="fg"><label>भरलेले दिले / Filled Given</label><input type="number" name="filled_given" value="0" min="0"></div>
        <div class="fg"><label>रिकामे घेतले / Empty Taken</label><input type="number" name="empty_taken" value="0" min="0"></div>
      </div>
      <button type="submit" class="btn bp">🔄 Transfer करा</button>
    </form>
  </div>
</div>

<!-- EXPENSES -->
<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>💸 Expenses / खर्च</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <form method="post" action="/office/expense">
      <div class="g3">
        <div class="fg"><label>प्रकार / Category</label>
          <select name="category" required>
            <option value="termination_voucher">Termination Voucher (cash to customer)</option>
            <option value="name_change_out">Name Change (if cash out)</option>
            <option value="salary_wages">Salary / Wages</option>
            <option value="stationery_courier">Stationery / Courier</option>
            <option value="diesel">Diesel (GPay)</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div class="fg"><label>रक्कम ₹</label><input type="number" name="amount" step="0.01" required></div>
        <div class="fg"><label>Payment</label>
          <select name="payment_mode"><option value="cash">Cash</option><option value="gpay">GPay</option><option value="online">Online</option></select>
        </div>
      </div>
      <div class="fg"><label>तपशील / Description</label><input type="text" name="description" required></div>
      <button type="submit" class="btn bd">💸 खर्च नोंदवा</button>
    </form>
  </div>
</div>

<!-- ADVANCE -->
<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>🏦 Staff Advance / अग्रिम</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <form method="post" action="/office/advance">
      <div class="g3">
        <div class="fg"><label>कर्मचारी</label>
          <select name="staff_id" required>
            {% for d in delivs %}<option value="{{ d.id }}">{{ d.name }}</option>{% endfor %}
          </select>
        </div>
        <div class="fg"><label>Type</label>
          <select name="advance_type"><option value="given">Given</option><option value="recovered">Recovered</option></select>
        </div>
        <div class="fg"><label>रक्कम ₹</label><input type="number" name="amount" step="0.01" required></div>
      </div>
      <div class="fg"><label>Reason</label><input type="text" name="notes"></div>
      <button type="submit" class="btn bw">🏦 नोंदवा</button>
    </form>
  </div>
</div>

<!-- ACCESSORY STOCK IN -->
<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>📦 Accessory Stock / Blue Book · Suraksha · DPR</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <div class="g3" style="margin-bottom:12px">
      <div class="sb p"><div class="sv">{{ bb }}</div><div class="sl">Blue Books</div></div>
      <div class="sb o"><div class="sv o">{{ sp }}</div><div class="sl">Suraksha Pipes</div></div>
      <div class="sb"><div class="sv">{{ dpr }}</div><div class="sl">DPR Stock</div></div>
    </div>
    <form method="post" action="/office/accessory-in">
      <div class="g3">
        <div class="fg"><label>Item</label>
          <select name="item_type">
            <option value="blue_book">Blue Book (₹60 each)</option>
            <option value="suraksha_pipe">Suraksha Pipe (₹190 each)</option>
            <option value="dpr">DPR</option>
          </select>
        </div>
        <div class="fg"><label>Qty (stock IN from office/month)</label><input type="number" name="qty" min="1" required></div>
      </div>
      <div class="fg"><label>Notes</label><input type="text" name="notes" placeholder="Monthly stock addition"></div>
      <button type="submit" class="btn bp">📦 Stock Add करा</button>
    </form>
  </div>
</div>

<!-- TODAY SALES LOG -->
<div class="card">
  <div class="ch"><div class="ct">📋 आजच्या विक्र्‍या / Today's Sales</div>
    <span style="font-size:13px;color:var(--mu)">Total: ₹{{ '{:,.0f}'.format(sales|sum(attribute='total_amount')) }}</span>
  </div>
  <div class="tw"><table>
    <tr><th>वेळ</th><th>प्रकार</th><th>Qty</th><th>रक्कम</th><th>Mode</th></tr>
    {% for s in sales %}
    <tr>
      <td>{{ s.created_at[11:16] }}</td>
      <td>{{ s.sale_type }}</td>
      <td>{{ s.quantity }}</td>
      <td>₹{{ '{:,.0f}'.format(s.total_amount) }}</td>
      <td><span class="badge bb">{{ s.payment_mode }}</span></td>
    </tr>
    {% else %}
    <tr><td colspan="5" style="text-align:center;color:var(--mu)">No sales today</td></tr>
    {% endfor %}
  </table></div>
</div>"""
        return R(TPL, active="office", stock=stock, ms=ms, cs=cs,
                 sales=sales, bb=bb, sp=sp, dpr=dpr, delivs=delivs, price=price)

    @app.route("/office/morning-stock", methods=["POST"])
    @login_required
    def office_morning_stock():
        t=today(); conn=get_db()
        conn.execute("""INSERT OR REPLACE INTO office_morning_stock
            (date,f_142,e_142,f_5kg,e_5kg,blue_books,suraksha_pipes,dpr_good,entered_by)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (t,int(request.form.get("f_142",0)),int(request.form.get("e_142",0)),
             int(request.form.get("f_5kg",0)),int(request.form.get("e_5kg",0)),
             int(request.form.get("blue_books",0)),int(request.form.get("suraksha_pipes",0)),
             int(request.form.get("dpr_good",0)),session["uid"]))
        conn.commit(); conn.close()
        flash("✅ सकाळचा साठा नोंदवला!","success")
        return redirect("/office")

    @app.route("/office/upload-csv", methods=["POST"])
    @login_required
    def upload_csv():
        f=request.files.get("csv_file")
        if not f: flash("No file selected","danger"); return redirect("/office")
        t=today(); conn=get_db()
        content=f.read().decode("utf-8-sig","ignore")
        rows=list(csv.reader(io.StringIO(content)))
        # Load blocked for quick check
        blocked={r["consumer_number"] for r in
            conn.execute("SELECT consumer_number FROM blocked_consumers").fetchall()}
        inserted=0; skipped=0
        data_rows=[]
        # Find header row with CashMemoNo/SLNo
        for i,row in enumerate(rows):
            if any("CashMemoNo" in str(c) or "SLNo" in str(c) for c in row):
                data_rows=rows[i+1:]; break
        if not data_rows:
            # fallback: skip 4 rows
            data_rows=[r for r in rows[4:] if r and len(r)>=10 and str(r[0]).strip().isdigit()]
        for row in data_rows:
            if len(row)<10: continue
            try:
                cashmemo=str(row[7]).strip(); consumer=str(row[9]).strip()
                name=str(row[10]).strip(); area=str(row[1]).strip()
                mobile=str(row[14]).strip() if len(row)>14 else ""
                addr=" ".join([str(row[11]).strip(),str(row[12]).strip(),str(row[13]).strip()]).strip() if len(row)>13 else ""
            except: continue
            if not cashmemo or not name: continue
            is_bl=1 if consumer in blocked else 0
            br=""
            if is_bl:
                x=conn.execute("SELECT block_reason FROM blocked_consumers WHERE consumer_number=?",(consumer,)).fetchone()
                br=x["block_reason"] if x else "Blocked"
            # GPS/type from consumer master
            lat=lng=None; loc="urban"; bda_id=None
            cm=conn.execute("SELECT * FROM consumer_master WHERE consumer_number=?",(consumer,)).fetchone()
            if cm:
                lat,lng=cm["lat"],cm["lng"]; loc=cm["location_type"] or "urban"; bda_id=cm["bda_id"]
            else:
                for bid,bda in BDA_MAP.items():
                    if bda["village"].lower() in area.lower():
                        bda_id=bid; loc="rural"; break
            ex=conn.execute("SELECT id,status FROM delivery_pool WHERE cashmemo_no=?",(cashmemo,)).fetchone()
            if ex:
                if ex["status"] not in ("delivered","emergency","spot","bda"):
                    conn.execute("UPDATE delivery_pool SET area_name=?,consumer_name=?,address=?,mobile=?,is_blocked=?,block_reason=? WHERE cashmemo_no=? AND status='pending'",
                        (area,name,addr,mobile,is_bl,br,cashmemo))
                skipped+=1
            else:
                try:
                    conn.execute("""INSERT INTO delivery_pool(date,cashmemo_no,consumer_number,
                        consumer_name,address,mobile,area_id,area_name,location_type,bda_id,
                        lat,lng,gps_saved,is_blocked,block_reason,status,cylinder_price)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'pending',?)""",
                        (t,cashmemo,consumer,name,addr,mobile,area,area,loc,bda_id,
                         lat,lng,1 if lat else 0,is_bl,br,cyl_price()))
                    inserted+=1
                except: skipped+=1
        conn.commit(); conn.close()
        flash(f"✅ CSV: {inserted} नवीन, {skipped} skip (already delivered/existing)","success")
        return redirect("/office")

    @app.route("/office/cylinder-sale", methods=["POST"])
    @login_required
    def cylinder_sale():
        t=today(); conn=get_db()
        qty=int(request.form.get("qty",1)); price=float(request.form.get("price",856))
        mode=request.form.get("payment_mode","cash"); notes=request.form.get("notes","")
        cn=request.form.get("consumer_no","")
        ca=float(request.form.get("cash_amount",0) or 0)
        oa=float(request.form.get("online_amount",0) or 0)
        total=qty*price
        if mode!="partial":
            ca=total if mode=="cash" else 0
            oa=total if mode!="cash" else 0
        denoms={str(d):int(request.form.get(f"d{d}",0)) for d in [500,200,100,50,20,10]}
        denoms["coins"]=float(request.form.get("d_coins",0))
        conn.execute("""INSERT INTO office_sales(date,sale_type,quantity,unit_price,total_amount,
            payment_mode,cash_amount,online_amount,cash_500,cash_200,cash_100,cash_50,cash_20,
            cash_10,cash_coins,consumer_number,notes,entered_by)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t,"cylinder",qty,price,total,mode,ca,oa,denoms["500"],denoms["200"],
             denoms["100"],denoms["50"],denoms["20"],denoms["10"],denoms["coins"],cn,notes,session["uid"]))
        if ca>0: add_cash(conn,"cylinder_sale",ca,"in","cash",remarks=f"{qty} cyl",by=session["uid"])
        if oa>0: add_cash(conn,"cylinder_sale",oa,"in",mode,remarks=f"{qty} cyl online",by=session["uid"])
        add_stock(conn,"office","filled",-qty,"out",remarks=f"Office sale {qty}",by=session["uid"])
        conn.commit(); conn.close()
        flash(f"✅ {qty} cylinder(s) — ₹{total:,.0f}","success")
        return redirect("/office")

    @app.route("/office/additional-sale", methods=["POST"])
    @login_required
    def additional_sale():
        t=today(); conn=get_db()
        stype=request.form.get("sale_type"); qty=int(request.form.get("qty",1))
        price=float(request.form.get("price",0)); mode=request.form.get("payment_mode","cash")
        cn=request.form.get("consumer_no",""); notes=request.form.get("notes","")
        total=qty*price
        is_out=stype in ["termination"]
        is_in=stype in ["name_change"]
        conn.execute("""INSERT INTO office_sales(date,sale_type,quantity,unit_price,total_amount,
            payment_mode,cash_amount,online_amount,consumer_number,notes,entered_by)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            (t,stype,qty,price,total,mode,total if not is_out else 0,0,cn,notes,session["uid"]))
        if total>0:
            direction="out" if is_out else "in"
            add_cash(conn,stype,total,direction,mode,remarks=notes,by=session["uid"])
        if stype in ["blue_book","suraksha","dpr_paid","dpr_free"]:
            imap={"blue_book":"blue_book","suraksha":"suraksha_pipe","dpr_paid":"dpr","dpr_free":"dpr"}
            conn.execute("INSERT INTO accessory_stock(date,item_type,quantity,movement_type,notes,entered_by) VALUES(?,?,?,'out',?,?)",
                (t,imap.get(stype,stype),qty,notes,session["uid"]))
        conn.commit(); conn.close()
        flash(f"✅ {stype} recorded","success")
        return redirect("/office")

    @app.route("/office/stock-transfer", methods=["POST"])
    @login_required
    def office_stock_transfer():
        t=today(); conn=get_db()
        dm_id=int(request.form.get("delivery_man_id"))
        filled=int(request.form.get("filled_given",0))
        empty=int(request.form.get("empty_taken",0))
        u=conn.execute("SELECT vehicle_id FROM users WHERE id=?",(dm_id,)).fetchone()
        vloc=f"vehicle_{u['vehicle_id']}" if u and u["vehicle_id"] else f"dm_{dm_id}"
        if filled>0:
            add_stock(conn,"office","filled",-filled,"out",remarks=f"Transfer to DM {dm_id}",by=session["uid"])
            add_stock(conn,vloc,"filled",filled,"in",remarks="From Office",by=session["uid"])
        if empty>0:
            add_stock(conn,vloc,"empty",-empty,"out",remarks="Empty to Office",by=session["uid"])
            add_stock(conn,"office","empty",empty,"in",remarks=f"From DM {dm_id}",by=session["uid"])
        conn.commit(); conn.close()
        flash("✅ Transfer recorded","success")
        return redirect("/office")

    @app.route("/office/expense", methods=["POST"])
    @login_required
    def add_expense():
        t=today(); conn=get_db()
        cat=request.form.get("category"); desc=request.form.get("description","")
        amt=float(request.form.get("amount",0)); mode=request.form.get("payment_mode","cash")
        conn.execute("INSERT INTO expenses(date,category,description,amount,payment_mode,entered_by) VALUES(?,?,?,?,?,?)",
            (t,cat,desc,amt,mode,session["uid"]))
        add_cash(conn,"expense",amt,"out",mode,remarks=f"{cat}: {desc}",by=session["uid"])
        conn.commit(); conn.close()
        flash("✅ Expense recorded","success")
        return redirect("/office")

    @app.route("/office/advance", methods=["POST"])
    @login_required
    def give_advance():
        t=today(); conn=get_db()
        sid=int(request.form.get("staff_id"))
        atype=request.form.get("advance_type","given")
        amt=float(request.form.get("amount",0))
        notes=request.form.get("notes","")
        conn.execute("INSERT INTO staff_advances(date,staff_id,advance_type,amount,notes,entered_by) VALUES(?,?,?,?,?,?)",
            (t,sid,atype,amt,notes,session["uid"]))
        add_cash(conn,"advance",amt,"out" if atype=="given" else "in",
            remarks=f"Advance {atype}",person_id=sid,by=session["uid"])
        conn.commit(); conn.close()
        flash(f"✅ Advance {atype}","success")
        return redirect("/office")

    @app.route("/office/accessory-in", methods=["POST"])
    @login_required
    def accessory_in():
        t=today(); conn=get_db()
        itype=request.form.get("item_type"); qty=int(request.form.get("qty",1))
        notes=request.form.get("notes","Monthly stock")
        conn.execute("INSERT INTO accessory_stock(date,item_type,quantity,movement_type,notes,entered_by) VALUES(?,?,?,'in',?,?)",
            (t,itype,qty,notes,session["uid"]))
        conn.commit(); conn.close()
        flash(f"✅ {itype} stock +{qty}","success")
        return redirect("/office")

    @app.route("/office/lock-day", methods=["POST"])
    @login_required
    @roles("owner","manager")
    def lock_day():
        t=today(); conn=get_db()
        conn.execute("INSERT OR REPLACE INTO erp_days(date,is_locked,locked_at,locked_by) VALUES(?,1,?,?)",
            (t,now_ts(),session["uid"]))
        conn.commit(); conn.close()
        flash("🔒 Day locked!","success")
        return redirect("/dashboard")
