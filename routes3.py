#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes Part 3: Godown + BDA — Shourya Bharatgas ERP"""
from flask import request, redirect, session, flash
from db import (get_db, today, now_ts, add_stock, stock_bal, full_stock,
                add_cash, accessory_bal, cyl_price, BDA_MAP, VEHICLES)

def register_routes_godown(app):
    from templates import BASE
    from flask import render_template_string

    def R(tpl, **ctx):
        ctx.setdefault("active", "godown")
        full = BASE.replace("{% block body %}{% endblock %}", tpl)\
                   .replace("{% block scripts %}{% endblock %}", ctx.pop("scripts",""))
        return render_template_string(full, **ctx)

    def lr(f):
        from functools import wraps
        @wraps(f)
        def d(*a,**k):
            if "uid" not in session: return redirect("/login")
            return f(*a,**k)
        return d

    # ── GODOWN MAIN ─────────────────────────────────────────────
    @app.route("/godown")
    @lr
    def godown():
        t=today(); conn=get_db()
        g_f = stock_bal(conn,"godown","filled")
        g_e = stock_bal(conn,"godown","empty")
        g_d = stock_bal(conn,"defective","filled") + stock_bal(conn,"defective","empty")
        vstock = {}
        for vid,vi in VEHICLES.items():
            vf=stock_bal(conn,f"vehicle_{vid}","filled")
            ve=stock_bal(conn,f"vehicle_{vid}","empty")
            vstock[vid]={"name":vi["name"],"filled":vf,"empty":ve,"cap":vi["cap"]}
        recent_phys = conn.execute("SELECT * FROM godown_physical ORDER BY id DESC LIMIT 5").fetchall()
        recent_mov  = conn.execute("SELECT * FROM bpcl_movements ORDER BY id DESC LIMIT 10").fetchall()
        conn.close()

        TPL = """
<div class="card">
  <div class="ch"><div class="ct">🏭 गोदाम / Godown Operations</div></div>
  <div class="g3">
    <div class="sc"><div class="sn">{{ g_f }}</div><div class="sk">भरलेले Filled</div></div>
    <div class="sc em"><div class="sn">{{ g_e }}</div><div class="sk">रिकामे Empty</div></div>
    <div class="sc df"><div class="sn">{{ g_d }}</div><div class="sk">Defective</div></div>
  </div>
</div>

<!-- VEHICLE STOCK -->
<div class="card">
  <div class="ch"><div class="ct">🚚 वाहन साठा / Vehicle Stock</div></div>
  <div class="sgrid">
    {% for vid,vs in vstock.items() %}
    <div style="background:#f8f9fa;border-radius:8px;padding:12px;border:2px solid #dde3ea;text-align:center">
      <div style="font-weight:700;font-size:12px;margin-bottom:6px">{{ vs.name }}</div>
      <div style="font-size:22px;font-weight:800;color:#003366">{{ vs.filled }}<span style="font-size:12px;color:#999">/{{ vs.cap }}</span></div>
      <div style="font-size:11px;color:#6c757d">ভ{{ vs.filled }} E{{ vs.empty }}</div>
    </div>
    {% endfor %}
  </div>
</div>

<!-- PHYSICAL COUNT -->
<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>📊 Physical Stock Count / वास्तविक मोजणी</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    <form method="post" action="/godown/physical">
      <div class="card" style="background:#f0f6ff">
        <strong>📦 भरलेले / Filled</strong>
        <div class="g3">
          <div class="fg"><label>Rows</label><input type="number" id="fr" name="f_rows" value="0" min="0" oninput="calcFill()"></div>
          <div class="fg"><label>Columns</label><input type="number" id="fc" name="f_cols" value="0" min="0" oninput="calcFill()"></div>
          <div class="fg"><label>Extra</label><input type="number" id="fe" name="f_extra" value="0" min="0" oninput="calcFill()"></div>
        </div>
        <div class="fg"><label>Total Filled</label><input type="number" id="ft" name="f_total" value="0"></div>
      </div>
      <div class="card" style="background:#f5f0ff">
        <strong>🔵 रिकामे Zone 1 / Empty Zone 1</strong>
        <small style="display:block;margin:4px 0;color:#6c757d">Formula: (rows×cols×2) + (double_extra×2) + single_extra</small>
        <div class="g4">
          <div class="fg"><label>Rows</label><input type="number" id="z1r" name="z1_rows" value="0" min="0" oninput="calcEmpty()"></div>
          <div class="fg"><label>Cols</label><input type="number" id="z1c" name="z1_cols" value="0" min="0" oninput="calcEmpty()"></div>
          <div class="fg"><label>Double Extra</label><input type="number" id="z1d" name="z1_d_extra" value="0" min="0" oninput="calcEmpty()"></div>
          <div class="fg"><label>Single Extra</label><input type="number" id="z1s" name="z1_s_extra" value="0" min="0" oninput="calcEmpty()"></div>
        </div>
        <div style="font-weight:700">Zone 1 Total: <span id="z1t" style="color:#003366">0</span></div>
      </div>
      <div class="card" style="background:#fff5f0">
        <strong>🔵 रिकामे Zone 2</strong>
        <div class="g4">
          <div class="fg"><label>Rows</label><input type="number" id="z2r" name="z2_rows" value="0" min="0" oninput="calcEmpty()"></div>
          <div class="fg"><label>Cols</label><input type="number" id="z2c" name="z2_cols" value="0" min="0" oninput="calcEmpty()"></div>
          <div class="fg"><label>Double Extra</label><input type="number" id="z2d" name="z2_d_extra" value="0" min="0" oninput="calcEmpty()"></div>
          <div class="fg"><label>Single Extra</label><input type="number" id="z2s" name="z2_s_extra" value="0" min="0" oninput="calcEmpty()"></div>
        </div>
        <div style="font-weight:700">Zone 2 Total: <span id="z2t" style="color:#003366">0</span></div>
      </div>
      <div class="card" style="background:#f0fff5">
        <strong>🔵 रिकामे Zone 3</strong>
        <div class="g4">
          <div class="fg"><label>Rows</label><input type="number" id="z3r" name="z3_rows" value="0" min="0" oninput="calcEmpty()"></div>
          <div class="fg"><label>Cols</label><input type="number" id="z3c" name="z3_cols" value="0" min="0" oninput="calcEmpty()"></div>
          <div class="fg"><label>Double Extra</label><input type="number" id="z3d" name="z3_d_extra" value="0" min="0" oninput="calcEmpty()"></div>
          <div class="fg"><label>Single Extra</label><input type="number" id="z3s" name="z3_s_extra" value="0" min="0" oninput="calcEmpty()"></div>
        </div>
        <div style="font-weight:700">Zone 3 Total: <span id="z3t" style="color:#003366">0</span></div>
      </div>
      <div class="card">
        <div class="g3">
          <div><label>Total Empty</label><input type="number" id="et" name="e_total" value="0" readonly></div>
          <div><label>System Filled</label><input type="number" name="sys_filled" value="{{ g_f }}" readonly></div>
          <div><label>System Empty</label><input type="number" name="sys_empty" value="{{ g_e }}" readonly></div>
        </div>
        <button type="submit" class="btn bs" style="margin-top:12px">✅ Physical Count जतन करा</button>
      </div>
    </form>
    {% if recent_phys %}
    <div class="tw" style="margin-top:14px"><table>
      <tr><th>तारीख</th><th>Filled (Physical)</th><th>Empty</th><th>Diff F</th><th>Diff E</th></tr>
      {% for p in recent_phys %}
      <tr>
        <td>{{ p.date }}</td><td>{{ p.f_total }}</td><td>{{ p.e_total }}</td>
        <td class="{{ 'der' if p.diff_filled else 'dok' }}">{{ p.diff_filled }}</td>
        <td class="{{ 'der' if p.diff_empty else 'dok' }}">{{ p.diff_empty }}</td>
      </tr>
      {% endfor %}
    </table></div>
    {% endif %}
  </div>
</div>

<!-- BPCL TRUCK MOVEMENT -->
<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>🚛 BPCL Truck Movement / BPCL ट्रक नोंद</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    <form method="post" action="/godown/bpcl-movement">
      <div class="g3">
        <div class="fg"><label>Type</label>
          <select name="movement_type">
            <option value="received">Received from BPCL (342 cylinders)</option>
            <option value="returned">Returned to BPCL</option>
          </select>
        </div>
        <div class="fg"><label>Quantity</label><input type="number" name="quantity" value="342" min="1" required></div>
        <div class="fg"><label>Invoice No.</label><input type="text" name="invoice_no" placeholder="Invoice number"></div>
        <div class="fg"><label>Vehicle No.</label><input type="text" name="vehicle_no" placeholder="e.g. MH09 AB 1234"></div>
      </div>
      <button type="submit" class="btn bp">🚛 नोंदवा</button>
    </form>
    <div class="tw" style="margin-top:14px"><table>
      <tr><th>तारीख</th><th>Type</th><th>Qty</th><th>Invoice</th><th>Vehicle</th></tr>
      {% for m in recent_mov %}
      <tr>
        <td>{{ m.date }}</td>
        <td><span class="badge {{ 'bg' if m.movement_type=='received' else 'br2' }}">{{ m.movement_type.upper() }}</span></td>
        <td>{{ m.quantity }}</td>
        <td>{{ m.invoice_no or '—' }}</td>
        <td>{{ m.vehicle_no or '—' }}</td>
      </tr>
      {% endfor %}
    </table></div>
  </div>
</div>

<!-- DEFECTIVE -->
<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>❌ Defective Cylinders / सदोष सिलेंडर</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <p>Current Defective Stock: <strong>{{ g_d }}</strong></p>
    <form method="post" action="/godown/defective" style="margin-top:10px">
      <div class="g3">
        <div class="fg"><label>Type</label>
          <select name="defective_type"><option value="add">Add Defective</option><option value="remove">Remove/Repair</option></select>
        </div>
        <div class="fg"><label>Qty</label><input type="number" name="qty" min="1" required></div>
        <div class="fg"><label>Reason</label><input type="text" name="reason" placeholder="e.g. valve damage"></div>
      </div>
      <button type="submit" class="btn bd">नोंदवा</button>
    </form>
  </div>
</div>"""
        return R(TPL, g_f=g_f, g_e=g_e, g_d=g_d, vstock=vstock,
                 recent_phys=recent_phys, recent_mov=recent_mov)

    @app.route("/godown/physical", methods=["POST"])
    @lr
    def godown_physical():
        t=today(); conn=get_db()
        f=request.form
        f_total=int(f.get("f_total",0)); e_total=int(f.get("e_total",0))
        sys_f=stock_bal(conn,"godown","filled"); sys_e=stock_bal(conn,"godown","empty")
        df=f_total-sys_f; de=e_total-sys_e
        conn.execute("""INSERT INTO godown_physical(date,entry_time,entered_by,
            f_rows,f_cols,f_extra,f_total,
            e_z1_rows,e_z1_cols,e_z1_d_extra,e_z1_s_extra,e_z1_total,
            e_z2_rows,e_z2_cols,e_z2_d_extra,e_z2_s_extra,e_z2_total,
            e_z3_rows,e_z3_cols,e_z3_d_extra,e_z3_s_extra,e_z3_total,
            e_total,sys_filled,sys_empty,diff_filled,diff_empty) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t,now_ts(),session["uid"],
             int(f.get("f_rows",0)),int(f.get("f_cols",0)),int(f.get("f_extra",0)),f_total,
             int(f.get("z1_rows",0)),int(f.get("z1_cols",0)),int(f.get("z1_d_extra",0)),int(f.get("z1_s_extra",0)),0,
             int(f.get("z2_rows",0)),int(f.get("z2_cols",0)),int(f.get("z2_d_extra",0)),int(f.get("z2_s_extra",0)),0,
             int(f.get("z3_rows",0)),int(f.get("z3_cols",0)),int(f.get("z3_d_extra",0)),int(f.get("z3_s_extra",0)),0,
             e_total,sys_f,sys_e,df,de))
        if df:
            add_stock(conn,"godown","filled",df,"adjust",remarks=f"Physical count adj",by=session["uid"])
        if de:
            add_stock(conn,"godown","empty",de,"adjust",remarks=f"Physical count adj",by=session["uid"])
        conn.commit(); conn.close()
        msg=f"✅ Count saved. Diff: Filled={df}, Empty={de}"
        flash(msg,"success" if not df and not de else "warning")
        return redirect("/godown")

    @app.route("/godown/bpcl-movement", methods=["POST"])
    @lr
    def bpcl_movement():
        t=today(); conn=get_db()
        mtype=request.form.get("movement_type"); qty=int(request.form.get("quantity",342))
        inv=request.form.get("invoice_no",""); vno=request.form.get("vehicle_no","")
        conn.execute("INSERT INTO bpcl_movements(date,movement_type,quantity,invoice_no,vehicle_no,entered_by) VALUES(?,?,?,?,?,?)",
            (t,mtype,qty,inv,vno,session["uid"]))
        if mtype=="received":
            add_stock(conn,"godown","filled",qty,"bpcl_in",remarks=f"BPCL Invoice {inv}",by=session["uid"])
        else:
            add_stock(conn,"godown","empty",-qty,"bpcl_return",remarks=f"Returned {inv}",by=session["uid"])
        conn.commit(); conn.close()
        flash(f"✅ BPCL {mtype}: {qty} cylinders","success")
        return redirect("/godown")

    @app.route("/godown/defective", methods=["POST"])
    @lr
    def godown_defective():
        t=today(); conn=get_db()
        dtype=request.form.get("defective_type"); qty=int(request.form.get("qty",1))
        reason=request.form.get("reason","")
        if dtype=="add":
            add_stock(conn,"godown","filled",-qty,"defective_out",remarks=reason,by=session["uid"])
            add_stock(conn,"defective","filled",qty,"defective_in",remarks=reason,by=session["uid"])
        else:
            add_stock(conn,"defective","filled",-qty,"defective_fixed",remarks=reason,by=session["uid"])
            add_stock(conn,"godown","filled",qty,"defective_fixed",remarks=reason,by=session["uid"])
        conn.commit(); conn.close()
        flash(f"✅ Defective {dtype}: {qty}","success")
        return redirect("/godown")

    @app.route("/godown/adjust", methods=["GET","POST"])
    @lr
    def godown_adjust():
        if session.get("role") not in ["owner","manager"]:
            flash("Only owner/manager can adjust","danger"); return redirect("/godown")
        if request.method=="POST":
            conn=get_db()
            loc=request.form.get("location","godown")
            ctype=request.form.get("ctype","filled")
            qty=int(request.form.get("qty",0))
            reason=request.form.get("reason","Manual adjustment")
            add_stock(conn,loc,ctype,qty,"manual_adjust",remarks=reason,by=session["uid"])
            conn.commit(); conn.close()
            flash(f"✅ Manual adjust: {loc} {ctype} {qty:+d}","success")
            return redirect("/godown")
        from templates import BASE
        TPL="""<div class="card"><div class="ch"><div class="ct">⚙️ Manual Stock Adjust</div></div>
<form method="post"><div class="g3">
<div class="fg"><label>Location</label><select name="location">
<option value="godown">Godown</option><option value="office">Office</option>
{% for v in vehicles %}<option value="vehicle_{{ v }}">Vehicle {{ v }}</option>{% endfor %}
</select></div>
<div class="fg"><label>Type</label><select name="ctype"><option value="filled">Filled</option><option value="empty">Empty</option></select></div>
<div class="fg"><label>Qty (+/-)</label><input type="number" name="qty" required placeholder="e.g. -5 or +10"></div>
</div><div class="fg"><label>Reason</label><input type="text" name="reason" required></div>
<button type="submit" class="btn bd">⚠️ Adjust करा</button>
</form></div>"""
        from flask import render_template_string
        full=BASE.replace("{% block body %}{% endblock %}",TPL).replace("{% block scripts %}{% endblock %}","")
        return render_template_string(full, active="godown", vehicles=list(VEHICLES.keys()))


def register_routes_bda(app):
    from templates import BASE
    from flask import render_template_string

    def R(tpl, **ctx):
        ctx.setdefault("active","bda")
        full=BASE.replace("{% block body %}{% endblock %}",tpl)\
                 .replace("{% block scripts %}{% endblock %}",ctx.pop("scripts",""))
        return render_template_string(full, **ctx)

    def lr(f):
        from functools import wraps
        @wraps(f)
        def d(*a,**k):
            if "uid" not in session: return redirect("/login")
            return f(*a,**k)
        return d

    @app.route("/bda")
    @lr
    def bda_portal():
        if session.get("role") not in ["bda","owner","manager"]:
            flash("BDA only","danger"); return redirect("/dashboard")
        bid=session.get("bda_id"); t=today(); conn=get_db()
        if session.get("role") in ["owner","manager"]:
            bid=request.args.get("bid",1,type=int)
        binfo=BDA_MAP.get(bid,{})
        b_f=stock_bal(conn,f"bda_{bid}","filled")
        b_e=stock_bal(conn,f"bda_{bid}","empty")
        customers=conn.execute("""SELECT * FROM delivery_pool
            WHERE date=? AND bda_id=? ORDER BY status,consumer_name""",(t,bid)).fetchall()
        conn.close()

        TPL="""
<div class="card">
  <div class="ch"><div class="ct">🏘️ BDA Portal — {{ binfo.get('village','BDA') }}<small>{{ binfo.get('owner','') }} · {{ binfo.get('mobile','') }}</small></div></div>
  <div class="g3">
    <div class="sc"><div class="sn">{{ b_f }}</div><div class="sk">भरलेले Filled</div></div>
    <div class="sc em"><div class="sn">{{ b_e }}</div><div class="sk">रिकामे Empty</div></div>
    <div class="sc" style="background:linear-gradient(135deg,#1a5276,#2471a3)">
      <div class="sn">{{ customers|length }}</div><div class="sk">आजचे ग्राहक</div>
    </div>
  </div>
</div>

<!-- CUSTOMER OTP LIST -->
<div class="card">
  <div class="ch"><div class="ct">📋 ग्राहक यादी + OTP / Customer List</div>
    <a href="/delivery/otp-export?bda={{ bid }}" class="btn bp btn-sm">⬇ Export</a>
  </div>
  <div class="tw"><table>
    <tr><th>#</th><th>नाव / Name</th><th>Mobile</th><th>OTP</th><th>Status</th></tr>
    {% for c in customers %}
    <tr class="{{ 'bg' if c.status=='delivered' else '' }}">
      <td>{{ loop.index }}</td>
      <td>{{ c.consumer_name }}<br><small style="color:#999">{{ c.area_name }}</small></td>
      <td><a href="tel:{{ c.mobile }}" style="color:inherit">{{ c.mobile }}</a></td>
      <td>
        {% if c.otp %}
          <span style="font-weight:700;color:green">{{ c.otp }}</span>
        {% elif c.status!='delivered' %}
          <input class="otp-in" type="text" maxlength="6" placeholder="OTP"
            onchange="saveOTP({{ c.id }},this.value)" id="otp{{ c.id }}">
        {% else %}—{% endif %}
      </td>
      <td><span class="badge {{ 'bg' if c.status=='delivered' else 'bb' }}">{{ c.status }}</span></td>
    </tr>
    {% endfor %}
  </table></div>
</div>

<!-- BDA TRANSACTION -->
<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>💳 Transaction / BDA विक्री नोंद</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    <form method="post" action="/bda/transaction">
      <input type="hidden" name="bda_id" value="{{ bid }}">
      <div class="g3">
        <div class="fg"><label>भरलेले दिले / Filled Received</label><input type="number" name="filled_received" value="0" min="0"></div>
        <div class="fg"><label>रिकामे दिले / Empties Given Back</label><input type="number" name="empty_given" value="0" min="0"></div>
        <div class="fg"><label>विकलेले / Sold</label><input type="number" name="sold" value="0" min="0"></div>
        <div class="fg"><label>Cash ₹</label><input type="number" name="cash_amount" value="0" step="0.01"></div>
        <div class="fg"><label>Online ₹</label><input type="number" name="online_amount" value="0" step="0.01"></div>
        <div class="fg"><label>Notes</label><input type="text" name="notes"></div>
      </div>
      <button type="submit" class="btn bp">✅ नोंदवा</button>
    </form>
  </div>
</div>

<!-- BDA SPOT DELIVERY -->
<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>⚡ Spot Delivery / BDA स्पॉट विक्री</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <form method="post" action="/bda/spot">
      <input type="hidden" name="bda_id" value="{{ bid }}">
      <div class="g3">
        <div class="fg"><label>ग्राहक नाव / Customer Name</label><input type="text" name="cname" required></div>
        <div class="fg"><label>Mobile</label><input type="tel" name="mobile" pattern="[0-9]{10}"></div>
        <div class="fg"><label>Cash ₹</label><input type="number" name="cash" value="856" step="0.01"></div>
      </div>
      <button type="submit" class="btn bw">⚡ Spot Sale</button>
    </form>
  </div>
</div>
<script>
function saveOTP(id,otp){
  if(!otp)return;
  fetch('/delivery/save-otp',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({delivery_id:id,otp:otp})})
  .then(r=>r.json()).then(d=>{if(d.ok)document.getElementById('otp'+id).style.background='#e8ffe8';});
}
</script>"""
        return R(TPL, binfo=binfo, b_f=b_f, b_e=b_e, customers=customers, bid=bid)

    @app.route("/bda/transaction", methods=["POST"])
    @lr
    def bda_transaction():
        t=today(); conn=get_db()
        bid=int(request.form.get("bda_id",0))
        fr=int(request.form.get("filled_received",0))
        eg=int(request.form.get("empty_given",0))
        sold=int(request.form.get("sold",0))
        cash=float(request.form.get("cash_amount",0))
        online=float(request.form.get("online_amount",0))
        notes=request.form.get("notes","")
        from db import add_stock, WAGE_RURAL
        bloc=f"bda_{bid}"
        if fr>0:
            add_stock(conn,"godown","filled",-fr,"bda_transfer",by=session["uid"])
            add_stock(conn,bloc,"filled",fr,"bda_in",remarks=notes,by=session["uid"])
        if eg>0:
            add_stock(conn,bloc,"empty",-eg,"bda_return",by=session["uid"])
            add_stock(conn,"godown","empty",eg,"bda_return",by=session["uid"])
        if sold>0:
            add_stock(conn,bloc,"filled",-sold,"bda_sale",by=session["uid"])
            add_stock(conn,bloc,"empty",sold,"bda_sale_emp",by=session["uid"])
            wage=sold*WAGE_RURAL
            conn.execute("INSERT INTO staff_advances(date,staff_id,advance_type,amount,notes,entered_by) VALUES(?,?,?,?,?,?)",
                (t,session["uid"],"wage_bda_sale",wage,f"BDA sale {sold} rural @₹{WAGE_RURAL}",session["uid"]))
        if cash>0: add_cash(conn,"bda_collection",cash,"in","cash",remarks=notes,by=session["uid"])
        if online>0: add_cash(conn,"bda_collection",online,"in","online",remarks=notes,by=session["uid"])
        conn.commit(); conn.close()
        flash(f"✅ BDA transaction recorded","success")
        return redirect(f"/bda?bid={bid}")

    @app.route("/bda/spot", methods=["POST"])
    @lr
    def bda_spot():
        import time; t=today(); conn=get_db()
        bid=int(request.form.get("bda_id",0))
        cname=request.form.get("cname",""); mobile=request.form.get("mobile","")
        cash=float(request.form.get("cash",856))
        cm=f"BDASP-{int(time.time())}"
        conn.execute("""INSERT INTO delivery_pool(date,cashmemo_no,consumer_name,mobile,
            bda_id,status,is_spot,spot_name,spot_mobile,cash_amount,cylinder_price,location_type)
            VALUES(?,?,?,?,?,'spot',1,?,?,?,?,'rural')""",
            (t,cm,cname,mobile,bid,cname,mobile,cash,cash))
        add_cash(conn,"bda_spot_sale",cash,"in","cash",remarks=f"BDA spot: {cname}",by=session["uid"])
        conn.commit(); conn.close()
        flash(f"✅ BDA Spot sale: {cname}","success")
        return redirect(f"/bda?bid={bid}")
