"""References TD 1 - questions C05 a C08 (Raphael).

Executes the four reference queries on data/boutique.sqlite opened READ-ONLY,
checks that each returns one row and one column 'revenue_cents', and writes
refs-raph.csv (case_id, sql, revenue_cents).

Option --merge: also fills the C05-C08 rows of reference-td1.csv
(the other rows are left untouched).

Run from the kit-td1 folder:
    python refs_raph.py
    python refs_raph.py --merge

Conventions applied (consigne-etudiante-en, section 1):
- revenue excluding VAT = SUM(quantity_product * price), integer cents;
- period closed on the left, open on the right: date >= start AND date < end;
- completed age from month and day, never the year difference alone;
- 0 instead of NULL when nothing matches (COALESCE).
"""
import csv
import sqlite3
import sys

DB = "file:data/boutique.sqlite?mode=ro"

QUERIES = {
    # C05 - period: one day, 1 June 2026 (00:00:00 included, 2 June excluded)
    "C05": """
        SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
        FROM orders o
        JOIN product p ON p.product_id = o.product_id
        WHERE o.date >= '2026-06-01 00:00:00'
          AND o.date <  '2026-06-02 00:00:00'
    """,
    # C06 - period: the whole of 2025 (may be 0 if the base has no 2025 order)
    "C06": """
        SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
        FROM orders o
        JOIN product p ON p.product_id = o.product_id
        WHERE o.date >= '2025-01-01 00:00:00'
          AND o.date <  '2026-01-01 00:00:00'
    """,
    # C07 - period: one day, 31 May 2026 (an order at 2026-06-01 00:00:00 is EXCLUDED)
    "C07": """
        SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
        FROM orders o
        JOIN product p ON p.product_id = o.product_id
        WHERE o.date >= '2026-05-31 00:00:00'
          AND o.date <  '2026-06-01 00:00:00'
    """,
    # C08 - customers exactly 25 on 2026-09-24, ALL their orders (no period filter).
    # Completed age = (2026 - birth year) - 1 if the birthday (MM-DD) is after 09-24.
    "C08": """
        SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
        FROM orders o
        JOIN product p   ON p.product_id  = o.product_id
        JOIN customers c ON c.customer_id = o.customer_id
        WHERE (2026 - CAST(substr(c.birth_date, 1, 4) AS INTEGER))
              - (substr(c.birth_date, 6, 5) > '09-24') = 25
    """,
}


def one_line(sql):
    return " ".join(sql.split())


def main():
    con = sqlite3.connect(DB, uri=True)
    con.execute("PRAGMA query_only = 1")

    results = {}
    for cid, sql in QUERIES.items():
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        assert cols == ["revenue_cents"], f"{cid}: column {cols}, expected ['revenue_cents']"
        assert len(rows) == 1 and len(rows[0]) == 1, f"{cid}: expected 1 row x 1 column, got {rows}"
        value = rows[0][0]
        assert isinstance(value, int), f"{cid}: value {value!r} is not an integer"
        results[cid] = value
        print(f"{cid}  revenue_cents = {value}")

    with open("refs-raph.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "sql", "revenue_cents"])
        for cid, sql in QUERIES.items():
            w.writerow([cid, one_line(sql), results[cid]])
    print("\n-> refs-raph.csv written")

    if "--merge" in sys.argv:
        with open("reference-td1.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames
            rows = list(reader)
        found = set()
        for row in rows:
            if row["case_id"] in QUERIES:
                row["sql"] = one_line(QUERIES[row["case_id"]])
                row["revenue_cents"] = results[row["case_id"]]
                found.add(row["case_id"])
        missing = set(QUERIES) - found
        assert not missing, f"rows not found in reference-td1.csv: {missing}"
        with open("reference-td1.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=header)
            w.writeheader()
            w.writerows(rows)
        print("-> C05-C08 filled in reference-td1.csv (other rows unchanged)")


if __name__ == "__main__":
    main()
