from typing import Optional, List
from app.models.fact import Fact
from extensions import db

class FactService:
    
    @staticmethod
    def get_fact_all() -> List[Fact]:
        return Fact.query.order_by(Fact.id.asc()).all()
    
    @staticmethod
    def get_fact_by_id(rule_id: int) -> Optional[Fact]:
        return Fact.query.get(rule_id)
    
    @staticmethod
    def create_fact(data: dict) -> Fact:
        fact = Fact()
        fact.name = data["name"] or ""
             
        db.session.add(fact)
        db.session.commit()
        return fact
    
    @staticmethod
    def update_fact(fact: Fact, data: dict) -> Fact:
        fact.name = data["name"] or ""
        
        db.session.add(fact)
        db.session.commit()
        return fact
    
    @staticmethod
    def delete_confirm_fact(fact: Fact) -> None:
        db.session.delete(fact)
        db.session.commit()
        
    