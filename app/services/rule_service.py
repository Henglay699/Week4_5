from typing import Optional, List
from app.models import Rule, Fact
from extensions import db

class RuleService:
    
    @staticmethod
    def get_rule_all(search_query: str, page: int, per_page: int = 10):
        query = Rule.query.order_by(Rule.id.asc())
        if search_query:
            query = query.filter(Rule.title.contains(search_query) | Rule.rule_id.contains(search_query))
        return query.paginate(page=page, per_page=per_page)
    
    @staticmethod
    def count_rules() -> int:
        return Rule.query.count()
    
    @staticmethod
    def get_rule_by_id(rule_id: int) -> Optional[Rule]:
        return Rule.query.get(rule_id)
    
    @staticmethod
    def create_rule(data: dict, fact_ids: List[int], user_id: int) -> Rule:
        rule = Rule()
        rule.rule_id = data["rule_id"]
        rule.title =  data["title"]
        rule.description = data.get("description")  or ""
        rule.category = data.get("category", "Hardware")
        rule.user_id = user_id
        rule.solution = data["solution"]
        rule.confidence = data["confidence"]
        
        if fact_ids:
            facts = db.session.scalars(
                db.select(Fact).filter(
                    Fact.id.in_(fact_ids)
                )
            ).all()
            
        rule.facts = facts # type: ignore
        
        db.session.add(rule)
        db.session.commit()
        return rule
    
    @staticmethod
    def update_rule(rule: Rule, data: dict, fact_ids: List[int], user_id: int) -> Rule:
        rule.user_id = user_id
        rule.rule_id = data["rule_id"]
        rule.title = data["title"]
        rule.description = data.get("description") or ""
        rule.category = data.get("category", "Hardware")
        rule.solution = data["solution"]
        rule.confidence = data["confidence"]
        
        facts = []
        
        if fact_ids:
            facts = db.session.scalars(
                db.select(Fact).filter(Fact.id.in_(fact_ids))
            ).all()
            
        rule.facts = facts # type: ignore
            
        db.session.add(rule)
        db.session.commit()
        return rule
    
    @staticmethod
    def delete_confirm_rule(rule: Rule) -> None:
        db.session.delete(rule)
        db.session.commit()