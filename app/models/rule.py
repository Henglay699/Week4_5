
from extensions import db
from datetime import datetime
from app.models.associations import rule_facts

class Rule(db.Model):
    __tablename__= "rules"
    
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    category = db.Column(db.String(80), nullable=False)
    solution = db.Column(db.Text, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    
    facts = db.relationship("Fact", secondary=rule_facts, back_populates="rules")
    user  = db.relationship("User", back_populates="rules")
    
    def __repr__(self) -> str:
        return f"<Rule {self.rule_id}>"
     