#!/usr/bin/env python3
"""TD 2 and TD 3: read the decisions of a routing rule, then adapt it to your own.

No API call, no key.

DIA3-G5 adaptation (TD 2, pair C): the resources are the five TD 1 models on their free
routes plus the billed route of gpt-oss-120b, read from routing/routing-rule.json. A
resource is eligible for a question family when the rule lists its model for that family;
the rule lists only models whose TD 1 rate justifies it (routing/family-rates-td1.json),
and every decision carries those TD 1 cells in its reason. Costs are USD excluding tax per
request (billed price x median TD 1 tokens). Quota availability is supplied as a scenario,
not measured from a provider.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULE = json.loads((ROOT / "routing" / "routing-rule.json").read_text(encoding="utf-8"))
RATES = json.loads((ROOT / "routing" / "family-rates-td1.json").read_text(encoding="utf-8"))
RESOURCES = RULE["resources"]


def evidence(family, model):
    rate = RATES["rates"][f"{family}|{model}"]
    cases = ", ".join(RATES["families"][family]["cases"])
    wrong = f", fails {', '.join(rate['wrong'])}" if rate["wrong"] else ""
    return f"{model} {rate['correct']}/{rate['cases']} on {family} ({cases}{wrong}) in TD1"


def evidence_model(resource):
    return resource.get("evidence_model", resource["model"])


def choose(request, resources):
    """A deterministic routing policy, with a reason the user can inspect.

    Already paid capacity is preferred before new spending. A nonurgent request
    can wait for included capacity. At wake-up, availability must be measured
    again: reaching a reset time does not prove that capacity is available.
    Among included resources, the rule order wins: the cheapest model that TD 1
    shows correct on the family comes first.
    """
    family = RULE["families"].get(request["family"])
    if family is None:
        return {"action": "abstain", "resource": None, "cash": 0, "checks": "none possible",
                "reason": f"no TD1 evidence for family {request['family']}: no model is eligible"}
    order = family["order"]
    rank = {model: i for i, model in enumerate(order)}
    eligible = [r for r in resources if evidence_model(r) in rank]
    checks = family["checks"][request["use"]]

    def reason(prefix, chosen):
        model = evidence_model(chosen)
        return f"{prefix}; rule order #{rank[model] + 1} for {request['family']}: {evidence(request['family'], model)}"

    included = [r for r in eligible if r["available"] and r["cash"] == 0]
    if included:
        chosen = min(included, key=lambda r: (rank[evidence_model(r)], r["allocation"], r["id"]))
        return {"action": "run", "resource": chosen["id"], "cash": 0, "checks": checks,
                "reason": reason("eligible included capacity", chosen)}
    waiting = [r for r in eligible if not r["available"] and r["cash"] == 0
               and r["reset_minutes"] is not None
               and 0 < r["reset_minutes"] <= request["deadline_minutes"]]
    if waiting and request["can_wait"]:
        chosen = min(waiting, key=lambda r: (r["reset_minutes"], rank[evidence_model(r)]))
        return {"action": "defer", "resource": chosen["id"], "cash": 0, "checks": checks,
                "reason": reason("free quota refills before the deadline, recheck availability at wake-up", chosen),
                "wake_in_minutes": chosen["reset_minutes"]}
    paid = [r for r in eligible if r["available"] and r["cash"] <= request["budget"]]
    if paid:
        chosen = min(paid, key=lambda r: (r["cash"], rank[evidence_model(r)], r["id"]))
        return {"action": "run", "resource": chosen["id"], "cash": chosen["cash"], "checks": checks,
                "reason": reason("available billed route within the authorised budget", chosen)}
    return {"action": "abstain", "resource": None, "cash": 0, "checks": checks,
            "reason": f"no eligible resource for {request['family']} within deadline and budget; eligible models: {', '.join(order)}"}


def with_state(resources, provider, **changes):
    return [dict(r, **changes) if r["model"].startswith(provider + ":") and r["access"] == "free" else dict(r)
            for r in resources]


def scenarios():
    base = {"family": "F1", "use": "dashboard", "can_wait": True, "deadline_minutes": 120, "budget": 0.01}
    groq_rate_limited = with_state(RESOURCES, "groq", available=False, reset_minutes=1)
    groq_down = with_state(RESOURCES, "groq", available=False, reset_minutes=None)
    return [
        ("simple", base, RESOURCES),
        ("complex", {**base, "family": "F2", "use": "customer"}, RESOURCES),
        ("provider unavailable", base, groq_down),
        ("deferrable", {**base, "family": "F2", "use": "customer"}, groq_rate_limited),
        ("urgent", {**base, "family": "F2", "use": "customer", "can_wait": False, "deadline_minutes": 0.5}, groq_rate_limited),
        ("budget exhausted", {**base, "family": "F2", "use": "customer", "can_wait": False, "budget": 0}, groq_rate_limited),
        ("high impact", {**base, "family": "F4", "use": "payout"}, RESOURCES),
        ("age at the order", {**base, "family": "F2b"}, RESOURCES),
        ("unknown capability", {**base, "family": "F5"}, RESOURCES),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", help="show only the named scenario")
    args = parser.parse_args()
    found = False
    for name, request, resources in scenarios():
        if args.scenario and name != args.scenario:
            continue
        found = True
        print(json.dumps({"scenario": name, "nature": "simulation", "request": request,
                          "result": choose(request, resources)}, ensure_ascii=False))
    if not found:
        parser.error("unknown scenario")


if __name__ == "__main__":
    main()
