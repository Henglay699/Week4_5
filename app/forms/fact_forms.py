from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Fact
from extensions import db


class FactCreateForm(FlaskForm):
    
    name = StringField(
        "Symptom",
        validators=[DataRequired(), Length(min=2, max=255)],
        render_kw={"placeholder": "Enter new fact"},
    )
    
    submit = SubmitField("Save Fact")
    
    
    def validate_name(self, field):
        exist = db.session.scalars(
            db.select(Fact).filter(Fact.name == field.data)
        ).first()
        
        if exist:
            raise ValidationError("This fact is already entered")
        
class FactEditForm(FlaskForm):
    
    name = StringField(
        "Symptom",
        validators=[DataRequired(), Length(min=2, max=255)],
        render_kw={"placeholder": "Enter new fact"},
    )
    
    submit = SubmitField("Update Fact")
    
    def __init__(self, original_fact:Fact, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_fact = original_fact
        
        
    def validate_name(self, field):
        exist = db.session.scalars(
            db.select(Fact).filter(Fact.name == field.data, Fact.id != self.original_fact.id)
        ).first()
        
        if exist:
            raise ValidationError("This fact is already entered")
        
class FactDeleteConfirm(FlaskForm):
    submit = SubmitField("Delete")