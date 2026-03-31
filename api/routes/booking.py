"""
booking.py — Bokning, Stripe Checkout, bekräftelse, QR
Prefix: /betala
"""
import os
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from api.config import db, login_required, generate_qr_base64, send_email, fmt_price

bp = Blueprint('booking', __name__)

_FEE_PCT = float(os.environ.get('STRIPE_PLATFORM_FEE_PCT', 6)) / 100


# ─── Initiera bokning / Stripe Checkout ───────────────────────────────────────

@bp.route('/<offer_id>', methods=['GET', 'POST'])
@login_required
def checkout(offer_id):
    offer = db.get_one('offers', {'id': offer_id})
    if not offer or offer.get('status') != 'active' or offer.get('remaining_qty', 0) < 1:
        flash('Det här erbjudandet är inte längre tillgängligt.', 'error')
        return redirect(url_for('public.index'))

    store    = db.get_one('stores', {'id': offer['store_id']},
                          'id,business_name,address,city,policy_text,stripe_account_id,stripe_onboarding_done')
    category = db.get_one('categories', {'id': offer.get('category_id')}, 'name,icon')

    if request.method == 'POST':
        qty = int(request.form.get('quantity', 1))
        if qty < 1 or qty > offer.get('remaining_qty', 1):
            flash('Ogiltigt antal.', 'error')
            return redirect(url_for('booking.checkout', offer_id=offer_id))

        stripe_key = os.environ.get('STRIPE_SECRET_KEY')
        if stripe_key:
            return _stripe_checkout(offer, store, qty)
        else:
            return _test_checkout(offer, store, qty)

    return render_template('booking/checkout.html',
                           offer=offer,
                           store=store,
                           category=category)


def _stripe_checkout(offer, store, qty):
    import stripe
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

    uid     = session['user_id']
    base    = os.environ.get('BASE_URL', 'http://localhost:5000')
    amount  = int(float(offer['deal_price']) * 100)  # öre
    fee     = int(amount * qty * _FEE_PCT)

    try:
        checkout = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'sek',
                    'unit_amount': amount,
                    'product_data': {'name': offer['title'],
                                     'description': f"Hämtas hos {store['business_name']}, {store['city']}"},
                },
                'quantity': qty,
            }],
            mode='payment',
            success_url=f"{base}/betala/klar?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{base}/erbjudande/{offer['id']}",
            payment_intent_data={
                'application_fee_amount': fee,
                'transfer_data': {'destination': store.get('stripe_account_id')},
            } if store.get('stripe_onboarding_done') else {},
            metadata={
                'offer_id':    offer['id'],
                'customer_id': uid,
                'store_id':    store['id'],
                'quantity':    qty,
            },
        )
        session['pending_checkout'] = checkout['id']
        return redirect(checkout['url'])
    except Exception as e:
        flash(f'Betalningsfel: {e}', 'error')
        return redirect(url_for('booking.checkout', offer_id=offer['id']))


def _test_checkout(offer, store, qty):
    """Testläge utan Stripe — skapar bokning direkt."""
    uid        = session['user_id']
    total      = float(offer['deal_price']) * qty
    fee        = round(total * _FEE_PCT, 2)
    expires_at = offer.get('expires_at', '')

    booking = db.insert('bookings', {
        'offer_id':       offer['id'],
        'customer_id':    uid,
        'store_id':       store['id'],
        'quantity':       qty,
        'total_paid':     total,
        'platform_fee':   fee,
        'payment_status': 'paid',
        'status':         'confirmed',
        'expires_at':     expires_at,
    })
    if not booking:
        flash('Något gick fel.', 'error')
        return redirect(url_for('public.index'))

    db.update('offers', {'id': offer['id']},
              {'remaining_qty': max(0, offer['remaining_qty'] - qty)})

    _send_booking_confirmation(booking, offer, store)
    flash('⚠️ TESTLÄGE — Stripe ej konfigurerat. Bokning skapad utan betalning.', 'warning')
    return redirect(url_for('booking.confirmation', booking_id=booking['id']))


# ─── Stripe webhook ───────────────────────────────────────────────────────────

@bp.route('/webhook', methods=['POST'])
def webhook():
    import stripe
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')
    payload   = request.get_data(as_text=False)
    sig       = request.headers.get('Stripe-Signature', '')
    secret    = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

    try:
        event = stripe.Webhook.construct_event(payload, sig, secret) if secret else \
                stripe.Event.construct_from(request.json, stripe.api_key)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if event['type'] == 'checkout.session.completed':
        _handle_checkout_completed(event['data']['object'])

    return jsonify({'ok': True})


