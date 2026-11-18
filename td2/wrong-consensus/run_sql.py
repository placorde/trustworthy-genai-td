"""TD2 step 2 (pair B): run one .sql file on the shop database, read-only.

Run from the repository root:
    python td2/wrong-consensus/run_sql.py td2/wrong-consensus/delta.sql
"""
import sqlite3
import sys

sql = open(sys.argv[1], encoding="utf-8").read()
con = sqlite3.connect("file:kit-td1/data/boutique.sqlite?mode=ro", uri=True)
cur = con.execute(sql)
print([d[0] for d in cur.description])
for row in cur.fetchall():
    print(row)
