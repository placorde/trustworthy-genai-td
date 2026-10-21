# Cross-check of references C01-C04 (member A)

Independent re-computation of the four values recorded in `reference-td1.csv` (PR #1), with queries
written separately from `compute_references.py`. Script: [`crosscheck_member_A.py`](crosscheck_member_A.py).

```powershell
python references/crosscheck_member_A.py --kit <path-to>/kit-td1
```

## Result

| Case | Type | Member A | `reference-td1.csv` | Status |
|---|---|---:|---:|---|
| C01 | period | 792800 | 792800 | OK |
| C02 | age on a reference date | 590320 | 590320 | OK |
| C03 | product list | 936350 | 936350 | OK |
| C04 | period | 2826250 | 2826250 | OK |

No mismatch: the four references are confirmed.

## What differs from the original method

- **Age (C02).** The reference uses the formula `year difference - (ref month-day < birth month-day)`, and
  its Python check uses the same formula. Here the age is a birth-date interval: exactly 25 completed years
  on 2026-09-25 means born in `(2000-09-25, 2001-09-25]`, i.e.
  `birth_date > '2000-09-25' AND birth_date <= '2001-09-25'`. The two methods agree.
- **Amounts.** Line amounts `quantity_product * price` are computed in a subquery with a `LEFT JOIN`, then
  summed, so an order line without a product would appear as a NULL amount (checked below: there is none).

## Conventions applied

- Revenue excluding VAT = `SUM(quantity_product * price)`, integer cents; `COALESCE(..., 0)` returns 0 instead of NULL.
- Period closed on the left, open on the right: `date >= start AND date < end`.
- Completed age from month and day, never from the year difference alone.
- Product list: `product_id IN ('a', 'b', 'c')`.

## Data checks behind these conventions

| Check | Result |
|---|---|
| Order dates not in `YYYY-MM-DD HH:MM:SS` | 0 (string comparison of timestamps is safe) |
| Birth dates not in `YYYY-MM-DD` | 0 |
| Order lines without product price / without known customer | 0 / 0 |
| Customers born on 29 February | 0 |
| Order lines exactly on `2026-03-01 00:00:00` | 3 (included in C01) |
| Order lines exactly on `2026-06-01 00:00:00` | 1 (excluded from C01) |
| Order lines exactly on `2026-01-01`, `2026-07-01`, `2026-10-01` at 00:00:00 | 0 |
| Customer born 2001-09-25 (turns 25 on the reference date) | 1, included |
| Customer born 2000-09-25 (turns 26 on the reference date) | 1, excluded |
| Customer born 2001-09-26 (still 24) | 1, excluded |
| Order date range | 2026-01-06 21:23:30 to 2026-09-20 19:24:25 |

## Effect of a broken convention (what a model may get wrong)

| Mistake | Value | Correct |
|---|---:|---:|
| C01 with `date <= end` (right bound included) | 801770 | 792800 |
| C01 with `date > start` (left bound excluded) | 775340 | 792800 |
| C02 with age = year difference only (`2026 - birth year = 25`) | 548920 | 590320 |
| C03 without the product filter | 1566220 | 936350 |

Note: `date BETWEEN '2026-03-01' AND '2026-06-01'` gives the right C01 value (792800) only by accident:
`'2026-06-01 00:00:00' > '2026-06-01'` as strings, so the line on the right bound is excluded. The same
query with full timestamps as bounds would include it. Such SQL must not be accepted as correct by
construction even when its value matches.
