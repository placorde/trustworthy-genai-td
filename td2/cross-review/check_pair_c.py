"""TD2 cross-review by pair B: recompute pair C's numbers independently from the raw traces.

Run from the repository root (no network, standard library only):
    python td2/cross-review/check_pair_c.py

Pair C computes its rates from `model-question-comparison-en.csv`. This script starts again from
`traces-td1.csv` (last attempt of each model per question, latest `date_utc`) and recomputes:
1. the correct / cases rate of each model on each question family, and each model's level;
2. the replay of pair C's three 2-of-3 panels (L1, L2, L3) on the 20 questions;
3. the consistency constraint: "none" only where the first model is 100 % on its family.
The expected values are the ones written in `routing/family-rates-td1.md` and
`routing/routing-rule-td2.md` (copied below), so any difference is printed.
"""
import collections
import csv

FAMILIES = {
    "F1": (1, ["C01", "C04", "C05", "C06", "C07", "C20"]),
    "F3": (1, ["C03", "C12", "C13", "C14"]),
    "F2": (2, ["C02", "C08", "C09", "C11"]),
    "F2b": (3, ["C10"]),
    "F4": (3, ["C15", "C16", "C17", "C18", "C19"]),
}
MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "cohere/north-mini-code:free",
          "qwen/qwen3.8-27b", "dots-studio/dots-3-note-preview:free"]
# What pair C wrote (routing/family-rates-td1.md), same model order as MODELS.
PAIR_C_RATES = {
    "F1": ["6/6", "6/6", "6/6", "6/6", "6/6"],
    "F3": ["4/4", "4/4", "4/4", "4/4", "4/4"],
    "F2": ["4/4", "1/4", "0/4", "4/4", "1/4"],
    "F2b": ["1/1", "1/1", "0/1", "0/1", "1/1"],
    "F4": ["4/5", "5/5", "1/5", "1/5", "1/5"],
}
PAIR_C_LEVELS = {"openai/gpt-oss-120b": 2, "openai/gpt-oss-20b": 1, "cohere/north-mini-code:free": 1,
                 "qwen/qwen3.8-27b": 2, "dots-studio/dots-3-note-preview:free": 1}
PANELS = {  # routing/routing-rule.json
    "L1": ["cohere/north-mini-code:free", "dots-studio/dots-3-note-preview:free", "openai/gpt-oss-20b"],
    "L2": ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "dots-studio/dots-3-note-preview:free"],
    "L3": ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "dots-studio/dots-3-note-preview:free"],
}
# First model and dashboard check per family (routing/routing-rule-td2.md).
FIRST_AND_DASHBOARD = {"F1": ("cohere/north-mini-code:free", "none"), "F3": ("cohere/north-mini-code:free", "none"),
                       "F2": ("openai/gpt-oss-120b", "none"), "F2b": ("panel L3", "panel vote"),
                       "F4": ("panel L3", "panel vote")}


def main():
    rows = list(csv.DictReader(open("td1/traces-td1.csv", encoding="utf-8")))
    refs = {r["case_id"]: int(r["revenue_cents"]) for r in csv.DictReader(open("td1/reference-td1.csv", encoding="utf-8"))}
    last = {}
    for r in rows:
        key = (r["case_id"], r["model_requested"])
        if key not in last or r["date_utc"] >= last[key]["date_utc"]:
            last[key] = r

    print("## 1. Rates per family, recomputed from traces-td1.csv\n")
    print("| Family | " + " | ".join(m.split("/")[1] for m in MODELS) + " | Same as pair C? |")
    print("|---" * (len(MODELS) + 2) + "|")
    ok_all = True
    for fam, (_, qs) in FAMILIES.items():
        cells = []
        for m in MODELS:
            good = sum(last[(q, m)]["verdict"] == "correct" for q in qs)
            cells.append(f"{good}/{len(qs)}")
        same = cells == PAIR_C_RATES[fam]
        ok_all &= same
        print(f"| {fam} | " + " | ".join(cells) + f" | {'yes' if same else '**NO**'} |")

    print("\n| Model | Level recomputed | Level by pair C | Same? |\n|---|---|---|---|")
    for m in MODELS:
        level = 0
        for lv in (1, 2, 3):
            qs = [q for _, (l, fq) in FAMILIES.items() if l <= lv for q in fq]
            if all(last[(q, m)]["verdict"] == "correct" for q in qs):
                level = lv
        same = level == PAIR_C_LEVELS[m]
        ok_all &= same
        print(f"| {m} | L{level} | L{PAIR_C_LEVELS[m]} | {'yes' if same else '**NO**'} |")

    print("\n## 2. Pair C's 2-of-3 panels replayed on the 20 questions\n")
    print("| Panel | Members | Correct | Abstain | Wrong | Abstentions |\n|---|---|---|---|---|---|")
    for name, members in PANELS.items():
        tally, abst = collections.Counter(), []
        for i in range(1, 21):
            q = f"C{i:02d}"
            votes = collections.Counter()
            for m in members:
                r = last[(q, m)]
                if r["verdict"] in {"correct", "incorrect"} and r["value"] != "":
                    votes[int(r["value"])] += 1
            value, n = votes.most_common(1)[0] if votes else (None, 0)
            if n >= 2:
                tally["correct" if value == refs[q] else "wrong"] += 1
            else:
                tally["abstain"] += 1
                abst.append(q)
        short = ", ".join(m.split("/")[1] for m in members)
        print(f"| {name} | {short} | {tally['correct']} | {tally['abstain']} | {tally['wrong']} | {', '.join(abst)} |")

    print("\n## 3. Consistency constraint (\"none\" only if the first model is 100 % on the family)\n")
    print("| Family | First model | Dashboard check | First model rate | Constraint respected? |\n|---|---|---|---|---|")
    for fam, (first, dash) in FIRST_AND_DASHBOARD.items():
        qs = FAMILIES[fam][1]
        if first.startswith("panel"):
            print(f"| {fam} | {first} | {dash} | (panel, not a single model) | yes (no single model alone) |")
            continue
        good = sum(last[(q, first)]["verdict"] == "correct" for q in qs)
        ok = dash != "none" or good == len(qs)
        ok_all &= ok
        print(f"| {fam} | {first} | {dash} | {good}/{len(qs)} | {'yes' if ok else '**NO**'} |")

    print(f"\nEverything matches pair C's files: {'yes' if ok_all else 'NO, see the rows marked NO'}")


if __name__ == "__main__":
    main()
