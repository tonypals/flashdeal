-- ================================================================
-- FlashDeal — Seed-data for Supabase
-- Kör i: Supabase Dashboard → SQL Editor
-- ================================================================

-- === 1. KATEGORIER ===
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Elektronik', '📱', 'elektronik', 1) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Kläder & mode', '👗', 'klader-mode', 2) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Mat & dryck', '🍞', 'mat-dryck', 3) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Hem & inredning', '🛋️', 'hem-inredning', 4) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Sport & fritid', '🏃', 'sport-fritid', 5) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Skönhet & hälsa', '💄', 'skonhet-halsa', 6) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Cykel & outdoor', '🚲', 'cykel', 7) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Böcker & media', '📚', 'bocker-media', 8) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Leksaker & hobby', '🎮', 'leksaker-hobby', 9) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Bygg & verktyg', '🔧', 'bygg-verktyg', 10) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Optik & glasögon', '👓', 'optik', 11) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Smycken & klockor', '⌚', 'smycken', 12) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Djur & tillbehör', '🐾', 'djur', 13) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Musik & instrument', '🎸', 'musik', 14) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Trädgård & utemiljö', '🌿', 'tradgard', 15) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Hårvård & frisör', '✂️', 'harvard', 16) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Spa & massage', '🧖', 'spa', 17) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Café & bageri', '☕', 'cafe-bageri', 18) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Gym & träning', '🏋️', 'gym', 19) ON CONFLICT (slug) DO NOTHING;
INSERT INTO fd_categories (name, icon, slug, sort_order) VALUES ('Florist & blommor', '🌸', 'florist', 20) ON CONFLICT (slug) DO NOTHING;

