"""
config.py — Delade hjälpfunktioner och tjänster
SupabaseREST · Mail (Gmail OAuth/SMTP) · SMS (46elks) · QR · Bilduppladdning · Notiser
"""
import os, json, base64, io, secrets, html as _html
import requests
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

# ─── Supabase REST ────────────────────────────────────────────────────────────

class SupabaseREST:
    def __init__(self):
        self.url = os.environ.get('SUPABASE_URL', '')
        self.key = os.environ.get('SUPABASE_KEY', '')

    def _h(self):
        return {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        }

    def _ep(self, table):
        return f'{self.url}/rest/v1/fd_{table}'

    def select(self, table, filters=None, columns='*', order=None, limit=None):
        params = {'select': columns}
        if filters:
            for k, v in filters.items():
                if isinstance(v, list):
                    params[k] = f'in.({",".join(str(x) for x in v)})'
                elif isinstance(v, dict):
                    op, val = next(iter(v.items()))
                    params[k] = f'{op}.{val}'
                else:
                    params[k] = f'eq.{v}'
        if order:  params['order']  = order
        if limit:  params['limit']  = str(limit)
        if not self.url:
            from api.demo_data import demo_select
            return demo_select(table, filters, columns, order, limit)
        try:
            r = requests.get(self._ep(table), headers=self._h(), params=params, timeout=10)
        except Exception as e:
            print(f'[DB select error] {table}: {e}')
            return []
        if not r.ok:
            print(f'[DB select error] {table}: {r.status_code} {r.text[:200]}')
            return []
        return r.json()

    def get_one(self, table, filters=None, columns='*'):
        rows = self.select(table, filters, columns, limit=1)
        return rows[0] if rows else None

    def insert(self, table, data):
        if not self.url:
            from api.demo_data import demo_insert
            return demo_insert(table, data)
        try:
            r = requests.post(self._ep(table), headers=self._h(), json=data, timeout=10)
        except Exception as e:
            print(f'[DB insert error] {table}: {e}'); return None
        if not r.ok:
            print(f'[DB insert error] {table}: {r.status_code} {r.text[:200]}')
            return None
        result = r.json()
        return result[0] if isinstance(result, list) and result else result

    def update(self, table, filters, data):
        if not self.url:
            from api.demo_data import demo_update
            return demo_update(table, filters, data)
        params = {}
        for k, v in filters.items():
            if isinstance(v, dict):
                op, val = next(iter(v.items()))
                params[k] = f'{op}.{val}'
            else:
                params[k] = f'eq.{v}'
        try:
            r = requests.patch(self._ep(table), headers=self._h(), params=params, json=data, timeout=10)
        except Exception as e:
            print(f'[DB update error] {table}: {e}'); return None
        if not r.ok:
            print(f'[DB update error] {table}: {r.status_code} {r.text[:200]}')
            return None
        result = r.json()
        return result[0] if isinstance(result, list) and result else result

    def delete(self, table, filters):
        if not self.url:
            from api.demo_data import demo_delete
            return demo_delete(table, filters)
        params = {k: f'eq.{v}' for k, v in filters.items()}
        try:
            r = requests.delete(self._ep(table), headers=self._h(), params=params, timeout=10)
            return r.ok
        except Exception as e:
            print(f'[DB delete error] {table}: {e}'); return False

    def rpc(self, fn, params=None):
        if not self.url:
            return None
        try:
            r = requests.post(
                f'{self.url}/rest/v1/rpc/{fn}',
                headers=self._h(),
                json=params or {},
                timeout=10,
            )
            return r.json() if r.ok else None
        except Exception as e:
            print(f'[DB rpc error] {fn}: {e}')
            return None


db = SupabaseREST()

# ─── Auth / Session-dekoratorer ───────────────────────────────────────────────

def hash_pw(pw):
    return generate_password_hash(pw)

