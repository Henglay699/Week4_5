from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, widgets
from app.models import Fact
from extensions import db

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class DiagnosisForm(FlaskForm):
    fact_ids = MultiCheckboxField("Symptoms/Facts", coerce=int)
    submit = SubmitField("Run Diagnosis")

    def __init__(self, *args, **kwargs):
        super(DiagnosisForm, self).__init__(*args, **kwargs)
        # Load all available facts from the database as choices
        self.fact_ids.choices = [
            (f.id, f.name) for f in db.session.scalars(db.select(Fact).order_by(Fact.name)).all()
        ]