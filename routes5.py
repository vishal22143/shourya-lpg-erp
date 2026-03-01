#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes Part 5: Users + Settings + Chat + Consumer Load — Shourya Bharatgas ERP"""
from flask import request, redirect, session, flash, jsonify
import csv, os
from db import (get_db, hpin, today, now_ts, gsetting, BDA_MAP, VEHICLES)

def register_routes_users(app):
    from templates import BASE
    from flask import render_template_string

    def R(tpl,**ctx):
        ctx.setdefault("active","users")
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

    @app.route("/users")
    @lr
    def users_list():
        if session.get("role") not in ["owner","manager"]:
            flash("Access denied","danger"); return redirect("/dashboard")
        conn=get_db()
        users=conn.execute("SELECT * FROM users ORDER BY role,name").fetchall()
        conn.close()
        ROLE_BADGE={"owner":"bpu","manager":"br2","office":"bb","delivery":"bg","bda":"by","loader":"bo2","driver":"bo2","accountant":"bb"}
        TPL="""
<div class="card">
  <div class="ch"><div class="ct">👥 कर्मचारी / Staff Management</div></div>
  <div class="tw"><table>
    <tr><th>नाव</th><th>Mobile</th><th>Role</th><th>Designation</th><th>Status</th><th>Actions</th></tr>
    {% for u in users %}
    <tr>
      <td><strong>{{ u.name }}</strong></td>
      <td>{{ u.mobile }}{% if u.alt_mobile %}<br><small>{{ u.alt_mobile }}</small>{% endif %}</td>
      <td><span class="badge {{ rbadge.get(u.role,'bb') }}">{{ u.role.upper() }}</span></td>
      <td style="font-size:12px">{{ u.designation }}<br>
        {% if u.wage_type=='salary' %}<span class="badge by">₹{{ '{:,.0f}'.format(u.salary_fixed) }}/mo</span>
        {% elif u.wage_type=='per_cylinder' %}<span class="badge bg">Per Cyl</span>
        {% elif u.wage_type=='per_truck' %}<span class="badge bo2">₹{{ u.salary_fixed }}/truck</span>
        {% endif %}
      </td>
      <td><span class="badge {{ 'bg' if u.is_active else 'br2' }}">{{ 'Active' if u.is_active else 'Inactive' }}</span>
        {% if u.must_change_pin %}<span class="badge by">PIN Pending</span>{% endif %}
      </td>
      <td style="white-space:nowrap">
        <form method="post" action="/users/toggle/{{ u.id }}" style="display:inline">
          <button class="btn btn-sm {{ 'bd' if u.is_active else 'bs' }}">{{ 'Deactivate' if u.is_active else 'Activate' }}</button>
        </form>
        <form method="post" action="/users/reset-pin/{{ u.id }}" style="display:inline"
          onsubmit="return confirm('Reset PIN to 1234?')">
          <button class="btn btn-sm bw">Reset PIN</button>
        </form>
      </td>
    </tr>
    {% endfor %}
  </table></div>
</div>

<!-- ADD STAFF -->
<div class="ex">
  <div class="exh op" onclick="xToggle(this)">
    <h3>➕ नवीन कर्मचारी / Add Staff</h3><span class="ar">▼</span>
  </div>
  <div class="exb sh">
    <form method="post" action="/users/add">
      <div class="g3">
        <div class="fg"><label>नाव / Name</label><input type="text" name="name" required></div>
        <div class="fg"><label>Mobile (login)</label><input type="tel" name="mobile" required pattern="[0-9]{10}"></div>
        <div class="fg"><label>Alt Mobile</label><input type="tel" name="alt_mobile" pattern="[0-9]{10}"></div>
        <div class="fg"><label>Role</label>
          <select name="role">
            <option value="delivery">Delivery Man</option>
            <option value="office">Office Staff</option>
            <option value="bda">BDA</option>
            <option value="loader">Loader</option>
            <option value="driver">Driver</option>
            <option value="accountant">Accountant</option>
            <option value="manager">Manager</option>
          </select>
        </div>
        <div class="fg"><label>Designation</label><input type="text" name="designation" placeholder="e.g. Delivery Man"></div>
        <div class="fg"><label>Wage Type</label>
          <select name="wage_type">
            <option value="per_cylinder">Per Cylinder (delivery)</option>
            <option value="salary">Fixed Salary</option>
            <option value="per_truck">Per Truck (loaders)</option>
            <option value="na">N/A</option>
          </select>
        </div>
        <div class="fg"><label>Salary / Rate ₹</label><input type="number" name="salary" value="0" step="0.01"></div>
        <div class="fg"><label>BDA Village</label>
          <select name="bda_id">
            <option value="">None</option>
            {% for bid,b in bda_map.items() %}
            <option value="{{ bid }}">{{ b.village }} ({{ b.owner }})</option>
            {% endfor %}
          </select>
        </div>
        <div class="fg"><label>Vehicle</label>
          <select name="vehicle_id">
            <option value="">None</option>
            {% for vid,v in vehicles.items() %}
            <option value="{{ vid }}">{{ v.name }}</option>
            {% endfor %}
          </select>
        </div>
        <div class="fg"><label>Temp? Expires</label><input type="date" name="temp_expires" placeholder="Leave blank if permanent"></div>
        <div class="fg"><label>Initial PIN</label><input type="text" name="pin" value="1234" maxlength="8"></div>
      </div>
      <button type="submit" class="btn bs">✅ Add Staff</button>
    </form>
  </div>
</div>"""
        return R(TPL, users=users, rbadge=ROLE_BADGE, bda_map=BDA_MAP, vehicles=VEHICLES)

    @app.route("/users/add", methods=["POST"])
    @lr
    def user_add():
        if session.get("role") not in ["owner","manager"]:
            flash("Access denied","danger"); return redirect("/dashboard")
        conn=get_db(); f=request.form
        is_temp=1 if f.get("temp_expires") else 0
        try:
            conn.execute("""INSERT INTO users(name,mobile,alt_mobile,role,designation,
                pin_hash,wage_type,salary_fixed,bda_id,vehicle_id,is_temp,temp_expires,must_change_pin)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,1)""",
                (f["name"],f["mobile"],f.get("alt_mobile",""),f["role"],f.get("designation",""),
                 hpin(f.get("pin","1234")),f.get("wage_type","na"),float(f.get("salary",0)),
                 int(f["bda_id"]) if f.get("bda_id") else None,
                 int(f["vehicle_id"]) if f.get("vehicle_id") else None,
                 is_temp,f.get("temp_expires") or None))
            conn.commit()
            flash(f"✅ {f['name']} added! Default PIN: {f.get('pin','1234')}","success")
        except Exception as e:
            flash(f"Error: {e}","danger")
        conn.close()
        return redirect("/users")

    @app.route("/users/toggle/<int:uid>", methods=["POST"])
    @lr
    def user_toggle(uid):
        conn=get_db()
        conn.execute("UPDATE users SET is_active=1-is_active WHERE id=?",(uid,))
        conn.commit(); conn.close()
        flash("✅ Status toggled","success"); return redirect("/users")

    @app.route("/users/reset-pin/<int:uid>", methods=["POST"])
    @lr
    def user_reset_pin(uid):
        conn=get_db()
        conn.execute("UPDATE users SET pin_hash=?,must_change_pin=1 WHERE id=?",(hpin("1234"),uid))
        conn.commit(); conn.close()
        flash("✅ PIN reset to 1234","success"); return redirect("/users")