def verify_pw(pw, h):
    return check_password_hash(h, pw)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Logga in för att fortsätta.', 'info')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def store_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('store_id'):
            flash('Logga in som butik.', 'info')
            return redirect(url_for('auth.store_login'))
        if session.get('store_status') != 'approved':
            return redirect(url_for('store.pending'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated

# ─── Mail (Gmail OAuth → SMTP → console) ─────────────────────────────────────

def send_email(to, subject, html_body):
    if os.environ.get('GOOGLE_CREDENTIALS'):
        return _gmail_api(to, subject, html_body)
    if os.environ.get('GMAIL_USER'):
        return _gmail_smtp(to, subject, html_body)
    print(f'\n[DEV MAIL → {to}]\nSubject: {subject}\n{html_body[:300]}\n')
    return True

def _gmail_api(to, subject, html_body):
    try:
        import email.mime.multipart, email.mime.text
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        creds = Credentials.from_authorized_user_info(
            json.loads(os.environ['GOOGLE_CREDENTIALS']),
            ['https://www.googleapis.com/auth/gmail.send']
        )
        svc = build('gmail', 'v1', credentials=creds, cache_discovery=False)
        msg = email.mime.multipart.MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['To']      = to
        msg['From']    = f'FlashDeal <{os.environ.get("GMAIL_USER", "me")}>'
        msg.attach(email.mime.text.MIMEText(html_body, 'html', 'utf-8'))
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        svc.users().messages().send(userId='me', body={'raw': raw}).execute()
        return True
    except Exception as e:
        print(f'[Gmail API error] {e}')
        return _gmail_smtp(to, subject, html_body)

def _gmail_smtp(to, subject, html_body):
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        user = os.environ.get('GMAIL_USER')
        pw   = os.environ.get('GMAIL_APP_PASSWORD')
        if not user or not pw:
            print(f'[SMTP] Inga uppgifter. Mail till {to} ej skickat.')
            return False
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From']    = f'FlashDeal <{user}>'
        msg['To']      = to
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(user, pw)
            s.sendmail(user, to, msg.as_string())
        return True
    except Exception as e:
        print(f'[SMTP error] {e}')
        return False

# ─── SMS via 46elks ───────────────────────────────────────────────────────────

def send_sms(to, message):
    u = os.environ.get('ELKS_USERNAME')
    p = os.environ.get('ELKS_PASSWORD')
    if not u or not p:
        print(f'[DEV SMS → {to}] {message}')
        return True
    try:
        r = requests.post(
            'https://api.46elks.com/a1/sms',
            auth=(u, p),
            data={'from': os.environ.get('ELKS_FROM', 'FlashDeal'), 'to': to, 'message': message},
            timeout=10
        )
        return r.ok
    except Exception as e:
        print(f'[SMS error] {e}')
        return False

# ─── QR-kod ───────────────────────────────────────────────────────────────────

def generate_qr_base64(token):
    try:
        import qrcode
        base = os.environ.get('BASE_URL', 'http://localhost:5000')
        url  = f'{base}/butik/skanna/verifiera/{token}'
        img  = qrcode.make(url)
        buf  = io.BytesIO()
        img.save(buf, format='PNG')
        return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        print(f'[QR error] {e}')
        return ''

# ─── Bilduppladdning till Supabase Storage ────────────────────────────────────

def upload_image(file_data, filename, bucket='offer-photos'):
    url = f"{os.environ.get('SUPABASE_URL')}/storage/v1/object/{bucket}/{filename}"
    headers = {
        'Authorization': f"Bearer {os.environ.get('SUPABASE_KEY')}",
        'Content-Type': 'image/jpeg',
        'x-upsert': 'true',
    }
    r = requests.post(url, headers=headers, data=file_data, timeout=30)
    if r.ok:
        return f"{os.environ.get('SUPABASE_URL')}/storage/v1/object/public/{bucket}/{filename}"
    print(f'[Upload error] {r.status_code} {r.text[:200]}')
    return None

# ─── Priser: formatering ──────────────────────────────────────────────────────

def fmt_price(amount):
    """Formatera SEK-belopp (NUMERIC) till snygg sträng, t.ex. 1 299."""
    if amount is None:
        return '0'
    try:
        return f'{int(float(amount)):,}'.replace(',', '\u00a0')
    except Exception:
        return str(amount)

# ─── Notifiering med throttle ─────────────────────────────────────────────────

def notify_subscribers(offer):
    """Skicka mail/SMS till prenumeranter på erbjudandets kategori.
    Throttle: max 1 notis per kund/kategori/kanal per 10 minuter."""
    category_id = offer.get('category_id')
    if not category_id:
        return

    store    = db.get_one('stores', {'id': offer['store_id']}, 'business_name,city,address')
    category = db.get_one('categories', {'id': category_id}, 'name,icon')
    if not store or not category:
        return

    subs = db.select('customer_subscriptions', {'category_id': category_id}, 'customer_id')
    if not subs:
        return

    cids = [s['customer_id'] for s in subs]
    customers = db.select('customers', {'id': cids}, 'id,email,phone,notify_email,notify_sms')

    cutoff = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()

    for c in customers:
        cid = c['id']
        if c.get('notify_email') and c.get('email'):
            if not _throttled(cid, category_id, 'email', cutoff):
                html = _offer_email_html(offer, store, category)
                if send_email(c['email'], f"⚡ {store['business_name']}: {offer['title']}", html):
                    db.insert('notification_log', {
                        'customer_id': cid, 'category_id': category_id, 'channel': 'email'
                    })

        if c.get('notify_sms') and c.get('phone'):
            if not _throttled(cid, category_id, 'sms', cutoff):
                base = os.environ.get('BASE_URL', 'http://localhost:5000')
                msg  = (f"⚡ {store['business_name']}: {offer['title']} — "
                        f"{fmt_price(offer['deal_price'])} kr. "
                        f"Boka: {base}/erbjudande/{offer['id']}")
                if send_sms(c['phone'], msg):
                    db.insert('notification_log', {
                        'customer_id': cid, 'category_id': category_id, 'channel': 'sms'
                    })

def _throttled(customer_id, category_id, channel, cutoff):
    rows = db.select('notification_log', {
        'customer_id': customer_id,
        'category_id': category_id,
        'channel':     channel,
        'sent_at':     {'gte': cutoff},
    }, limit=1)
    return bool(rows)

def _offer_email_html(offer, store, category):
    base     = os.environ.get('BASE_URL', 'http://localhost:5000')
    price    = fmt_price(offer.get('deal_price'))
    orig     = fmt_price(offer.get('original_price'))
    expires  = (offer.get('expires_at') or '')[:16].replace('T', ' kl ')
    # Escape all user-controlled strings before embedding in HTML
    s_name   = _html.escape(store.get('business_name', ''))
    s_city   = _html.escape(store.get('city', ''))
    o_title  = _html.escape(offer.get('title', ''))
    o_desc   = _html.escape(offer.get('description', '') or '')
    c_name   = _html.escape(category.get('name', 'Erbjudande'))
    c_icon   = _html.escape(category.get('icon', ''))
    img_html = ''
    if offer.get('photo_url'):
        img_html = f'<img src="{_html.escape(offer["photo_url"])}" style="width:100%;max-height:220px;object-fit:cover;border-radius:8px;margin-bottom:18px">'
    discount = ''
    if offer.get('original_price') and offer.get('deal_price'):
        try:
            pct = round((1 - float(offer['deal_price']) / float(offer['original_price'])) * 100)
            discount = f'<span style="background:#d4541a;color:#fff;padding:3px 10px;border-radius:4px;font-size:12px;font-weight:700;margin-left:8px">-{pct}%</span>'
        except Exception:
            pass

    return f"""<div style="font-family:'Segoe UI',sans-serif;max-width:520px;margin:0 auto;background:#0f0e0c;color:#f7f5f0;border-radius:12px;overflow:hidden">
  <div style="background:#d4541a;padding:14px 24px;font-size:11px;letter-spacing:3px;text-transform:uppercase;font-weight:600">
    ⚡ FlashDeal &middot; {c_icon} {c_name}
  </div>
  <div style="padding:28px 28px 20px">
    {img_html}
    <div style="font-size:12px;color:#7a7570;margin-bottom:6px">{s_name} &middot; {s_city}</div>
    <h2 style="font-size:22px;margin:0 0 10px;color:#f7f5f0;line-height:1.3">{o_title}</h2>
    <p style="color:#b0a898;font-size:14px;margin:0 0 18px;line-height:1.6">{o_desc}</p>
    <div style="margin-bottom:18px">
      <span style="font-size:30px;font-weight:700;color:#d4541a">{price} kr</span>{discount}
      <span style="font-size:13px;color:#5a5650;text-decoration:line-through;margin-left:10px">{orig} kr</span>
    </div>
    <div style="background:#1a1814;border:1px solid #2a2824;border-radius:8px;padding:12px 16px;margin-bottom:22px;font-size:13px;color:#febc2e">
      ⏱ Gäller till: {expires}
    </div>
    <a href="{base}/erbjudande/{_html.escape(str(offer.get('id','')))}",
       style="display:block;background:#d4541a;color:#fff;text-align:center;padding:15px;border-radius:8px;text-decoration:none;font-weight:700;font-size:16px">
      Boka nu &rarr;
    </a>
  </div>
  <div style="padding:14px 24px;border-top:1px solid #1e1c18;font-size:11px;color:#5a5650;text-align:center">
    Du får detta för att du prenumererar på {c_name}-erbjudanden.
  </div>
</div>"""