-- === 2. BUTIKER ===
-- OBS: password_hash är en platshållare. Butiker loggar in via Supabase Auth i produktion.
-- I testläge: butiker behöver registreras via /butik/registrera för att få riktigt lösenord.
INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('info@klippaklapp.se', 'seed-no-login', 'Klippa Klapp Sax', 'klippa-klapp-sax',
        'Rodrigo Persson', '08-123456', 'Drottninggatan 88, Stockholm',
        'Stockholm', 'Stockholms mest överskattade frisörsalong — men med riktigt bra priser på osålda tider. Vi klipper, vi färgar, vi lovar att lyssna på dig (ungefär).', 'Betalning vid bokning. Hämta (infinn dig) inom tidsfönstret. Utebliven kund = ingen återbetalning.',
        'Gå in genom den blå dörren. Om Rodrigo spelar gitarr — avbryt honom, det är OK.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('hej@permanentwave.se', 'seed-no-login', 'Permanent Wave & Spa Malmö', 'permanent-wave-spa-malmo',
        'Birgitta Håkansson', '040-654321', 'Södergatan 14, Malmö',
        'Malmö', 'Klassisk salong med modern touch. Vi gör permanent (ja, vi menar det), ansiktsbehandlingar och existentiella kriser till reducerat pris.', 'Fullbetalning vid bokning. Vill du avboka? Ring senast 2 timmar innan.',
        'Fråga efter Birgitta. Ignorera doften — det är permlösning, inte fara.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('kaffe@gurkanochgubben.se', 'seed-no-login', 'Gurkan & Gubben Café', 'gurkan-gubben-cafe',
        'Gurkan Yilmaz', '018-998877', 'Fyristorg 3, Uppsala',
        'Uppsala', 'Brunch-café med turkisk-svensk fusion. Gurkan bakar, gubben (hans far) sitter i hörnet och kritiserar. Osålda bakverk säljs via FlashDeal — oftast bättre än det som säljs normalt.', 'Hämta senast kl 17. Betalning vid bokning. Vi ger dig alltid lite extra.',
        'Säg att du hämtar en FlashDeal-beställning. Gurkan ler. Det är ovanligt. Njut av det.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('lasse@bergetsbageri.se', 'seed-no-login', 'Lasse på Bergets Bageri', 'lasse-bergets-bageri',
        'Lars-Göran Bergström', '042-112233', 'Stortorget 7, Helsingborg',
        'Helsingborg', 'Tredje generationens surdegsbagare i Helsingborg. Lasse börjar baka kl 03 och har lite för mycket kvar vid 16-tiden. Det är din vinst.', 'Hämta senast kl 18. Allt bröd är bakat samma dag. Betalning vid bokning.',
        'Knacka på bakdörren om skylten säger stängt — Lasse är där. Han är alltid där.', 'approved', false)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('info@gymmetsomdömer.se', 'seed-no-login', 'Gymmet som inte dömer', 'gymmet-som-inte-domer',
        'Pontus Stark', '011-334455', 'Industrigatan 22, Norrköping',
        'Norrköping', 'Vi dömer verkligen inte. Inte ens om du köper ett 10-kortskort och bara använder ett. Vi säljer oanvända kort och utgångna träningspaket via FlashDeal.', 'Köpta träningskort är personliga och ej återköpbara. Giltighet framgår av erbjudandet.',
        'Visa QR-koden i receptionen. Pontus scannar och ger dig ett högt fem. Oavsett om du vill.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('namaste@yogaipyjamas.se', 'seed-no-login', 'Yoga i Pyjamas Lund', 'yoga-i-pyjamas-lund',
        'Frida Stillsam', '046-556677', 'Klostergatan 9, Lund',
        'Lund', 'Lunds mjukaste yogastudio. Vi kräver inte leggings — pyjamas välkomnas, joggers accepteras, kostym är OK om du är den typen. Osålda klasser säljs billigt via FlashDeal.', 'Bokad klass gäller specifikt datum och tid. Ej hämtad = ej återbetald. Stressen stannar utanför dörren.',
        'Dörren är alltid öppen (bildligt och bokstavligt). Meddela Frida på SMS om du är sen.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('hej@mjauvoff.se', 'seed-no-login', 'Mjau, Voff & Fikus AB', 'mjau-voff-fikus',
        'Annika Djurberg', '090-223344', 'Rådhusesplanaden 12, Umeå',
        'Umeå', 'Djuraffär och plantbutik i ett. För oss är en katt och en fikus likvärdiga sällskapsdjur. Vi säljer utgångna eller skadade förpackningar av djurmat och överskotts-krukor via FlashDeal.', 'Alla produkter är kontrollerade och säkra. Hämta inom 24 timmar.',
        'Hitta Annika bakom terrarierna. Ignorera papegojans kommentarer.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('blommor@botaniskabrak.se', 'seed-no-login', 'Botaniska Bråkmakeriet', 'botaniska-brakmakeriet',
        'Stellan Grönberg', '019-445566', 'Storgatan 44, Örebro',
        'Örebro', 'Örebros mest kaotiska blomsterhandlare. Stellan har alltid för mycket och vet aldrig riktigt vad han har. Det gör varje FlashDeal-köp till en liten överraskning.', 'Växter är levande — hämta snabbt. Betalning vid bokning. Stellan tar inget ansvar för känslosamma reaktioner vid blomöppning.',
        'Ring på om dörren är stängd. Eller kliv bara in, det är OK också.', 'approved', false)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('info@trasigaknaby.se', 'seed-no-login', 'Trasiga Knäbyxor Vintage', 'trasiga-knabyxor-vintage',
        'Maja Hedlund', '013-667788', 'Ågatan 18, Linköping',
        'Linköping', 'Vintage-butik med ett hjärta av guld och ett lager av 90-talskläder. Hålen i byxorna är avsiktliga, prislapparna är inte det. Överlager och säsongsslutsplagg säljs via FlashDeal.', 'Alla plagg är kontrollerade. Storlekar kan variera — vintage är vintage. Ej återköpt.',
        'Maja finns alltid. Kaffe bjuds alltid. Det är en regel.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('halvan@modecentrum.se', 'seed-no-login', 'Modecentrum Halvpris AB', 'modecentrum-halvpris',
        'Kenneth Kjell', '026-889900', 'Drottninggatan 31, Gävle',
        'Gävle', 'Kenneth sålde bilar i 20 år och vet fortfarande ingenting om mode. Men han köper in bra och säljer billigt, och det är det enda som räknas. Alltid 40–70% rabatt.', 'Betalning vid bokning. Allt säljs i befintligt skick. Kenneth lovar ingenting om passform.',
        'Kenneth är alltid på plats. Han vill prata. Det är en del av upplevelsen.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('info@pixelpaniken.se', 'seed-no-login', 'Pixelpaniken AB', 'pixelpaniken',
        'Christer Bygg', '031-101010', 'Södra Vägen 2, Göteborg',
        'Göteborg', 'Elektronikbutik med panik i blicken och rabatter i lagret. Returvaror, utställningsex och förra årets modeller. Christer köper in för mycket — det är din fördel.', 'Betalning vid bokning. Hämta inom 3 timmar. Allt är kontrollerat.',
        'Fråga efter Christer vid teknikdisken.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('hej@skruvochsoffa.se', 'seed-no-login', 'Skruv & Soffa Inredning', 'skruv-soffa',
        'Gunilla Möbel', '013-202020', 'Industrigatan 8, Linköping',
        'Linköping', 'Möbler och inredning med lite för många reor och lite för litet lager. Gunilla har åsikter om allt men säljer billigt. Showroom-ex och returnerade möbler till bottenpriser.', 'Hämta inom 24 h. Stora möbler kräver eget fordon. Betalning vid bokning.',
        'Kör till bakfickan på Industrigatan 8. Gunilla hjälper bära.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('pedal@vattjakke.se', 'seed-no-login', 'Våttjacka & Vind Outdoor', 'vattjakka-vind',
        'Björn Frilufts', '090-303030', 'Strandvägen 3, Umeå',
        'Umeå', 'Outdoorbutik driven av Björn som tältar 200 nätter om året och inte förstår varför alla andra inte gör det. Förra säsongens jackor, hjälmar och cykeltillbehör.', 'Alla varor i fullgott skick. Hämta inom 48 h.',
        'Björn är ute och springer. Ringa så kommer han in.', 'approved', false)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('info@kapiteloddsen.se', 'seed-no-login', 'Kapitlet på Oddsen', 'kapitlet-pa-oddsen',
        'Ingrid Bokstav', '040-404040', 'Möllevångstorget 9, Malmö',
        'Malmö', 'Antikvariat och ny-bokhandel i ett. Ingrid kan varje bok utantill men kan inte hålla reda på lagret. Överlager, felbeställningar och dubbelpryar säljs billigt.', 'Hämta inom 48 h. Böcker är böcker — inga returer.',
        'Knacka på. Ingrid är alltid där, omgiven av böcker.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('lek@toysanarkiet.se', 'seed-no-login', 'Toys Anarki AB', 'toys-anarki',
        'Ragnar Lekman', '011-505050', 'Kungsgatan 77, Norrköping',
        'Norrköping', 'Leksaksbutik driven som ett experiment i kaos. Ragnar har aldrig haft ordning på lagret men alltid haft bra priser. Skadade förpackningar, returnerade leksaker, säsongsöverlager.', 'Alla leksaker är säkerhetskontrollerade. Hämta inom 24 h.',
        'Hitta kassan. Det kan ta ett ögonblick.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('verktyg@spikochspara.se', 'seed-no-login', 'Spik & Spara Byggvaror', 'spik-spara',
        'Rune Hammar', '019-606060', 'Fabriksgatan 22, Örebro',
        'Örebro', 'Byggmaterialhandlare med Rune som aldrig slänger något. Returnerade verktyg, öppnade paket, exdemo-maskiner. Om du vet vad du letar efter hittar du guld här.', 'Alla verktyg är testade. Hämta inom 48 h. Inga returer på el-verktyg.',
        'Bakdörren mot parkeringen. Rune bär ut om det är tungt.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('syn@glaskaramellen.se', 'seed-no-login', 'Glaskaramellen Optik', 'glaskaramellen',
        'Viola Syn', '026-707070', 'Drottninggatan 5, Gävle',
        'Gävle', 'Optiker med ett öga för fynd (och ett för precision). Provbågarna från förra kollektionen, solglasögon med skadade fodral och displayglasögon säljs via FlashDeal.', 'Glasögon utan styrka. Hämta inom 48 h. Fullbetalning vid bokning.',
        'Fråga efter Viola. Hon ser dig komma på långt håll.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('guld@ticktackjuvelern.se', 'seed-no-login', 'Tick Tack Juvelerarn', 'tick-tack-juvelerarn',
        'Harriet Guld', '018-808080', 'Stora Torget 1, Uppsala',
        'Uppsala', 'Tredje generationens guldsmed. Harriet säljer det kunden ångrat, det klockan tappat och det smycket som aldrig passade. Äkta silver, äkta fynd.', 'Alla smycken äkthetsgaranterade. Hämta inom 24 h. Fullbetalning vid bokning.',
        'Ring klockan (på dörren, inte på mobilen). Harriet öppnar.', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO fd_stores (email, password_hash, business_name, slug, contact_person, phone, address, city, description, policy_text, pickup_instructions, status, stripe_onboarding_done)
VALUES ('noter@falsktonerna.se', 'seed-no-login', 'Falsktonernas Musikhörna', 'falsktonernas-musikhorna',
        'Otto Ackord', '042-909090', 'Järnvägsgatan 14, Helsingborg',
        'Helsingborg', 'Musikaffär startad av Otto som lovat sin mor att "inte bara spela gitarr". Han säljer även instrument nu. Repade gitarrer, öppnade strängar, demo-keyboards och det ena trumsettet.', 'Instrument i angivet skick. Hämta inom 48 h.',
        'Om du hör musik inifrån — Otto är i form. Kliv in.', 'approved', false)
ON CONFLICT (email) DO NOTHING;


-- === 3. KOPPLA BUTIKER TILL DERAS KATEGORIER (fd_store_categories) ===
-- Kräver att butikerna ovan skapats. Kör detta EFTER butiks-inserts.
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'klippa-klapp-sax' AND c.slug = 'harvard'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'klippa-klapp-sax' AND c.slug = 'skonhet-halsa'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'permanent-wave-spa-malmo' AND c.slug = 'harvard'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'permanent-wave-spa-malmo' AND c.slug = 'spa'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'permanent-wave-spa-malmo' AND c.slug = 'skonhet-halsa'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'gurkan-gubben-cafe' AND c.slug = 'cafe-bageri'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'gurkan-gubben-cafe' AND c.slug = 'mat-dryck'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'lasse-bergets-bageri' AND c.slug = 'cafe-bageri'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'lasse-bergets-bageri' AND c.slug = 'mat-dryck'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'gymmet-som-inte-domer' AND c.slug = 'gym'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'gymmet-som-inte-domer' AND c.slug = 'sport-fritid'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'yoga-i-pyjamas-lund' AND c.slug = 'gym'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'yoga-i-pyjamas-lund' AND c.slug = 'sport-fritid'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'yoga-i-pyjamas-lund' AND c.slug = 'skonhet-halsa'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'mjau-voff-fikus' AND c.slug = 'djur'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'mjau-voff-fikus' AND c.slug = 'tradgard'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'botaniska-brakmakeriet' AND c.slug = 'florist'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'botaniska-brakmakeriet' AND c.slug = 'tradgard'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'trasiga-knabyxor-vintage' AND c.slug = 'klader-mode'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'trasiga-knabyxor-vintage' AND c.slug = 'hem-inredning'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'modecentrum-halvpris' AND c.slug = 'klader-mode'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'pixelpaniken' AND c.slug = 'elektronik'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'skruv-soffa' AND c.slug = 'hem-inredning'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'skruv-soffa' AND c.slug = 'bygg-verktyg'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'vattjakka-vind' AND c.slug = 'cykel'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'vattjakka-vind' AND c.slug = 'sport-fritid'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'kapitlet-pa-oddsen' AND c.slug = 'bocker-media'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'kapitlet-pa-oddsen' AND c.slug = 'leksaker-hobby'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'toys-anarki' AND c.slug = 'leksaker-hobby'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'toys-anarki' AND c.slug = 'bocker-media'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'spik-spara' AND c.slug = 'bygg-verktyg'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'spik-spara' AND c.slug = 'hem-inredning'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'glaskaramellen' AND c.slug = 'optik'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'glaskaramellen' AND c.slug = 'skonhet-halsa'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'tick-tack-juvelerarn' AND c.slug = 'smycken'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'falsktonernas-musikhorna' AND c.slug = 'musik'
ON CONFLICT DO NOTHING;
INSERT INTO fd_store_categories (store_id, category_id)
SELECT s.id, c.id FROM fd_stores s, fd_categories c
WHERE s.slug = 'falsktonernas-musikhorna' AND c.slug = 'leksaker-hobby'
ON CONFLICT DO NOTHING;

-- === 4. ERBJUDANDEN ===
-- expires_at sätts relativt nu. Kör scriptet när du vill ha aktiva deals.
INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Klippning + tvätt — 3 tider idag', 'Tre osålda tider kl 14, 15 och 16. Dam eller herr, kort eller långt. Rodrigo klipper, du bestämmer stil.',
       650.0, 290.0, 3, 3,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'klippa-klapp-sax' AND c.slug = 'harvard';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Ansiktsbehandling 60 min — 2 tider', 'Djuprengörande ansiktsbehandling med Biologique Recherche-produkter. Normalt fullbokat 3 veckor framåt.',
       1200.0, 499.0, 2, 2,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'permanent-wave-spa-malmo' AND c.slug = 'spa';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Brunchkasse för 2 — mix turkisk-svensk', 'Menemen, surdegsbröd, ajvar, labneh, skinka och kaffe. Ihopsatt av Gurkan idag. Pappan kritiserade upplägget men gillade smaken.',
       220.0, 89.0, 5, 5,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'gurkan-gubben-cafe' AND c.slug = 'cafe-bageri';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Surdegspåsen — 4 limpor blandat', 'Rågsur, vetemjölssur, dinkel och en mystisk fjärde som Lasse kallar "fredagslimpan". Bakade kl 04 i morse.',
       240.0, 95.0, 4, 3,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'lasse-bergets-bageri' AND c.slug = 'cafe-bageri';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       '10-kortskort gym — oanvänt', 'Köpt av en kund med goda intentioner. Aldrig stämplat. Nu ditt. Inkl. bastu och gruppträning.',
       990.0, 390.0, 3, 3,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'gymmet-som-inte-domer' AND c.slug = 'gym';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Yoga-klass 5-pack — Yin & Hatha', 'Fem klasser att nyttja när du vill under 30 dagar. Yin på tisdagar, Hatha på torsdagar. Pyjamas OK.',
       750.0, 299.0, 4, 4,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'yoga-i-pyjamas-lund' AND c.slug = 'gym';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Royal Canin storpack — skadad förpackning', '15 kg Adult Indoor. Förpackningen har ett hörn-bula men innehållet är perfekt. Bäst-före om 9 månader.',
       480.0, 199.0, 4, 4,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'mjau-voff-fikus' AND c.slug = 'djur';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Blandad blomsterkasse — "vad Stellan hittar"', 'Stellan sätter ihop en bukett av vad som är kvar och är ärlig om att han inte vet vad det innehåller. 100% garanterat botaniskt.',
       350.0, 99.0, 6, 6,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'botaniska-brakmakeriet' AND c.slug = 'florist';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Levi''s 501 vintage — 3 storlekar kvar', 'W30, W32 och W34. Äkta 90-tal, inga konstgjorda hål (hålen är verkliga). Tvättade och kontrollerade.',
       899.0, 349.0, 3, 3,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'trasiga-knabyxor-vintage' AND c.slug = 'klader-mode';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Herrkavaj märke okänt — 5 storlekar', 'Kenneth vet inte vilket märke. "Den ser dyr ut" är hans bedömning. S, M, L, XL och "stor XL". Prova gärna.',
       1200.0, 299.0, 5, 5,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'modecentrum-halvpris' AND c.slug = 'klader-mode';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'iPad 10:e gen 64 GB — öppnad retur', 'Kund bytte storlek. Öppnad men aldrig använd. Kvitto medföljer. Fullt fabriksgaranti kvar.',
       5990.0, 3490.0, 1, 1,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'pixelpaniken' AND c.slug = 'elektronik';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Sony-hörlurar + Philips-rakapparat — showroom-paket', 'Två utställningsex som aldrig såldes ihop. Sony WH-CH720N + Philips Series 3000. Tillsammans 40% under ordinarie.',
       2800.0, 1190.0, 2, 2,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'pixelpaniken' AND c.slug = 'elektronik';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'IKEA-fåtölj STRANDMON — showroom', 'Provad av otaliga kunder, fortfarande i perfekt skick. Gunilla har polerat den personligen. Mörkgrå.',
       2995.0, 990.0, 1, 1,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'skruv-soffa' AND c.slug = 'hem-inredning';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Kökslampor 3-pack — skadad förpackning', 'Kartongen har ett hörn intryckt men lamporna är hela. LED, 2700K varmt vitt. Normalt 799 kr/pack.',
       799.0, 249.0, 4, 4,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'skruv-soffa' AND c.slug = 'hem-inredning';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Cykelhjälm POC Axion — förra säsongens', 'Röd/svart, storlek M. Aldrig använd, hängt i butik ett år. Normalt 1 490 kr. Fullt godkänd och säker.',
       1490.0, 490.0, 2, 2,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'vattjakka-vind' AND c.slug = 'cykel';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Bergsportjacka Haglöfs — dam S och M', 'Provad på mässa, inga defekter. Gore-Tex, röd. Björn tycker alla borde ha en sådan. Han kan ha rätt.',
       3200.0, 1290.0, 2, 2,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'vattjakka-vind' AND c.slug = 'sport-fritid';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       '8 romaner i kasse — Ingrid väljer åt dig', 'Ingrid plockar ihop 8 böcker baserat på dina preferenser (ange vid hämtning). Garanterat inget skräp.',
       640.0, 199.0, 5, 5,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'kapitlet-pa-oddsen' AND c.slug = 'bocker-media';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'LEGO-kasse — 3 set med skadad box', 'LEGO Creator 31141, City 60380 och Technic 42151. Lådorna är klämda men innehållet är komplett. Ragnar räknade brikkarna. Ungefär.',
       990.0, 349.0, 3, 3,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'toys-anarki' AND c.slug = 'leksaker-hobby';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Bosch slagborrmaskin — exdemo med väska', 'Visad på mässa, aldrig i produktion. GSB 18V-55. Batteri medföljer. Rune testade den — "snurrar som den ska".',
       2490.0, 990.0, 1, 1,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'spik-spara' AND c.slug = 'bygg-verktyg';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Ray-Ban Clubmaster — 6 par provbågar', 'Utan styrka, utan repor. Svart/guld-finish. Viola har torkat dem med microfiber. De är rena.',
       1800.0, 590.0, 6, 6,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'glaskaramellen' AND c.slug = 'optik';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Silverarmband — kundåterlämnat, oanvänt', 'Kund betalade, hämtade aldrig. 925 silver, 18 cm, droppformat hänge. Harriet är förargad. Du får köpa det billigt.',
       890.0, 390.0, 1, 1,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'tick-tack-juvelerarn' AND c.slug = 'smycken';

INSERT INTO fd_offers (store_id, category_id, title, description, original_price, deal_price, total_quantity, remaining_qty, expires_at, status)
SELECT s.id, c.id,
       'Yamaha P-45 digitalpiano — demoanvänt', 'Stått i butiken i 8 månader, provspelat dagligen. 88 tangenter, viktade. Otto säger det låter bättre av att ha spelats in. Han ljuger inte.',
       5900.0, 2990.0, 1, 1,
       now() + interval '6 hours', 'active'
FROM fd_stores s,
     fd_categories c
WHERE s.slug = 'falsktonernas-musikhorna' AND c.slug = 'musik';

