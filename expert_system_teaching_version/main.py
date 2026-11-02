from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = "kb/laptop_rules.json"


def collect_initial_facts():
    facts = []
    # TODO: Ask more questions to collect facts for reasoning
    if input("Is portability important? (y/n): ").lower().startswith("y"):
        facts.append("portable")
    if input("Do you need long battery life? (y/n): ").lower().startswith("y"):
        facts.append("long_battery")

    if input("Is your budget high? (y/n): ").lower().startswith("y"):
        facts.append("budget_high")
    else:
        facts.append("budget_low")

    if input("Is gaming a priority? (y/n): ").lower().startswith("y"):
        facts.append("gaming")
    if input("Do you edit videos? (y/n): ").lower().startswith("y"):
        facts.append("video_editing")
    if input("Do you do any programming? (y/n): ").lower().startswith("y"):
        facts.append("programming")
    if input("Is this for basic, everyday taks(ie. not a heavy workload)? (y/n): ").lower().startswith("y"):
        facts.append("light_processing")
    return facts


def main():
    # TODO: Load rules, create engine, assert facts, and run inference
    rules = load_rules(KB_PATH)
    engine = ForwardChainingEngine(rules)

    initial_facts = collect_initial_facts()
    engine.assert_facts(initial_facts)

    engine.run()

    results = engine.conclusions()
    print("\n" + "="*30)

    if results["recommendations"]:
        for rec in results["recommendations"]:
            print(f"=> Recommendation: {rec}")
    else:
        print("=> Recommendation: No matches found.")

    if results["trace"]:
        last_rule = results["trace"][-1]["rule_fired"]
        print(f"=> Explanation: derived from rule '{last_rule}")
        print("\n --Inference Trace--")
        for step in results["trace"]:
            print(f"Rule '{step['rule_fired']}' fired -> added '{step['fact_added']}'")

if __name__ == "__main__":
    main()
