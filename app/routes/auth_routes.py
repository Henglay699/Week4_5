from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from flask_login import login_user, login_required, logout_user
from app.models.user import User
from app.models.role import Role
from app.services.user_service import UserService

auth_bp = Blueprint("auth",__name__, url_prefix="/auth")

@auth_bp.route("/login", methods =["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash("Your account is inactive. Please contact administrator", "warning")
                return redirect(url_for("auth.login"))
            
            login_user(user)
            if user.has_role("Admin"):
                flash("Logged in Successgfully.","success")
                return redirect(url_for("dashboard.index"))
            elif user.has_role("Expert"):
                flash("Logged in Successgfully.","success")
                return redirect(url_for("rules.index"))
            else: 
                flash("Logged in Successgfully.","success")
                return redirect(url_for("diagnosis.diagnose"))
        
        flash("Invalid username or password", "danger")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method =="POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        errors: list[str] = []
        if not username:
            errors.append("Username is required.")
        if not email:
            errors.append("Email is required.")
        if not full_name:
            errors.append("Full name is required.")
        if not password:
            errors.append("Password is required.")
        if password and confirm_password != password:
            errors.append("Password password do not match.")
        if username and User.query.filter_by(username=username).first():
            errors.append("This username is already registerd.")
        if email and User.query.filter_by(email=email).first():
            errors.append("This username is already registerd.")

        if errors:
                for msg in errors:
                    flash(msg, "danger")

                return render_template(
                    "auth/register.html",
                    username = username,
                    email = email,
                    full_name = full_name
                    )
        default_role = Role.query.filter_by(name="User").first()
        default_role_id = default_role.id if default_role else None

        data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "is_active": True
        }

        new_user = UserService.create(
            data= data,
            password=password,
            role_id=default_role_id
        )

        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))