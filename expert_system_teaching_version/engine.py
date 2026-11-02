from dataclasses import dataclass
from typing import List, Set, Dict, Any

@dataclass
class Rule:
    antecedents: List[str]
    consequent: str
    priority: int = 0
    name: str = ""

class ForwardChainingEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.facts: Set[str] = set()
        self.trace: List[Dict[str, Any]] = []

    def assert_facts(self, initial: List[str]) -> None:
        """Store initial facts into the working memory."""
        self.facts.update(initial)

    def can_fire(self, rule: Rule) -> bool:
        """ Return True if all antecedents are true and consequent not yet known."""
        has_antecedents = all(ant in self.facts for ant in rule.antecedents)
        is_new_consequent = rule.consequent not in self.facts
        return has_antecedents and is_new_consequent

    def run(self) -> None:
        """TODO: Implement the forward chaining loop."""
        while True:
            eligible_rules = [rule for rule in self.rules if self.can_fire(rule)]

            if not eligible_rules:
                break

            eligible_rules.sort(key=lambda r: r.priority, reverse = True)
            selected_rule = eligible_rules[0]

            self.facts.add(selected_rule.consequent)

            self.trace.append({
                "rule_fired": selected_rule.name,
                "fact_added": selected_rule.consequent
            })

    def conclusions(self) -> Dict[str, List[str]]:
        """TODO: Return separated results (recommendations, specs, other facts)."""
        recommendations = [f.split("recommend:")[1] for f in self.facts if f.startswith("recommend:")]
        other_facts = [f for f in self.facts if not f.startswith("recommend:")]

        return {
            "recommendations": recommendations,
            "all_facts": other_facts,
            "trace": self.trace
        }
