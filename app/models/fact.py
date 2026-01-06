from extensions import db
from datetime import datetime
from app.models.associations import rule_facts

class Fact(db.Model):
    __tablename__="facts"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    rules = db.relationship("Rule", secondary=rule_facts, back_populates="facts")
    
    def  __repr__(self) -> str:
        return f"<Fact {self.name}>"