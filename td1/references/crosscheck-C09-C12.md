# Cross-check of references C09-C12 (member C)

Independent re-computation by Thomas of four values recorded in `reference-td1.csv`, with queries written
separately from `compute_references.py`. Script: [`crosscheck_member_C.py`](crosscheck_member_C.py); it
expects `data/boutique.sqlite` next to it, so copy it into the kit's `kit-td1/` folder to run it.

| Case | Type | Member C | `reference-td1.csv` | Status |
|---|---|---:|---:|---|
| C09 | age on a reference date | 487980 | 487980 | OK |
| C10 | age at the time of the order | 558980 | 558980 | OK |
| C11 | age on a reference date | 446690 | 446690 | OK |
| C12 | product list | 1666490 | 1666490 | OK |

C09 and C11 select the birth dates of a completed age of 25 directly (born after the reference date minus
26 years, on or before the reference date minus 25 years); C10 computes the completed age on each order date.
No mismatch: the four references are confirmed.
