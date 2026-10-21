import csv
import sqlite3
from pathlib import Path

base = Path(__file__).resolve().parent
database = (base / "data" / "boutique.sqlite").as_uri() + "?mode=ro"

queries = {
    "C09": """
        SELECT COALESCE(SUM(p.price * o.quantity_product), 0) AS revenue_cents
        FROM orders AS o
        JOIN customers AS c ON c.customer_id = o.customer_id
        JOIN product AS p ON p.product_id = o.product_id
        WHERE date(c.birth_date) > '2000-09-26'
          AND date(c.birth_date) <= '2001-09-26'
    """,
    "C10": """
        SELECT COALESCE(SUM(p.price * o.quantity_product), 0) AS revenue_cents
        FROM orders AS o
        JOIN customers AS c ON c.customer_id = o.customer_id
        JOIN product AS p ON p.product_id = o.product_id
        WHERE (
            CAST(strftime('%Y', o.date) AS INTEGER)
            - CAST(strftime('%Y', c.birth_date) AS INTEGER)
            - CASE
                WHEN strftime('%m-%d', o.date)
                     < strftime('%m-%d', c.birth_date)
                THEN 1 ELSE 0
              END
        ) = 25
    """,
    "C11": """
        SELECT COALESCE(SUM(p.price * o.quantity_product), 0) AS revenue_cents
        FROM orders AS o
        JOIN customers AS c ON c.customer_id = o.customer_id
        JOIN product AS p ON p.product_id = o.product_id
        WHERE date(c.birth_date) > '2000-12-01'
          AND date(c.birth_date) <= '2001-12-01'
    """,
    "C12": """
        SELECT COALESCE(SUM(p.price * o.quantity_product), 0) AS revenue_cents
        FROM orders AS o
        JOIN product AS p ON p.product_id = o.product_id
        WHERE p.product_id IN ('a', 'b', 'c')
    """,
}

output = base / "references-model C.csv"

with sqlite3.connect(database, uri=True) as connection:
    print("Produits et prix :")
    for row in connection.execute(
        "SELECT product_id, price FROM product ORDER BY product_id"
    ):
        print(row)

    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["case_id", "sql", "revenue_cents"]
        )
        writer.writeheader()

        for case_id, query in queries.items():
            sql = " ".join(query.split())
            result = connection.execute(sql).fetchall()

            if len(result) != 1 or len(result[0]) != 1:
                raise ValueError(f"{case_id} : résultat non conforme")

            value = result[0][0]
            writer.writerow({
                "case_id": case_id,
                "sql": sql,
                "revenue_cents": value,
            })
            print(f"{case_id} : {value} centimes HT")

print(f"\nFichier créé : {output}")