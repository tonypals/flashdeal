"""
public.py — Kundvyer: startsida, erbjudanden, butikssida, hur-det-fungerar
"""
from flask import Blueprint, render_template, request, jsonify, session
from api.config import db

bp = Blueprint('public', __name__)


@bp.route('/')
def index():
    categories = db.select('categories', order='name')
    cat_filter = request.args.get('kategori')

    filters = {'status': 'active'}
    if cat_filter:
        cat = db.get_one('categories', {'slug': cat_filter})
        if cat:
            filters['category_id'] = cat['id']

    offers = db.select('offers', filters,
                       columns='*',
                       order='expires_at.asc',
                       limit=50)

    # Berika med butiksnamn
    store_ids = list({o['store_id'] for o in offers})
    stores_map = {}
    if store_ids:
        stores = db.select('stores', {'id': store_ids}, 'id,business_name,city,address,logo_url')
        stores_map = {s['id']: s for s in stores}
    for o in offers:
        o['store'] = stores_map.get(o['store_id'], {})

    cat_names = {c['slug']: c for c in categories}

    return render_template('index.html',
                           offers=offers,
                           categories=categories,
                           active_category=cat_filter,
                           cat_names=cat_names)


@bp.route('/erbjudande/<offer_id>')
def offer_detail(offer_id):
    offer = db.get_one('offers', {'id': offer_id})
    if not offer or offer.get('status') not in ('active', 'draft'):
        return render_template('404.html'), 404

    store    = db.get_one('stores', {'id': offer['store_id']},
                          'id,business_name,city,address,description,policy_text,pickup_instructions,logo_url')
    category = db.get_one('categories', {'id': offer.get('category_id')}, 'name,icon')

    # Räkna befintliga bokningar
    bookings = db.select('bookings', {'offer_id': offer_id, 'payment_status': 'paid'})
    booked_qty = sum(b.get('quantity', 1) for b in bookings)

    return render_template('offer_detail.html',
                           offer=offer,
                           store=store,
                           category=category,
                           booked_qty=booked_qty)


@bp.route('/butiker')
def stores_list():
    city = request.args.get('stad', '')
    cat  = request.args.get('kategori', '')

    filters = {'status': 'approved'}
    if city:
        filters['city'] = city
    if cat:
        c = db.get_one('categories', {'slug': cat})
        if c:
            filters['category_id'] = c['id']

    stores     = db.select('stores', filters, 'id,business_name,slug,city,description,logo_url,category_id')
    categories = db.select('categories', order='name')
    return render_template('stores_list.html', stores=stores, categories=categories,
                           active_city=city, active_cat=cat)


@bp.route('/hur-det-fungerar')
def how_it_works():
    return render_template('how_it_works.html')


@bp.route('/for-butiker')
def for_stores():
    return render_template('for_stores.html')


@bp.route('/api/erbjudanden')
def api_offers():
    """JSON-endpoint för erbjudanden (används av eventuell framtida app)."""
    cat_slug = request.args.get('kategori')
    filters  = {'status': 'active'}
    if cat_slug:
        cat = db.get_one('categories', {'slug': cat_slug})
        if cat:
            filters['category_id'] = cat['id']
    offers = db.select('offers', filters, order='expires_at.asc', limit=50)
    return jsonify(offers)
