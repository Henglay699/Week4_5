from collections import defaultdict
from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import Permission, Role
from extensions import db
from app.forms.multi_checkbox_field import Multi_Checkbox_Field


def _permission_choices():
    return [
        (perm.id, f"{perm.code} - {perm.name}")
        for perm in db.session.scalars(
            db.select(Permission).order_by(Permission.code)
        )
    ]

def _permissions_grouped_by_module():
    perms = list(
        db.session.scalars(
            db.select(Permission).order_by(
                Permission.module, Permission.code
            )
        )
    )
    
    grouped = defaultdict(list)
    for perm in perms:
        module = perm.module or "General"
        grouped[module].append(perm)

    return dict(grouped)

class RoleCreateForm(FlaskForm):
    name = StringField(
        "Name",
        validators = [DataRequired(), Length(min=2, max=80)],
        render_kw={"placeholder": "Role Name"}
    )

    description = TextAreaField(
        "Description",
        render_kw= {"placeholder": "Short description (optional)"}
    )

    permission_ids = Multi_Checkbox_Field(
        "Permission",
        coerce=int,
        render_kw= {"placeholder": "Permission granted for this role"}
    )

    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_ids.choices = list(_permission_choices())
        self.permissions_by_module = _permissions_grouped_by_module()

    def validate_name(self, field):
        exist = db.session.scalars(
            db.select(Role).filter(Role.name == field.data)
        ).first()
        
        if exist:
            raise ValidationError("This role name has already been created.")
        
class RoleEditForm(FlaskForm):
    name = StringField(
        "Name",
        validators = [DataRequired(), Length(min=2, max=80)],
    )

    description = TextAreaField("Description")

    permission_ids = Multi_Checkbox_Field(
        "Permission",
        coerce=int,
    )

    submit = SubmitField("Update")

    def __init__(self, original_role:Role, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.original_role = original_role 
       self.permission_ids.choices = list(_permission_choices())
       self.permissions_by_module = _permissions_grouped_by_module()

       if not self.is_submitted():
            self.permission_ids.data = [p.id for p in original_role.permissions]

    def validate_name(self, field):
        q = db.select(Role).filter(
            Role.name == field.data,
            Role.id != self.original_role.id
        )

        exist = db.session.scalars(q).first()
        if exist:
            raise ValidationError("This role name has already been created.")
        
class RoleConfirmDeleteForm(FlaskForm):
    submit = SubmitField("Confirm Delete")