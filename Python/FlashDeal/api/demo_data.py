"""
demo_data.py — Hårdkodad testdata för lokal utveckling utan Supabase.
Returneras automatiskt från SupabaseREST när SUPABASE_URL är tom.

Inloggning som demo-butik/kund fungerar inte i demo-läge — sessionen
sätts direkt via admin-panelen eller via /butik/logga-in med riktiga uppgifter.
"""
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash

_PW = generate_password_hash('EjAnvändbart!Demo#2026')

def _future(hours):
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()

CATEGORIES = [
    {'id': 'cat-01', 'name': 'Elektronik',          'icon': '📱', 'slug': 'elektronik'},
    {'id': 'cat-02', 'name': 'Kläder & mode',        'icon': '👗', 'slug': 'klader-mode'},
    {'id': 'cat-03', 'name': 'Mat & dryck',           'icon': '🍞', 'slug': 'mat-dryck'},
    {'id': 'cat-04', 'name': 'Hem & inredning',       'icon': '🛋️', 'slug': 'hem-inredning'},
    {'id': 'cat-05', 'name': 'Sport & fritid',        'icon': '🏃', 'slug': 'sport-fritid'},
    {'id': 'cat-06', 'name': 'Skönhet & hälsa',       'icon': '💄', 'slug': 'skonhet-halsa'},
    {'id': 'cat-07', 'name': 'Cykel & outdoor',       'icon': '🚲', 'slug': 'cykel'},
    {'id': 'cat-08', 'name': 'Böcker & media',        'icon': '📚', 'slug': 'bocker-media'},
    {'id': 'cat-09', 'name': 'Leksaker & hobby',      'icon': '🎮', 'slug': 'leksaker-hobby'},
    {'id': 'cat-10', 'name': 'Bygg & verktyg',        'icon': '🔧', 'slug': 'bygg-verktyg'},
    {'id': 'cat-11', 'name': 'Optik & glasögon',      'icon': '👓', 'slug': 'optik'},
    {'id': 'cat-12', 'name': 'Smycken & klockor',     'icon': '⌚', 'slug': 'smycken'},
    {'id': 'cat-13', 'name': 'Djur & tillbehör',      'icon': '🐾', 'slug': 'djur'},
    {'id': 'cat-14', 'name': 'Musik & instrument',    'icon': '🎸', 'slug': 'musik'},
    {'id': 'cat-15', 'name': 'Trädgård & utemiljö',   'icon': '🌿', 'slug': 'tradgard'},
    {'id': 'cat-16', 'name': 'Hårvård & frisör',      'icon': '✂️', 'slug': 'harvard'},
    {'id': 'cat-17', 'name': 'Spa & massage',          'icon': '🧖', 'slug': 'spa'},
    {'id': 'cat-18', 'name': 'Café & bageri',          'icon': '☕', 'slug': 'cafe-bageri'},
    {'id': 'cat-19', 'name': 'Gym & träning',          'icon': '🏋️', 'slug': 'gym'},
    {'id': 'cat-20', 'name': 'Florist & blommor',      'icon': '🌸', 'slug': 'florist'},
]

# ── 10 butiker, 2 och 2 per kategoripar, i 10 olika städer ────────────────────
#
# Par 1 — Hårvård & Skönhet (cat-16 + cat-06): Stockholm, Malmö
# Par 2 — Café & Bageri (cat-18 + cat-03):     Uppsala, Helsingborg
# Par 3 — Gym & Sport (cat-19 + cat-05):       Norrköping, Lund
# Par 4 — Djur & Trädgård (cat-13 + cat-15):   Umeå, Örebro
# Par 5 — Vintage & Mode (cat-02 + cat-04):    Linköping, Gävle