def register_routes_settings(app):
    from templates import BASE
    from flask import render_template_string

    def R(tpl,**ctx):
        ctx.setdefault("active","settings")
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

    @app.route("/settings", methods=["GET","POST"])
    @lr
    def settings():
        if session.get("role")!="owner":
            flash("Owner only","danger"); return redirect("/dashboard")
        conn=get_db()
        if request.method=="POST":
            for k in ["cylinder_price","company_name","dist_code","gst_no","company_address","godown_address","gpay_mobile"]:
                v=request.form.get(k,"")
                conn.execute("INSERT OR REPLACE INTO settings VALUES(?,?)",(k,v))
            conn.commit(); conn.close()
            flash("✅ Settings saved!","success"); return redirect("/settings")
        settings_data={}
        for row in conn.execute("SELECT key,value FROM settings"):
            settings_data[row["key"]]=row["value"]
        blk=conn.execute("SELECT COUNT(*) FROM blocked_consumers").fetchone()[0]
        cm=conn.execute("SELECT COUNT(*) FROM consumer_master").fetchone()[0]
        conn.close()
        TPL="""
<div class="card">
  <div class="ch"><div class="ct">⚙️ ERP Settings / सेटिंग्ज</div></div>
  <form method="post">
    <div class="g3">
      <div class="fg"><label>Cylinder Price ₹ <small>(14.2kg)</small></label>
        <input type="number" name="cylinder_price" value="{{ s.get('cylinder_price','856') }}" step="0.01" required></div>
      <div class="fg"><label>Company Name</label><input type="text" name="company_name" value="{{ s.get('company_name','') }}"></div>
      <div class="fg"><label>BPCL Dist Code</label><input type="text" name="dist_code" value="{{ s.get('dist_code','187618') }}"></div>
      <div class="fg"><label>GST Number</label><input type="text" name="gst_no" value="{{ s.get('gst_no','') }}"></div>
      <div class="fg"><label>Company Address</label><input type="text" name="company_address" value="{{ s.get('company_address','') }}"></div>
      <div class="fg"><label>Godown Address</label><input type="text" name="godown_address" value="{{ s.get('godown_address','') }}"></div>
      <div class="fg"><label>GPay Mobile</label><input type="tel" name="gpay_mobile" value="{{ s.get('gpay_mobile','') }}"></div>
    </div>
    <button type="submit" class="btn bs">✅ Settings जतन करा</button>
  </form>
</div>

<!-- DATA IMPORT -->
<div class="card">
  <div class="ch"><div class="ct">📂 Data Import / डेटा</div></div>
  <div class="g3">
    <div class="sb"><div class="sv">{{ cm }}</div><div class="sl">Consumer Master Records</div></div>
    <div class="sb r"><div class="sv r">{{ blk }}</div><div class="sl">Blocked Consumers</div></div>
  </div>
  <div style="margin-top:14px;display:flex;gap:10px;flex-wrap:wrap">
    <a href="/load-consumers" class="btn bp" onclick="return confirm('Load/refresh ni.csv consumer master?')">
      📂 Load Consumer Master (ni.csv)</a>
    <a href="/load-blocked" class="btn bd" onclick="return confirm('Load/refresh blocked consumers?')">
      🚫 Load Blocked List</a>
  </div>
  <div class="al ali" style="margin-top:10px">
    ni.csv and ListOfBlockedConsumers.csv must be in the same folder as erp.py
  </div>
</div>"""
        return R(TPL, s=settings_data, blk=blk, cm=cm)

    @app.route("/load-consumers")
    @lr
    def load_consumers():
        if session.get("role")!="owner":
            flash("Owner only","danger"); return redirect("/settings")
        base=os.path.dirname(os.path.abspath(__file__))
        fpath=os.path.join(base,"ni.csv")
        if not os.path.exists(fpath):
            flash("❌ ni.csv not found in app folder","danger")
            return redirect("/settings")
        conn=get_db(); inserted=0; updated=0
        with open(fpath,"r",encoding="utf-8-sig",errors="ignore") as f:
            reader=csv.reader(f)
            headers=[h.strip().lower() for h in next(reader,[])]
            for row in reader:
                if not row: continue
                try:
                    d=dict(zip(headers,[c.strip() for c in row]))
                    cno=d.get("consumer_no") or d.get("consumerno") or d.get("consumer_number","")
                    name=d.get("consumer_name") or d.get("name","")
                    if not cno: continue
                    area=d.get("area",""); mob=d.get("mobile","")
                    loc="rural" if any(b["village"].lower() in area.lower() for b in BDA_MAP.values()) else "urban"
                    conn.execute("""INSERT OR REPLACE INTO consumer_master
                        (consumer_number,consumer_name,area_id,area_desc,mobile,location_type)
                        VALUES(?,?,?,?,?,?)""",(cno,name,area,area,mob,loc))
                    inserted+=1
                except: pass
        conn.commit(); conn.close()
        flash(f"✅ Consumer master: {inserted} records loaded","success")
        return redirect("/settings")

    @app.route("/load-blocked")
    @lr
    def load_blocked():
        if session.get("role")!="owner":
            flash("Owner only","danger"); return redirect("/settings")
        base=os.path.dirname(os.path.abspath(__file__))
        fpath=os.path.join(base,"ListOfBlockedConsumers.csv")
        if not os.path.exists(fpath):
            flash("❌ ListOfBlockedConsumers.csv not found","danger")
            return redirect("/settings")
        conn=get_db(); inserted=0
        with open(fpath,"r",encoding="utf-8-sig",errors="ignore") as f:
            reader=csv.reader(f)
            headers=[h.strip().lower() for h in next(reader,[])]
            for row in reader:
                if not row: continue
                try:
                    d=dict(zip(headers,[c.strip() for c in row]))
                    cno=d.get("consumer_no") or d.get("consumerno") or d.get("consumer_number","")
                    name=d.get("consumer_name") or d.get("name","")
                    reason=d.get("block_reason") or d.get("reason","Blocked")
                    if not cno: continue
                    conn.execute("INSERT OR REPLACE INTO blocked_consumers(consumer_number,consumer_name,block_reason) VALUES(?,?,?)",
                        (cno,name,reason))
                    inserted+=1
                except: pass
        conn.commit(); conn.close()
        flash(f"✅ Blocked consumers: {inserted} records loaded","success")
        return redirect("/settings")


