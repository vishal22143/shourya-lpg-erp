#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes Part 2: Delivery — Shourya Bharatgas ERP"""
from flask import request, redirect, session, jsonify, flash
from db import (get_db, today, now_ts, add_stock, stock_bal, add_cash,
                advance_balance, cyl_price, BDA_MAP, VEHICLES,
                WAGE_URBAN, WAGE_RURAL, WAGE_PAIR)

def register_routes_delivery(app):
    from templates import BASE
    from flask import render_template_string

    def R(tpl, **ctx):
        ctx.setdefault("active", "delivery")
        full = BASE.replace("{% block body %}{% endblock %}", tpl)\
                   .replace("{% block scripts %}{% endblock %}", ctx.pop("scripts", ""))
        return render_template_string(full, **ctx)

    def lr(f):
        from functools import wraps
        @wraps(f)
        def d(*a, **k):
            if "uid" not in session: return redirect("/login")
            return f(*a, **k)
        return d

    # ── DELIVERY HOME ────────────────────────────────────────────
    @app.route("/delivery")
    @lr
    def delivery():
        t = today(); conn = get_db()
        tot  = conn.execute("SELECT COUNT(*) FROM delivery_pool WHERE date=?",(t,)).fetchone()[0]
        done = conn.execute("SELECT COUNT(*) FROM delivery_pool WHERE date=? AND status NOT IN ('pending','blocked')",(t,)).fetchone()[0]
        pend = conn.execute("SELECT COUNT(*) FROM delivery_pool WHERE date=? AND status='pending' AND is_blocked=0",(t,)).fetchone()[0]
        otpc = conn.execute("SELECT COUNT(*) FROM delivery_pool WHERE date=? AND otp IS NOT NULL",(t,)).fetchone()[0]
        trips = conn.execute("""SELECT t.*,u.name dm,v.name vn FROM trips t
            JOIN users u ON t.delivery_man_id=u.id
            LEFT JOIN (SELECT id,name FROM users) v ON v.id=t.helper_id
            WHERE t.date=? ORDER BY t.created_at DESC""",(t,)).fetchall()
        delivs = conn.execute("SELECT * FROM users WHERE role='delivery' AND is_active=1 ORDER BY name").fetchall()
        helpers= conn.execute("SELECT * FROM users WHERE role IN ('delivery','loader','driver') AND is_active=1 ORDER BY name").fetchall()
        vehs  = VEHICLES; conn.close()

        TPL = """
<div class="card">
  <div class="ch"><div class="ct">🚚 डिलिव्हरी पॅनेल <small>Delivery Operations</small></div>
    <div style="display:flex;gap:8px">
      <a href="/delivery/otp-report" class="btn bo btn-sm">📋 OTP Report</a>
      <a href="/delivery/otp-export" class="btn bo btn-sm">⬇ OTP Export</a>
    </div>
  </div>
  <div class="g4">
    <div class="sb"><div class="sv">{{ tot }}</div><div class="sl">एकूण Deliveries</div></div>
    <div class="sb g"><div class="sv g">{{ done }}</div><div class="sl">पूर्ण झाल्या</div></div>
    <div class="sb o"><div class="sv o">{{ pend }}</div><div class="sl">Pending</div></div>
    <div class="sb p"><div class="sv">{{ otpc }}</div><div class="sl">OTP मिळाले</div></div>
  </div>
</div>

<!-- START NEW TRIP -->
<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>🆕 नवीन Trip सुरू करा / Start Trip</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    <form method="post" action="/delivery/start-trip">
      <div class="g3">
        <div class="fg"><label>डिलिव्हरी मॅन</label>
          <select name="dm_id" required>
            <option value="">निवडा...</option>
            {% for d in delivs %}<option value="{{ d.id }}">{{ d.name }}</option>{% endfor %}
          </select>
        </div>
        <div class="fg"><label>गाडी / Vehicle</label>
          <select name="vehicle_id" required>
            <option value="">निवडा...</option>
            {% for vid,v in vehs.items() %}<option value="{{ vid }}">{{ v.name }} (cap {{ v.cap }}+{{ v.extra }})</option>{% endfor %}
          </select>
        </div>
        <div class="fg"><label>Helper (optional)</label>
          <select name="helper_id">
            <option value="">None (No Pair Bonus)</option>
            {% for h in helpers %}<option value="{{ h.id }}">{{ h.name }}</option>{% endfor %}
          </select>
        </div>
        <div class="fg"><label>Trip Number</label>
          <select name="trip_number"><option value="1">Trip 1</option><option value="2">Trip 2</option><option value="3">Trip 3</option></select>
        </div>
        <div class="fg"><label>Opening Filled (vehicle)</label><input type="number" name="opening_filled" value="0" min="0" required></div>
        <div class="fg"><label>Opening Empty Loaded</label><input type="number" name="opening_empty" value="0" min="0"></div>
      </div>
      <button type="submit" class="btn bs btn-bl">🚀 Trip सुरू करा</button>
    </form>
  </div>
</div>

<!-- ACTIVE TRIPS -->
{% for trip in trips %}
<div class="card" style="border-left:4px solid {% if trip.status=='open' %}#f0ad4e{% else %}#28a745{% endif %}">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
    <div>
      <strong style="font-size:15px">{{ trip.dm }}</strong>
      <span class="badge {% if trip.status=='open' %}by{% else %}bg{% endif %}">{{ trip.status.upper() }}</span>
      <span class="badge bb">Trip {{ trip.trip_number }}</span>
      {% if trip.vn %}<span class="badge bpu">Helper: {{ trip.vn }}</span>{% endif %}
    </div>
    {% if trip.status=='open' %}
    <a href="/delivery/trip/{{ trip.id }}" class="btn bp">📍 ऑपरेट करा</a>
    {% endif %}
  </div>
  <div class="g4">
    <div class="sb" style="padding:8px"><div class="sv" style="font-size:18px">{{ trip.opening_filled }}</div><div class="sl">Opening</div></div>
    <div class="sb g" style="padding:8px"><div class="sv g" style="font-size:18px">{{ trip.total_delivered }}</div><div class="sl">Delivered</div></div>
    <div class="sb" style="padding:8px"><div class="sv" style="font-size:18px">₹{{ '{:,.0f}'.format(trip.cash_collected) }}</div><div class="sl">Cash</div></div>
    <div class="sb" style="padding:8px"><div class="sv" style="font-size:18px">₹{{ '{:,.0f}'.format(trip.online_collected) }}</div><div class="sl">Online</div></div>
  </div>
  {% if trip.status=='closed' %}
  <div style="background:#f0f4f8;border-radius:8px;padding:10px;margin-top:8px;font-size:13px">
    Wage: Urban={{ trip.wage_cyl_urban }} × ₹8 + Rural={{ trip.wage_cyl_rural }} × ₹7
    {% if trip.pair_bonus %} + Pair ₹200{% endif %}
    = <strong>₹{{ '{:,.0f}'.format(trip.wage_amount + trip.pair_bonus) }}</strong>
    {% if trip.cash_shortage %} | <span style="color:var(--rd)">Shortage: ₹{{ trip.cash_shortage }}</span>{% endif %}
    {% if trip.cash_excess %} | <span style="color:var(--gr)">Excess: ₹{{ trip.cash_excess }}</span>{% endif %}
  </div>
  {% endif %}
</div>
{% else %}
<div class="card" style="text-align:center;padding:30px;color:var(--mu)">
  आज कोणतीही trip नाही. वरून नवीन trip सुरू करा.
</div>
{% endfor %}"""
        return R(TPL, tot=tot, done=done, pend=pend, otpc=otpc,
                 trips=trips, delivs=delivs, helpers=helpers, vehs=vehs)

    @app.route("/delivery/start-trip", methods=["POST"])
    @lr
    def start_trip():
        t = today(); conn = get_db()
        dm  = int(request.form.get("dm_id"))
        vid = int(request.form.get("vehicle_id"))
        hid = request.form.get("helper_id") or None
        tn  = int(request.form.get("trip_number", 1))
        of  = int(request.form.get("opening_filled", 0))
        oe  = int(request.form.get("opening_empty", 0))
        if hid: hid = int(hid)
        conn.execute("""INSERT INTO trips(date,delivery_man_id,helper_id,vehicle_id,trip_number,
            opening_filled,opening_empty,status) VALUES(?,?,?,?,?,?,?,'open')""",
            (t, dm, hid, vid, tn, of, oe))
        trip_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        vloc = f"vehicle_{vid}"
        if of: add_stock(conn, vloc, "filled", of, "in", remarks=f"Trip {tn} opening", by=session["uid"])
        if oe: add_stock(conn, vloc, "empty",  oe, "in", remarks=f"Trip {tn} opening empties", by=session["uid"])
        conn.commit(); conn.close()
        flash("✅ Trip सुरू झाली!", "success")
        return redirect(f"/delivery/trip/{trip_id}")

    # ── TRIP DETAIL (MAP + LIST) ─────────────────────────────────
    @app.route("/delivery/trip/<int:tid>")
    @lr
    def trip_detail(tid):
        conn = get_db()
        trip = conn.execute("SELECT t.*,u.name dm FROM trips t JOIN users u ON t.delivery_man_id=u.id WHERE t.id=?",(tid,)).fetchone()
        if not trip: conn.close(); flash("Trip not found","danger"); return redirect("/delivery")
        t = trip["date"]
        pool = conn.execute("""SELECT * FROM delivery_pool WHERE date=?
            ORDER BY CASE status WHEN 'pending' THEN 0 WHEN 'delivered' THEN 1 ELSE 2 END, area_name""",(t,)).fetchall()
        areas = sorted(set(p["area_name"] or "" for p in pool if p["area_name"]))
        delivs = conn.execute("SELECT id,name FROM users WHERE role='delivery' AND is_active=1").fetchall()
        bdas   = list(BDA_MAP.items())
        price  = cyl_price()
        # Build map markers JSON
        markers = []
        for p in pool:
            if p["lat"] and p["lng"]:
                markers.append({"lat": p["lat"], "lng": p["lng"],
                    "name": p["consumer_name"], "cashmemo": p["cashmemo_no"],
                    "status": p["status"], "mobile": p["mobile"] or ""})
        import json
        markers_json = json.dumps(markers)
        conn.close()

        TPL = """
<div style="margin-bottom:10px;display:flex;align-items:center;gap:8px;flex-wrap:wrap">
  <a href="/delivery" class="btn bo btn-sm">← Back</a>
  <strong style="font-size:15px">{{ trip.dm }}</strong>
  <span class="badge by">Trip {{ trip.trip_number }}</span>
  <span class="badge {% if trip.status=='open' %}bo2{% else %}bg{% endif %}">{{ trip.status.upper() }}</span>
</div>

<!-- MAP -->
<div class="card" style="padding:10px">
  <div id="dmap"></div>
  <div style="display:flex;gap:10px;margin-top:8px;font-size:11px;flex-wrap:wrap">
    <span>🔴 Nearest/Pending</span><span>🟢 Delivered</span><span>🔵 GPS Pending</span><span>🔵 You</span>
  </div>
</div>

<!-- AREA PILLS -->
<div class="card" style="padding:10px">
  <div class="ap-row">
    <button class="ap ac" onclick="filterArea('all',this)">सर्व</button>
    {% for a in areas %}<button class="ap" onclick="filterArea('{{ a }}',this)">{{ a }}</button>{% endfor %}
  </div>
</div>

<!-- CUSTOMER LIST -->
<div id="clist">
{% for p in pool %}
<div class="ci" data-area="{{ p.area_name }}" data-status="{{ p.status }}"
  onclick="openModal({{ loop.index0 }})">
  <div class="cdot" style="background:{% if p.status=='delivered' %}#28a745{% elif p.is_blocked %}#dc3545{% elif p.status=='pending' %}#0066cc{% else %}#fd7e14{% endif %}"></div>
  <div class="cif">
    <div class="cn">{{ p.consumer_name }}</div>
    <div class="ca">{{ p.area_name }} · {{ p.cashmemo_no }}
      {% if p.is_blocked %}<span class="badge br2">BLOCKED</span>{% endif %}
    </div>
    {% if p.otp %}<div class="cotp">✅ OTP: {{ p.otp }}</div>{% endif %}
  </div>
  <div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px">
    {% if p.mobile %}<a href="tel:{{ p.mobile }}" onclick="event.stopPropagation()" class="btn bp btn-sm">📞</a>{% endif %}
    {% if p.status=='pending' and not p.is_blocked %}
    <input type="text" class="otp-in" placeholder="OTP" id="otp_{{ p.cashmemo_no }}"
      onclick="event.stopPropagation()" onchange="saveOtp('{{ p.cashmemo_no }}',this.value)">
    {% endif %}
  </div>
</div>
{% endfor %}
</div>

<!-- DELIVERY MODAL -->
<div class="mo" id="dModal">
  <div class="ms" id="dModalInner">
    <div class="mh"></div>
    <div id="modalContent"></div>
  </div>
</div>

<!-- SPOT DELIVERY -->
<div class="ex" style="margin-top:14px">
  <div class="exh" onclick="xToggle(this)">
    <h3>⚡ Spot Delivery / नवीन ग्राहक</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <div class="al alw">Spot = BPCL list मध्ये नाही. GPS save होणार नाही.</div>
    <form method="post" action="/delivery/spot">
      <input type="hidden" name="trip_id" value="{{ trip.id }}">
      <div class="g3">
        <div class="fg"><label>ग्राहकाचे नाव</label><input type="text" name="spot_name" required></div>
        <div class="fg"><label>मोबाईल</label><input type="tel" name="spot_mobile" required></div>
        <div class="fg"><label>Payment</label>
          <select name="payment_mode">
            <option value="cash">Cash</option><option value="qr">QR</option>
            <option value="gpay">GPay</option><option value="paytm">Paytm</option>
          </select>
        </div>
        <div class="fg"><label>रक्कम ₹</label><input type="number" name="amount" value="{{ price }}" step="0.01"></div>
      </div>
      <button type="submit" class="btn bp">⚡ Spot Record करा</button>
    </form>
  </div>
</div>

<!-- TRANSFER -->
<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>🔄 Transfer / स्थानांतर</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <form method="post" action="/delivery/transfer">
      <input type="hidden" name="trip_id" value="{{ trip.id }}">
      <div class="g3">
        <div class="fg"><label>To</label>
          <select name="to_type" onchange="updToId(this)">
            <option value="office">Office</option>
            <option value="godown">Godown</option>
            {% for bid,bda in bdas %}<option value="bda_{{ bid }}">BDA: {{ bda.village }}</option>{% endfor %}
          </select>
        </div>
        <div class="fg"><label>Filled दिले</label><input type="number" name="filled_given" value="0" min="0"></div>
        <div class="fg"><label>Empty घेतले</label><input type="number" name="empty_taken" value="0" min="0"></div>
      </div>
      <div class="al ali" id="wage_note">BDA transfer = Rural wage (₹7/cyl)</div>
      <button type="submit" class="btn bw">🔄 Transfer करा</button>
    </form>
  </div>
</div>

<!-- CLOSE TRIP -->
{% if trip.status=='open' %}
<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>🏁 Trip बंद करा / Close Trip</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <form method="post" action="/delivery/close/{{ trip.id }}">
      <div class="g3">
        <div class="fg"><label>Urban cylinders (₹8 each)</label><input type="number" name="urban_cyl" id="uc" value="{{ trip.wage_cyl_urban }}" min="0" oninput="calcWage()"></div>
        <div class="fg"><label>Rural cylinders (₹7 each)</label><input type="number" name="rural_cyl" id="rc" value="{{ trip.wage_cyl_rural }}" min="0" oninput="calcWage()"></div>
        <div class="fg"><label>Closing Filled (return)</label><input type="number" name="closing_filled" value="0" min="0"></div>
        <div class="fg"><label>Closing Empty</label><input type="number" name="closing_empty" value="0" min="0"></div>
        <div class="fg"><label>Cash submitted ₹</label><input type="number" name="cash_submitted" id="csub" step="0.01" value="{{ trip.cash_collected }}" oninput="calcWage()"></div>
        <div class="fg"><label>Online ₹</label><input type="number" name="online_submitted" step="0.01" value="{{ trip.online_collected }}"></div>
      </div>
      <div style="background:#f0f4f8;border-radius:8px;padding:12px;margin:10px 0">
        <div id="wCalc" style="font-size:14px;font-weight:700">
          Wage: Urban 0×₹8 + Rural 0×₹7{% if trip.helper_id %} + Pair ₹200{% endif %} = ₹0
        </div>
        <div id="shortCalc" style="font-size:12px;color:var(--rd);margin-top:4px"></div>
      </div>
      <div class="dc">
        <strong>🪙 Cash Count</strong>
        {% for d in [500,200,100,50,20,10] %}
        <div class="dc-row">
          <label>₹{{ d }}</label>
          <input type="number" name="d{{ d }}" id="cl_{{ d }}" value="0" min="0" oninput="denom('cl')">
          <span id="cl_s{{ d }}">₹0</span>
        </div>{% endfor %}
        <div class="dc-row"><label>Coins</label><input type="number" name="d_coins" id="cl_coins" value="0" step="0.5" oninput="denom('cl')"><span></span></div>
        <div class="dc-tot"><span>Total</span><span id="cl_tot">₹0</span></div>
      </div>
      <div class="fg" style="margin-top:10px"><label>Notes</label><input type="text" name="notes"></div>
      <button type="submit" class="btn bd btn-bl" style="margin-top:8px"
        onclick="return confirm('Trip बंद करायची? बदल होणार नाही!')">
        🏁 Trip बंद करा
      </button>
    </form>
  </div>
</div>
{% endif %}"""

        SCRIPTS = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