STORES = [
    # ── Par 1: Hårvård & Skönhet ─────────────────────────────────────────────
    {
        'id': 'store-01',
        'email': 'info@klippaklapp.se',
        'password_hash': _PW,
        'business_name': 'Klippa Klapp Sax',
        'slug': 'klippa-klapp-sax',
        'contact_person': 'Rodrigo Persson',
        'phone': '08-123456',
        'address': 'Drottninggatan 88, Stockholm',
        'city': 'Stockholm',
        'description': 'Stockholms mest överskattade frisörsalong — men med riktigt bra priser på osålda tider. Vi klipper, vi färgar, vi lovar att lyssna på dig (ungefär).',
        'policy_text': 'Betalning vid bokning. Hämta (infinn dig) inom tidsfönstret. Utebliven kund = ingen återbetalning.',
        'pickup_instructions': 'Gå in genom den blå dörren. Om Rodrigo spelar gitarr — avbryt honom, det är OK.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-16',
        'created_at': '2026-01-10T10:00:00+00:00',
    },
    {
        'id': 'store-02',
        'email': 'hej@permanentwave.se',
        'password_hash': _PW,
        'business_name': 'Permanent Wave & Spa Malmö',
        'slug': 'permanent-wave-spa-malmo',
        'contact_person': 'Birgitta Håkansson',
        'phone': '040-654321',
        'address': 'Södergatan 14, Malmö',
        'city': 'Malmö',
        'description': 'Klassisk salong med modern touch. Vi gör permanent (ja, vi menar det), ansiktsbehandlingar och existentiella kriser till reducerat pris.',
        'policy_text': 'Fullbetalning vid bokning. Vill du avboka? Ring senast 2 timmar innan.',
        'pickup_instructions': 'Fråga efter Birgitta. Ignorera doften — det är permlösning, inte fara.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-16',
        'created_at': '2026-01-18T11:00:00+00:00',
    },

    # ── Par 2: Café & Bageri ──────────────────────────────────────────────────
    {
        'id': 'store-03',
        'email': 'kaffe@gurkanochgubben.se',
        'password_hash': _PW,
        'business_name': 'Gurkan & Gubben Café',
        'slug': 'gurkan-gubben-cafe',
        'contact_person': 'Gurkan Yilmaz',
        'phone': '018-998877',
        'address': 'Fyristorg 3, Uppsala',
        'city': 'Uppsala',
        'description': 'Brunch-café med turkisk-svensk fusion. Gurkan bakar, gubben (hans far) sitter i hörnet och kritiserar. Osålda bakverk säljs via FlashDeal — oftast bättre än det som säljs normalt.',
        'policy_text': 'Hämta senast kl 17. Betalning vid bokning. Vi ger dig alltid lite extra.',
        'pickup_instructions': 'Säg att du hämtar en FlashDeal-beställning. Gurkan ler. Det är ovanligt. Njut av det.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-18',
        'created_at': '2026-01-25T08:00:00+00:00',
    },
    {
        'id': 'store-04',
        'email': 'lasse@bergetsbageri.se',
        'password_hash': _PW,
        'business_name': 'Lasse på Bergets Bageri',
        'slug': 'lasse-bergets-bageri',
        'contact_person': 'Lars-Göran Bergström',
        'phone': '042-112233',
        'address': 'Stortorget 7, Helsingborg',
        'city': 'Helsingborg',
        'description': 'Tredje generationens surdegsbagare i Helsingborg. Lasse börjar baka kl 03 och har lite för mycket kvar vid 16-tiden. Det är din vinst.',
        'policy_text': 'Hämta senast kl 18. Allt bröd är bakat samma dag. Betalning vid bokning.',
        'pickup_instructions': 'Knacka på bakdörren om skylten säger stängt — Lasse är där. Han är alltid där.',
        'status': 'approved',
        'stripe_onboarding_done': False,
        'category_id': 'cat-18',
        'created_at': '2026-02-01T07:00:00+00:00',
    },

    # ── Par 3: Gym & Sport ────────────────────────────────────────────────────
    {
        'id': 'store-05',
        'email': 'info@gymmetsomdömer.se',
        'password_hash': _PW,
        'business_name': 'Gymmet som inte dömer',
        'slug': 'gymmet-som-inte-domer',
        'contact_person': 'Pontus Stark',
        'phone': '011-334455',
        'address': 'Industrigatan 22, Norrköping',
        'city': 'Norrköping',
        'description': 'Vi dömer verkligen inte. Inte ens om du köper ett 10-kortskort och bara använder ett. Vi säljer oanvända kort och utgångna träningspaket via FlashDeal.',
        'policy_text': 'Köpta träningskort är personliga och ej återköpbara. Giltighet framgår av erbjudandet.',
        'pickup_instructions': 'Visa QR-koden i receptionen. Pontus scannar och ger dig ett högt fem. Oavsett om du vill.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-19',
        'created_at': '2026-02-05T09:00:00+00:00',
    },
    {
        'id': 'store-06',
        'email': 'namaste@yogaipyjamas.se',
        'password_hash': _PW,
        'business_name': 'Yoga i Pyjamas Lund',
        'slug': 'yoga-i-pyjamas-lund',
        'contact_person': 'Frida Stillsam',
        'phone': '046-556677',
        'address': 'Klostergatan 9, Lund',
        'city': 'Lund',
        'description': 'Lunds mjukaste yogastudio. Vi kräver inte leggings — pyjamas välkomnas, joggers accepteras, kostym är OK om du är den typen. Osålda klasser säljs billigt via FlashDeal.',
        'policy_text': 'Bokad klass gäller specifikt datum och tid. Ej hämtad = ej återbetald. Stressen stannar utanför dörren.',
        'pickup_instructions': 'Dörren är alltid öppen (bildligt och bokstavligt). Meddela Frida på SMS om du är sen.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-19',
        'created_at': '2026-02-12T10:00:00+00:00',
    },

    # ── Par 4: Djur & Trädgård ────────────────────────────────────────────────
    {
        'id': 'store-07',
        'email': 'hej@mjauvoff.se',
        'password_hash': _PW,
        'business_name': 'Mjau, Voff & Fikus AB',
        'slug': 'mjau-voff-fikus',
        'contact_person': 'Annika Djurberg',
        'phone': '090-223344',
        'address': 'Rådhusesplanaden 12, Umeå',
        'city': 'Umeå',
        'description': 'Djuraffär och plantbutik i ett. För oss är en katt och en fikus likvärdiga sällskapsdjur. Vi säljer utgångna eller skadade förpackningar av djurmat och överskotts-krukor via FlashDeal.',
        'policy_text': 'Alla produkter är kontrollerade och säkra. Hämta inom 24 timmar.',
        'pickup_instructions': 'Hitta Annika bakom terrarierna. Ignorera papegojans kommentarer.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-13',
        'created_at': '2026-02-18T11:00:00+00:00',
    },
    {
        'id': 'store-08',
        'email': 'blommor@botaniskabrak.se',
        'password_hash': _PW,
        'business_name': 'Botaniska Bråkmakeriet',
        'slug': 'botaniska-brakmakeriet',
        'contact_person': 'Stellan Grönberg',
        'phone': '019-445566',
        'address': 'Storgatan 44, Örebro',
        'city': 'Örebro',
        'description': 'Örebros mest kaotiska blomsterhandlare. Stellan har alltid för mycket och vet aldrig riktigt vad han har. Det gör varje FlashDeal-köp till en liten överraskning.',
        'policy_text': 'Växter är levande — hämta snabbt. Betalning vid bokning. Stellan tar inget ansvar för känslosamma reaktioner vid blomöppning.',
        'pickup_instructions': 'Ring på om dörren är stängd. Eller kliv bara in, det är OK också.',
        'status': 'approved',
        'stripe_onboarding_done': False,
        'category_id': 'cat-20',
        'created_at': '2026-02-25T09:30:00+00:00',
    },

    # ── Par 5: Vintage & Mode ─────────────────────────────────────────────────
    {
        'id': 'store-09',
        'email': 'info@trasigaknaby.se',
        'password_hash': _PW,
        'business_name': 'Trasiga Knäbyxor Vintage',
        'slug': 'trasiga-knabyxor-vintage',
        'contact_person': 'Maja Hedlund',
        'phone': '013-667788',
        'address': 'Ågatan 18, Linköping',
        'city': 'Linköping',
        'description': 'Vintage-butik med ett hjärta av guld och ett lager av 90-talskläder. Hålen i byxorna är avsiktliga, prislapparna är inte det. Överlager och säsongsslutsplagg säljs via FlashDeal.',
        'policy_text': 'Alla plagg är kontrollerade. Storlekar kan variera — vintage är vintage. Ej återköpt.',
        'pickup_instructions': 'Maja finns alltid. Kaffe bjuds alltid. Det är en regel.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-02',
        'created_at': '2026-03-01T12:00:00+00:00',
    },
    {
        'id': 'store-10',
        'email': 'halvan@modecentrum.se',
        'password_hash': _PW,
        'business_name': 'Modecentrum Halvpris AB',
        'slug': 'modecentrum-halvpris',
        'contact_person': 'Kenneth Kjell',
        'phone': '026-889900',
        'address': 'Drottninggatan 31, Gävle',
        'city': 'Gävle',
        'description': 'Kenneth sålde bilar i 20 år och vet fortfarande ingenting om mode. Men han köper in bra och säljer billigt, och det är det enda som räknas. Alltid 40–70% rabatt.',
        'policy_text': 'Betalning vid bokning. Allt säljs i befintligt skick. Kenneth lovar ingenting om passform.',
        'pickup_instructions': 'Kenneth är alltid på plats. Han vill prata. Det är en del av upplevelsen.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-02',
        'created_at': '2026-03-05T10:00:00+00:00',
    },

    # ── Elektronik ────────────────────────────────────────────────────────────
    {
        'id': 'store-11',
        'email': 'info@pixelpaniken.se',
        'password_hash': _PW,
        'business_name': 'Pixelpaniken AB',
        'slug': 'pixelpaniken',
        'contact_person': 'Christer Bygg',
        'phone': '031-101010',
        'address': 'Södra Vägen 2, Göteborg',
        'city': 'Göteborg',
        'description': 'Elektronikbutik med panik i blicken och rabatter i lagret. Returvaror, utställningsex och förra årets modeller. Christer köper in för mycket — det är din fördel.',
        'policy_text': 'Betalning vid bokning. Hämta inom 3 timmar. Allt är kontrollerat.',
        'pickup_instructions': 'Fråga efter Christer vid teknikdisken.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-01',
        'created_at': '2026-03-06T09:00:00+00:00',
    },

    # ── Hem & inredning ───────────────────────────────────────────────────────
    {
        'id': 'store-12',
        'email': 'hej@skruvochsoffa.se',
        'password_hash': _PW,
        'business_name': 'Skruv & Soffa Inredning',
        'slug': 'skruv-soffa',
        'contact_person': 'Gunilla Möbel',
        'phone': '013-202020',
        'address': 'Industrigatan 8, Linköping',
        'city': 'Linköping',
        'description': 'Möbler och inredning med lite för många reor och lite för litet lager. Gunilla har åsikter om allt men säljer billigt. Showroom-ex och returnerade möbler till bottenpriser.',
        'policy_text': 'Hämta inom 24 h. Stora möbler kräver eget fordon. Betalning vid bokning.',
        'pickup_instructions': 'Kör till bakfickan på Industrigatan 8. Gunilla hjälper bära.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-04',
        'created_at': '2026-03-07T10:00:00+00:00',
    },

    # ── Cykel & outdoor ───────────────────────────────────────────────────────
    {
        'id': 'store-13',
        'email': 'pedal@vattjakke.se',
        'password_hash': _PW,
        'business_name': 'Våttjacka & Vind Outdoor',
        'slug': 'vattjakka-vind',
        'contact_person': 'Björn Frilufts',
        'phone': '090-303030',
        'address': 'Strandvägen 3, Umeå',
        'city': 'Umeå',
        'description': 'Outdoorbutik driven av Björn som tältar 200 nätter om året och inte förstår varför alla andra inte gör det. Förra säsongens jackor, hjälmar och cykeltillbehör.',
        'policy_text': 'Alla varor i fullgott skick. Hämta inom 48 h.',
        'pickup_instructions': 'Björn är ute och springer. Ringa så kommer han in.',
        'status': 'approved',
        'stripe_onboarding_done': False,
        'category_id': 'cat-07',
        'created_at': '2026-03-08T08:00:00+00:00',
    },

    # ── Böcker & media ────────────────────────────────────────────────────────
    {
        'id': 'store-14',
        'email': 'info@kapiteloddsen.se',
        'password_hash': _PW,
        'business_name': 'Kapitlet på Oddsen',
        'slug': 'kapitlet-pa-oddsen',
        'contact_person': 'Ingrid Bokstav',
        'phone': '040-404040',
        'address': 'Möllevångstorget 9, Malmö',
        'city': 'Malmö',
        'description': 'Antikvariat och ny-bokhandel i ett. Ingrid kan varje bok utantill men kan inte hålla reda på lagret. Överlager, felbeställningar och dubbelpryar säljs billigt.',
        'policy_text': 'Hämta inom 48 h. Böcker är böcker — inga returer.',
        'pickup_instructions': 'Knacka på. Ingrid är alltid där, omgiven av böcker.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-08',
        'created_at': '2026-03-09T11:00:00+00:00',
    },

    # ── Leksaker & hobby ──────────────────────────────────────────────────────
    {
        'id': 'store-15',
        'email': 'lek@toysanarkiet.se',
        'password_hash': _PW,
        'business_name': 'Toys Anarki AB',
        'slug': 'toys-anarki',
        'contact_person': 'Ragnar Lekman',
        'phone': '011-505050',
        'address': 'Kungsgatan 77, Norrköping',
        'city': 'Norrköping',
        'description': 'Leksaksbutik driven som ett experiment i kaos. Ragnar har aldrig haft ordning på lagret men alltid haft bra priser. Skadade förpackningar, returnerade leksaker, säsongsöverlager.',
        'policy_text': 'Alla leksaker är säkerhetskontrollerade. Hämta inom 24 h.',
        'pickup_instructions': 'Hitta kassan. Det kan ta ett ögonblick.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-09',
        'created_at': '2026-03-10T09:00:00+00:00',
    },

    # ── Bygg & verktyg ────────────────────────────────────────────────────────
    {
        'id': 'store-16',
        'email': 'verktyg@spikochspara.se',
        'password_hash': _PW,
        'business_name': 'Spik & Spara Byggvaror',
        'slug': 'spik-spara',
        'contact_person': 'Rune Hammar',
        'phone': '019-606060',
        'address': 'Fabriksgatan 22, Örebro',
        'city': 'Örebro',
        'description': 'Byggmaterialhandlare med Rune som aldrig slänger något. Returnerade verktyg, öppnade paket, exdemo-maskiner. Om du vet vad du letar efter hittar du guld här.',
        'policy_text': 'Alla verktyg är testade. Hämta inom 48 h. Inga returer på el-verktyg.',
        'pickup_instructions': 'Bakdörren mot parkeringen. Rune bär ut om det är tungt.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-10',
        'created_at': '2026-03-11T08:00:00+00:00',
    },

    # ── Optik & glasögon ──────────────────────────────────────────────────────
    {
        'id': 'store-17',
        'email': 'syn@glaskaramellen.se',
        'password_hash': _PW,
        'business_name': 'Glaskaramellen Optik',
        'slug': 'glaskaramellen',
        'contact_person': 'Viola Syn',
        'phone': '026-707070',
        'address': 'Drottninggatan 5, Gävle',
        'city': 'Gävle',
        'description': 'Optiker med ett öga för fynd (och ett för precision). Provbågarna från förra kollektionen, solglasögon med skadade fodral och displayglasögon säljs via FlashDeal.',
        'policy_text': 'Glasögon utan styrka. Hämta inom 48 h. Fullbetalning vid bokning.',
        'pickup_instructions': 'Fråga efter Viola. Hon ser dig komma på långt håll.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-11',
        'created_at': '2026-03-12T10:00:00+00:00',
    },

    # ── Smycken & klockor ─────────────────────────────────────────────────────
    {
        'id': 'store-18',
        'email': 'guld@ticktackjuvelern.se',
        'password_hash': _PW,
        'business_name': 'Tick Tack Juvelerarn',
        'slug': 'tick-tack-juvelerarn',
        'contact_person': 'Harriet Guld',
        'phone': '018-808080',
        'address': 'Stora Torget 1, Uppsala',
        'city': 'Uppsala',
        'description': 'Tredje generationens guldsmed. Harriet säljer det kunden ångrat, det klockan tappat och det smycket som aldrig passade. Äkta silver, äkta fynd.',
        'policy_text': 'Alla smycken äkthetsgaranterade. Hämta inom 24 h. Fullbetalning vid bokning.',
        'pickup_instructions': 'Ring klockan (på dörren, inte på mobilen). Harriet öppnar.',
        'status': 'approved',
        'stripe_onboarding_done': True,
        'category_id': 'cat-12',
        'created_at': '2026-03-13T11:00:00+00:00',
    },

    # ── Musik & instrument ────────────────────────────────────────────────────
    {
        'id': 'store-19',
        'email': 'noter@falsktonerna.se',
        'password_hash': _PW,
        'business_name': 'Falsktonernas Musikhörna',
        'slug': 'falsktonernas-musikhorna',
        'contact_person': 'Otto Ackord',
        'phone': '042-909090',
        'address': 'Järnvägsgatan 14, Helsingborg',
        'city': 'Helsingborg',
        'description': 'Musikaffär startad av Otto som lovat sin mor att "inte bara spela gitarr". Han säljer även instrument nu. Repade gitarrer, öppnade strängar, demo-keyboards och det ena trumsettet.',
        'policy_text': 'Instrument i angivet skick. Hämta inom 48 h.',
        'pickup_instructions': 'Om du hör musik inifrån — Otto är i form. Kliv in.',
        'status': 'approved',
        'stripe_onboarding_done': False,
        'category_id': 'cat-14',
        'created_at': '2026-03-14T12:00:00+00:00',
    },
]

