"""
index.py — Flask-app och blueprint-registrering
Vercel entry point: exporterar 'app'
Lokalt: python run.py
"""
import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static',
    )

    app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-byt-i-produktion')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max för bilduppladdning

    app.config['SESSION_COOKIE_SECURE']   = os.environ.get('FLASK_ENV') == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 60 * 60 * 24 * 30  # 30 dagar

    # Rate limiting (lagras i minne — OK för Vercel, byt till Redis i prod vid behov)
    Limiter(
        get_remote_address,
        app=app,
        default_limits=['200 per day', '50 per hour'],
        storage_uri='memory://',
    )

    # ── Registrera blueprints ────────────────────────────────────────────────
    from api.routes.public   import bp as public_bp
    from api.routes.auth     import bp as auth_bp
    from api.routes.store    import bp as store_bp
    from api.routes.booking  import bp as booking_bp
    from api.routes.admin    import bp as admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(store_bp,   url_prefix='/butik')
    app.register_blueprint(booking_bp, url_prefix='/betala')
    app.register_blueprint(admin_bp,   url_prefix='/admin')

    # ── Jinja-filter ─────────────────────────────────────────────────────────
    from api.config import fmt_price
    app.jinja_env.filters['price'] = fmt_price

    @app.template_filter('timeago')
    def timeago_filter(dt_str):
        if not dt_str:
            return ''
        try:
            from datetime import datetime, timezone
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            diff = dt - now
            secs = int(diff.total_seconds())
            if secs < 0:
                return 'utgångna'
            if secs < 3600:
                return f'{secs // 60} min kvar'
            if secs < 86400:
                return f'{secs // 3600} tim kvar'
            return f'{secs // 86400} dag kvar'
        except Exception:
            return dt_str[:16].replace('T', ' kl ')

    return app


app = create_app()
