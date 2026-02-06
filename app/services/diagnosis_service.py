from typing import List, Dict
from app.models import Rule, Fact

class DiagnosisService:
    @staticmethod
    def perform_diagnosis(selected_fact_ids: List[int]) -> List[Dict]:
        all_rules = Rule.query.all()
        results = []
        user_fact_set = set(selected_fact_ids)

        for rule in all_rules:
            rule_fact_ids = {f.id for f in rule.facts}
            if not rule_fact_ids:
                continue
            
            # Find the intersection (facts in rule AND selected by user)
            matched_facts = rule_fact_ids.intersection(user_fact_set)
            
            if matched_facts:
                match_count = len(matched_facts)
                total_required = len(rule_fact_ids)
                
                # Confidence = (Rule's base certainty) * (% of symptoms matched)
                match_ratio = match_count / total_required
                adjusted_confidence = rule.confidence * match_ratio

                results.append({
                    "rule": rule,
                    "base_confidence": rule.confidence * 100,
                    "adjusted_confidence": adjusted_confidence * 100,
                    "match_count": match_count,
                    "total_required": total_required,
                    "matched_fact_names": [f.name for f in rule.facts if f.id in user_fact_set]
                })

        # Sort results: Highest adjusted confidence first
        return sorted(results, key=lambda x: x['adjusted_confidence'], reverse=True)