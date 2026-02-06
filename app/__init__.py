from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, logout_user, current_user
from app.decorator_method import role_required, permission_required
from config import Config
from extensions import db, csrf, login_manager, migrate
from app.models.user import User

def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login" # type: ignore
    login_manager.login_message = "Please login to access this page."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.role_routes import role_bp
    from app.routes.permission_routes import permission_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.fact_routes import fact_bp
    from app.routes.rule_routes import rule_bp
    from app.routes.diagnosis_routes import diag_bp
    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(permission_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(fact_bp)
    app.register_blueprint(rule_bp)
    app.register_blueprint(diag_bp)
    app.register_blueprint(dashboard_bp)


    @app.route("/")
    def home():
        if current_user.is_authenticated:
            if current_user.has_role("Admin"):
                return redirect(url_for("dashboard.index"))

            elif current_user.has_role("Expert"):
                return redirect(url_for("facts.index"))

            else:  return redirect(url_for("diagnosis.diagnose"))
        else:
            return redirect(url_for("diagnosis.diagnose"))
              
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("auth/unauthorized.html")

    # Create tables
    with app.app_context():
        from app.models import User, Role, Permission, Rule, Fact
        db.create_all()

    return app
