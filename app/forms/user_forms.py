import re
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from app.models import User
from app.models import Role
from extensions import db

# ----- helpers -----

def strong_password(form, field):
    """Require: min 8 chars, upper, lower, digit, special."""
    password = field.data or ""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one digit.")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", password):
        raise ValidationError("Password must contain at least one special character.")


def _role_choices():
    return [(role.id, role.name) for role in db.session.scalars(
        db.select(Role).order_by(Role.name)
    )]

class UserCreateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"placeholder": "Enter username"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
        render_kw={"placeholder": "Enter email"},
    )
    full_name = StringField(
        "Full name",
        validators=[DataRequired(), Length(min=3, max=120)],
        render_kw={"placeholder": "Enter full name"},
    )
    is_active = BooleanField("Active", default=True)
 
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            strong_password,
        ],
        render_kw={"placeholder": "Strong password"},
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "Confirm password"},
    )
    role_id = SelectField(
        "Role",
        coerce = int,
        validators = [DataRequired()],
        render_kw= {"Placeholer":  "Select role"}
    )

    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_id.choices = _role_choices()

# ---- server-side uniqueness checks ----

    def validate_username(self, field):
        exists = db.session.scalar(
            db.select(User).filter(User.username == field.data)
        )
        if exists:
            raise ValidationError("This username is already taken.")

    def validate_email(self, field):
        exists = db.session.scalar(
            db.select(User).filter(User.email == field.data)
        )
        if exists:
            raise ValidationError("This email is already registered.")


class UserEditForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"placeholder": "Enter username"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
        render_kw={"placeholder": "Enter email"},
    )
    full_name = StringField(
        "Full name",
        validators=[DataRequired(), Length(min=3, max=120)],
        render_kw={"placeholder": "Enter full name"},
    )
    is_active = BooleanField("Active")

    password = PasswordField(
        "New password (leave blank to keep current)",
        validators=[Optional(), strong_password],
        render_kw={"placeholder": "New strong password (optional)"},
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[EqualTo("password", message="Passwords must match.")],
    )
    role_id = SelectField(
        "Role",
        coerce=int,
        validators=[DataRequired()],
        render_kw= {"Placeholer":  "Select role"} 
    )

    submit = SubmitField("Update")

    def __init__(self, original_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_user = original_user
        self.role_id.choices = _role_choices()

        if not self.is_submitted():
            if original_user.roles:
                self.role_id.data = original_user.roles[0].id
            else:
                self.role_id.data = None


    def validate_username(self, field):
        q = db.select(User).filter(User.username == field.data, User.id != self.original_user.id)
        exists = db.session.scalar(q)
        if exists:
            raise ValidationError("This username is already taken.")
        

    def validate_email(self, field):
        q = db.select(User).filter(User.email == field.data, User.id != self.original_user.id)
        exists = db.session.scalar(q)
        if exists:
            raise ValidationError("This email is already registered.")
        
        
    def validate_password(self, field):
        if field.data:
            strong_password(self, field)

class UserConfirmDeleteForm(FlaskForm):
    submit = SubmitField("Confirm Delete")


