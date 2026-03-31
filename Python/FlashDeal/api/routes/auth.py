"""
auth.py — Registrering och inloggning för kunder och butiker
"""
import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from api.config import db, hash_pw, verify_pw

bp = Blueprint('auth', __name__)

# ─── Kund: registrera ─────────────────────────────────────────────────────────

@bp.route('/registrera', methods=['GET', 'POST'])
def register():
    categories = db.select('categories', order='name')
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        phone    = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        name     = request.form.get('full_name', '').strip()
        cat_ids  = request.form.getlist('categories')
        n_email  = 'notify_email' in request.form
        n_sms    = 'notify_sms' in request.form

        if not email or not password:
            flash('E-post och lösenord krävs.', 'error')
            return render_template('auth/register.html', categories=categories)

        if len(password) < 8:
            flash('Lösenordet måste vara minst 8 tecken.', 'error')
            return render_template('auth/register.html', categories=categories)

        if db.get_one('customers', {'email': email}):
            flash('E-postadressen är redan registrerad.', 'error')
            return render_template('auth/register.html', categories=categories)

        customer = db.insert('customers', {
            'email':        email,
            'phone':        phone or None,
            'password_hash': hash_pw(password),
            'full_name':    name or None,
            'notify_email': n_email,
            'notify_sms':   n_sms,
        })
        if not customer:
            flash('Något gick fel. Försök igen.', 'error')
            return render_template('auth/register.html', categories=categories)

        for cid in cat_ids:
            db.insert('customer_subscriptions', {'customer_id': customer['id'], 'category_id': cid})

        session['user_id']   = customer['id']
        session['user_name'] = customer.get('full_name') or email
        session['role']      = 'customer'
        flash('Välkommen! Du är nu registrerad.', 'success')
        return redirect(url_for('public.index'))

    return render_template('auth/register.html', categories=categories)


# ─── Kund: logga in ───────────────────────────────────────────────────────────

@bp.route('/logga-in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        customer = db.get_one('customers', {'email': email})
        if customer and verify_pw(password, customer['password_hash']):
            session['user_id']   = customer['id']
            session['user_name'] = customer.get('full_name') or email
            session['role']      = 'customer'
            next_url = request.args.get('next', '')
            if not next_url.startswith('/'):
                next_url = url_for('public.index')
            return redirect(next_url)

        flash('Fel e-post eller lösenord.', 'error')

    return render_template('auth/login.html')


# ─── Butik: registrera ────────────────────────────────────────────────────────

@bp.route('/butik/registrera', methods=['GET', 'POST'])
def store_register():
    import os as _os
    _has_backend = bool(_os.environ.get('SUPABASE_URL', ''))
    categories = db.select('categories', order='name')
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        name     = request.form.get('business_name', '').strip()
        contact  = request.form.get('contact_person', '').strip()
        phone    = request.form.get('phone', '').strip()
        address  = request.form.get('address', '').strip()
        city     = request.form.get('city', '').strip()
        cat_ids  = request.form.getlist('category_ids')   # flerkategori
        desc     = request.form.get('description', '').strip()
        gdpr_ok  = 'gdpr_accept' in request.form

        def _err(msg):
            flash(msg, 'error')
            return render_template('auth/store_register.html', categories=categories, has_backend=_has_backend)

        if not email or not password or not name:
            return _err('Namn, e-post och lösenord krävs.')
        if not gdpr_ok:
            return _err('Du måste godkänna integritetspolicyn för att registrera dig.')
        if len(password) < 8:
            return _err('Lösenordet måste vara minst 8 tecken.')
        if db.get_one('stores', {'email': email}):
            return _err('E-postadressen är redan registrerad.')

        slug = _make_slug(name)
        if db.get_one('stores', {'slug': slug}):
            slug = slug + '-2'

        primary_cat = cat_ids[0] if cat_ids else None

        store = db.insert('stores', {
            'email':          email,
            'password_hash':  hash_pw(password),
            'business_name':  name,
            'slug':           slug,
            'contact_person': contact or None,
            'phone':          phone or None,
            'address':        address or None,
            'city':           city or 'Sverige',
            'category_id':    primary_cat,
            'description':    desc or None,
            'status':         'pending',
            'gdpr_accepted':  True,
        })
        if not store:
            flash('Något gick fel. Försök igen.', 'error')
            return render_template('auth/store_register.html', categories=categories, has_backend=_has_backend)

        # Spara alla valda kategorier i kopplingtabellen
        for cid in cat_ids:
            db.insert('store_categories', {'store_id': store['id'], 'category_id': cid})

        session['store_id']     = store['id']
        session['store_name']   = name
        session['store_status'] = 'pending'
        session['role']         = 'store'
        flash('Registrering mottagen! Vi granskar din ansökan och återkommer via e-post.', 'success')
        return redirect(url_for('store.pending'))

    return render_template('auth/store_register.html', categories=categories, has_backend=_has_backend)


# ─── Butik: logga in ──────────────────────────────────────────────────────────

@bp.route('/butik/logga-in', methods=['GET', 'POST'])
def store_login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        store = db.get_one('stores', {'email': email})
        if store and verify_pw(password, store['password_hash']):
            session['store_id']     = store['id']
            session['store_name']   = store['business_name']
            session['store_status'] = store['status']
            session['role']         = 'store'
            if store['status'] == 'approved':
                return redirect(url_for('store.dashboard'))
            return redirect(url_for('store.pending'))

        flash('Fel e-post eller lösenord.', 'error')

    return render_template('auth/store_login.html')


# ─── Logga ut ─────────────────────────────────────────────────────────────────

@bp.route('/logga-ut')
def logout():
    session.clear()
    flash('Du är nu utloggad.', 'info')
    return redirect(url_for('public.index'))


# ─── Hjälpfunktioner ──────────────────────────────────────────────────────────

def _make_slug(name):
    import unicodedata
    s = unicodedata.normalize('NFD', name.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:60]
