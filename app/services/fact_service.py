from typing import Optional, List
from app.models.fact import Fact
from extensions import db

class FactService:
    
    @staticmethod
    def get_fact_all(search_query: str, page: int, per_page: int = 10) :
        query = Fact.query.order_by(Fact.id.asc())
        if search_query:
            query = query.filter(Fact.name.ilike(f"%{search_query}%"))
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def count_facts() -> int:
        return Fact.query.count()
    
    @staticmethod
    def get_fact_by_id(rule_id: int) -> Optional[Fact]:
        return Fact.query.get(rule_id)
    
    @staticmethod
    def create_fact(data: dict, user_id: int) -> Fact:
        fact = Fact()
        fact.name = data["name"] or ""
        fact.user_id = user_id
             
        db.session.add(fact)
        db.session.commit()
        return fact
    
    @staticmethod
    def update_fact(fact: Fact, data: dict, user_id: int) -> Fact:
        fact.name = data["name"] or ""
        fact.user_id = user_id
        
        db.session.add(fact)
        db.session.commit()
        return fact
    
    @staticmethod
    def delete_confirm_fact(fact: Fact) -> None:
        db.session.delete(fact)
        db.session.commit()
        
    