# Flerkategori-kopplingar (utöver primär category_id på butiken)
STORE_CATEGORIES = [
    # Klippa Klapp Sax: Hårvård (primär) + Skönhet & hälsa
    {'store_id': 'store-01', 'category_id': 'cat-16'},
    {'store_id': 'store-01', 'category_id': 'cat-06'},
    # Permanent Wave & Spa: Hårvård (primär) + Spa + Skönhet
    {'store_id': 'store-02', 'category_id': 'cat-16'},
    {'store_id': 'store-02', 'category_id': 'cat-17'},
    {'store_id': 'store-02', 'category_id': 'cat-06'},
    # Gurkan & Gubben: Café (primär) + Mat & dryck
    {'store_id': 'store-03', 'category_id': 'cat-18'},
    {'store_id': 'store-03', 'category_id': 'cat-03'},
    # Lasse på Berget: Café (primär) + Mat & dryck
    {'store_id': 'store-04', 'category_id': 'cat-18'},
    {'store_id': 'store-04', 'category_id': 'cat-03'},
    # Gymmet som inte dömer: Gym (primär) + Sport & fritid
    {'store_id': 'store-05', 'category_id': 'cat-19'},
    {'store_id': 'store-05', 'category_id': 'cat-05'},
    # Yoga i Pyjamas: Gym (primär) + Sport + Skönhet & hälsa
    {'store_id': 'store-06', 'category_id': 'cat-19'},
    {'store_id': 'store-06', 'category_id': 'cat-05'},
    {'store_id': 'store-06', 'category_id': 'cat-06'},
    # Mjau, Voff & Fikus: Djur (primär) + Trädgård
    {'store_id': 'store-07', 'category_id': 'cat-13'},
    {'store_id': 'store-07', 'category_id': 'cat-15'},
    # Botaniska Bråkmakeriet: Florist (primär) + Trädgård + Djur
    {'store_id': 'store-08', 'category_id': 'cat-20'},
    {'store_id': 'store-08', 'category_id': 'cat-15'},
    # Trasiga Knäbyxor: Mode (primär) + Hem & inredning
    {'store_id': 'store-09', 'category_id': 'cat-02'},
    {'store_id': 'store-09', 'category_id': 'cat-04'},
    # Modecentrum Halvpris: Mode (primär)
    {'store_id': 'store-10', 'category_id': 'cat-02'},
    # Pixelpaniken: Elektronik
    {'store_id': 'store-11', 'category_id': 'cat-01'},
    # Skruv & Soffa: Hem & inredning + Bygg
    {'store_id': 'store-12', 'category_id': 'cat-04'},
    {'store_id': 'store-12', 'category_id': 'cat-10'},
    # Våttjacka & Vind: Cykel + Sport
    {'store_id': 'store-13', 'category_id': 'cat-07'},
    {'store_id': 'store-13', 'category_id': 'cat-05'},
    # Kapitlet på Oddsen: Böcker + Leksaker & hobby
    {'store_id': 'store-14', 'category_id': 'cat-08'},
    {'store_id': 'store-14', 'category_id': 'cat-09'},
    # Toys Anarki: Leksaker + Böcker
    {'store_id': 'store-15', 'category_id': 'cat-09'},
    {'store_id': 'store-15', 'category_id': 'cat-08'},
    # Spik & Spara: Bygg + Hem
    {'store_id': 'store-16', 'category_id': 'cat-10'},
    {'store_id': 'store-16', 'category_id': 'cat-04'},
    # Glaskaramellen: Optik + Skönhet
    {'store_id': 'store-17', 'category_id': 'cat-11'},
    {'store_id': 'store-17', 'category_id': 'cat-06'},
    # Tick Tack Juvelerarn: Smycken
    {'store_id': 'store-18', 'category_id': 'cat-12'},
    # Falsktonernas Musikhörna: Musik + Leksaker
    {'store_id': 'store-19', 'category_id': 'cat-14'},
    {'store_id': 'store-19', 'category_id': 'cat-09'},
]

