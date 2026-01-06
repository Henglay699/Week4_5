from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Permission
from extensions import db

MODULE_CHOICES = [
    ("Users", "Users"),
    ("Roles", "Roles"),
    ("Permissions", "Permissions"),
    ("System", "System"),
    ("Audit", "Audit"),
    ("General", "General"),
    ("Rule", "Rule"),
    ("Fact", "Fact"),
] 

class PermissionCreateForm(FlaskForm):
    code = StringField(
        "Code",
        validators=[DataRequired(), Length(min=2, max=64)],
        render_kw={"placeholder": "eg user.view"},
    )

    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=2, max=120)],
        render_kw={"placeholder": "Human-readable name"},
    )

    module = SelectField(
        "Module",
        choices=MODULE_CHOICES,
        default="General"
    )

    description = TextAreaField(
        "Description",
        render_kw={"placeholder": "What does this permission allow?"}
    )

    submit = SubmitField("Save")


    def validate_code(self, field):
        exist = db.session.scalars(
            db.select(Permission).filter(
            Permission.code == field.data)
        ).first()

        if exist:
            raise ValidationError("This code is already in use.")
        
    def validate_name(self, field):
        exist = db.session.scalars(
            db.select(Permission).filter(
                Permission.name == field.data)
        ).first()
        
        if exist:
            raise ValidationError("This name is already in use.")
        

class PermissionEditForm(FlaskForm):
    code = StringField(
        "Code",
        validators=[DataRequired(), Length(min=2, max=64)],
    )
    name =  name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=2, max=120)],
    )
    module = SelectField(
        "Module",
        choices=MODULE_CHOICES,
        default="General"
    )
    description = TextAreaField(
        "Description",
        render_kw={"placeholder": "What does this permission allow?"}
    )

    submit = SubmitField("Update")


    def __init__(self, original_permission:Permission, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_permission = original_permission
        if not self.is_submitted():
            self.module.data = original_permission.module

    def validate_code(self, field):
        exist = db.session.scalars(
            db.select(Permission).filter(
                Permission.code == field.data,
                Permission.id != self.original_permission.id)
        ).first()
        
        if exist:
            raise ValidationError("This code is already in use.")
        
    def validate_name(self, field):
        exist = db.session.scalars(
            db.select(Permission).filter(
                Permission.name == field.data,
                Permission.id != self.original_permission.id)
        ).first()
        
        if exist:
            raise ValidationError("This name is already in use.")
        
class PermissionConfirmDeleteForm(FlaskForm):
    submit = SubmitField("Confirm Delete")