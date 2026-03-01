#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes Part 4: Wages + Accounting + BPCL Day End — Shourya Bharatgas ERP"""
from flask import request, redirect, session, flash, make_response
import csv, io
from db import (get_db, today, now_ts, this_month, add_cash, cash_summary,
                advance_balance, stock_bal, cyl_price, gsetting,
                WAGE_URBAN, WAGE_RURAL, WAGE_PAIR)

def register_routes_wages(app):
    from templates import BASE
    from flask import render_template_string

    def R(tpl,**ctx):
        ctx.setdefault("active","wages")
        full=BASE.replace("{% block body %}{% endblock %}",tpl)\
                 .replace("{% block scripts %}{% endblock %}",ctx.pop("scripts",""))
        return render_template_string(full,**ctx)

    def lr(f):
        from functools import wraps
        @wraps(f)
        def d(*a,**k):
            if "uid" not in session: return redirect("/login")
            return f(*a,**k)
        return d

    @app.route("/wages")
    @lr
    def wages():
        if session.get("role") not in ["owner","manager","accountant"]:
            flash("Access denied","danger"); return redirect("/dashboard")
        month=request.args.get("month",this_month())
        conn=get_db()
        dm_list=conn.execute("SELECT * FROM users WHERE role='delivery' AND is_active=1 ORDER BY name").fetchall()
        entries={}
        for dm in dm_list:
            e=conn.execute("SELECT * FROM wage_entries WHERE month=? AND staff_id=?",(month,dm["id"])).fetchone()
            entries[dm["id"]]=dict(e) if e else None

        # Calculate from trips for this month
        trip_data={}
        trips=conn.execute("""SELECT * FROM trips WHERE date LIKE ? AND status='closed'""",(f"{month}%",)).fetchall()
        for tr in trips:
            sid=tr["delivery_man_id"]
            if sid not in trip_data:
                trip_data[sid]={"urban":0,"rural":0,"pair_bonus":0,"shortage":0}
            trip_data[sid]["urban"]+=tr["wage_cyl_urban"]
            trip_data[sid]["rural"]+=tr["wage_cyl_rural"]
            if tr["helper_id"]: trip_data[sid]["pair_bonus"]+=WAGE_PAIR
            trip_data[sid]["shortage"]+=tr["cash_shortage"]

        conn.close()
        TPL="""
<div class="card">
  <div class="ch"><div class="ct">💰 पगार पत्रक / Wage Sheet</div>
    <form method="get" style="display:flex;gap:8px">
      <input type="month" name="month" value="{{ month }}" style="width:160px">
      <button type="submit" class="btn bp btn-sm">Filter</button>
    </form>
  </div>
</div>
{% for dm in dm_list %}
{% set td=trip_data.get(dm.id,{}) %}
{% set e=entries.get(dm.id) %}
{% set u=td.get('urban',0) %}{% set ru=td.get('rural',0) %}
{% set pb=td.get('pair_bonus',0) %}{% set sh=td.get('shortage',0) %}
{% set wage=(u*w_urban)+(ru*w_rural)+pb %}
{% set adv_bal=adv_bals.get(dm.id,0) %}
{% set max_rec=wage*0.2 %}{% set rec=[sh,adv_bal,max_rec]|min %}
{% set net=wage-rec %}
<div class="wr">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
    <div><strong>{{ dm.name }}</strong><br>
      <small>{{ u }} Urban + {{ ru }} Rural + {{ (td.get('pair_bonus',0)/200)|int }} Helper trips</small>
    </div>
    <div style="text-align:right">
      <div style="font-size:20px;font-weight:900;color:#003366">₹{{ '{:,.0f}'.format(net) }}</div>
      <small>Net Payable</small>
    </div>
  </div>
  <div class="g4" style="margin-bottom:8px">
    <div class="sb g" style="padding:8px"><div class="sv g" style="font-size:15px">₹{{ '{:,.0f}'.format(wage) }}</div><div class="sl">Gross Wage</div></div>
    <div class="sb" style="padding:8px"><div class="sv" style="font-size:15px">₹{{ '{:,.0f}'.format(rec) }}</div><div class="sl">Recovery</div></div>
    <div class="sb o" style="padding:8px"><div class="sv o" style="font-size:15px">₹{{ '{:,.0f}'.format(adv_bal) }}</div><div class="sl">Advance Bal</div></div>
    <div class="sb r" style="padding:8px"><div class="sv r" style="font-size:15px">₹{{ '{:,.0f}'.format(sh) }}</div><div class="sl">Cash Short</div></div>
  </div>
  {% if e %}
    <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">
      <span class="badge {{ 'bg' if e.mgr_approved else 'by' }}">{{ 'Mgr ✓' if e.mgr_approved else 'Mgr Pending' }}</span>
      <span class="badge {{ 'bg' if e.owner_approved else 'by' }}">{{ 'Owner ✓' if e.owner_approved else 'Owner Pending' }}</span>
      <span class="badge {{ 'bg' if e.is_paid else 'br2' }}">{{ 'PAID ✓' if e.is_paid else 'NOT PAID' }}</span>
      {% if session.role=='manager' and not e.mgr_approved %}
      <form method="post" action="/wages/approve-mgr"><input type="hidden" name="eid" value="{{ e.id }}"><button class="btn bp btn-sm">Mgr Approve</button></form>
      {% endif %}
      {% if session.role in ['owner'] and e.mgr_approved and not e.owner_approved %}
      <form method="post" action="/wages/approve-owner"><input type="hidden" name="eid" value="{{ e.id }}"><button class="btn bs btn-sm">Owner Approve</button></form>
      {% endif %}
      {% if session.role=='owner' and e.owner_approved and not e.is_paid %}
      <form method="post" action="/wages/pay" onsubmit="return confirm('Mark as PAID?')"><input type="hidden" name="eid" value="{{ e.id }}"><button class="btn bd btn-sm">💰 Mark Paid</button></form>
      {% endif %}
    </div>
  {% else %}
    <form method="post" action="/wages/save">
      <input type="hidden" name="staff_id" value="{{ dm.id }}">
      <input type="hidden" name="month" value="{{ month }}">
      <input type="hidden" name="urban_cyl" value="{{ u }}">
      <input type="hidden" name="rural_cyl" value="{{ ru }}">
      <input type="hidden" name="pair_bonus" value="{{ pb }}">
      <input type="hidden" name="shortage" value="{{ sh }}">
      <input type="hidden" name="adv_rec" value="{{ rec }}">
      <input type="hidden" name="wage" value="{{ wage }}">
      <input type="hidden" name="net" value="{{ net }}">
      <button type="submit" class="btn bw btn-sm">💾 Save Wage Entry</button>
    </form>
  {% endif %}
</div>
{% endfor %}"""
        adv_bals={dm["id"]:advance_balance(get_db(),dm["id"]) for dm in dm_list}
        return R(TPL, dm_list=dm_list, entries=entries, trip_data=trip_data,
                 adv_bals=adv_bals, month=month,
                 w_urban=WAGE_URBAN, w_rural=WAGE_RURAL)

    @app.route("/wages/save", methods=["POST"])
    @lr
    def wage_save():
        conn=get_db()
        f=request.form
        conn.execute("""INSERT OR IGNORE INTO wage_entries(month,staff_id,urban_cyl,rural_cyl,
            pair_bonus,cash_shortage,wage_amount,advance_recovered,net_payable)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (f["month"],int(f["staff_id"]),int(f.get("urban_cyl",0)),
             int(f.get("rural_cyl",0)),float(f.get("pair_bonus",0)),
             float(f.get("shortage",0)),float(f.get("wage",0)),
             float(f.get("adv_rec",0)),float(f.get("net",0))))
        conn.commit(); conn.close()
        flash("✅ Wage entry saved","success")
        return redirect(f"/wages?month={f['month']}")

    @app.route("/wages/approve-mgr", methods=["POST"])
    @lr
    def wage_approve_mgr():
        eid=int(request.form.get("eid")); conn=get_db()
        conn.execute("UPDATE wage_entries SET mgr_approved=1,mgr_approved_by=?,mgr_approved_at=? WHERE id=?",
            (session["uid"],now_ts(),eid))
        conn.commit(); conn.close()
        flash("✅ Manager approved","success"); return redirect("/wages")

    @app.route("/wages/approve-owner", methods=["POST"])
    @lr
    def wage_approve_owner():
        eid=int(request.form.get("eid")); conn=get_db()
        conn.execute("UPDATE wage_entries SET owner_approved=1,owner_approved_by=?,owner_approved_at=? WHERE id=?",
            (session["uid"],now_ts(),eid))
        conn.commit(); conn.close()
        flash("✅ Owner approved","success"); return redirect("/wages")

    @app.route("/wages/pay", methods=["POST"])
    @lr
    def wage_pay():
        if session.get("role")!="owner":
            flash("Owner only","danger"); return redirect("/wages")
        eid=int(request.form.get("eid")); conn=get_db()
        we=conn.execute("SELECT * FROM wage_entries WHERE id=?",(eid,)).fetchone()
        if we:
            conn.execute("UPDATE wage_entries SET is_paid=1,paid_at=? WHERE id=?",(now_ts(),eid))
            add_cash(conn,"salary_wages",we["net_payable"],"out","cash",
                     remarks=f"Wage paid staff {we['staff_id']}",by=session["uid"])
        conn.commit(); conn.close()
        flash("✅ Wage marked paid","success"); return redirect("/wages")


def register_routes_accounting(app):
    from templates import BASE
    from flask import render_template_string

    def R(tpl,**ctx):
        ctx.setdefault("active","accounting")
        full=BASE.replace("{% block body %}{% endblock %}",tpl)\
                 .replace("{% block scripts %}{% endblock %}",ctx.pop("scripts",""))
        return render_template_string(full,**ctx)

    def lr(f):
        from functools import wraps
        @wraps(f)
        def d(*a,**k):
            if "uid" not in session: return redirect("/login")
            return f(*a,**k)
        return d

    @app.route("/accounting")
    @lr
    def accounting():
        if session.get("role") not in ["owner","manager","accountant"]:
            flash("Access denied","danger"); return redirect("/dashboard")
        month=request.args.get("month",this_month())
        conn=get_db()
        soa=conn.execute("SELECT * FROM bpcl_soa WHERE month=? ORDER BY doc_date",(month,)).fetchall()
        soa_dr=sum(r["amount_debit"] for r in soa)
        soa_cr=sum(r["amount_credit"] for r in soa)
        soa_bal=soa_dr-soa_cr
        cs=cash_summary(conn)
        sales_total=conn.execute(
            "SELECT COALESCE(SUM(total_amount),0) FROM office_sales WHERE date LIKE ?",(f"{month}%",)).fetchone()[0]
        trip_online=conn.execute(
            "SELECT COALESCE(SUM(online_collected),0) FROM trips WHERE date LIKE ?",(f"{month}%",)).fetchone()[0]
        # GST: outward sales
        cyl_qty=conn.execute("SELECT COALESCE(SUM(quantity),0) FROM office_sales WHERE date LIKE ? AND sale_type='cylinder'",(f"{month}%",)).fetchone()[0]
        conn.close()
        TPL="""
<div class="card">
  <div class="ch"><div class="ct">📊 हिशेब / Accounting & SOA</div>
    <form method="get" style="display:flex;gap:8px">
      <input type="month" name="month" value="{{ month }}" style="width:160px">
      <button type="submit" class="btn bp btn-sm">Filter</button>
    </form>
  </div>
  <div class="g4">
    <div class="sb r"><div class="sv r">₹{{ '{:,.0f}'.format(soa_bal) }}</div><div class="sl">BPCL SOA Balance (we owe)</div></div>
    <div class="sb g"><div class="sv">₹{{ '{:,.0f}'.format(sales_total) }}</div><div class="sl">Office Sales</div></div>
    <div class="sb"><div class="sv">₹{{ '{:,.0f}'.format(cs.net) }}</div><div class="sl">Cash Net (all time)</div></div>
    <div class="sb p"><div class="sv">{{ cyl_qty }}</div><div class="sl">Cylinders Sold</div></div>
  </div>
</div>

<!-- SOA UPLOAD -->
<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>📤 BPCL SOA Upload / अपलोड</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    <div class="al ali">BPCL eConnect → SOA → Export Excel/CSV → Upload here</div>
    <form method="post" action="/accounting/upload-soa" enctype="multipart/form-data">
      <div class="g3">
        <div class="fg"><label>SOA File (Excel/CSV)</label><input type="file" name="soa_file" accept=".xlsx,.xls,.csv" required></div>
        <div class="fg"><label>Month (YYYY-MM)</label><input type="month" name="month" value="{{ month }}" required></div>
      </div>
      <button type="submit" class="btn bp">📤 Upload SOA</button>
    </form>
  </div>
</div>

<!-- SOA TABLE -->
<div class="card">
  <div class="ch"><div class="ct">📋 BPCL SOA Entries — {{ month }}</div>
    <div style="display:flex;gap:6px">
      <a href="/accounting/cash-export?month={{ month }}" class="btn bo btn-sm">⬇ Cash CSV</a>
      <a href="/accounting/gst-export?month={{ month }}" class="btn bs btn-sm">⬇ GST Export</a>
    </div>
  </div>
  <div class="al ali">
    Total Debit: ₹{{ '{:,.0f}'.format(soa_dr) }} |
    Total Credit: ₹{{ '{:,.0f}'.format(soa_cr) }} |
    <strong>Balance (we owe): ₹{{ '{:,.0f}'.format(soa_bal) }}</strong>
  </div>
  <div class="tw"><table>
    <tr><th>Doc Date</th><th>Narration</th><th>Doc Type</th><th>Debit</th><th>Credit</th></tr>
    {% for r in soa %}
    <tr>
      <td>{{ r.doc_date }}</td><td>{{ r.narration }}</td>
      <td><span class="badge bb">{{ r.doc_type }}</span></td>
      <td>{% if r.amount_debit %}<span class="der">₹{{ '{:,.0f}'.format(r.amount_debit) }}</span>{% endif %}</td>
      <td>{% if r.amount_credit %}<span class="dok">₹{{ '{:,.0f}'.format(r.amount_credit) }}</span>{% endif %}</td>
    </tr>
    {% else %}
    <tr><td colspan="5" style="text-align:center;color:var(--mu)">No SOA entries for {{ month }}</td></tr>
    {% endfor %}
  </table></div>
</div>

<!-- MANUAL SOA ENTRY -->
<div class="ex">
  <div class="exh" onclick="xToggle(this)">
    <h3>✏️ Manual SOA Entry</h3><span class="ar">▼</span>
  </div>
  <div class="exb">
    <form method="post" action="/accounting/soa-entry">
      <div class="g3">
        <div class="fg"><label>Doc Date</label><input type="date" name="doc_date" required></div>
        <div class="fg"><label>Doc Type</label><select name="doc_type">
          <option value="Invoice">Invoice (cylinder lot)</option>
          <option value="SV_Debit">SV Debit</option>
          <option value="TV_Credit">TV Credit</option>
          <option value="Transit_Loss">Transit Loss</option>
          <option value="Cyl_Rent">Cylinder Rent</option>
          <option value="Bank_Payment">Bank Payment</option>
          <option value="DBTL">DBTL Recovery</option>
          <option value="GST">GST Invoice</option>
          <option value="Other">Other</option>
        </select></div>
        <div class="fg"><label>Doc Number</label><input type="text" name="doc_number"></div>
        <div class="fg"><label>Narration</label><input type="text" name="narration" required></div>
        <div class="fg"><label>Debit ₹ (we owe BPCL)</label><input type="number" name="amount_debit" value="0" step="0.01"></div>
        <div class="fg"><label>Credit ₹ (BPCL owes us)</label><input type="number" name="amount_credit" value="0" step="0.01"></div>
        <div class="fg"><label>Month</label><input type="month" name="month" value="{{ month }}"></div>
      </div>
      <button type="submit" class="btn bw">✅ SOA Entry नोंदवा</button>
    </form>
  </div>
</div>"""
        return R(TPL, month=month, soa=soa, soa_dr=soa_dr, soa_cr=soa_cr,
                 soa_bal=soa_bal, cs=cs, sales_total=sales_total, cyl_qty=cyl_qty)

    @app.route("/accounting/upload-soa", methods=["POST"])
    @lr
    def upload_soa():
        f=request.files.get("soa_file"); month=request.form.get("month",this_month())
        if not f: flash("No file","danger"); return redirect("/accounting")
        conn=get_db(); inserted=0
        fname=f.filename.lower()
        try:
            if fname.endswith(".csv"):
                content=f.read().decode("utf-8-sig","ignore")
                rows=list(csv.reader(io.StringIO(content)))
                for row in rows[1:]:
                    if len(row)<6: continue
                    try:
                        conn.execute("""INSERT INTO bpcl_soa(doc_date,narration,doc_type,doc_number,
                            amount_debit,amount_credit,month,uploaded_by)
                            VALUES(?,?,?,?,?,?,?,?)""",
                            (row[0].strip(),row[1].strip(),row[2].strip(),row[3].strip(),
                             float(row[4] or 0),float(row[5] or 0),month,session["uid"]))
                        inserted+=1
                    except: pass
            else:
                import openpyxl
                wb=openpyxl.load_workbook(io.BytesIO(f.read()))
                ws=wb.active
                for row in ws.iter_rows(min_row=2,values_only=True):
                    if not row[0]: continue
                    try:
                        conn.execute("""INSERT INTO bpcl_soa(doc_date,narration,doc_type,doc_number,
                            amount_debit,amount_credit,month,uploaded_by)
                            VALUES(?,?,?,?,?,?,?,?)""",
                            (str(row[0]),str(row[1] or ""),str(row[2] or ""),str(row[3] or ""),
                             float(row[4] or 0),float(row[5] or 0),month,session["uid"]))
                        inserted+=1
                    except: pass
        except Exception as e:
            flash(f"Upload error: {e}","danger"); return redirect("/accounting")
        conn.commit(); conn.close()
        flash(f"✅ SOA: {inserted} entries uploaded","success")
        return redirect(f"/accounting?month={month}")

    @app.route("/accounting/soa-entry", methods=["POST"])
    @lr
    def soa_entry():
        conn=get_db(); f=request.form
        conn.execute("""INSERT INTO bpcl_soa(doc_date,narration,doc_type,doc_number,
            amount_debit,amount_credit,month,uploaded_by) VALUES(?,?,?,?,?,?,?,?)""",
            (f["doc_date"],f["narration"],f["doc_type"],f.get("doc_number",""),
             float(f.get("amount_debit",0)),float(f.get("amount_credit",0)),
             f.get("month",this_month()),session["uid"]))
        conn.commit(); conn.close()
        flash("✅ SOA entry added","success")
        return redirect(f"/accounting?month={f.get('month',this_month())}")

    @app.route("/accounting/gst-export")
    @lr
    def gst_export():
        month=request.args.get("month",this_month())
        conn=get_db()
        sales=conn.execute(
            "SELECT * FROM office_sales WHERE date LIKE ? ORDER BY date",(f"{month}%",)).fetchall()
        purchases=conn.execute(
            "SELECT * FROM bpcl_soa WHERE month=? AND doc_type IN ('Invoice','GST')",(month,)).fetchall()
        conn.close()
        buf=io.StringIO()
        w=csv.writer(buf)
        w.writerow(["=== GSTR-1 OUTWARD SUPPLIES ==="])
        w.writerow(["Date","Type","Qty","Rate","Taxable Value","GST @5%","Total"])
        gst_rate=0.05
        for s in sales:
            taxable=s["total_amount"]/(1+gst_rate)
            gst=s["total_amount"]-taxable
            w.writerow([s["date"],s["sale_type"],s["quantity"],s["unit_price"],
                        f"{taxable:.2f}",f"{gst:.2f}",f"{s['total_amount']:.2f}"])
        w.writerow([])
        w.writerow(["=== GSTR-2 INWARD SUPPLIES (BPCL Invoices) ==="])
        w.writerow(["Date","Narration","Doc No","Debit","Credit"])
        for p in purchases:
            w.writerow([p["doc_date"],p["narration"],p["doc_number"],p["amount_debit"],p["amount_credit"]])
        resp=make_response(buf.getvalue())
        resp.headers["Content-Type"]="text/csv"
        resp.headers["Content-Disposition"]=f"attachment; filename=GST_{month}.csv"
        return resp

    @app.route("/accounting/cash-export")
    @lr
    def cash_export():
        month=request.args.get("month",this_month())
        conn=get_db()
        rows=conn.execute("SELECT * FROM cash_ledger WHERE date LIKE ? ORDER BY date",(f"{month}%",)).fetchall()
        conn.close()
        buf=io.StringIO(); w=csv.writer(buf)
        w.writerow(["Date","Type","Amount","Direction","Mode","Remarks"])
        for r in rows:
            w.writerow([r["date"],r["entry_type"],r["amount"],r["direction"],r["payment_mode"],r["remarks"]])
        resp=make_response(buf.getvalue())
        resp.headers["Content-Type"]="text/csv"
        resp.headers["Content-Disposition"]=f"attachment; filename=Cash_{month}.csv"
        return resp


def register_routes_bpcl_dayend(app):
    from templates import BASE
    from flask import render_template_string

    def R(tpl,**ctx):
        ctx.setdefault("active","bpcld")
        full=BASE.replace("{% block body %}{% endblock %}",tpl)\
                 .replace("{% block scripts %}{% endblock %}",ctx.pop("scripts",""))
        return render_template_string(full,**ctx)

    def lr(f):
        from functools import wraps
        @wraps(f)
        def d(*a,**k):
            if "uid" not in session: return redirect("/login")
            return f(*a,**k)
        return d

    @app.route("/bpcl-dayend", methods=["GET","POST"])
    @lr
    def bpcl_dayend():
        t=today(); conn=get_db()
        if request.method=="POST":
            f=request.form
            b_open=int(f.get("bpcl_open_filled",0))
            b_recv=int(f.get("bpcl_received",0))
            b_issued=int(f.get("bpcl_issued",0))
            b_close_f=int(f.get("bpcl_close_filled",0))
            b_close_e=int(f.get("bpcl_close_empty",0))
            e_open_f=stock_bal(conn,"godown","filled")
            e_close_f=stock_bal(conn,"godown","filled")
            e_close_e=stock_bal(conn,"godown","empty")
            diff_f=b_close_f-e_close_f
            diff_e=b_close_e-e_close_e
            status="ok" if abs(diff_f)<=1 and abs(diff_e)<=1 else "difference"
            conn.execute("""INSERT OR REPLACE INTO bpcl_day_end(date,status,
                bpcl_open_filled,bpcl_received,bpcl_issued,bpcl_close_filled,bpcl_close_empty,
                erp_open_filled,erp_close_filled,erp_close_empty,
                diff_filled,diff_empty,entered_by) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (t,status,b_open,b_recv,b_issued,b_close_f,b_close_e,
                 e_open_f,e_close_f,e_close_e,diff_f,diff_e,session["uid"]))
            conn.commit()
            flash(f"✅ Day End saved — Status: {status.upper()}","success" if status=="ok" else "warning")
            return redirect("/bpcl-dayend")
        existing=conn.execute("SELECT * FROM bpcl_day_end WHERE date=?",(t,)).fetchone()
        g_f=stock_bal(conn,"godown","filled"); g_e=stock_bal(conn,"godown","empty")
        history=conn.execute("SELECT * FROM bpcl_day_end ORDER BY date DESC LIMIT 10").fetchall()
        conn.close()
        TPL="""
<div class="card">
  <div class="ch"><div class="ct">📊 BPCL Day End Comparison / तुलना</div>
    <span style="font-size:12px;color:var(--mu)">{{ t }}</span>
  </div>
  {% if existing %}
  <div class="al {{ 'als' if existing.status=='ok' else 'ald' }}">
    <strong>{{ '✅ OK' if existing.status=='ok' else '❌ Difference Found' }}</strong> —
    Diff Filled: {{ existing.diff_filled }}, Diff Empty: {{ existing.diff_empty }}
  </div>
  <div class="cmp">
    <div class="cmpr"><div>Item</div><div>ERP</div><div>BPCL SAP</div></div>
    <div class="cmpr"><div>Opening Filled</div><div>{{ existing.erp_open_filled }}</div><div>{{ existing.bpcl_open_filled }}</div></div>
    <div class="cmpr"><div>Received</div><div>—</div><div>{{ existing.bpcl_received }}</div></div>
    <div class="cmpr"><div>Closing Filled</div>
      <div class="{{ 'der' if existing.diff_filled else 'dok' }}">{{ existing.erp_close_filled }}</div>
      <div>{{ existing.bpcl_close_filled }}</div>
    </div>
    <div class="cmpr"><div>Closing Empty</div>
      <div class="{{ 'der' if existing.diff_empty else 'dok' }}">{{ existing.erp_close_empty }}</div>
      <div>{{ existing.bpcl_close_empty }}</div>
    </div>
  </div>
  {% endif %}
</div>
<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>✏️ {{ 'Update' if existing else 'Enter' }} Today's BPCL SAP Figures</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    <div class="al alw">BPCL eConnect → DayEnd → Copy figures below</div>
    <form method="post">
      <div class="g3">
        <div class="fg"><label>BPCL Opening Filled</label><input type="number" name="bpcl_open_filled" value="{{ existing.bpcl_open_filled if existing else '' }}" required></div>
        <div class="fg"><label>BPCL Received (from plant)</label><input type="number" name="bpcl_received" value="{{ existing.bpcl_received if existing else 0 }}"></div>
        <div class="fg"><label>BPCL Issued (to customers)</label><input type="number" name="bpcl_issued" value="{{ existing.bpcl_issued if existing else 0 }}"></div>
        <div class="fg"><label>BPCL Closing Filled</label><input type="number" name="bpcl_close_filled" value="{{ existing.bpcl_close_filled if existing else '' }}" required></div>
        <div class="fg"><label>BPCL Closing Empty</label><input type="number" name="bpcl_close_empty" value="{{ existing.bpcl_close_empty if existing else '' }}" required></div>
      </div>
      <div class="al ali">ERP values (auto): Godown Filled={{ g_f }}, Empty={{ g_e }}</div>
      <button type="submit" class="btn bs">✅ Save & Compare</button>
    </form>
  </div>
</div>
<div class="card">
  <div class="ch"><div class="ct">📋 Day End History</div></div>
  <div class="tw"><table>
    <tr><th>Date</th><th>Status</th><th>BPCL Close F</th><th>ERP Close F</th><th>Diff F</th><th>Diff E</th></tr>
    {% for h in history %}
    <tr>
      <td>{{ h.date }}</td>
      <td><span class="badge {{ 'bg' if h.status=='ok' else 'br2' }}">{{ h.status.upper() }}</span></td>
      <td>{{ h.bpcl_close_filled }}</td><td>{{ h.erp_close_filled }}</td>
      <td class="{{ 'der' if h.diff_filled else 'dok' }}">{{ h.diff_filled }}</td>
      <td class="{{ 'der' if h.diff_empty else 'dok' }}">{{ h.diff_empty }}</td>
    </tr>
    {% endfor %}
  </table></div>
</div>"""
        return R(TPL, t=t, existing=existing, g_f=g_f, g_e=g_e, history=history)
