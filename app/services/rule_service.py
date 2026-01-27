from typing import Optional, List
from app.models import Rule, Fact
from extensions import db

class RuleService:
    
    @staticmethod
    def get_rule_all() -> List[Rule]:
        return Rule.query.order_by(Rule.id.asc()).all()
    
    @staticmethod
    def count_rules() -> int:
        return Rule.query.count()
    
    @staticmethod
    def get_rule_by_id(rule_id: int) -> Optional[Rule]:
        return Rule.query.get(rule_id)
    
    @staticmethod
    def create_rule(data: dict, fact_ids: List[int]) -> Rule:
        rule = Rule()
        rule.rule_id = data["rule_id"]
        rule.title =  data["title"]
        rule.description = data.get("description")  or ""
        rule.category = data.get("category", "Hardware")
        rule.solution = data["solution"]
        rule.confidence = data["confidence"]
        
        if fact_ids:
            facts = db.session.scalars(
                db.select(Fact).filter(
                    Fact.id.in_(fact_ids)
                )
            ).all()
            
        rule.facts = [facts] # type: ignore
        
        db.session.add(rule)
        db.session.commit()
        return rule
    
    @staticmethod
    def update_rule(rule: Rule, data: dict, fact_ids: List[int]) -> Rule:
        
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