OFFERS = [
    {
        'id': 'offer-01',
        'store_id': 'store-01',
        'category_id': 'cat-16',
        'title': 'Klippning + tvätt — 3 tider idag',
        'description': 'Tre osålda tider kl 14, 15 och 16. Dam eller herr, kort eller långt. Rodrigo klipper, du bestämmer stil.',
        'original_price': 650.0,
        'deal_price': 290.0,
        'total_quantity': 3,
        'remaining_qty': 3,
        'photo_url': None,
        'expires_at': _future(4),
        'status': 'active',
        'created_at': _future(-1),
    },
    {
        'id': 'offer-02',
        'store_id': 'store-02',
        'category_id': 'cat-17',
        'title': 'Ansiktsbehandling 60 min — 2 tider',
        'description': 'Djuprengörande ansiktsbehandling med Biologique Recherche-produkter. Normalt fullbokat 3 veckor framåt.',
        'original_price': 1200.0,
        'deal_price': 499.0,
        'total_quantity': 2,
        'remaining_qty': 2,
        'photo_url': None,
        'expires_at': _future(6),
        'status': 'active',
        'created_at': _future(-0.5),
    },
    {
        'id': 'offer-03',
        'store_id': 'store-03',
        'category_id': 'cat-18',
        'title': 'Brunchkasse för 2 — mix turkisk-svensk',
        'description': 'Menemen, surdegsbröd, ajvar, labneh, skinka och kaffe. Ihopsatt av Gurkan idag. Pappan kritiserade upplägget men gillade smaken.',
        'original_price': 220.0,
        'deal_price': 89.0,
        'total_quantity': 5,
        'remaining_qty': 5,
        'photo_url': None,
        'expires_at': _future(2),
        'status': 'active',
        'created_at': _future(-0.5),
    },
    {
        'id': 'offer-04',
        'store_id': 'store-04',
        'category_id': 'cat-18',
        'title': 'Surdegspåsen — 4 limpor blandat',
        'description': 'Rågsur, vetemjölssur, dinkel och en mystisk fjärde som Lasse kallar "fredagslimpan". Bakade kl 04 i morse.',
        'original_price': 240.0,
        'deal_price': 95.0,
        'total_quantity': 4,
        'remaining_qty': 3,
        'photo_url': None,
        'expires_at': _future(3),
        'status': 'active',
        'created_at': _future(-2),
    },
    {
        'id': 'offer-05',
        'store_id': 'store-05',
        'category_id': 'cat-19',
        'title': '10-kortskort gym — oanvänt',
        'description': 'Köpt av en kund med goda intentioner. Aldrig stämplat. Nu ditt. Inkl. bastu och gruppträning.',
        'original_price': 990.0,
        'deal_price': 390.0,
        'total_quantity': 3,
        'remaining_qty': 3,
        'photo_url': None,
        'expires_at': _future(12),
        'status': 'active',
        'created_at': _future(-1),
    },
    {
        'id': 'offer-06',
        'store_id': 'store-06',
        'category_id': 'cat-19',
        'title': 'Yoga-klass 5-pack — Yin & Hatha',
        'description': 'Fem klasser att nyttja när du vill under 30 dagar. Yin på tisdagar, Hatha på torsdagar. Pyjamas OK.',
        'original_price': 750.0,
        'deal_price': 299.0,
        'total_quantity': 4,
        'remaining_qty': 4,
        'photo_url': None,
        'expires_at': _future(8),
        'status': 'active',
        'created_at': _future(-0.5),
    },
    {
        'id': 'offer-07',
        'store_id': 'store-07',
        'category_id': 'cat-13',
        'title': 'Royal Canin storpack — skadad förpackning',
        'description': '15 kg Adult Indoor. Förpackningen har ett hörn-bula men innehållet är perfekt. Bäst-före om 9 månader.',
        'original_price': 480.0,
        'deal_price': 199.0,
        'total_quantity': 4,
        'remaining_qty': 4,
        'photo_url': None,
        'expires_at': _future(24),
        'status': 'active',
        'created_at': _future(-2),
    },
    {
        'id': 'offer-08',
        'store_id': 'store-08',
        'category_id': 'cat-20',
        'title': 'Blandad blomsterkasse — "vad Stellan hittar"',
        'description': 'Stellan sätter ihop en bukett av vad som är kvar och är ärlig om att han inte vet vad det innehåller. 100% garanterat botaniskt.',
        'original_price': 350.0,
        'deal_price': 99.0,
        'total_quantity': 6,
        'remaining_qty': 6,
        'photo_url': None,
        'expires_at': _future(5),
        'status': 'active',
        'created_at': _future(-0.5),
    },
    {
        'id': 'offer-09',
        'store_id': 'store-09',
        'category_id': 'cat-02',
        'title': 'Levi\'s 501 vintage — 3 storlekar kvar',
        'description': 'W30, W32 och W34. Äkta 90-tal, inga konstgjorda hål (hålen är verkliga). Tvättade och kontrollerade.',
        'original_price': 899.0,
        'deal_price': 349.0,
        'total_quantity': 3,
        'remaining_qty': 3,
        'photo_url': None,
        'expires_at': _future(10),
        'status': 'active',
        'created_at': _future(-1),
    },
    {
        'id': 'offer-10',
        'store_id': 'store-10',
        'category_id': 'cat-02',
        'title': 'Herrkavaj märke okänt — 5 storlekar',
        'description': 'Kenneth vet inte vilket märke. "Den ser dyr ut" är hans bedömning. S, M, L, XL och "stor XL". Prova gärna.',
        'original_price': 1200.0,
        'deal_price': 299.0,
        'total_quantity': 5,
        'remaining_qty': 5,
        'photo_url': None,
        'expires_at': _future(18),
        'status': 'active',
        'created_at': _future(-0.5),
    },
    {
        'id': 'offer-11',
        'store_id': 'store-11',
        'category_id': 'cat-01',
        'title': 'iPad 10:e gen 64 GB — öppnad retur',
        'description': 'Kund bytte storlek. Öppnad men aldrig använd. Kvitto medföljer. Fullt fabriksgaranti kvar.',
        'original_price': 5990.0,
        'deal_price': 3490.0,
        'total_quantity': 1,
        'remaining_qty': 1,
        'photo_url': None,
        'expires_at': _future(5),
        'status': 'active',
        'created_at': _future(-1),
    },
    {
        'id': 'offer-12',
        'store_id': 'store-11',
        'category_id': 'cat-01',
        'title': 'Sony-hörlurar + Philips-rakapparat — showroom-paket',
        'description': 'Två utställningsex som aldrig såldes ihop. Sony WH-CH720N + Philips Series 3000. Tillsammans 40% under ordinarie.',
        'original_price': 2800.0,
        'deal_price': 1190.0,
        'total_quantity': 2,
        'remaining_qty': 2,
        'photo_url': None,
        'expires_at': _future(8),
        'status': 'active',
        'created_at': _future(-0.5),
    },
    {
        'id': 'offer-13',
        'store_id': 'store-12',
        'category_id': 'cat-04',
        'title': 'IKEA-fåtölj STRANDMON — showroom',
        'description': 'Provad av otaliga kunder, fortfarande i perfekt skick. Gunilla har polerat den personligen. Mörkgrå.',
        'original_price': 2995.0,
        'deal_price': 990.0,
        'total_quantity': 1,
        'remaining_qty': 1,
        'photo_url': None,
        'expires_at': _future(24),
        'status': 'active',
        'created_at': _future(-2),
    },
    {
        'id': 'offer-14',
        'store_id': 'store-12',
        'category_id': 'cat-04',
        'title': 'Kökslampor 3-pack — skadad förpackning',
        'description': 'Kartongen har ett hörn intryckt men lamporna är hela. LED, 2700K varmt vitt. Normalt 799 kr/pack.',
        'original_price': 799.0,
        'deal_price': 249.0,
        'total_quantity': 4,
        'remaining_qty': 4,
        'photo_url': None,
        'expires_at': _future(12),
        'status': 'active',
        'created_at': _future(-1),
    },
    {
        'id': 'offer-15',
        'store_id': 'store-13',
        'category_id': 'cat-07',
        'title': 'Cykelhjälm POC Axion — förra säsongens',
        'description': 'Röd/svart, storlek M. Aldrig använd, hängt i butik ett år. Normalt 1 490 kr. Fullt godkänd och säker.',
        'original_price': 1490.0,
        'deal_price': 490.0,
        'total_quantity': 2,
        'remaining_qty': 2,
        'photo_url': None,
        'expires_at': _future(48),
        'status': 'active',
        'created_at': _future(-3),
    },
    {
        'id': 'offer-16',
        'store_id': 'store-13',
        'category_id': 'cat-05',
        'title': 'Bergsportjacka Haglöfs — dam S och M',
        'description': 'Provad på mässa, inga defekter. Gore-Tex, röd. Björn tycker alla borde ha en sådan. Han kan ha rätt.',
        'original_price': 3200.0,
        'deal_price': 1290.0,
        'total_quantity': 2,
        'remaining_qty': 2,
        'photo_url': None,
        'expires_at': _future(36),
        'status': 'active',
        'created_at': _future(-1),
    },
    {
        'id': 'offer-17',
        'store_id': 'store-14',
        'category_id': 'cat-08',
        'title': '8 romaner i kasse — Ingrid väljer åt dig',
        'description': 'Ingrid plockar ihop 8 böcker baserat på dina preferenser (ange vid hämtning). Garanterat inget skräp.',
        'original_price': 640.0,
        'deal_price': 199.0,
        'total_quantity': 5,
        'remaining_qty': 5,
        'photo_url': None,
        'expires_at': _future(24),
        'status': 'active',
        'created_at': _future(-0.5),
    },
    {
        'id': 'offer-18',
        'store_id': 'store-15',
        'category_id': 'cat-09',
        'title': 'LEGO-kasse — 3 set med skadad box',
        'description': 'LEGO Creator 31141, City 60380 och Technic 42151. Lådorna är klämda men innehållet är komplett. Ragnar räknade brikkarna. Ungefär.',
        'original_price': 990.0,
        'deal_price': 349.0,
        'total_quantity': 3,
        'remaining_qty': 3,
        'photo_url': None,
        'expires_at': _future(20),
        'status': 'active',
        'created_at': _future(-1),
    },
    {
        'id': 'offer-19',
        'store_id': 'store-16',
        'category_id': 'cat-10',
        'title': 'Bosch slagborrmaskin — exdemo med väska',
        'description': 'Visad på mässa, aldrig i produktion. GSB 18V-55. Batteri medföljer. Rune testade den — "snurrar som den ska".',
        'original_price': 2490.0,
        'deal_price': 990.0,
        'total_quantity': 1,
        'remaining_qty': 1,
        'photo_url': None,
        'expires_at': _future(48),
        'status': 'active',
        'created_at': _future(-2),
    },
    {
        'id': 'offer-20',
        'store_id': 'store-17',
        'category_id': 'cat-11',
        'title': 'Ray-Ban Clubmaster — 6 par provbågar',
        'description': 'Utan styrka, utan repor. Svart/guld-finish. Viola har torkat dem med microfiber. De är rena.',
        'original_price': 1800.0,
        'deal_price': 590.0,
        'total_quantity': 6,
        'remaining_qty': 6,
        'photo_url': None,
        'expires_at': _future(72),
        'status': 'active',
        'created_at': _future(-1),
    },
    {
        'id': 'offer-21',
        'store_id': 'store-18',
        'category_id': 'cat-12',
        'title': 'Silverarmband — kundåterlämnat, oanvänt',
        'description': 'Kund betalade, hämtade aldrig. 925 silver, 18 cm, droppformat hänge. Harriet är förargad. Du får köpa det billigt.',
        'original_price': 890.0,
        'deal_price': 390.0,
        'total_quantity': 1,
        'remaining_qty': 1,
        'photo_url': None,
        'expires_at': _future(24),
        'status': 'active',
        'created_at': _future(-0.5),
    },
    {
        'id': 'offer-22',
        'store_id': 'store-19',
        'category_id': 'cat-14',
        'title': 'Yamaha P-45 digitalpiano — demoanvänt',
        'description': 'Stått i butiken i 8 månader, provspelat dagligen. 88 tangenter, viktade. Otto säger det låter bättre av att ha spelats in. Han ljuger inte.',
        'original_price': 5900.0,
        'deal_price': 2990.0,
        'total_quantity': 1,
        'remaining_qty': 1,
        'photo_url': None,
        'expires_at': _future(48),
        'status': 'active',
        'created_at': _future(-3),
    },
]

