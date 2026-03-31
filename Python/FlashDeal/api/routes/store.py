"""
store.py — Butikspanel: erbjudanden, bokningar, QR-skanning, profil
Prefix: /butik
"""
import os, secrets
from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from api.config import db, store_required, notify_subscribers, upload_image, generate_qr_base64

bp = Blueprint('store', __name__)

# ─── Väntar på godkännande ────────────────────────────────────────────────────

@bp.route('/vantar')
def pending():
    if session.get('store_status') == 'approved':
        return redirect(url_for('store.dashboard'))
    status = session.get('store_status', 'pending')
    return render_template('store/pending.html', status=status)


# ─── Dashboard ────────────────────────────────────────────────────────────────

@bp.route('/panel')
@store_required
def dashboard():
    sid = session['store_id']
    store = db.get_one('stores', {'id': sid})

    offers = db.select('offers', {'store_id': sid},
                       order='created_at.desc', limit=20)

    # Statistik
    active_offers = [o for o in offers if o.get('status') == 'active']
    today = datetime.now(timezone.utc).date().isoformat()
    bookings_today = db.select('bookings', {
        'store_id':       sid,
        'payment_status': 'paid',
        'created_at':     {'gte': today},
    })
    total_revenue = sum(float(b.get('total_paid') or 0) for b in bookings_today)
    platform_fee  = sum(float(b.get('platform_fee') or 0) for b in bookings_today)

    return render_template('store/dashboard.html',
                           store=store,
                           offers=offers,
                           active_count=len(active_offers),
                           bookings_today=len(bookings_today),
                           revenue_today=total_revenue - platform_fee,
                           stripe_ok=bool(store.get('stripe_onboarding_done')))


# ─── Nytt erbjudande ─────────────────────────────────────────────────────────

@bp.route('/nytt-erbjudande', methods=['GET', 'POST'])
@store_required
def new_offer():
    categories = db.select('categories', order='name')
    sid = session['store_id']

    if not db.get_one('stores', {'id': sid, 'stripe_onboarding_done': True}):
        flash('Du måste koppla ditt bankkonto via Stripe innan du kan publicera erbjudanden.', 'warning')

    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        orig_price  = request.form.get('original_price', '').strip()
        deal_price  = request.form.get('deal_price', '').strip()
        quantity    = request.form.get('quantity', '1').strip()
        cat_id      = request.form.get('category_id')
        publish_now = 'publish' in request.form
        # Ny tidhantering
        expires_date = request.form.get('expires_date', '').strip()
        expires_time = request.form.get('expires_time', '17:00').strip()
        pickup_from  = request.form.get('pickup_from', '').strip() or None
        pickup_to    = request.form.get('pickup_to', '').strip() or None

        if not title or not deal_price or not quantity:
            flash('Titel, pris och antal är obligatoriska.', 'error')
            return render_template('store/new_offer.html', categories=categories)

        try:
            deal_price_f = float(deal_price)
            orig_price_f = float(orig_price) if orig_price else None
            qty          = int(quantity)
        except ValueError:
            flash('Ogiltigt pris eller antal.', 'error')
            return render_template('store/new_offer.html', categories=categories)

        # Bygg expires_at från datum + tid (tolkas som lokal tid Sverige)
        try:
            naive = datetime.strptime(f'{expires_date} {expires_time}', '%Y-%m-%d %H:%M')
            expires_at = naive.replace(tzinfo=timezone.utc).isoformat()
        except (ValueError, TypeError):
            expires_at = (datetime.now(timezone.utc) + timedelta(hours=3)).isoformat()

        # Bygg pickup_window-sträng för visning
        pickup_window = None
        if pickup_from and pickup_to:
            pickup_window = f'{pickup_from}–{pickup_to}'
        elif pickup_from:
            pickup_window = f'från {pickup_from}'
        elif pickup_to:
            pickup_window = f'senast {pickup_to}'

        photo_url = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename:
                ext      = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else 'jpg'
                filename = f'{sid}/{secrets.token_hex(8)}.{ext}'
                photo_url = upload_image(file.read(), filename)

        status = 'active' if publish_now else 'draft'

        offer = db.insert('offers', {
            'store_id':       sid,
            'category_id':    cat_id or None,
            'title':          title,
            'description':    description or None,
            'original_price': orig_price_f,
            'deal_price':     deal_price_f,
            'total_quantity': qty,
            'remaining_qty':  qty,
            'photo_url':      photo_url,
            'expires_at':     expires_at,
            'pickup_window':  pickup_window,
            'status':         status,
        })

        if not offer:
            flash('Något gick fel. Försök igen.', 'error')
            return render_template('store/new_offer.html', categories=categories)

        if status == 'active':
            notify_subscribers(offer)
            flash('Erbjudandet är publicerat och prenumeranter har fått notis!', 'success')
        else:
            flash('Erbjudandet sparades som utkast.', 'info')

        return redirect(url_for('store.dashboard'))

    return render_template('store/new_offer.html', categories=categories)