var markers = """ + markers_json + """;
var map = L.map('dmap').setView([16.68, 74.56], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  {attribution:'© OSM',maxZoom:19}).addTo(map);
var userMarker=null;
function updatePos(pos){
  var lat=pos.coords.latitude, lng=pos.coords.longitude;
  if(userMarker) userMarker.setLatLng([lat,lng]);
  else { userMarker=L.circleMarker([lat,lng],{radius:10,color:'#0066cc',fillColor:'#0066cc',fillOpacity:0.8}).addTo(map); }
}
if(navigator.geolocation) navigator.geolocation.watchPosition(updatePos,null,{enableHighAccuracy:true});
markers.forEach(function(m){
  var col=m.status==='delivered'?'#28a745':'#dc3545';
  var ci=L.circleMarker([m.lat,m.lng],{radius:8,color:col,fillColor:col,fillOpacity:0.9}).addTo(map);
  ci.bindPopup('<strong>'+m.name+'</strong><br>'+m.cashmemo+
    (m.mobile?'<br><a href="tel:'+m.mobile+'">📞 '+m.mobile+'</a>':''));
});

var poolData = """ + __import__('json').dumps([dict(p) for p in pool]) + """;

function openModal(i){
  var p=poolData[i];
  if(p.is_blocked){alert('❌ Blocked: '+p.block_reason); return;}
  var html='<div style="margin-bottom:12px"><strong style="font-size:17px">'+p.consumer_name+'</strong><br>';
  html+='<span style="color:#666;font-size:12px">'+p.area_name+' · '+p.cashmemo_no+'</span>';
  if(p.mobile) html+='<br><a href="tel:'+p.mobile+'" class="btn bp btn-sm" style="margin-top:6px">📞 Call</a>';
  html+='</div>';
  if(p.status==='delivered'){
    html+='<div class="al als">✅ Delivered '+p.delivered_at+'</div>';
  } else if(p.status==='pending'){
    html+=`<form method="post" action="/delivery/record">
      <input type="hidden" name="pool_id" value="${p.id}">
      <input type="hidden" name="trip_id" value="{{ trip.id }}">
      <div class="fg"><label>OTP</label><input type="text" name="otp" value="${p.otp||''}" placeholder="Customer OTP" id="mod_otp"></div>
      <div class="fg"><label>Doorstep delivery? (GPS save होईल)</label>
        <select name="at_doorstep"><option value="yes">✅ हो — Doorstep वर आहे</option><option value="no">❌ नाही — GPS Save नको</option></select>
      </div>
      <div class="fg"><label>Payment Mode</label>
        <input type="hidden" name="payment_mode" id="md_pm" value="cash">
        <div class="pm-row">
          <button type="button" class="pm ac" data-mode="cash" onclick="selPay(this,'md')">💵 Cash</button>
          <button type="button" class="pm" data-mode="qr" onclick="selPay(this,'md')">📱 QR</button>
          <button type="button" class="pm" data-mode="gpay" onclick="selPay(this,'md')">🟢 GPay</button>
          <button type="button" class="pm" data-mode="paytm" onclick="selPay(this,'md')">🔵 Paytm</button>
          <button type="button" class="pm" data-mode="partial" onclick="selPay(this,'md')">½ Partial</button>
        </div>
        <div id="md_cd" style="display:none" class="fg"><label>Cash ₹</label><input type="number" name="cash_amount" step="0.01"></div>
        <div id="md_od" style="display:none" class="fg"><label>Online ₹</label><input type="number" name="online_amount" step="0.01"></div>
      </div>
      <button type="submit" class="btn bs btn-bl">✅ Delivered Mark करा</button>
    </form>`;
  }
  document.getElementById('modalContent').innerHTML=html;
  document.getElementById('dModal').classList.add('sh');
}
document.getElementById('dModal').addEventListener('click',function(e){
  if(e.target===this) this.classList.remove('sh');
});