BOOKINGS = [
    {
        'id': 'booking-01',
        'offer_id': 'offer-03',
        'customer_id': 'cust-01',
        'store_id': 'store-03',
        'quantity': 1,
        'total_paid': 89.0,
        'platform_fee': 5.34,
        'payment_status': 'paid',
        'status': 'picked_up',
        'qr_token': 'aabbcc' * 8,
        'qr_used': True,
        'expires_at': _future(-1),
        'created_at': _future(-5),
    },
    {
        'id': 'booking-02',
        'offer_id': 'offer-01',
        'customer_id': 'cust-02',
        'store_id': 'store-01',
        'quantity': 1,
        'total_paid': 290.0,
        'platform_fee': 17.4,
        'payment_status': 'paid',
        'status': 'confirmed',
        'qr_token': 'ddeeff' * 8,
        'qr_used': False,
        'expires_at': _future(3),
        'created_at': _future(-0.5),
    },
]

CUSTOMERS = [
    {
        'id': 'cust-01',
        'email': 'test@flashdeal.se',
        'password_hash': _PW,
        'full_name': 'Test Testsson',
        'phone': '+46701234567',
        'notify_email': True,
        'notify_sms': False,
        'created_at': '2026-03-01T10:00:00+00:00',
    },
    {
        'id': 'cust-02',
        'email': 'kund2@example.se',
        'password_hash': _PW,
        'full_name': 'Anna Andersson',
        'phone': '+46709876543',
        'notify_email': True,
        'notify_sms': True,
        'created_at': '2026-03-10T12:00:00+00:00',
    },
]

