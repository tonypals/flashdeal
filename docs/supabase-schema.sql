-- ============================================================
-- FlashDeal — Supabase databasschema
-- Kör detta i Supabase Dashboard → SQL Editor
-- ============================================================

-- Kategorier
CREATE TABLE categories (
    id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name  TEXT UNIQUE NOT NULL,
    icon  TEXT DEFAULT '🏷️',
    slug  TEXT UNIQUE NOT NULL
);

-- Kunder
CREATE TABLE customers (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email         TEXT UNIQUE NOT NULL,
    phone         TEXT,
    password_hash TEXT NOT NULL,
    full_name     TEXT,
    city          TEXT DEFAULT 'Göteborg',
    notify_email  BOOLEAN DEFAULT TRUE,
    notify_sms    BOOLEAN DEFAULT FALSE,
    created_at    TIMESTAMPTZ DEFAULT now()
);

-- Kunders kategori-prenumerationer
CREATE TABLE customer_subscriptions (
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (customer_id, category_id)
);

-- Butiker
CREATE TABLE stores (
    id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email                  TEXT UNIQUE NOT NULL,
    password_hash          TEXT NOT NULL,
    business_name          TEXT NOT NULL,
    slug                   TEXT UNIQUE NOT NULL,
    contact_person         TEXT,
    phone                  TEXT,
    address                TEXT,
    city                   TEXT DEFAULT 'Göteborg',
    description            TEXT,
    policy_text            TEXT DEFAULT 'Full betalning krävs vid bokning. Ej hämtad vara återbetalas ej.',
    pickup_instructions    TEXT,
    logo_url               TEXT,
    -- Stripe Connect
    stripe_account_id      TEXT,
    stripe_onboarding_done BOOLEAN DEFAULT FALSE,
    -- Godkännande
    status                 TEXT DEFAULT 'pending'
        CHECK (status IN ('pending', 'approved', 'rejected', 'suspended')),
    approved_at            TIMESTAMPTZ,
    rejection_note         TEXT,
    created_at             TIMESTAMPTZ DEFAULT now()
);

-- Erbjudanden
CREATE TABLE offers (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    store_id         UUID REFERENCES stores(id) ON DELETE CASCADE,
    category_id      UUID REFERENCES categories(id),
    title            TEXT NOT NULL,
    description      TEXT,
    original_price   NUMERIC(10,2),
    deal_price       NUMERIC(10,2) NOT NULL,
    total_quantity   INTEGER NOT NULL,
    remaining_qty    INTEGER NOT NULL,
    photo_url        TEXT,
    expires_at       TIMESTAMPTZ NOT NULL,
    status           TEXT DEFAULT 'draft'
        CHECK (status IN ('draft', 'active', 'expired', 'cancelled')),
    notifications_sent BOOLEAN DEFAULT FALSE,
    created_at       TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_offers_status ON offers(status);
CREATE INDEX idx_offers_expires ON offers(expires_at);
CREATE INDEX idx_offers_category ON offers(category_id);

-- Bokningar
CREATE TABLE bookings (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    offer_id                 UUID REFERENCES offers(id),
    customer_id              UUID REFERENCES customers(id),
    store_id                 UUID REFERENCES stores(id),
    quantity                 INTEGER DEFAULT 1,
    total_paid               NUMERIC(10,2),
    platform_fee             NUMERIC(10,2),
    -- Stripe
    stripe_payment_intent_id TEXT UNIQUE,
    stripe_session_id        TEXT,
    payment_status           TEXT DEFAULT 'pending'
        CHECK (payment_status IN ('pending', 'paid', 'refunded', 'failed')),
    -- QR
    qr_token                 TEXT UNIQUE NOT NULL DEFAULT encode(gen_random_bytes(24), 'hex'),
    qr_used                  BOOLEAN DEFAULT FALSE,
    qr_used_at               TIMESTAMPTZ,
    -- Status
    status                   TEXT DEFAULT 'confirmed'
        CHECK (status IN ('confirmed', 'picked_up', 'cancelled')),
    expires_at               TIMESTAMPTZ NOT NULL,
    created_at               TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_bookings_qr ON bookings(qr_token);
CREATE INDEX idx_bookings_customer ON bookings(customer_id);
CREATE INDEX idx_bookings_store ON bookings(store_id);

-- Notifieringslogg (throttling: max 1/kategori/kanal per 10 min)
CREATE TABLE notification_log (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id),
    channel     TEXT CHECK (channel IN ('email', 'sms')),
    sent_at     TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_notif_throttle
    ON notification_log(customer_id, category_id, channel, sent_at DESC);

-- ── Startdata: kategorier ──────────────────────────────────────────────────
INSERT INTO categories (name, icon, slug) VALUES
    ('Elektronik',       '📱', 'elektronik'),
    ('Kläder & skor',    '👗', 'klader-skor'),
    ('Mat & dryck',      '🍞', 'mat-dryck'),
    ('Hem & inredning',  '🛋️', 'hem-inredning'),
    ('Sport & fritid',   '🏃', 'sport-fritid'),
    ('Skönhet & hälsa',  '💄', 'skonhet-halsa'),
    ('Cykel',            '🚲', 'cykel'),
    ('Böcker & media',   '📚', 'bocker-media'),
    ('Leksaker & hobby', '🎮', 'leksaker-hobby'),
    ('Bygg & verktyg',   '🔧', 'bygg-verktyg');
