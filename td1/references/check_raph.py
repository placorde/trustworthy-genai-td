"""Independent check of C05-C08 - pure Python on the CSV files, no SQL.

Recomputes the four values from data/orders.csv, data/product.csv and
data/customers.csv with datetime, then compares them with refs-raph.csv.
Also prints the details useful to explain each value (boundary orders,
matched customers).

Run from kit-td1 after refs_raph.py:
    python check_raph.py
"""
import csv
from datetime import date, datetime


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


products = {r["product_id"]: int(r["price"]) for r in load("data/product.csv")}
customers = {r["customer_id"]: r for r in load("data/customers.csv")}
orders = load("data/orders.csv")

TS = "%Y-%m-%d %H:%M:%S"
for o in orders:
    o["_dt"] = datetime.strptime(o["date"], TS)          # fails loudly on a bad format
    o["_amount"] = int(o["quantity_product"]) * products[o["product_id"]]


def period(start, end):
    s, e = datetime.strptime(start, TS), datetime.strptime(end, TS)
    return [o for o in orders if s <= o["_dt"] < e]      # closed left, open right


def completed_age(birth, ref):
    return ref.year - birth.year - ((ref.month, ref.day) < (birth.month, birth.day))


def customers_aged(age, ref):
    out = []
    for cid, c in customers.items():
        b = date.fromisoformat(c["birth_date"])
        if completed_age(b, ref) == age:
            out.append((cid, c["birth_date"]))
    return out


check = {}

# C05 / C06 / C07 - periods
for cid, start, end in [
    ("C05", "2026-06-01 00:00:00", "2026-06-02 00:00:00"),
    ("C06", "2025-01-01 00:00:00", "2026-01-01 00:00:00"),
    ("C07", "2026-05-31 00:00:00", "2026-06-01 00:00:00"),
]:
    lines = period(start, end)
    check[cid] = sum(o["_amount"] for o in lines)
    print(f"{cid}: {len(lines)} order lines in [{start}, {end})")

boundary = [o for o in orders if o["date"] == "2026-06-01 00:00:00"]
print(f"     lines exactly at 2026-06-01 00:00:00 (in C05, not in C07): {len(boundary)}")
print(f"     date range in the base: {min(o['date'] for o in orders)} -> {max(o['date'] for o in orders)}")

# C08 - exactly 25 on 2026-09-24, all their orders
ref = date(2026, 9, 24)
aged = customers_aged(25, ref)
ids = {cid for cid, _ in aged}
check["C08"] = sum(o["_amount"] for o in orders if o["customer_id"] in ids)
print(f"C08: {len(aged)} customer(s) exactly 25 on {ref}: {sorted(aged, key=lambda x: x[1])}")
near = [(cid, c["birth_date"]) for cid, c in customers.items()
        if c["birth_date"][5:] in ("09-23", "09-24", "09-25", "09-26", "09-27")]
print(f"     customers with a birthday around 24 Sept (useful for C02/C08/C09): {sorted(near, key=lambda x: x[1])}")
leap = [cid for cid, c in customers.items() if c["birth_date"][5:] == "02-29"]
print(f"     customers born on 29 February: {leap or 'none'}")

# Comparison with the SQL results
print("\nComparison SQL (refs-raph.csv) vs independent check:")
sql_values = {r["case_id"]: int(r["revenue_cents"]) for r in load("refs-raph.csv")}
all_ok = True
for cid in ["C05", "C06", "C07", "C08"]:
    ok = sql_values.get(cid) == check[cid]
    all_ok &= ok
    print(f"  {cid}  SQL={sql_values.get(cid)}  check={check[cid]}  {'OK' if ok else 'DIFFERENT'}")
print("\nAll identical." if all_ok else "\nDifference found: re-read the convention involved.")