# ── Demo-select: slår upp hårdkodad data ──────────────────────────────────────

def demo_select(table, filters=None, columns='*', order=None, limit=None):
    data_map = {
        'categories':           CATEGORIES,
        'stores':               STORES,
        'offers':               OFFERS,
        'bookings':             BOOKINGS,
        'customers':            CUSTOMERS,
        'store_categories':     STORE_CATEGORIES,
        'customer_subscriptions': [],
        'notification_log':    [],
    }
    rows = list(data_map.get(table, []))

    if filters:
        for key, val in filters.items():
            if key in ('order', 'limit', 'select'):
                continue
            if isinstance(val, list):
                rows = [r for r in rows if r.get(key) in val]
            elif isinstance(val, dict):
                pass  # gte/lte — ignoreras i demo
            else:
                rows = [r for r in rows if str(r.get(key, '')) == str(val)]

    if order:
        field   = order.replace('.asc', '').replace('.desc', '')
        reverse = '.desc' in order
        rows    = sorted(rows, key=lambda r: r.get(field, ''), reverse=reverse)

    if limit:
        rows = rows[:int(limit)]

    return rows


# ── In-memory writes (nollställs vid omstart) ─────────────────────────────────

import uuid as _uuid

_DEMO_WRITES = {
    'customers':              [],
    'stores':                 [],
    'bookings':               [],
    'store_categories':       [],
    'customer_subscriptions': [],
    'notification_log':       [],
}

def demo_insert(table, data):
    store = _DEMO_WRITES.setdefault(table, [])
    row   = dict(data)
    if 'id' not in row:
        row['id'] = str(_uuid.uuid4())
    store.append(row)
    _inject(table, row)
    return row

def demo_update(table, filters, data):
    for row in _get_list(table):
        if all(str(row.get(k, '')) == str(v) for k, v in filters.items()):
            row.update(data)
            return row
    return None

def demo_delete(table, filters):
    target   = _get_list(table)
    to_remove = [r for r in target if all(str(r.get(k,'')) == str(v) for k,v in filters.items())]
    for r in to_remove:
        target.remove(r)
    return bool(to_remove)

def _get_list(table):
    _map = {
        'categories': CATEGORIES, 'stores': STORES, 'offers': OFFERS,
        'bookings': BOOKINGS, 'customers': CUSTOMERS,
        'store_categories': STORE_CATEGORIES,
    }
    return _map.get(table, _DEMO_WRITES.setdefault(table, []))

def _inject(table, row):
    lst = _get_list(table)
    if row not in lst:
        lst.append(row)
