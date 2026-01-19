from flask import flash
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, widgets 
from wtforms.validators import ValidationError
from app.models import Fact
from extensions import db

def fact_validator(form, field):
    if not field.data:
        flash("please select a problem", "danger")

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class DiagnosisForm(FlaskForm):
    fact_ids = MultiCheckboxField("Symptoms/Facts", coerce=int, validators=[fact_validator] )
    submit = SubmitField("Run Diagnosis")

    def __init__(self, *args, **kwargs):
        super(DiagnosisForm, self).__init__(*args, **kwargs)
        self.fact_ids.choices = [
            (f.id, f.name) for f in db.session.scalars(db.select(Fact).order_by(Fact.name)).all()
        ]