function filterArea(area,btn){
  document.querySelectorAll('.ap').forEach(b=>b.classList.remove('ac'));
  btn.classList.add('ac');
  document.querySelectorAll('.ci').forEach(function(el){
    el.style.display=(area==='all'||el.dataset.area===area)?'flex':'none';
  });
}

function saveOtp(cm,otp){
  if(!otp) return;
  fetch('/delivery/save-otp',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({cashmemo_no:cm,otp:otp})})
  .then(r=>r.json()).then(d=>{if(d.ok) console.log('OTP saved')});
}

function calcWage(){
  var u=parseInt(document.getElementById('uc').value)||0;
  var r=parseInt(document.getElementById('rc').value)||0;
  var pair={{ 200 if trip.helper_id else 0 }};
  var w=u*8+r*7+pair;
  var cs=parseFloat(document.getElementById('csub').value)||0;
  var collected={{ trip.cash_collected }};
  var diff=cs-collected;
  document.getElementById('wCalc').textContent='Wage: Urban '+u+'×₹8 + Rural '+r+'×₹7'+(pair?' + Pair ₹200':'')+' = ₹'+w.toLocaleString('en-IN');
  if(diff<0) document.getElementById('shortCalc').textContent='⚠️ Shortage: ₹'+Math.abs(diff)+' — Auto advance debit होईल';
  else if(diff>0) document.getElementById('shortCalc').textContent='✅ Excess: ₹'+diff;
  else document.getElementById('shortCalc').textContent='';
}
function updToId(sel){
  var v=sel.value;
  var note=document.getElementById('wage_note');
  note.style.display=v.startsWith('bda')?'block':'none';
}
</script>"""
        return R(TPL, trip=trip, pool=pool, areas=areas,
                 delivs=delivs, bdas=bdas, price=price,
                 scripts=SCRIPTS)

    # ── RECORD DELIVERY ─────────────────────────────────────────
    @app.route("/delivery/record", methods=["POST"])
    @lr
    def record_delivery():
        import json
        pool_id = int(request.form.get("pool_id"))
        trip_id = int(request.form.get("trip_id"))
        otp     = request.form.get("otp","").strip()
        atd     = request.form.get("at_doorstep","no")
        mode    = request.form.get("payment_mode","cash")
        ca      = float(request.form.get("cash_amount",0) or 0)
        oa      = float(request.form.get("online_amount",0) or 0)
        conn    = get_db()
        pool    = conn.execute("SELECT * FROM delivery_pool WHERE id=?",(pool_id,)).fetchone()
        trip    = conn.execute("SELECT * FROM trips WHERE id=?",(trip_id,)).fetchone()
        if not pool or not trip:
            conn.close(); flash("Not found","danger"); return redirect("/delivery")
        price = pool["cylinder_price"] or cyl_price()
        if mode != "partial":
            ca = price if mode == "cash" else 0
            oa = price if mode != "cash" else 0
        total = ca + oa
        # GPS
        save_gps = 0; lat = lng = None
        if atd == "yes" and not pool["gps_saved"]:
            # Try to get GPS from request (sent via hidden field if JS captures it)
            glat = request.form.get("lat"); glng = request.form.get("lng")
            if glat and glng:
                lat = float(glat); lng = float(glng); save_gps = 1
                conn.execute("UPDATE consumer_master SET lat=?,lng=?,gps_saved=1 WHERE consumer_number=?",
                    (lat, lng, pool["consumer_number"]))
        loc_type = pool["location_type"] or "urban"
        urban_add = 1 if loc_type == "urban" else 0
        rural_add = 1 if loc_type == "rural" else 0
        conn.execute("""UPDATE delivery_pool SET status='delivered',otp=?,otp_saved_at=?,
            lat=COALESCE(NULLIF(?,0),lat),lng=COALESCE(NULLIF(?,0),lng),
            gps_saved=CASE WHEN ? THEN 1 ELSE gps_saved END,
            trip_id=?,delivered_by=?,payment_mode=?,cash_amount=?,
            online_amount=?,delivered_at=? WHERE id=?""",
            (otp or None, now_ts() if otp else None,
             lat,lng,save_gps,trip_id,session["uid"],mode,ca,oa,now_ts(),pool_id))
        conn.execute("""UPDATE trips SET
            total_delivered=total_delivered+1,
            cash_collected=cash_collected+?,
            online_collected=online_collected+?,
            wage_cyl_urban=wage_cyl_urban+?,
            wage_cyl_rural=wage_cyl_rural+?,
            otp_count=COALESCE(otp_count,0)+? WHERE id=?""",
            (ca, oa, urban_add, rural_add, 1 if otp else 0, trip_id))
        vloc = f"vehicle_{trip['vehicle_id']}"
        add_stock(conn, vloc, "filled", -1, "out", remarks=f"Delivery {pool['cashmemo_no']}", by=session["uid"])
        add_stock(conn, vloc, "empty",   1, "in",  remarks=f"Empty from {pool['cashmemo_no']}", by=session["uid"])
        if ca > 0: add_cash(conn, "delivery", ca, "in", "cash", ref_id=pool_id, ref_type="delivery", by=session["uid"])
        if oa > 0: add_cash(conn, "delivery", oa, "in", mode,   ref_id=pool_id, ref_type="delivery", by=session["uid"])
        conn.commit(); conn.close()
        return jsonify({"ok": True}) if request.is_json else redirect(f"/delivery/trip/{trip_id}")

    # ── SPOT DELIVERY ────────────────────────────────────────────
    @app.route("/delivery/spot", methods=["POST"])
    @lr
    def spot_delivery():
        t = today(); conn = get_db()
        trip_id = int(request.form.get("trip_id"))
        name    = request.form.get("spot_name","")
        mobile  = request.form.get("spot_mobile","")
        mode    = request.form.get("payment_mode","cash")
        amt     = float(request.form.get("amount", cyl_price()))
        import time
        cashmemo = f"SPOT-{int(time.time())}"
        trip = conn.execute("SELECT * FROM trips WHERE id=?",(trip_id,)).fetchone()
        conn.execute("""INSERT INTO delivery_pool(date,cashmemo_no,consumer_name,mobile,
            status,is_spot,spot_name,spot_mobile,trip_id,delivered_by,
            payment_mode,cash_amount,online_amount,cylinder_price,delivered_at)
            VALUES(?,?,?,?,'spot',1,?,?,?,?,?,?,?,?,?)""",
            (t,cashmemo,name,mobile,name,mobile,trip_id,session["uid"],
             mode, amt if mode=="cash" else 0, amt if mode!="cash" else 0, amt, now_ts()))
        conn.execute("UPDATE trips SET total_spot=total_spot+1,cash_collected=cash_collected+?,total_delivered=total_delivered+1 WHERE id=?",
            (amt if mode=="cash" else 0, trip_id))
        vloc = f"vehicle_{trip['vehicle_id']}"
        add_stock(conn, vloc, "filled", -1, "out", remarks=f"Spot {name}", by=session["uid"])
        add_stock(conn, vloc, "empty",   1, "in",  remarks=f"Spot empty", by=session["uid"])
        if mode == "cash": add_cash(conn, "spot_delivery", amt, "in", "cash", by=session["uid"])
        conn.commit(); conn.close()
        flash(f"⚡ Spot delivery: {name}","success")
        return redirect(f"/delivery/trip/{trip_id}")

    # ── TRIP TRANSFER ─────────────────────────────────────────────
    @app.route("/delivery/transfer", methods=["POST"])
    @lr
    def trip_transfer():
        t = today(); conn = get_db()
        trip_id  = int(request.form.get("trip_id"))
        to_type  = request.form.get("to_type","office")
        filled   = int(request.form.get("filled_given",0))
        empty    = int(request.form.get("empty_taken",0))
        trip     = conn.execute("SELECT * FROM trips WHERE id=?",(trip_id,)).fetchone()
        vloc     = f"vehicle_{trip['vehicle_id']}"
        is_bda   = to_type.startswith("bda_")
        bda_id   = int(to_type.split("_")[1]) if is_bda else None
        to_loc   = to_type if is_bda else to_type
        if filled:
            add_stock(conn, vloc,   "filled", -filled, "out", remarks=f"Transfer to {to_type}", by=session["uid"])
            add_stock(conn, to_loc, "filled",  filled, "in",  remarks=f"From vehicle {trip['vehicle_id']}", by=session["uid"])
        if empty:
            add_stock(conn, to_loc, "empty", -empty, "out", remarks="Transfer", by=session["uid"])
            add_stock(conn, vloc,   "empty",  empty, "in",  remarks=f"From {to_type}", by=session["uid"])
        if is_bda and filled:
            conn.execute("""UPDATE trips SET wage_cyl_rural=wage_cyl_rural+? WHERE id=?""",
                (filled, trip_id))
        conn.execute("""INSERT INTO trip_transfers(trip_id,transfer_type,to_location,to_id,
            filled_given,empty_taken) VALUES(?,?,?,?,?,?)""",
            (trip_id, "bda" if is_bda else to_type, to_loc, bda_id, filled, empty))
        conn.commit(); conn.close()
        flash("✅ Transfer recorded","success")
        return redirect(f"/delivery/trip/{trip_id}")

    # ── SAVE OTP (AJAX) ──────────────────────────────────────────
    @app.route("/delivery/save-otp", methods=["POST"])
    @lr
    def save_otp():
        data = request.get_json()
        cm   = data.get("cashmemo_no",""); otp = data.get("otp","")
        if not cm or not otp: return jsonify({"ok":False})
        conn = get_db()
        conn.execute("UPDATE delivery_pool SET otp=?,otp_saved_at=? WHERE cashmemo_no=? AND otp IS NULL",
            (otp, now_ts(), cm))
        conn.commit(); conn.close()
        return jsonify({"ok":True})

    # ── CLOSE TRIP ───────────────────────────────────────────────
    @app.route("/delivery/close/<int:tid>", methods=["POST"])
    @lr
    def close_trip(tid):
        t = today(); conn = get_db()
        trip = conn.execute("SELECT * FROM trips WHERE id=?",(tid,)).fetchone()
        if not trip: conn.close(); flash("Trip not found","danger"); return redirect("/delivery")
        uc  = int(request.form.get("urban_cyl",0))
        rc  = int(request.form.get("rural_cyl",0))
        cf  = int(request.form.get("closing_filled",0))
        ce  = int(request.form.get("closing_empty",0))
        cs  = float(request.form.get("cash_submitted",0))
        os_ = float(request.form.get("online_submitted",0))
        notes= request.form.get("notes","")
        denoms = {str(d):int(request.form.get(f"d{d}",0)) for d in [500,200,100,50,20,10]}
        denoms["coins"] = float(request.form.get("d_coins",0))
        has_helper = bool(trip["helper_id"])
        wage  = uc * WAGE_URBAN + rc * WAGE_RURAL
        pair  = WAGE_PAIR if has_helper else 0.0
        total_cash = trip["cash_collected"]
        shortage = max(0.0, total_cash - cs)
        excess   = max(0.0, cs - total_cash)
        if shortage > 0:
            conn.execute("INSERT INTO staff_advances(date,staff_id,advance_type,amount,notes,entered_by) VALUES(?,?,?,?,?,?)",
                (t, trip["delivery_man_id"], "given", shortage, "Auto: cash shortage", session["uid"]))
        conn.execute("""UPDATE trips SET status='closed', wage_cyl_urban=?,wage_cyl_rural=?,
            wage_amount=?,pair_bonus=?,cash_shortage=?,cash_excess=?,
            closing_filled=?,closing_empty=?,
            cash_submitted_amt=?,online_submitted_amt=?,
            cash_500=?,cash_200=?,cash_100=?,cash_50=?,cash_20=?,cash_10=?,cash_coins=?,
            notes=?,closed_at=? WHERE id=?""",
            (uc, rc, wage, pair, shortage, excess, cf, ce,
             cs, os_, denoms["500"],denoms["200"],denoms["100"],
             denoms["50"],denoms["20"],denoms["10"],denoms.get("coins",0),
             notes, now_ts(), tid))
        vloc = f"vehicle_{trip['vehicle_id']}"
        if cf: add_stock(conn, vloc, "filled", -cf, "out", remarks="Trip closing return", by=session["uid"])
        if ce: add_stock(conn, vloc, "empty",  -ce, "out", remarks="Trip closing empties", by=session["uid"])
        conn.commit(); conn.close()
        flash(f"🏁 Trip बंद! Wage: ₹{wage+pair:,.0f}","success")
        return redirect("/delivery")

    # ── OTP REPORT ───────────────────────────────────────────────
    @app.route("/delivery/otp-report")
    @lr
    def otp_report():
        t = today(); conn = get_db()
        rows = conn.execute("""SELECT d.*,t.trip_number,u.name dm FROM delivery_pool d
            LEFT JOIN trips t ON d.trip_id=t.id
            LEFT JOIN users u ON t.delivery_man_id=u.id
            WHERE d.date=? ORDER BY d.area_name, d.consumer_name""",(t,)).fetchall()
        conn.close()
        TPL = """