# ─── Publicera / avpublicera erbjudande ──────────────────────────────────────

@bp.route('/erbjudande/<offer_id>/publicera', methods=['POST'])
@store_required
def publish_offer(offer_id):
    sid   = session['store_id']
    offer = db.get_one('offers', {'id': offer_id, 'store_id': sid})
    if not offer:
        flash('Erbjudandet hittades inte.', 'error')
        return redirect(url_for('store.dashboard'))

    duration_h = int(request.form.get('duration_hours', 3))
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=duration_h)).isoformat()
    updated    = db.update('offers', {'id': offer_id}, {'status': 'active', 'expires_at': expires_at})
    if updated:
        notify_subscribers(updated)
        flash('Erbjudandet är nu publicerat!', 'success')
    return redirect(url_for('store.dashboard'))


@bp.route('/erbjudande/<offer_id>/avbryt', methods=['POST'])
@store_required
def cancel_offer(offer_id):
    sid = session['store_id']
    if not db.get_one('offers', {'id': offer_id, 'store_id': sid}):
        flash('Erbjudandet hittades inte.', 'error')
        return redirect(url_for('store.dashboard'))
    db.update('offers', {'id': offer_id}, {'status': 'cancelled'})
    flash('Erbjudandet avbröts.', 'info')
    return redirect(url_for('store.dashboard'))


# ─── Bokningar ────────────────────────────────────────────────────────────────

@bp.route('/bokningar')
@store_required
def bookings():
    sid      = session['store_id']
    all_b    = db.select('bookings', {'store_id': sid},
                         order='created_at.desc', limit=100)

    # Berika med kundnamn och erbjudandetitel
    offer_ids   = list({b['offer_id'] for b in all_b})
    customer_ids = list({b['customer_id'] for b in all_b if b.get('customer_id')})

    offers_map    = {}
    customers_map = {}
    if offer_ids:
        offers_map = {o['id']: o for o in db.select('offers', {'id': offer_ids}, 'id,title')}
    if customer_ids:
        customers_map = {c['id']: c for c in db.select('customers', {'id': customer_ids}, 'id,full_name,email,phone')}

    for b in all_b:
        b['offer']    = offers_map.get(b['offer_id'], {})
        b['customer'] = customers_map.get(b.get('customer_id'), {})

    return render_template('store/bookings.html', bookings=all_b)


# ─── QR-skanner (mobil) ───────────────────────────────────────────────────────

@bp.route('/skanna')
@store_required
def scanner():
    return render_template('store/scanner.html')


