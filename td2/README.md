# TD2 --- Vote and route (18 November 2026)

DIA3-G5. No new model call: everything runs on the TD1 traces in [`../td1/`](../td1/README.md).
The sub-group split into three pairs. Report: [`reports/td2.md`](reports/td2.md).

| Step | Pair | Work | Where |
|---|---|---|---|
| 1. k-of-n vote | A | `Orchestrateur.vote_k_sur_n` (strict majority, executed values only, duplicate pair refused, abstain without inventing a value); fixed 2-of-3 panel against 3-of-5 on the twenty questions | [`../kit-td1/skeleton-multi-llm-en.py`](../kit-td1/skeleton-multi-llm-en.py), [`reports/td2.md`](reports/td2.md) step 1 |
| 2. Wrong consensus | B | C02: gpt-oss-20b and Cohere both return 0 (reference 590320); faulty SQL clauses and delta query | [`wrong-consensus/`](wrong-consensus/case-C02.md) |
| 3. Routing rule | C | TD1 rates per family, difficulty levels L1/L2/L3, one-page rule, adapted simulator, priority analysis of `choose` | [`routing/`](routing/routing-rule-td2.md) |

## Files

| Path | Content |
|---|---|
| `reports/td2.md` | TD2 report: the three steps, simulator outputs, priority analysis, limits |
| `wrong-consensus/case-C02.md` | Pair B: identification, quorum verdict, SQL diagnosis, delta query, consequence for checking |
| `wrong-consensus/*.sql`, `scan.py`, `run_sql.py` | The two wrong queries, the reference, the delta query; scan of shared wrong values; read-only SQL runner |
| `routing/routing-rule-td2.md` | Pair C: the one-page routing rule (machine form `routing-rule.json`) |
| `routing/family_rates.py` → `family-rates-td1.md` / `.json` | TD1 accuracy per family and level, model levels, billed-equivalent cost |
| `routing/quorum_check.py` → `quorum-check-td1.md` / `.json` | Every 2-of-3 panel replayed on the TD1 traces |
| `routing/atelier-routage.py` | Kit simulator adapted to our rule (`RESOURCES` and `choose`); the kit file stays byte-identical |
| `routing/simulator-before.jsonl`, `simulator-after.jsonl` | Simulator outputs before (kit rule) and after (our rule) |
| `routing/priority_check.py` → `priority-check.jsonl` | The kit's `choose` on the subscription-versus-wait case |

## Reproducing

From the repository root, offline, no key needed:

```powershell
python td2/wrong-consensus/scan.py
python td2/wrong-consensus/scan.py C02
python td2/wrong-consensus/run_sql.py td2/wrong-consensus/delta.sql
python td2/routing/family_rates.py
python td2/routing/quorum_check.py
python kit-td1/atelier-routage.py > td2/routing/simulator-before.jsonl
python td2/routing/atelier-routage.py > td2/routing/simulator-after.jsonl
python td2/routing/priority_check.py
```