<div class="card">
  <div class="ch"><div class="ct">📋 OTP Report <small>{{ t }}</small></div>
    <a href="/delivery/otp-export" class="btn bp btn-sm">⬇ CSV Export</a>
  </div>
  <div class="tw"><table>
    <tr><th>Area</th><th>Consumer No</th><th>नाव</th><th>Mobile</th><th>Cash Memo</th><th>OTP</th><th>Status</th><th>DM</th></tr>
    {% for r in rows %}
    <tr>
      <td>{{ r.area_name }}</td><td>{{ r.consumer_number }}</td>
      <td>{{ r.consumer_name }}</td><td>{{ r.mobile }}</td>
      <td>{{ r.cashmemo_no }}</td>
      <td style="font-weight:700;color:{% if r.otp %}var(--gr){% else %}var(--rd){% endif %}">
        {{ r.otp or '—' }}
      </td>
      <td><span class="badge {% if r.status=='delivered' %}bg{% else %}by{% endif %}">{{ r.status }}</span></td>
      <td>{{ r.dm or '—' }}</td>
    </tr>
    {% endfor %}
  </table></div>
</div>"""
        return R(TPL, rows=rows, t=t)

    @app.route("/delivery/otp-export")
    @lr
    def otp_export():
        import csv, io
        t = today(); conn = get_db()
        rows = conn.execute("""SELECT area_name,consumer_number,consumer_name,mobile,
            cashmemo_no,otp,status FROM delivery_pool WHERE date=? ORDER BY area_name,consumer_name""",(t,)).fetchall()
        conn.close()
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["Area","Consumer No","Name","Mobile","Cash Memo","OTP","Status"])
        for r in rows: w.writerow(list(r))
        from flask import make_response
        resp = make_response(buf.getvalue())
        resp.headers["Content-Type"]        = "text/csv"
        resp.headers["Content-Disposition"] = f"attachment; filename=OTP_{t}.csv"
        return resp
