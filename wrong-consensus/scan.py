"""TD2 step 2 (pair B): find wrong values shared by several TD1 models.

Run from the repository root:
    python wrong-consensus/scan.py          # scan the TD1 cells for shared wrong values
    python wrong-consensus/scan.py C02      # show every attempt of the five models on one question
"""
import collections
import csv
import sys

rows = list(csv.DictReader(open("traces-td1.csv", encoding="utf-8")))

if len(sys.argv) > 1:  # detail of one question
    for r in rows:
        if r["case_id"] == sys.argv[1]:
            print("====", r["model_requested"], "| verdict:", r["verdict"],
                  "| value:", r["value"], "| ref:", r["reference"], "| date:", r["date_utc"])
            print(r["sql"], "\n")
    sys.exit()

groups = collections.defaultdict(set)  # (question, wrong value) -> models
for r in rows:
    if r["verdict"] == "incorrect" and r["value"] != "":
        groups[(r["case_id"], r["value"])].add(r["model_requested"])

found = False
for (case, value), models in sorted(groups.items()):
    if len(models) >= 2:
        found = True
        print(case, "value =", value, "->", sorted(models))
if not found:
    print("No shared wrong value -> use the fallback DEMO-SQL-C11")
