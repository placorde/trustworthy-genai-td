# TD2 report --- DIA3 / DIA3-G5

Vote and route, 18 November 2026. No new model call: every figure comes from the TD1 traces
(`traces-td1.csv`, `model-question-comparison-en.csv`, `reference-td1.csv`).

## Step 1 --- k-of-n vote (pair A)

*To be added by pair A.*

## Step 2 --- Wrong consensus (pair B)

*To be added by pair B.*

## Step 3 --- Routing rule (pair C)

### The rule

One page: [`routing/routing-rule-td2.md`](../routing/routing-rule-td2.md). In short:

| Family (difficulty) | First model | Dashboard / customer figure / payout |
|---|---|---|
| F1 period, F3 product list (L1) | Cohere free (10/10 L1 cells) | none / 2-of-3 panel L1 / reference SQL + review |
| F2 completed age at a date (L2) | gpt-oss-120b free (4/4 on C02, C08, C09, C11) | none / 2-of-3 panel L2 / reference SQL + review |
| F2b age at the order, F4 combinations (L3) | 2-of-3 panel (20b, 120b, Dots): no single model is correct on all of C10, C15-C19 | vote / vote + reference SQL / reference SQL + review |

Per-family TD1 rates: [`routing/family-rates-td1.md`](../routing/family-rates-td1.md). Every 2-of-3 panel
replayed on the TD1 traces: [`routing/quorum-check-td1.md`](../routing/quorum-check-td1.md).

### Simulator before adaptation (kit rule, `python kit-td1/atelier-routage.py`)

Full output: [`routing/simulator-before.jsonl`](../routing/simulator-before.jsonl).

| Scenario | Action | Resource | Cash | Reason |
|---|---|---|---|---|
| simple | run | small-free | 0 | eligible included capacity |
| complex | run | senior-subscription | 0 | eligible included capacity |
| deferrable | defer 60 min | senior-subscription | 0 | recheck availability at wake-up |
| urgent | run | senior-api | 0.30 | available route within the authorised budget |
| budget exhausted | abstain | --- | 0 | no eligible resource within deadline and budget |
| high impact | run | senior-subscription | 0 | eligible included capacity (checks: source verification and human review) |
| unknown capability | abstain | --- | 0 | no eligible resource within deadline and budget |

### Simulator after adaptation (our rule, `python routing/atelier-routage.py`)

The kit file is left byte-identical (its SHA-256 is in `kit-td1/manifest.json`); the adapted copy is
`routing/atelier-routage.py`. Changes:
- `RESOURCES`: the five TD1 models on their free routes (level from TD1, billed-equivalent cost), the
  billed OpenRouter route of gpt-oss-120b (0.000207 USD per request), and the L3 panel as one resource
  (available only when its three members are).
- `choose`: same order as the kit (included, then wait, then paid, then abstain), "filter then cheapest"
  with ties broken by billed-equivalent cost; `stakes` (dashboard / customer / payout) sets the check;
  waiting is capped at 10 attempts, 1 min apart (lecture retry policy); every reason cites TD1 cells.

Full output: [`routing/simulator-after.jsonl`](../routing/simulator-after.jsonl).

| Scenario | Request | Action | Resource | Cash (USD) | TD1 evidence in the reason |
|---|---|---|---|---|---|
| simple | F1, L1, dashboard | run | Cohere free | 0 | 10/10 L1 cells |
| provider unavailable | same, OpenRouter down | run | gpt-oss-20b free | 0 | 10/10 L1 cells |
| complex | F2, L2, customer | run | gpt-oss-120b free | 0 | 14/14 cells up to L2; check: panel L2, 4 correct 0 wrong |
| deferrable | same, Groq 429, refill 1 min | defer 1 min (retry 1 of 10) | gpt-oss-120b free | 0 | 14/14 cells up to L2 |
| retries exhausted | same, 10 attempts done | run | billed gpt-oss-120b | 0.000207 | 14/14 cells up to L2 |
| urgent | same, cannot wait | run | billed gpt-oss-120b | 0.000207 | 14/14 cells up to L2 |
| budget exhausted | same, budget 0 | abstain | --- | 0 | no eligible route within deadline, retries and budget |
| high impact | F4, L3, payout | run | panel L3 (3 free calls) | 0 | never wrong on 20 cells; reference SQL + human review |
| hard question, quota exhausted | F4, L3, customer, Groq 429 | defer 1 min | panel L3 | 0 | panel waits for its Groq members |
| unknown capability | unseen family, L4 | abstain | --- | 0 | no TD1 evidence at L4 |

### Priority order in the kit's `choose`

`choose` builds three lists from the eligible resources (`level >= difficulty`) and returns at the first one
that is not empty:

1. `included`: available now and `cash == 0` (free and subscription alike), the minimum by
   `(allocation, level, id)`, so a free route (allocation 0) beats a subscription when both are up;
2. `waiting`: `cash == 0`, unavailable, `0 < reset_minutes <= deadline_minutes`, and only if `can_wait`;
3. `paid`: available with `cash <= budget`, the cheapest first;
4. otherwise abstain.

An exhausted free resource has `available == False`, so it can only be in `waiting`, never in `included`.
An available subscription (`cash == 0`, `allocation > 0`) is in `included`. Because `included` is tested
first, the subscription runs **before** the request is deferred to the free resource, even when the free
quota would refill well before the deadline. Checked on the unmodified kit function
(`python routing/priority_check.py`, output in [`routing/priority-check.jsonl`](../routing/priority-check.jsonl)):
free exhausted with reset 30 min, deadline 120 min, subscription up → `run subscription`; the same with
the subscription down → `defer free-exhausted, wake in 30`.

Why this order: both cost zero cash; the subscription answers now while waiting adds delay; reaching a reset
time does not prove the quota is back (the docstring asks to re-measure at wake-up); and subscription
allocation is already paid, so leaving it unused is lost value.

When to reverse it (wait for the free route first):
- the subscription allocation is scarce (close to its cap for the period) and must stay for urgent or
  high-stakes requests that cannot wait; spending it on a deferrable request would push a later urgent one
  to paid tokens or to abstention;
- the free route's model has the better TD1 record on the family (higher level for that difficulty);
- the request is a non-urgent batch (an internal dashboard refreshed overnight) and the refill comes well
  inside the deadline;
- the subscription bills overage beyond its allocation.
The reversal needs the remaining allocation and the refill to be measured, not assumed.

### Limits

Twenty questions, one sample per cell at temperature 0: the levels and panels are a hypothesis for this
batch, not a general error rate or a permanent ranking. Availability and refill times in the scenarios are
supplied, not measured. The L3 panel relies on two gpt-oss models; a shared error would pass its vote.
Questions where no free model is sufficient alone: C10, C15, C16, C17, C18, C19 (input for TD3).

### Replay

```bash
python routing/family_rates.py
python routing/quorum_check.py
python kit-td1/atelier-routage.py > routing/simulator-before.jsonl
python routing/atelier-routage.py > routing/simulator-after.jsonl
python routing/priority_check.py
```
