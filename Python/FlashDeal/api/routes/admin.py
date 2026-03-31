"""
admin.py — Plattformsadmin: godkänn butiker, se aktivitet
Prefix: /admin
Skyddad med PIN från .env (ADMIN_PIN)
"""
import os, html as _html
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from api.config import db, admin_required, send_email

bp = Blueprint('admin', __name__)

# ─── Login / logout ───────────────────────────────────────────────────────────

@bp.route('/logga-in', methods=['GET', 'POST'])
def login():
    if session.get('is_admin'):
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        pin = request.form.get('pin', '').strip()
        if pin == os.environ.get('ADMIN_PIN', ''):
            session['is_admin'] = True
            session['role']     = 'admin'
            return redirect(url_for('admin.dashboard'))
        flash('Fel PIN-kod.', 'error')

    return render_template('admin/login.html')


@bp.route('/logga-ut')
def logout():
    session.pop('is_admin', None)
    if session.get('role') == 'admin':
        session.pop('role', None)
    return redirect(url_for('admin.login'))


# ─── Dashboard ────────────────────────────────────────────────────────────────

@bp.route('/')
@admin_required
def dashboard():
    pending_stores = db.select('stores', {'status': 'pending'}, order='created_at.asc')
    recent_bookings = db.select('bookings', {'payment_status': 'paid'},
                                order='created_at.desc', limit=20)
    # Statistik
    all_stores   = db.select('stores', columns='id,status')
    all_customers = db.select('customers', columns='id', limit=1)

    approved_count = sum(1 for s in all_stores if s.get('status') == 'approved')
    pending_count  = sum(1 for s in all_stores if s.get('status') == 'pending')
    total_revenue  = sum(float(b.get('platform_fee') or 0) for b in recent_bookings)

    # Berika bokningar
    offer_ids = list({b['offer_id'] for b in recent_bookings})
    store_ids = list({b['store_id'] for b in recent_bookings})
    offers_map = {}
    stores_map = {}
    if offer_ids:
        offers_map = {o['id']: o for o in db.select('offers', {'id': offer_ids}, 'id,title')}
    if store_ids:
        stores_map = {s['id']: s for s in db.select('stores', {'id': store_ids}, 'id,business_name')}
    for b in recent_bookings:
        b['offer'] = offers_map.get(b['offer_id'], {})
        b['store'] = stores_map.get(b['store_id'], {})

    recent_customers = db.select('customers', columns='id,email,full_name,created_at',
                                 order='created_at.desc', limit=20)

    return render_template('admin/dashboard.html',
                           pending_stores=pending_stores,
                           recent_bookings=recent_bookings,
                           approved_count=approved_count,
                           pending_count=pending_count,
                           total_revenue=total_revenue,
                           recent_customers=recent_customers)


# ─── Butikslista ──────────────────────────────────────────────────────────────

@bp.route('/butiker')
@admin_required
def stores():
    status = request.args.get('status', 'all')
    filters = {} if status == 'all' else {'status': status}
    all_stores = db.select('stores', filters or None, order='created_at.desc')
    return render_template('admin/stores.html', stores=all_stores, active_status=status)


@bp.route('/butik/<store_id>')
@admin_required
def store_detail(store_id):
    store    = db.get_one('stores', {'id': store_id})
    offers   = db.select('offers', {'store_id': store_id}, order='created_at.desc', limit=20)
    bookings = db.select('bookings', {'store_id': store_id}, order='created_at.desc', limit=20)
    return render_template('admin/store_detail.html', store=store, offers=offers, bookings=bookings)


# ─── Godkänn / avvisa butik ──────────────────────────────────────────────────

@bp.route('/butik/<store_id>/godkann', methods=['POST'])
@admin_required
def approve_store(store_id):
    from datetime import datetime, timezone
    store = db.get_one('stores', {'id': store_id})
    if not store:
        flash('Butiken hittades inte.', 'error')
        return redirect(url_for('admin.dashboard'))

    db.update('stores', {'id': store_id}, {
        'status':      'approved',
        'approved_at': datetime.now(timezone.utc).isoformat(),
    })

    _send_store_status_email(store, 'approved')
    flash(f'✅ {store["business_name"]} är godkänd!', 'success')
    return redirect(url_for('admin.dashboard'))


@bp.route('/butik/<store_id>/avvisa', methods=['POST'])
@admin_required
def reject_store(store_id):
    store = db.get_one('stores', {'id': store_id})
    if not store:
        flash('Butiken hittades inte.', 'error')
        return redirect(url_for('admin.dashboard'))

    note = request.form.get('note', '').strip()
    db.update('stores', {'id': store_id}, {'status': 'rejected', 'rejection_note': note or None})
    _send_store_status_email(store, 'rejected', note)
    flash(f'Butiken {store["business_name"]} avvisades.', 'info')
    return redirect(url_for('admin.dashboard'))


# ─── Mailutskick ─────────────────────────────────────────────────────────────

def _send_store_status_email(store, status, note=''):
    base = os.environ.get('BASE_URL', 'http://localhost:5000')
    name = _html.escape(store.get('business_name', 'Butik'))
    if status == 'approved':
        subject = f'✅ Välkommen till FlashDeal — {store.get("business_name", "")}'
        body = f"""<div style="font-family:sans-serif;max-width:500px;margin:0 auto;background:#0f0e0c;color:#f7f5f0;border-radius:12px;overflow:hidden">
  <div style="background:#1a9a6c;padding:14px 24px;font-size:11px;letter-spacing:2px;text-transform:uppercase">✅ Ansökan godkänd</div>
  <div style="padding:28px">
    <h2 style="font-size:22px;margin:0 0 12px">Välkommen, {name}!</h2>
    <p style="color:#b0a898">Er butik är nu godkänd på FlashDeal. Logga in för att börja publicera erbjudanden.</p>
    <a href="{base}/butik/logga-in" style="display:block;background:#d4541a;color:#fff;text-align:center;padding:14px;border-radius:8px;text-decoration:none;font-weight:700;margin-top:20px">Logga in nu &rarr;</a>
  </div>
</div>"""
    else:
        subject = 'FlashDeal — Uppdatering om er ansökan'
        note_html = f'<p style="color:#b0a898;font-size:14px">Anledning: {_html.escape(note)}</p>' if note else ''
        body = f"""<div style="font-family:sans-serif;max-width:500px;margin:0 auto;background:#0f0e0c;color:#f7f5f0;border-radius:12px;overflow:hidden">
  <div style="background:#c84040;padding:14px 24px;font-size:11px;letter-spacing:2px;text-transform:uppercase">Ansökan ej godkänd</div>
  <div style="padding:28px">
    <h2 style="font-size:20px;margin:0 0 12px">Hej {name}</h2>
    <p style="color:#b0a898">Vi kan tyvärr inte godkänna er ansökan just nu.</p>
    {note_html}
    <p style="color:#7a7570;font-size:13px">Kontakta oss om ni har frågor.</p>
  </div>
</div>"""

    send_email(store['email'], subject, body)