def register_routes_chat(app):
    from templates import BASE
    from flask import render_template_string
    import os

    UPLOAD_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),"static","chat_photos")
    os.makedirs(UPLOAD_DIR,exist_ok=True)

    def R(tpl,**ctx):
        ctx.setdefault("active","chat")
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

    @app.route("/chat")
    @lr
    def chat():
        conn=get_db()
        msgs=conn.execute("""SELECT m.*,u.name sender_name,u.role sender_role
            FROM chat_messages m JOIN users u ON m.sender_id=u.id
            ORDER BY m.id DESC LIMIT 100""").fetchall()
        msgs=list(reversed(msgs))
        conn.close()
        TPL="""
<div class="card" style="padding:0;overflow:hidden">
  <div style="background:linear-gradient(135deg,#002244,#0066cc);padding:14px;color:#fff">
    <strong>💬 Shourya Team Chat</strong>
    <small style="display:block;opacity:.7;margin-top:2px">सर्व कर्मचाऱ्यांसाठी / All Staff</small>
  </div>
  <div id="chatbox" style="height:55vh;overflow-y:auto;padding:14px;background:#f8f9fa;display:flex;flex-direction:column;gap:8px">
    {% for m in msgs %}
    {% set mine=m.sender_id==session.uid %}
    <div style="display:flex;flex-direction:column;align-items:{{ 'flex-end' if mine else 'flex-start' }}">
      {% if not mine %}
      <div style="font-size:10px;color:#999;margin-bottom:2px">{{ m.sender_name }}
        <span class="badge bb" style="font-size:9px">{{ m.sender_role }}</span>
      </div>
      {% endif %}
      {% if m.is_notice %}
      <div style="background:#FFD700;color:#002244;border-radius:10px;padding:8px 13px;max-width:85%;
        font-weight:700;border:2px solid #e5c200;font-size:13px">📢 {{ m.message }}</div>
      {% elif m.photo_path %}
      <div style="background:{{ '#d1e7ff' if not mine else '#003366' }};border-radius:10px;padding:8px;max-width:80%">
        <img src="/static/chat_photos/{{ m.photo_path }}" style="max-width:220px;border-radius:8px;display:block">
        {% if m.message %}<div style="font-size:12px;margin-top:4px;color:{{ '#fff' if mine else '#333' }}">{{ m.message }}</div>{% endif %}
      </div>
      {% else %}
      <div style="background:{{ '#003366' if mine else '#fff' }};color:{{ '#fff' if mine else '#333' }};
        border-radius:{{ '14px 14px 4px 14px' if mine else '14px 14px 14px 4px' }};
        padding:9px 13px;max-width:80%;font-size:13.5px;box-shadow:0 1px 3px rgba(0,0,0,.1)">
        {{ m.message }}
      </div>
      {% endif %}
      <div style="font-size:10px;color:#aaa;margin-top:2px">{{ m.created_at[11:16] }}</div>
    </div>
    {% else %}
    <div style="text-align:center;color:#aaa;font-size:12px;padding:20px">
      No messages yet. Start chatting! 💬
    </div>
    {% endfor %}
  </div>
  <!-- SEND FORM -->
  <div style="padding:12px;border-top:2px solid #eee;background:#fff">
    {% if session.role in ['owner','manager'] %}
    <div style="margin-bottom:8px">
      <label style="font-size:11px;font-weight:700;color:#666">Notice mode:
        <input type="checkbox" id="notice_toggle" onchange="toggleNotice()">
        <span style="color:#d4a000">📢 Broadcast Notice</span>
      </label>
    </div>
    {% endif %}
    <form method="post" action="/chat/send" enctype="multipart/form-data" id="chatForm">
      <input type="hidden" name="is_notice" id="is_notice_val" value="0">
      <div style="display:flex;gap:8px;align-items:flex-end">
        <div style="flex:1">
          <textarea name="message" id="msgbox" placeholder="संदेश लिहा... (Type message)" required
            rows="2" style="resize:none;border-radius:10px;padding:8px 11px;font-size:14px"
            onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();document.getElementById('chatForm').submit();}"></textarea>
        </div>
        <div style="display:flex;flex-direction:column;gap:4px">
          <label style="background:#0066cc;color:#fff;border-radius:8px;padding:8px 14px;
            cursor:pointer;font-size:13px;font-weight:700;text-align:center">
            📷<input type="file" name="photo" accept="image/*" style="display:none" onchange="this.form.submit()">
          </label>
          <button type="submit" class="btn bp" style="padding:8px 14px">Send ▶</button>
        </div>
      </div>
    </form>
  </div>
</div>
<script>
var cb=document.getElementById('chatbox');
if(cb) cb.scrollTop=cb.scrollHeight;
function toggleNotice(){
  var v=document.getElementById('notice_toggle').checked?'1':'0';
  document.getElementById('is_notice_val').value=v;
  document.getElementById('msgbox').style.background=v==='1'?'#fffde7':'';
}
// Auto-refresh every 15s
setTimeout(function(){location.reload();},15000);
</script>"""
        return R(TPL, msgs=msgs)

    @app.route("/chat/send", methods=["POST"])
    @lr
    def chat_send():
        msg=request.form.get("message","").strip()
        is_notice=1 if request.form.get("is_notice")=="1" else 0
        photo=request.files.get("photo")
        photo_path=None
        if photo and photo.filename:
            import time; ext=os.path.splitext(photo.filename)[1].lower()
            fname=f"{int(time.time())}_{session['uid']}{ext}"
            photo.save(os.path.join(UPLOAD_DIR,fname))
            photo_path=fname
        if not msg and not photo_path:
            return redirect("/chat")
        conn=get_db()
        conn.execute("INSERT INTO chat_messages(sender_id,message,is_notice,photo_path) VALUES(?,?,?,?)",
            (session["uid"],msg or "",is_notice,photo_path))
        conn.commit(); conn.close()
        return redirect("/chat")
