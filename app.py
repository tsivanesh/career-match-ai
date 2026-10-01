import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, session
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.jobs import jobs_bp
    from routes.recommendations import recommendations_bp
    from routes.dashboard import dashboard_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)

    # Landing page route
    from flask import Blueprint
    main_bp = Blueprint('main', __name__)

    @main_bp.route('/')
    def index():
        from database.database import query_db
        total_jobs = query_db("SELECT COUNT(*) as c FROM jobs WHERE is_active=1", one=True)
        total_skills = query_db("SELECT COUNT(*) as c FROM skills", one=True)
        return render_template('index.html',
                               total_jobs=total_jobs['c'] if total_jobs else 0,
                               total_skills=total_skills['c'] if total_skills else 0)

    app.register_blueprint(main_bp)

    # Template filters
    @app.template_filter('format_salary')
    def format_salary(value):
        if not value:
            return 'Not disclosed'
        try:
            v = int(value)
            if v >= 100000:
                return f'₹{v//100000}L'
            return f'₹{v:,}'
        except:
            return str(value)

    @app.template_filter('score_color')
    def score_color(score):
        try:
            s = float(score)
            if s >= 80: return 'success'
            if s >= 60: return 'warning'
            return 'danger'
        except:
            return 'secondary'

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    return app


if __name__ == '__main__':
    # Auto-initialize database on first run
    from database.database import init_db
    import sqlite3
    import os as _os
    db_path = Config.DATABASE_PATH
    need_seed = not _os.path.exists(db_path)
    init_db()
    if need_seed:
        print("[*] First run detected - seeding database with demo data...")
        from database.seed_data import seed_database
        seed_database()

    app = create_app()
    print("\n" + "="*55)
    print("  [>] CareerMatch AI - Running!")
    print("="*55)
    port = int(os.environ.get('PORT', 5000))
    print(f"  URL:   http://127.0.0.1:{port}/")
    print(f"  Demo:  http://127.0.0.1:{port}/demo-login")
    print(f"  Admin: http://127.0.0.1:{port}/admin-demo-login")
    print("="*55 + "\n")
    app.run(debug=Config.DEBUG, use_reloader=False, host='127.0.0.1', port=port)
