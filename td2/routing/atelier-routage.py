#!/usr/bin/env python3
"""TD 2 step 3 (pair C, DIA3-G5): the kit's atelier-routage.py adapted to our TD 1 portfolio.

Adapted copy of kit-td1/atelier-routage.py (the kit file stays byte-identical, see its manifest;
the "before" output is produced by the kit file). No API call, no key.

Routing follows the four factors of the TD 2 lecture, in this order:
  difficulty -> minimum level L1/L2/L3 (filter), stakes -> required check,
  deadline -> wait for a free resource or pay now, budget -> which paid resources are allowed;
then "filter then cheapest".
RESOURCES are the five TD 1 models on their free routes, the billed route of gpt-oss-120b and the
L3 quorum panel (no single model is correct on every L3 cell in TD 1). A resource's level is the
highest difficulty on which it was correct on every TD 1 cell (td2/routing/family-rates-td1.json); the
panel's level comes from its replay on the TD 1 traces (td2/routing/quorum-check-td1.json). Every
reason string cites those TD 1 cells. Costs are USD excluding tax per request (dated billed price x
median TD 1 tokens). Quota availability is supplied as a scenario, not measured from a provider.
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RATES = json.loads((HERE / "family-rates-td1.json").read_text(encoding="utf-8"))
RULE = json.loads((HERE / "routing-rule.json").read_text(encoding="utf-8"))
PANELS = json.loads((HERE / "quorum-check-td1.json").read_text(encoding="utf-8"))
MAX_ATTEMPTS = RULE["retry"]["max_attempts"]
INTERVAL = RULE["retry"]["interval_minutes"]


def cells_up_to(level):
    return [c for lv in range(1, level + 1) for c in RATES["level_cells"][str(lv)]]


def build_resources():
    resources = []
    for model, info in RATES["models"].items():
        resources.append({"id": model.replace(":free", "") + " (free)", "model": model, "provider": model.split(":")[0],
                          "level": info["level"], "access": "free", "available": True, "cash": 0.0,
                          "allocation": 0.0, "billed_equivalent": info["billed_usd_per_request"] or 0.0,
                          "calls": 1, "reset_minutes": None})
    for paid in RULE["paid_routes"]:
        info = RATES["models"][paid["evidence_model"]]
        resources.append({"id": paid["id"], "model": paid["evidence_model"], "provider": "openrouter-billed",
                          "level": info["level"], "access": "tokens", "available": True,
                          "cash": info["billed_usd_per_request"], "allocation": 0.0,
                          "billed_equivalent": info["billed_usd_per_request"], "calls": 1, "reset_minutes": None})
    members = PANELS["L3"]["members"]
    resources.append({"id": "panel-L3 2-of-3", "members": members, "level": 3, "access": "free", "cash": 0.0,
                      "allocation": 0.0, "calls": 3,
                      "billed_equivalent": round(sum(RATES["models"][m]["billed_usd_per_request"] or 0 for m in members), 6)})
    return resources


RESOURCES = build_resources()


def resolve(resources):
    """A panel is available only when its three members are; it waits for the slowest member."""
    by_model = {r["model"]: r for r in resources if r.get("access") == "free" and "model" in r}
    out = []
    for r in resources:
        if "members" in r:
            states = [by_model[m] for m in r["members"]]
            available = all(s["available"] for s in states)
            resets = [s["reset_minutes"] for s in states if not s["available"]]
            reset = None if available or None in resets else max(resets)
            r = dict(r, available=available, reset_minutes=reset)
        out.append(r)
    return out


def evidence(r, difficulty):
    if "members" in r:
        by = PANELS["L3_panel_by_level"]
        per = "; ".join(f'{lv}: {v["correct"]} correct, {v["abstain"]} abstain, {v["wrong"]} wrong'
                        + (f' ({", ".join(v["not_correct"])})' if v["not_correct"] else "") for lv, v in by.items())
        return (f'panel {", ".join(m.split("/")[-1] for m in r["members"])} replayed on the 20 TD1 cells, '
                f'never wrong, abstains instead: {per}')
    cells = cells_up_to(r["level"])
    span = "L1" if r["level"] == 1 else f'L1-L{r["level"]}'
    return f'{r["model"]} level L{r["level"]}: correct on all {len(cells)} TD1 cells of {span} ({", ".join(cells)})'


def required_check(request, r):
    """Stakes -> check. Deterministic checks are done by code, not by a model."""
    d, stakes = request["difficulty"], request["stakes"]
    base = "SQL returned with the value and value normalised by code before any vote"
    if stakes == "dashboard":
        if "members" in r:
            return f"{base}; the 2-of-3 vote of the panel itself, abstain without majority"
        return f"{base}; none beyond that: single model correct on every TD1 cell up to L{d}"
    if stakes == "customer":
        panel = RULE["panels"][f"L{d}"]["members"]
        q = PANELS[f"L{d}"]
        text = (f'{base}; 2-of-3 quorum of panel L{d} ({", ".join(m.split("/")[-1] for m in panel)}: '
                f'{q["correct"]} correct, {q["abstain"]} abstain, {q["wrong"]} wrong on TD1 L{d} cells), abstain without majority')
        if d == 3:
            text += "; plus deterministic check: reference SQL template re-run on the database and value compared"
        return text
    return (f"{base}; deterministic check: reference SQL template re-run on the database and value compared; "
            "human review if they differ; abstain until reviewed")


def choose(request, resources):
    """Filter then cheapest, with a reason the user can inspect.

    Already paid capacity is preferred before new spending. A nonurgent request
    can wait for included capacity, at most MAX_ATTEMPTS times, INTERVAL minute(s) apart.
    At wake-up, availability must be measured again: reaching a reset time does
    not prove that capacity is available.
    """
    resources = resolve(resources)
    eligible = [r for r in resources if r["level"] >= request["difficulty"]]
    if not eligible:
        return {"action": "abstain", "resource": None, "cash": 0, "checks": "none possible",
                "reason": (f'no TD1 evidence at difficulty L{request["difficulty"]}: TD1 cells stop at L3 '
                           f'({", ".join(RATES["level_cells"]["3"])}), so no resource reaches this level')}
    checks = required_check(request, eligible[0]) if request["difficulty"] <= 3 else "none possible"

    def cheapest(r):
        return (r["cash"], r["allocation"], r["billed_equivalent"], r["calls"], r["id"])

    included = [r for r in eligible if r["available"] and r["cash"] == 0]
    if included:
        chosen = min(included, key=cheapest)
        return {"action": "run", "resource": chosen["id"], "cash": 0, "calls": chosen["calls"],
                "checks": required_check(request, chosen),
                "reason": f"cheapest eligible included capacity; {evidence(chosen, request['difficulty'])}"}
    waiting = [r for r in eligible if not r["available"] and r["cash"] == 0
               and r["reset_minutes"] is not None
               and 0 < r["reset_minutes"] <= request["deadline_minutes"]]
    if waiting and request["can_wait"] and request["attempts"] < MAX_ATTEMPTS:
        chosen = min(waiting, key=lambda r: (r["reset_minutes"],) + cheapest(r))
        return {"action": "defer", "resource": chosen["id"], "cash": 0, "calls": chosen["calls"],
                "checks": required_check(request, chosen),
                "reason": (f'free quota refills before the deadline: retry {request["attempts"] + 1} of {MAX_ATTEMPTS}, '
                           f"recheck availability at wake-up; {evidence(chosen, request['difficulty'])}"),
                "wake_in_minutes": max(chosen["reset_minutes"], INTERVAL)}
    paid = [r for r in eligible if r["available"] and r["cash"] <= request["budget"]]
    if paid:
        chosen = min(paid, key=cheapest)
        why = "retries exhausted" if request["attempts"] >= MAX_ATTEMPTS else "cannot wait"
        return {"action": "run", "resource": chosen["id"], "cash": chosen["cash"], "calls": chosen["calls"],
                "checks": required_check(request, chosen),
                "reason": f"{why}; cheapest available billed route within the authorised budget; {evidence(chosen, request['difficulty'])}"}
    return {"action": "abstain", "resource": None, "cash": 0, "checks": checks,
            "reason": (f'no eligible resource at L{request["difficulty"]} within deadline, retries and budget; '
                       f'eligible by TD1 level >= L{request["difficulty"]} (never wrong on '
                       f'{", ".join(cells_up_to(request["difficulty"]))}): {", ".join(r["id"] for r in eligible)}')}


def with_provider(resources, provider, **changes):
    return [dict(r, **changes) if r.get("provider") == provider and r["access"] == "free" else dict(r)
            for r in resources]


def scenarios():
    base = {"family": "F1", "difficulty": 1, "stakes": "dashboard", "can_wait": True,
            "deadline_minutes": 120, "budget": 0.01, "attempts": 0}
    f2 = {**base, "family": "F2", "difficulty": 2, "stakes": "customer"}
    groq_429 = with_provider(RESOURCES, "groq", available=False, reset_minutes=1)
    openrouter_down = with_provider(RESOURCES, "openrouter", available=False, reset_minutes=None)
    return [
        ("simple", base, RESOURCES),
        ("provider unavailable", base, openrouter_down),
        ("complex", f2, RESOURCES),
        ("deferrable", f2, groq_429),
        ("retries exhausted", {**f2, "attempts": MAX_ATTEMPTS}, groq_429),
        ("urgent", {**f2, "can_wait": False, "deadline_minutes": 0.5}, groq_429),
        ("budget exhausted", {**f2, "can_wait": False, "budget": 0}, groq_429),
        ("high impact", {**base, "family": "F4", "difficulty": 3, "stakes": "payout"}, RESOURCES),
        ("hard question, quota exhausted", {**base, "family": "F4", "difficulty": 3, "stakes": "customer"}, groq_429),
        ("unknown capability", {**base, "family": "F5 (unseen)", "difficulty": 4}, RESOURCES),
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
