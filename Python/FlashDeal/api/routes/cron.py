"""
cron.py — Schemalagda jobb (körs av Vercel Cron varje timme)
Prefix: /intern
"""
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify
from api.config import db, send_email, send_sms, fmt_price
import os

bp = Blueprint('cron', __name__)


@bp.route('/cron/cleanup')
def cleanup():
    # Verifiera att anropet kommer från Vercel Cron — inte en slumpmässig besökare
    if not request.headers.get('x-vercel-cron'):
        return jsonify({'error': 'Ej tillåtet'}), 403

    now = datetime.now(timezone.utc)
    results = {'expired_offers': 0, 'expired_queues': 0, 'queue_notified': 0}

    # ── Jobb 1: Stäng utgångna erbjudanden ───────────────────────────────────
    expired_offers = db.select('offers', {
        'status':     'active',
        'expires_at': {'lt': now.isoformat()},
    }, columns='id')

    for o in expired_offers:
        db.update('offers', {'id': o['id']}, {'status': 'expired'})
        results['expired_offers'] += 1

    # ── Jobb 2: Expire:a kö-platser där 2h gått sedan notis skickades ────────
    cutoff = (now - timedelta(hours=2)).isoformat()
    stale_queues = db.select('queues', {
        'status':      'notified',
        'notified_at': {'lt': cutoff},
    }, columns='id,offer_id')

    for q in stale_queues:
        db.update('queues', {'id': q['id']}, {'status': 'expired'})
        results['expired_queues'] += 1
        # Aktivera nästa i kön för samma erbjudande
        _activate_next_in_queue(q['offer_id'])
        results['queue_notified'] += 1

    print(f'[Cron] {now.isoformat()} — {results}')
    return jsonify({'ok': True, 'results': results})


def _activate_next_in_queue(offer_id):
    next_q = db.select('queues', {'offer_id': offer_id, 'status': 'waiting'},
                       order='created_at.asc', limit=1)
    if not next_q:
        return
    q        = next_q[0]
    customer = db.get_one('customers', {'id': q['customer_id']}, 'email,full_name,phone')
    offer    = db.get_one('offers', {'id': offer_id}, 'title,deal_price')
    if not customer or not offer:
        return

    import html as _html
    db.update('queues', {'id': q['id']}, {
        'status':      'notified',
        'notified_at': datetime.now(timezone.utc).isoformat(),
    })

    base    = os.environ.get('BASE_URL', 'http://localhost:5000')
    name    = _html.escape(customer.get('full_name') or 'där')
    price   = fmt_price(offer.get('deal_price'))
    url     = f"{base}/erbjudande/{offer_id}"
    o_title = _html.escape(offer.get('title', ''))

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
    send_email(customer['email'], f'⚡ Din tur! {offer.get("title", "")} väntar på dig', body)

    if customer.get('phone'):
        send_sms(customer['phone'],
                 f"⚡ FlashDeal: Din plats är ledig! {offer.get('title','')} – {price} kr. "
                 f"Boka inom 2h: {url}")
