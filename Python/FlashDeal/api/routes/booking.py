"""
booking.py — Bokning, Stripe Checkout, bekräftelse, QR
Prefix: /betala
"""
import os, secrets, html as _html
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
        elif os.environ.get('FLASK_ENV') == 'production':
            flash('Betalning är inte konfigurerat. Kontakta support.', 'error')
            return redirect(url_for('public.index'))
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
        'qr_token':       secrets.token_urlsafe(32),
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

    if not secret:
        return jsonify({'error': 'Webhook secret saknas'}), 400
    try:
        event = stripe.Webhook.construct_event(payload, sig, secret)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if event['type'] == 'checkout.session.completed':
        _handle_checkout_completed(event['data']['object'])

    return jsonify({'ok': True})


def _handle_checkout_completed(sess):
    meta        = sess.get('metadata', {})
    offer_id    = meta.get('offer_id')
    customer_id = meta.get('customer_id')
    store_id    = meta.get('store_id')
    qty         = int(meta.get('quantity', 1))

    if not offer_id:
        return

    # Atomisk minskning av remaining_qty via RPC.
    # Returnerar den uppdaterade offer-raden, eller None om qty inte räckte.
    offer = db.rpc('fd_decrement_offer_qty', {'p_offer_id': offer_id, 'p_qty': qty})

    if not offer:
        # Varan är slut — pengarna har redan tagits. Återbetala direkt.
        pi = sess.get('payment_intent')
        if pi:
            try:
                import stripe
                stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')
                stripe.Refund.create(payment_intent=pi)
                print(f'[Webhook] Återbetalning skapad för {pi} — offer {offer_id} slut')
            except Exception as e:
                print(f'[Webhook] Återbetalningsfel: {e}')
        return

    store      = db.get_one('stores', {'id': store_id}, 'business_name,city')
    total      = (sess.get('amount_total') or 0) / 100
    fee        = round(total * _FEE_PCT, 2)
    expires_at = offer.get('expires_at', '')

    booking = db.insert('bookings', {
        'offer_id':                 offer_id,
        'customer_id':              customer_id,
        'store_id':                 store_id,
        'quantity':                 qty,
        'total_paid':               total,
        'platform_fee':             fee,
        'stripe_session_id':        sess.get('id'),
        'stripe_payment_intent_id': sess.get('payment_intent'),
        'payment_status':           'paid',
        'status':                   'confirmed',
        'expires_at':               expires_at,
        'qr_token':                 secrets.token_urlsafe(32),
    })

    if booking:
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


# ─── Avboka ──────────────────────────────────────────────────────────────────

@bp.route('/avboka/<booking_id>', methods=['POST'])
@login_required
def cancel(booking_id):
    uid     = session['user_id']
    booking = db.get_one('bookings', {'id': booking_id, 'customer_id': uid})

    if not booking or booking.get('status') != 'confirmed' or booking.get('qr_used'):
        flash('Bokningen kan inte avbokas.', 'error')
        return redirect(url_for('booking.my_bookings'))

    now        = datetime.now(timezone.utc)
    expires_at = booking.get('expires_at', '')
    try:
        exp = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
    except Exception:
        exp = now

    # Pickup-fönstret har startat = ingen återbetalning
    if now >= exp:
        db.update('bookings', {'id': booking_id}, {'status': 'cancelled'})
        _activate_next_in_queue(booking['offer_id'])
        flash('Bokningen avbokades. Ingen återbetalning — hämtningstiden har passerat.', 'info')
        return redirect(url_for('booking.my_bookings'))

    # Avbokar i tid — återbetala via Stripe om möjligt
    refunded = False
    stripe_key = os.environ.get('STRIPE_SECRET_KEY')
    pi = booking.get('stripe_payment_intent_id')
    if stripe_key and pi:
        try:
            import stripe
            stripe.api_key = stripe_key
            stripe.Refund.create(payment_intent=pi)
            refunded = True
        except Exception as e:
            print(f'[Stripe refund error] {e}')

    db.update('bookings', {'id': booking_id}, {
        'status':         'cancelled',
        'payment_status': 'refunded' if refunded else 'cancelled',
    })
    # Återställ remaining_qty
    offer = db.get_one('offers', {'id': booking['offer_id']}, 'remaining_qty')
    if offer:
        db.update('offers', {'id': booking['offer_id']},
                  {'remaining_qty': offer['remaining_qty'] + booking.get('quantity', 1)})

    _activate_next_in_queue(booking['offer_id'])

    if refunded:
        flash('Bokningen avbokades och pengarna återbetalas inom 3–5 bankdagar.', 'success')
    else:
        flash('Bokningen avbokades.', 'info')
    return redirect(url_for('booking.my_bookings'))


# ─── Kö ───────────────────────────────────────────────────────────────────────

