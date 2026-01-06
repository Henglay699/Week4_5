from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FloatField
from app.forms.multi_checkbox_field import Multi_Checkbox_Field
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired
from collections import defaultdict
from app.models import Rule, Fact
from extensions import db

    
def at_least_one_fact(form, field):
    if not field.data:
        raise ValidationError("Choose at least one fact")

CATEGORIES = [
    ("Hardware", "Hardware"),
    ("Software", "Software"),
    ("Performance", "Performance"),
    ("Network", "Network")
]

def _fact_choices():
    return [
        (f.id, f"{f.name}") 
        for f in db.session.scalars(
            db.select(Fact).order_by(Fact.id)
        )
    ]

class RuleCreateForm(FlaskForm):
    
    rule_id = StringField(
        "Rule Code",
        validators=[DataRequired(), Length(min=7, max=20)],
        render_kw={"placeholder": "E.G RULE001"},
    )
    
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=255)],
        render_kw={"placeholder": "E.G Internet Connection Issues"}
    )
    
    description = TextAreaField(
        "Description",
        render_kw= {"placeholder": "Short description (optional)"}
    )
    
    category = SelectField(
        "Category",
        choices=CATEGORIES,
        validators=[DataRequired()],
        default="Hardware"
    )
    
    fact_ids = Multi_Checkbox_Field(
        "Fact",
        coerce=int,
        validators=[at_least_one_fact],
        render_kw={"placeholder": "Facts for this rule"},
    )
    
    solution = TextAreaField(
        "Solution",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter troubleshooting steps, one per line"}
    )
    
    confidence = FloatField(
        "Confidence Percentage",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter confidence in percentage E.G (0.85)"}
    )
    
    submit = SubmitField("Save Rule")
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fact_ids.choices = list(_fact_choices())      
            
    
    def validate_rule_id(self, field):       
        exist = db.session.scalars(
            db.select(Rule).filter(
                Rule.rule_id == field.data,          
            )
        ).first()
        
        if exist:
            raise ValidationError("This rule code had already been used")
        
    def validate_title(self, field):        
        q = db.select(Rule).filter(Rule.title == field.data)
        exist = db.session.scalars(q).first()
        if exist:
            raise ValidationError("This title had already been used")
        
        
class RuleEditForm(FlaskForm):
    
    rule_id = StringField(
        "Rule Code",
        validators=[DataRequired(), Length(min=7, max=20)],
        render_kw={"placeholder": "E.G RULE001"},
    )
    
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=255)],
        render_kw={"placeholder": "E.G Internet Connection Issues"}
    )
    
    description = TextAreaField(
        "Description",
        render_kw= {"placeholder": "Short description (optional)"}
    )
    
    category = SelectField(
        "Category",
        choices=CATEGORIES,
        validators=[DataRequired()],
        default="Hardware"
    )
    
    fact_ids = Multi_Checkbox_Field(
        "Fact",
        coerce=int,
        validators=[at_least_one_fact],
        render_kw={"placeholder": "Facts for this rule"}
    )
    
    solution = TextAreaField(
        "Solution",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter troubleshooting steps, one per line"}
    )
    
    confidence = FloatField(
        "Confidence Percentage",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter confidence in percentage E.G (0.85)"}
    )
    
    submit = SubmitField("Update Rule")
    
    def __init__(self, original_rule:Rule, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_rule = original_rule
        self.fact_ids.choices = list(_fact_choices())      
        if not self.is_submitted():
            self.fact_ids.data = [f.id for f in original_rule.facts]
    
    def validate_rule_id(self, field):       
        exist = db.session.scalars(
            db.select(Rule).filter(
                Rule.rule_id == field.data,
                Rule.id != self.original_rule.id          
            )
        ).first()
        
        if exist:
            raise ValidationError("This rule code had already been used")
        
    def validate_title(self, field):        
        q = db.select(Rule).filter(
            Rule.title == field.data, Rule.id != self.original_rule.id)
        
        exist = db.session.scalars(q).first()
        if exist:
            raise ValidationError("This title had already been used")
        
class RuleDeleteConfirm(FlaskForm):
    submit = SubmitField("Delete")