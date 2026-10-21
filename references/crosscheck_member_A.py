"""Member A: independent cross-check of the C01-C04 references.

Written separately from compute_references.py, with different methods:
- completed age by a birth-date interval instead of the strftime year/month-day formula;
- line amounts computed in a subquery instead of a direct aggregate over the join;
- data checks on the formats and boundary cases the conventions depend on.
"""
import argparse
import csv
import re
import sqlite3
from pathlib import Path

# Line amounts first, then the sum: an order line with no matching product would show up as NULL.
LINES = ("SELECT o.date, o.customer_id, o.product_id, o.quantity_product * p.price AS amount"
         " FROM orders o LEFT JOIN product p ON p.product_id = o.product_id")

QUERIES = {
    # Period [2026-03-01, 2026-06-01): closed on the left, open on the right.
    "C01": f"SELECT COALESCE(SUM(amount), 0) AS revenue_cents FROM ({LINES}) l"
           " WHERE l.date >= '2026-03-01 00:00:00' AND l.date < '2026-06-01 00:00:00';",
    # Exactly 25 completed years on 2026-09-25 <=> born in (2000-09-25, 2001-09-25].
    "C02": f"SELECT COALESCE(SUM(amount), 0) AS revenue_cents FROM ({LINES}) l"
           " WHERE l.customer_id IN (SELECT customer_id FROM customers"
           " WHERE birth_date > '2000-09-25' AND birth_date <= '2001-09-25');",
    "C03": f"SELECT COALESCE(SUM(amount), 0) AS revenue_cents FROM ({LINES}) l"
           " WHERE l.date >= '2026-01-01 00:00:00' AND l.date < '2026-07-01 00:00:00'"
           " AND l.product_id IN ('a', 'b', 'c');",
    "C04": f"SELECT COALESCE(SUM(amount), 0) AS revenue_cents FROM ({LINES}) l"
           " WHERE l.date >= '2026-01-01 00:00:00' AND l.date < '2026-10-01 00:00:00';",
}

TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BOUNDS = ["2026-01-01 00:00:00", "2026-03-01 00:00:00", "2026-06-01 00:00:00",
          "2026-07-01 00:00:00", "2026-10-01 00:00:00"]


def data_checks(db):
    """Return (label, result) pairs for the assumptions the C01-C04 queries rely on."""
    one = lambda sql, *args: db.execute(sql, args).fetchone()[0]
    dates = [r[0] for r in db.execute("SELECT date FROM orders")]
    births = [r[0] for r in db.execute("SELECT birth_date FROM customers")]
    return [
        ("order dates not in 'YYYY-MM-DD HH:MM:SS'", sum(not TIMESTAMP.match(d) for d in dates)),
        ("birth dates not in 'YYYY-MM-DD'", sum(not DAY.match(b) for b in births)),
        ("order lines without a product price",
         one("SELECT COUNT(*) FROM orders o LEFT JOIN product p ON p.product_id = o.product_id"
             " WHERE p.price IS NULL")),
        ("order lines without a known customer",
         one("SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON c.customer_id = o.customer_id"
             " WHERE c.customer_id IS NULL")),
        ("customers born on 29 February", sum(b[5:] == "02-29" for b in births)),
        ("order lines exactly on a period bound " + ", ".join(b[:10] for b in BOUNDS),
         {b[:10]: dates.count(b) for b in BOUNDS}),
        ("customers born exactly on 2001-09-25 (25 that day, included)", births.count("2001-09-25")),
        ("customers born exactly on 2000-09-25 (26 that day, excluded)", births.count("2000-09-25")),
        ("customers born on 2001-09-26 (still 24, excluded)", births.count("2001-09-26")),
        ("order date range", (min(dates), max(dates))),
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kit", type=Path, required=True)
    parser.add_argument("--reference", type=Path,
                        default=Path(__file__).resolve().parent.parent / "reference-td1.csv")
    args = parser.parse_args()
    db = sqlite3.connect(f"file:{(args.kit / 'data' / 'boutique.sqlite').as_posix()}?mode=ro", uri=True)
    db.execute("PRAGMA query_only = 1")

    print("Data checks")
    for label, result in data_checks(db):
        print(f"  {label}: {result}")

    with open(args.reference, newline="", encoding="utf-8") as f:
        reference = {r["case_id"]: int(r["revenue_cents"]) for r in csv.DictReader(f)}

    print("\nCross-check against", args.reference.name)
    mismatches = []
    for case_id, sql in QUERIES.items():
        cursor = db.execute(sql)
        rows = cursor.fetchall()
        assert [d[0] for d in cursor.description] == ["revenue_cents"] and len(rows) == 1, case_id
        value = rows[0][0]
        status = "OK" if value == reference[case_id] else "MISMATCH"
        if status != "OK":
            mismatches.append(case_id)
        print(f"  {case_id} member_A={value:>10} reference={reference[case_id]:>10} {status}")
    print(f"Mismatches: {mismatches or 'none'}")


if __name__ == "__main__":
    main()