@bp.route('/skanna/verifiera/<token>', methods=['GET', 'POST'])
@store_required
def verify_qr(token):
    """Verifiera QR-kod. GET: direkt via URL (skanner). POST: returnerar JSON."""
    sid     = session['store_id']
    booking = db.get_one('bookings', {'qr_token': token})

    if not booking:
        result = {'ok': False, 'msg': '❌ QR-koden hittades inte.'}
    elif booking.get('store_id') != sid:
        result = {'ok': False, 'msg': '❌ Denna bokning tillhör en annan butik.'}
    elif booking.get('payment_status') != 'paid':
        result = {'ok': False, 'msg': '⚠️ Bokningen är inte betald.'}
    elif booking.get('qr_used'):
        used_at = (booking.get('qr_used_at') or '')[:16].replace('T', ' kl ')
        result = {'ok': False, 'msg': f'⚠️ QR-koden användes redan {used_at}.'}
    else:
        db.update('bookings', {'id': booking['id']}, {
            'qr_used':    True,
            'qr_used_at': datetime.now(timezone.utc).isoformat(),
            'status':     'picked_up',
        })
        offer    = db.get_one('offers', {'id': booking['offer_id']}, 'title')
        customer = db.get_one('customers', {'id': booking.get('customer_id')}, 'full_name,email')
        result   = {
            'ok':      True,
            'msg':     '✅ Giltig bokning — utlämna varan!',
            'title':   offer.get('title', '') if offer else '',
            'customer': (customer.get('full_name') or customer.get('email', '')) if customer else '',
            'qty':     booking.get('quantity', 1),
        }

    if request.method == 'POST':
        return jsonify(result)

    return render_template('store/scan_result.html', result=result, booking=booking)


# ─── Stripe Connect onboarding ────────────────────────────────────────────────

@bp.route('/stripe/koppla')
@store_required
def stripe_onboard():
    import stripe
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    if not stripe.api_key:
        flash('Stripe är inte konfigurerat ännu.', 'warning')
        return redirect(url_for('store.dashboard'))

    sid   = session['store_id']
    store = db.get_one('stores', {'id': sid})

    acct_id = store.get('stripe_account_id')
    if not acct_id:
        acct    = stripe.Account.create(type='express', country='SE', email=store['email'])
        acct_id = acct['id']
        db.update('stores', {'id': sid}, {'stripe_account_id': acct_id})

    base = os.environ.get('BASE_URL', 'http://localhost:5000')
    link = stripe.AccountLink.create(
        account=acct_id,
        refresh_url=f'{base}/butik/stripe/koppla',
        return_url=f'{base}/butik/stripe/klar',
        type='account_onboarding',
    )
    return redirect(link['url'])


@bp.route('/stripe/klar')
@store_required
def stripe_return():
    import stripe
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    sid   = session['store_id']
    store = db.get_one('stores', {'id': sid})
    if store.get('stripe_account_id'):
        try:
            acct = stripe.Account.retrieve(store['stripe_account_id'])
            if acct.get('details_submitted'):
                db.update('stores', {'id': sid}, {'stripe_onboarding_done': True})
                flash('Betalningsuppgifterna är kopplade! Du kan nu publicera erbjudanden.', 'success')
            else:
                flash('Stripe-kopplingen är inte klar ännu. Fyll i alla uppgifter.', 'warning')
        except Exception as e:
            flash(f'Stripe-fel: {e}', 'error')
    return redirect(url_for('store.dashboard'))


# ─── Butiksprofil ─────────────────────────────────────────────────────────────

@bp.route('/profil', methods=['GET', 'POST'])
@store_required
def profile():
    sid   = session['store_id']
    store = db.get_one('stores', {'id': sid})

    if request.method == 'POST':
        updates = {
            'description':         request.form.get('description', '').strip() or None,
            'policy_text':         request.form.get('policy_text', '').strip() or None,
            'pickup_instructions': request.form.get('pickup_instructions', '').strip() or None,
            'address':             request.form.get('address', '').strip() or None,
            'phone':               request.form.get('phone', '').strip() or None,
        }
        db.update('stores', {'id': sid}, updates)
        flash('Profilen är uppdaterad.', 'success')
        return redirect(url_for('store.dashboard'))

    return render_template('store/profile.html', store=store)
