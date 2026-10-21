import argparse
import csv
import sqlite3
from datetime import date
from pathlib import Path

REVENUE = "SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents FROM orders o JOIN product p ON p.product_id = o.product_id"
CUSTOMER = " JOIN customers c ON c.customer_id = o.customer_id"


def age_on(ref):
    return (f"(CAST(strftime('%Y', '{ref}') AS INTEGER) - CAST(strftime('%Y', c.birth_date) AS INTEGER)"
            f" - (strftime('%m-%d', '{ref}') < strftime('%m-%d', c.birth_date)))")


AGE_AT_ORDER = ("(CAST(strftime('%Y', o.date) AS INTEGER) - CAST(strftime('%Y', c.birth_date) AS INTEGER)"
                " - (strftime('%m-%d', o.date) < strftime('%m-%d', c.birth_date)))")


def period(start, end):
    return f"o.date >= '{start} 00:00:00' AND o.date < '{end} 00:00:00'"


def products(*ids):
    return "o.product_id IN (" + ", ".join(f"'{i}'" for i in ids) + ")"


def build(period_=None, age_ref=None, at_order=False, product_ids=None):
    sql = REVENUE + (CUSTOMER if age_ref or at_order else "")
    where = []
    if period_:
        where.append(period(*period_))
    if age_ref:
        where.append(f"{age_on(age_ref)} = 25")
    if at_order:
        where.append(f"{AGE_AT_ORDER} = 25")
    if product_ids:
        where.append(products(*product_ids))
    return sql + (" WHERE " + " AND ".join(where) if where else "") + ";"


SPECS = {
    "C01": dict(period_=("2026-03-01", "2026-06-01")),
    "C02": dict(age_ref="2026-09-25"),
    "C03": dict(period_=("2026-01-01", "2026-07-01"), product_ids="abc"),
    "C04": dict(period_=("2026-01-01", "2026-10-01")),
    "C05": dict(period_=("2026-06-01", "2026-06-02")),
    "C06": dict(period_=("2025-01-01", "2026-01-01")),
    "C07": dict(period_=("2026-05-31", "2026-06-01")),
    "C08": dict(age_ref="2026-09-24"),
    "C09": dict(age_ref="2026-09-26"),
    "C10": dict(at_order=True),
    "C11": dict(age_ref="2026-12-01"),
    "C12": dict(product_ids="abc"),
    "C13": dict(period_=("2026-04-01", "2026-05-01"), product_ids="ac"),
    "C14": dict(period_=("2026-10-01", "2026-12-01"), product_ids="abc"),
    "C15": dict(period_=("2026-03-01", "2026-06-01"), age_ref="2026-09-25"),
    "C16": dict(age_ref="2026-09-25", product_ids="abc"),
    "C17": dict(period_=("2026-01-01", "2026-07-01"), age_ref="2026-09-25", product_ids="abc"),
    "C18": dict(period_=("2026-05-01", "2026-06-01"), at_order=True),
    "C19": dict(period_=("2026-09-01", "2026-10-01"), age_ref="2026-09-25", product_ids="d"),
    "C20": dict(period_=("2026-06-01", "2026-09-01")),
}


def completed_age(birth, on):
    return on.year - birth.year - ((on.month, on.day) < (birth.month, birth.day))


def independent(data_dir, period_=None, age_ref=None, at_order=False, product_ids=None):
    with open(data_dir / "product.csv", newline="") as f:
        price = {r["product_id"]: int(r["price"]) for r in csv.DictReader(f)}
    with open(data_dir / "customers.csv", newline="") as f:
        birth = {r["customer_id"]: date.fromisoformat(r["birth_date"]) for r in csv.DictReader(f)}
    total = 0
    with open(data_dir / "orders.csv", newline="") as f:
        for r in csv.DictReader(f):
            ordered = r["date"]
            if period_ and not (f"{period_[0]} 00:00:00" <= ordered < f"{period_[1]} 00:00:00"):
                continue
            if age_ref and completed_age(birth[r["customer_id"]], date.fromisoformat(age_ref)) != 25:
                continue
            if at_order and completed_age(birth[r["customer_id"]], date.fromisoformat(ordered[:10])) != 25:
                continue
            if product_ids and r["product_id"] not in product_ids:
                continue
            total += int(r["quantity_product"]) * price[r["product_id"]]
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kit", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent.parent / "reference-td1.csv")
    args = parser.parse_args()
    db = sqlite3.connect(f"file:{(args.kit / 'data' / 'boutique.sqlite').as_posix()}?mode=ro", uri=True)
    rows, mismatches = [], []
    for case_id, spec in SPECS.items():
        sql = build(**spec)
        cursor = db.execute(sql)
        result = cursor.fetchall()
        assert [d[0] for d in cursor.description] == ["revenue_cents"] and len(result) == 1, case_id
        value = result[0][0]
        check = independent(args.kit / "data", **spec)
        status = "OK" if value == check else "MISMATCH"
        if value != check:
            mismatches.append(case_id)
        print(f"{case_id} sql={value:>10} python_csv={check:>10} {status}")
        rows.append({"case_id": case_id, "sql": sql, "revenue_cents": value})
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["case_id", "sql", "revenue_cents"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} references written to {args.out}; mismatches: {mismatches or 'none'}")


if __name__ == "__main__":
    main()
