#!/usr/bin/env python3
"""TD2 step 3 (pair C): read the priority order of the kit's `choose` on two controlled cases.

Imports choose() from the unmodified kit-td1/atelier-routage.py and runs one request against:
  A. an available subscription (cash 0, allocation > 0) and an exhausted free route that refills
     before the deadline (cash 0, allocation 0, reset 30 min < deadline 120 min);
  B. the same, with the subscription unavailable and no reset.
Writes td2/routing/priority-check.jsonl. Standard library only.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("kit_routage", ROOT / "kit-td1" / "atelier-routage.py")
kit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit)

FREE_EXHAUSTED = {"id": "free-exhausted", "level": 3, "access": "free", "available": False,
                  "cash": 0.0, "allocation": 0.0, "reset_minutes": 30}
SUBSCRIPTION = {"id": "subscription", "level": 3, "access": "subscription", "available": True,
                "cash": 0.0, "allocation": 0.04, "reset_minutes": None}
REQUEST = {"difficulty": 3, "high_impact": False, "can_wait": True, "deadline_minutes": 120, "budget": 0.30}

cases = [
    ("A subscription available, free exhausted refilling in 30 min", [FREE_EXHAUSTED, SUBSCRIPTION]),
    ("B subscription unavailable, free exhausted refilling in 30 min",
     [FREE_EXHAUSTED, dict(SUBSCRIPTION, available=False)]),
]
lines = [json.dumps({"case": name, "request": REQUEST, "result": kit.choose(REQUEST, res)}) for name, res in cases]
(Path(__file__).resolve().parent / "priority-check.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