@bp.route('/ko/<offer_id>', methods=['POST'])
@login_required
def join_queue(offer_id):
    uid   = session['user_id']
    offer = db.get_one('offers', {'id': offer_id})
    if not offer:
        flash('Erbjudandet hittades inte.', 'error')
        return redirect(url_for('public.index'))

    # Redan i kön?
    existing = db.get_one('queues', {'offer_id': offer_id, 'customer_id': uid, 'status': 'waiting'})
    if existing:
        flash('Du står redan i kön.', 'info')
        return redirect(url_for('public.offer_detail', offer_id=offer_id))

    db.insert('queues', {
        'offer_id':    offer_id,
        'customer_id': uid,
        'status':      'waiting',
    })
    flash('Du är nu i kön! Vi meddelar dig via mail/SMS om en plats öppnas.', 'success')
    return redirect(url_for('public.offer_detail', offer_id=offer_id))


def _activate_next_in_queue(offer_id):
    """Hämtar nästa i kön, skickar notis och ger dem 2 timmar att boka."""
    next_q = db.select('queues', {'offer_id': offer_id, 'status': 'waiting'},
                       order='created_at.asc', limit=1)
    if not next_q:
        return
    q        = next_q[0]
    customer = db.get_one('customers', {'id': q['customer_id']}, 'email,full_name,phone')
    offer    = db.get_one('offers', {'id': offer_id}, 'title,deal_price')
    if not customer or not offer:
        return

    db.update('queues', {'id': q['id']}, {
        'status':      'notified',
        'notified_at': datetime.now(timezone.utc).isoformat(),
    })

    base    = os.environ.get('BASE_URL', 'http://localhost:5000')
    name    = _html.escape(customer.get('full_name') or 'där')
    price   = fmt_price(offer.get('deal_price'))
    url     = f"{base}/erbjudande/{offer_id}"
    o_title = _html.escape(offer.get('title', '') if offer else '')

    body = f"""<div style="font-family:sans-serif;max-width:520px;margin:0 auto;background:#0f0e0c;color:#f7f5f0;border-radius:12px;overflow:hidden">
  <div style="background:#d4541a;padding:14px 24px;font-size:11px;letter-spacing:2px;text-transform:uppercase;font-weight:600">
    ⚡ FlashDeal &middot; Din plats i kön är nu ledig!
  </div>
  <div style="padding:28px">
    <h2 style="font-size:20px;margin:0 0 10px">Hej {name}!</h2>
    <p style="color:#b0a898;font-size:14px;margin:0 0 20px">
      En plats har öppnats upp för <strong style="color:#f7f5f0">{o_title}</strong>.
      Du har <strong style="color:#febc2e">2 timmar</strong> på dig att boka.
    </p>
    <a href="{url}" style="display:block;background:#d4541a;color:#fff;text-align:center;padding:14px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px">
      Boka nu — {price} kr &rarr;
    </a>
    <p style="font-size:12px;color:#5a5650;text-align:center;margin-top:14px">
      Erbjudandet kan gå till nästa i kön om du inte bokar inom 2 timmar.
    </p>
  </div>
</div>"""
    send_email(customer['email'], f'⚡ Din tur! {offer.get("title", "") if offer else ""} väntar på dig', body)

    from api.config import send_sms
    if customer.get('phone'):
        send_sms(customer['phone'],
                 f"⚡ FlashDeal: Din plats är ledig! {offer['title']} – {price} kr. "
                 f"Boka inom 2h: {url}")


# ─── Hjälpfunktioner ──────────────────────────────────────────────────────────

def _send_booking_confirmation(booking, offer, store):
    customer = db.get_one('customers', {'id': booking.get('customer_id')}, 'email,full_name')
    if not customer or not customer.get('email'):
        return

    base    = os.environ.get('BASE_URL', 'http://localhost:5000')
    name    = _html.escape(customer.get('full_name') or 'där')
    expires = (booking.get('expires_at') or '')[:16].replace('T', ' kl ')
    price   = fmt_price(booking.get('total_paid'))
    qr_url  = f"{base}/betala/bekraftelse/{booking['id']}"
    o_title = _html.escape(offer.get('title', '') if offer else '')
    s_name  = _html.escape(store.get('business_name', '') if store else '')
    s_city  = _html.escape(store.get('city', '') if store else '')

    body = f"""<div style="font-family:sans-serif;max-width:520px;margin:0 auto;background:#0f0e0c;color:#f7f5f0;border-radius:12px;overflow:hidden">
  <div style="background:#1a9a6c;padding:14px 24px;font-size:11px;letter-spacing:2px;text-transform:uppercase;font-weight:600">
    ✅ FlashDeal &middot; Bokningsbekräftelse
  </div>
  <div style="padding:28px">
    <h2 style="font-size:20px;margin:0 0 8px;color:#f7f5f0">Hej {name}!</h2>
    <p style="color:#b0a898;font-size:14px;margin:0 0 20px">Din bokning är bekräftad och betalning mottagen.</p>
    <div style="background:#1a1814;border:1px solid #2a2824;border-radius:10px;padding:18px;margin-bottom:20px">
      <div style="font-size:18px;font-weight:700;color:#f7f5f0;margin-bottom:4px">{o_title}</div>
      <div style="color:#7a7570;font-size:13px">{s_name} &middot; {s_city}</div>
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
    send_email(customer['email'], f'✅ Bokningsbekräftelse — {offer.get("title", "") if offer else ""}', body)