def _handle_checkout_completed(sess):
    meta    = sess.get('metadata', {})
    offer_id    = meta.get('offer_id')
    customer_id = meta.get('customer_id')
    store_id    = meta.get('store_id')
    qty     = int(meta.get('quantity', 1))

    if not offer_id:
        return

    offer  = db.get_one('offers', {'id': offer_id})
    store  = db.get_one('stores', {'id': store_id}, 'business_name,city')
    total  = (sess.get('amount_total') or 0) / 100
    fee    = round(total * _FEE_PCT, 2)
    expires_at = offer.get('expires_at', '') if offer else ''

    booking = db.insert('bookings', {
        'offer_id':               offer_id,
        'customer_id':            customer_id,
        'store_id':               store_id,
        'quantity':               qty,
        'total_paid':             total,
        'platform_fee':           fee,
        'stripe_session_id':      sess.get('id'),
        'stripe_payment_intent_id': sess.get('payment_intent'),
        'payment_status':         'paid',
        'status':                 'confirmed',
        'expires_at':             expires_at,
    })

    if booking and offer:
        db.update('offers', {'id': offer_id},
                  {'remaining_qty': max(0, offer['remaining_qty'] - qty)})
        _send_booking_confirmation(booking, offer, store)


# ─── Bekräftelsesida ──────────────────────────────────────────────────────────

@bp.route('/klar')
@login_required
def success():
    """Stripe redirectar hit efter betalning. Visar bekräftelse."""
    sess_id  = request.args.get('session_id')
    if sess_id:
        booking = db.get_one('bookings', {'stripe_session_id': sess_id})
    else:
        return redirect(url_for('public.index'))
    if not booking:
        return render_template('booking/success_pending.html')
    return redirect(url_for('booking.confirmation', booking_id=booking['id']))


@bp.route('/bekraftelse/<booking_id>')
@login_required
def confirmation(booking_id):
    booking = db.get_one('bookings', {'id': booking_id, 'customer_id': session['user_id']})
    if not booking:
        flash('Bokningen hittades inte.', 'error')
        return redirect(url_for('public.index'))

    offer    = db.get_one('offers', {'id': booking['offer_id']}, 'title,description,photo_url')
    store    = db.get_one('stores', {'id': booking['store_id']},
                          'business_name,address,city,pickup_instructions')
    qr_image = generate_qr_base64(booking['qr_token'])

    return render_template('booking/confirmation.html',
                           booking=booking,
                           offer=offer,
                           store=store,
                           qr_image=qr_image)


# ─── Kundens bokningslista ────────────────────────────────────────────────────

@bp.route('/mina-bokningar')
@login_required
def my_bookings():
    uid      = session['user_id']
    bookings = db.select('bookings', {'customer_id': uid}, order='created_at.desc', limit=50)

    offer_ids = list({b['offer_id'] for b in bookings})
    store_ids = list({b['store_id'] for b in bookings})

    offers_map = {}
    stores_map = {}
    if offer_ids:
        offers_map = {o['id']: o for o in db.select('offers', {'id': offer_ids}, 'id,title,photo_url')}
    if store_ids:
        stores_map = {s['id']: s for s in db.select('stores', {'id': store_ids}, 'id,business_name,city')}

    for b in bookings:
        b['offer'] = offers_map.get(b['offer_id'], {})
        b['store'] = stores_map.get(b['store_id'], {})

    return render_template('booking/my_bookings.html', bookings=bookings)


# ─── Hjälpfunktioner ──────────────────────────────────────────────────────────

def _send_booking_confirmation(booking, offer, store):
    customer = db.get_one('customers', {'id': booking.get('customer_id')}, 'email,full_name')
    if not customer or not customer.get('email'):
        return

    base    = os.environ.get('BASE_URL', 'http://localhost:5000')
    name    = customer.get('full_name') or 'där'
    expires = (booking.get('expires_at') or '')[:16].replace('T', ' kl ')
    price   = fmt_price(booking.get('total_paid'))
    qr_url  = f"{base}/betala/bekraftelse/{booking['id']}"

    html = f"""<div style="font-family:sans-serif;max-width:520px;margin:0 auto;background:#0f0e0c;color:#f7f5f0;border-radius:12px;overflow:hidden">
  <div style="background:#1a9a6c;padding:14px 24px;font-size:11px;letter-spacing:2px;text-transform:uppercase;font-weight:600">
    ✅ FlashDeal &middot; Bokningsbekräftelse
  </div>
  <div style="padding:28px">
    <h2 style="font-size:20px;margin:0 0 8px;color:#f7f5f0">Hej {name}!</h2>
    <p style="color:#b0a898;font-size:14px;margin:0 0 20px">Din bokning är bekräftad och betalning mottagen.</p>
    <div style="background:#1a1814;border:1px solid #2a2824;border-radius:10px;padding:18px;margin-bottom:20px">
      <div style="font-size:18px;font-weight:700;color:#f7f5f0;margin-bottom:4px">{offer.get('title','')}</div>
      <div style="color:#7a7570;font-size:13px">{store.get('business_name','') if store else ''} &middot; {store.get('city','') if store else ''}</div>
      <div style="margin-top:12px;font-size:24px;font-weight:700;color:#d4541a">{price} kr</div>
    </div>
    <div style="background:#0d3020;border:1px solid #1a5030;border-radius:8px;padding:12px 16px;margin-bottom:20px;font-size:13px;color:#4ade80">
      ⏱ Hämta senast: {expires}
    </div>
    <a href="{qr_url}" style="display:block;background:#d4541a;color:#fff;text-align:center;padding:14px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px">
      Visa din QR-kod &rarr;
    </a>
  </div>
</div>"""
    send_email(customer['email'], f'✅ Bokningsbekräftelse — {offer.get("title","")}', html)
