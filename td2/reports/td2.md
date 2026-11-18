# TD2 report --- DIA3 / DIA3-G5

Vote and route, 18 November 2026. No new model call: every figure comes from the TD1 traces
(`td1/traces-td1.csv`, `td1/model-question-comparison-en.csv`, `td1/reference-td1.csv`).

## Step 1 --- k-of-n vote (pair A)

We used the last real attempt per model and question from the merged TD 1 CSV, keeping unsuccessful attempts in the panel size. Both `correct` and `incorrect` rows can vote when they contain an executed value. We compared the decision with `reference-td1.csv` only after the vote. All amounts are in cents.

The fixed panel uses GPT-OSS 120B (Groq), North Mini Code (OpenRouter), and Qwen 27B (Groq). The five-model quorum adds GPT-OSS 20B (Groq) and Dots 3 Note (OpenRouter).

### Voting policy

1. Fix the panel before voting and use each member's last real attempt for the question. The two configurations use a strict majority of the full panel, with two votes out of three or three votes out of five. Reject thresholds outside `n // 2 < k <= n` and reject duplicate `(provider, model_requested)` pairs.
2. Count one vote for the exact integer value (in cents) of each executed proposal, including zero. Failed or unavailable members stay in the denominator and cast no vote.
3. Return a value only if it reaches the threshold, along with the vote count and agreeing members. Otherwise abstain, record the highest vote count (zero if there were no votes), and leave the value and agreeing-member list empty. There is no tie-break or fallback value.
4. Compare the result with the independent TD 1 reference only after the decision. A consensus can still be wrong, as the synthetic case with two votes for zero shows.

### Synthetic examples

| Example | Proposals | Decision | Reference | Matches |
| --- | --- | --- | ---: | --- |
| Agreement | 100, 100, 120 | 100 (2/3) | 100 | Yes |
| Disagreement | 100, 110, 120 | Abstain (best 1/3) | 100 | — |
| Unavailable | 100, unavailable, unavailable | Abstain (best 1/3) | 100 | — |
| Wrong consensus | 0, 0, 100 | 0 (2/3) | 100 | No |

### Comparison on the twenty TD 1 questions

| Question | Reference | 2-of-3 | Matches | 3-of-5 | Matches |
| --- | ---: | --- | --- | --- | --- |
| C01 | 792800 | 792800 (3/3) | Yes | 792800 (5/5) | Yes |
| C02 | 590320 | 590320 (2/3) | Yes | Abstain (best 2/5) | — |
| C03 | 936350 | 936350 (3/3) | Yes | 936350 (5/5) | Yes |
| C04 | 2826250 | 2826250 (3/3) | Yes | 2826250 (5/5) | Yes |
| C05 | 38480 | 38480 (3/3) | Yes | 38480 (5/5) | Yes |
| C06 | 0 | 0 (3/3) | Yes | 0 (5/5) | Yes |
| C07 | 13970 | 13970 (3/3) | Yes | 13970 (5/5) | Yes |
| C08 | 605580 | 605580 (2/3) | Yes | 605580 (3/5) | Yes |
| C09 | 487980 | 487980 (2/3) | Yes | 487980 (3/5) | Yes |
| C10 | 558980 | Abstain (best 1/3) | — | 558980 (3/5) | Yes |
| C11 | 446690 | 446690 (2/3) | Yes | Abstain (best 2/5) | — |
| C12 | 1666490 | 1666490 (3/3) | Yes | 1666490 (5/5) | Yes |
| C13 | 107740 | 107740 (3/3) | Yes | 107740 (5/5) | Yes |
| C14 | 0 | 0 (3/3) | Yes | 0 (5/5) | Yes |
| C15 | 168680 | Abstain (best 1/3) | — | Abstain (best 2/5) | — |
| C16 | 376740 | 376740 (2/3) | Yes | 376740 (4/5) | Yes |
| C17 | 258180 | Abstain (best 1/3) | — | Abstain (best 1/5) | — |
| C18 | 62480 | 62480 (2/3) | Yes | 62480 (3/5) | Yes |
| C19 | 1990 | Abstain (best 1/3) | — | Abstain (best 2/5) | — |
| C20 | 1106090 | 1106090 (3/3) | Yes | 1106090 (5/5) | Yes |

- **2-of-3** yielded 16 correct consensuses, 0 incorrect consensuses and 4 abstentions.
- **3-of-5** yielded 15 correct consensuses, 0 incorrect consensuses and 5 abstentions.

### Changes in the decision or vote count

- **C01**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 792800. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 792800. GPT-OSS 120B 792800 (`correct`), North Mini Code 792800 (`correct`), Qwen 27B 792800 (`correct`), GPT-OSS 20B 792800 (`correct`), Dots 3 Note 792800 (`correct`).
- **C02**. For 2-of-3, GPT-OSS 120B, Qwen 27B reach 2 for 590320. For 3-of-5, the largest bloc of 2 in the 5-model panel falls short of 3. GPT-OSS 120B 590320 (`correct`), North Mini Code 0 (`incorrect`), Qwen 27B 590320 (`correct`), GPT-OSS 20B 0 (`incorrect`), Dots 3 Note 135000 (`incorrect`).
- **C03**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 936350. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 936350. GPT-OSS 120B 936350 (`correct`), North Mini Code 936350 (`correct`), Qwen 27B 936350 (`correct`), GPT-OSS 20B 936350 (`correct`), Dots 3 Note 936350 (`correct`).
- **C04**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 2826250. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 2826250. GPT-OSS 120B 2826250 (`correct`), North Mini Code 2826250 (`correct`), Qwen 27B 2826250 (`correct`), GPT-OSS 20B 2826250 (`correct`), Dots 3 Note 2826250 (`correct`).
- **C05**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 38480. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 38480. GPT-OSS 120B 38480 (`correct`), North Mini Code 38480 (`correct`), Qwen 27B 38480 (`correct`), GPT-OSS 20B 38480 (`correct`), Dots 3 Note 38480 (`correct`).
- **C06**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 0. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 0. GPT-OSS 120B 0 (`correct`), North Mini Code 0 (`correct`), Qwen 27B 0 (`correct`), GPT-OSS 20B 0 (`correct`), Dots 3 Note 0 (`correct`).
- **C07**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 13970. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 13970. GPT-OSS 120B 13970 (`correct`), North Mini Code 13970 (`correct`), Qwen 27B 13970 (`correct`), GPT-OSS 20B 13970 (`correct`), Dots 3 Note 13970 (`correct`).
- **C08**. For 2-of-3, GPT-OSS 120B, Qwen 27B reach 2 for 605580. For 3-of-5, GPT-OSS 120B, Qwen 27B, Dots 3 Note reach 3 for 605580. GPT-OSS 120B 605580 (`correct`), North Mini Code 1188090 (`incorrect`), Qwen 27B 605580 (`correct`), GPT-OSS 20B 25920 (`incorrect`), Dots 3 Note 605580 (`correct`).
- **C09**. For 2-of-3, GPT-OSS 120B, Qwen 27B reach 2 for 487980. For 3-of-5, GPT-OSS 120B, Qwen 27B, GPT-OSS 20B reach 3 for 487980. GPT-OSS 120B 487980 (`correct`), North Mini Code 1901780 (`incorrect`), Qwen 27B 487980 (`correct`), GPT-OSS 20B 487980 (`correct`), Dots 3 Note 47900 (`incorrect`).
- **C10**. For 2-of-3, the largest bloc of 1 in the 3-model panel falls short of 2. For 3-of-5, GPT-OSS 120B, GPT-OSS 20B, Dots 3 Note reach 3 for 558980. GPT-OSS 120B 558980 (`correct`), North Mini Code 219930 (`incorrect`), Qwen 27B 119410 (`incorrect`), GPT-OSS 20B 558980 (`correct`), Dots 3 Note 558980 (`correct`).
- **C11**. For 2-of-3, GPT-OSS 120B, Qwen 27B reach 2 for 446690. For 3-of-5, the largest bloc of 2 in the 5-model panel falls short of 3. GPT-OSS 120B 446690 (`correct`), North Mini Code 768850 (`incorrect`), Qwen 27B 446690 (`correct`), GPT-OSS 20B 322160 (`incorrect`), Dots 3 Note 0 (`incorrect`).
- **C12**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 1666490. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 1666490. GPT-OSS 120B 1666490 (`correct`), North Mini Code 1666490 (`correct`), Qwen 27B 1666490 (`correct`), GPT-OSS 20B 1666490 (`correct`), Dots 3 Note 1666490 (`correct`).
- **C13**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 107740. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 107740. GPT-OSS 120B 107740 (`correct`), North Mini Code 107740 (`correct`), Qwen 27B 107740 (`correct`), GPT-OSS 20B 107740 (`correct`), Dots 3 Note 107740 (`correct`).
- **C14**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 0. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 0. GPT-OSS 120B 0 (`correct`), North Mini Code 0 (`correct`), Qwen 27B 0 (`correct`), GPT-OSS 20B 0 (`correct`), Dots 3 Note 0 (`correct`).
- **C15**. For 2-of-3, the largest bloc of 1 in the 3-model panel falls short of 2. For 3-of-5, the largest bloc of 2 in the 5-model panel falls short of 3. GPT-OSS 120B 168680 (`correct`), North Mini Code 314020 (`incorrect`), Qwen 27B 0 (`incorrect`), GPT-OSS 20B 168680 (`correct`), Dots 3 Note 138920 (`incorrect`).
- **C16**. For 2-of-3, GPT-OSS 120B, North Mini Code reach 2 for 376740. For 3-of-5, GPT-OSS 120B, North Mini Code, GPT-OSS 20B, Dots 3 Note reach 3 for 376740. GPT-OSS 120B 376740 (`correct`), North Mini Code 376740 (`correct`), Qwen 27B 208520 (`incorrect`), GPT-OSS 20B 376740 (`correct`), Dots 3 Note 376740 (`correct`).
- **C18**. For 2-of-3, GPT-OSS 120B, Qwen 27B reach 2 for 62480. For 3-of-5, GPT-OSS 120B, Qwen 27B, GPT-OSS 20B reach 3 for 62480. GPT-OSS 120B 62480 (`correct`), North Mini Code 67150 (`incorrect`), Qwen 27B 62480 (`correct`), GPT-OSS 20B 62480 (`correct`), Dots 3 Note 39580 (`incorrect`).
- **C19**. For 2-of-3, the largest bloc of 1 in the 3-model panel falls short of 2. For 3-of-5, the largest bloc of 2 in the 5-model panel falls short of 3. GPT-OSS 120B 1990 (`correct`), North Mini Code 71640 (`incorrect`), Qwen 27B 83580 (`incorrect`), GPT-OSS 20B 1990 (`correct`), Dots 3 Note 71640 (`incorrect`).
- **C20**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 1106090. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 1106090. GPT-OSS 120B 1106090 (`correct`), North Mini Code 1106090 (`correct`), Qwen 27B 1106090 (`correct`), GPT-OSS 20B 1106090 (`correct`), Dots 3 Note 1106090 (`correct`).

Code: `Orchestrateur.vote_k_sur_n` in [`kit-td1/skeleton-multi-llm-en.py`](../../kit-td1/skeleton-multi-llm-en.py) (from branch `td2-benchmarking-A`).
Driver that calls it on the twenty questions and the vote tests: [`td2/vote/vote_driver.py`](../vote/vote_driver.py)
(`python td2/vote/vote_driver.py`). It regenerates the table above ([`vote-table-td1.md`](../vote/vote-table-td1.md), identical
on all 20 rows) and writes [`voting-tests-en.csv`](../vote/voting-tests-en.csv): 14 tests (the four synthetic examples, duplicate
route, thresholds, unavailable members, invalid SQL on C17, C02), 14 pass. Added at the cross-review.

## Step 2 --- Wrong consensus (pair B)

Real case from our TD1 batch: on **C02** (customers aged exactly 25 on 2026-09-25), `openai/gpt-oss-20b` and `cohere/north-mini-code:free` both return **0**, against a reference of 590320. Full analysis (identification, faulty SQL clauses, delta query on `kit-td1/data/boutique.sqlite`, consequence for checking, link with Lecture 2): [`td2/wrong-consensus/case-C02.md`](../wrong-consensus/case-C02.md).

```bash
python td2/wrong-consensus/scan.py C02
python td2/wrong-consensus/run_sql.py td2/wrong-consensus/delta.sql
```

## Step 3 --- Routing rule (pair C)

### The rule

One page: [`td2/routing/routing-rule-td2.md`](../routing/routing-rule-td2.md). In short:

| Family (difficulty) | First model | Dashboard / customer figure / payout |
|---|---|---|
| F1 period, F3 product list (L1) | Cohere free (10/10 L1 cells) | none / 2-of-3 panel L1 / reference SQL + review |
| F2 completed age at a date (L2) | gpt-oss-120b free (4/4 on C02, C08, C09, C11) | none / 2-of-3 panel L2 / reference SQL + review |
| F2b age at the order, F4 combinations (L3) | 2-of-3 panel (20b, 120b, Dots): no single model is correct on all of C10, C15-C19 | vote / vote + reference SQL / reference SQL + review |

Per-family TD1 rates: [`td2/routing/family-rates-td1.md`](../routing/family-rates-td1.md). Every 2-of-3 panel
replayed on the TD1 traces: [`td2/routing/quorum-check-td1.md`](../routing/quorum-check-td1.md).

### Simulator before adaptation (kit rule, `python kit-td1/atelier-routage.py`)

Full output: [`td2/routing/simulator-before.jsonl`](../routing/simulator-before.jsonl).

| Scenario | Action | Resource | Cash | Reason |
|---|---|---|---|---|
| simple | run | small-free | 0 | eligible included capacity |
| complex | run | senior-subscription | 0 | eligible included capacity |
| deferrable | defer 60 min | senior-subscription | 0 | recheck availability at wake-up |
| urgent | run | senior-api | 0.30 | available route within the authorised budget |
| budget exhausted | abstain | --- | 0 | no eligible resource within deadline and budget |
| high impact | run | senior-subscription | 0 | eligible included capacity (checks: source verification and human review) |
| unknown capability | abstain | --- | 0 | no eligible resource within deadline and budget |

### Simulator after adaptation (our rule, `python td2/routing/atelier-routage.py`)

The kit file is left byte-identical (its SHA-256 is in `kit-td1/manifest.json`); the adapted copy is
`td2/routing/atelier-routage.py`. Changes:
- `RESOURCES`: the five TD1 models on their free routes (level from TD1, billed-equivalent cost), the
  billed OpenRouter route of gpt-oss-120b (0.000207 USD per request), and the L3 panel as one resource
  (available only when its three members are).
- `choose`: same order as the kit (included, then wait, then paid, then abstain), "filter then cheapest"
  with ties broken by billed-equivalent cost; `stakes` (dashboard / customer / payout) sets the check;
  waiting is capped at 10 attempts, 1 min apart (lecture retry policy); every reason cites TD1 cells.

Full output: [`td2/routing/simulator-after.jsonl`](../routing/simulator-after.jsonl).

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
(`python td2/routing/priority_check.py`, output in [`td2/routing/priority-check.jsonl`](../routing/priority-check.jsonl)):
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
python td2/routing/family_rates.py
python td2/routing/quorum_check.py
python kit-td1/atelier-routage.py > td2/routing/simulator-before.jsonl
python td2/routing/atelier-routage.py > td2/routing/simulator-after.jsonl
python td2/routing/priority_check.py
```

## Internal cross-review

Each pair's work was replayed and recomputed independently by another pair, from the TD1 traces:
- by pair B, of pairs A and C: [`../cross-review/cross-review-td2.md`](../cross-review/cross-review-td2.md);
- by pair C, of pairs A and B, with pair C's answer to pair B's remarks:
  [`../cross-review/cross-review-pair-c.md`](../cross-review/cross-review-pair-c.md).

Both reviews find the three steps correct and reproducible; their remaining remarks are listed there.

## Contributions

Seven members: three pairs, pair C as a group of three (assignment: groups of three beyond six members).

| Pair | Members | Step | Work and evidence |
|---|---|---|---|
| A | Raphaël, Florentin | 1. k-of-n vote | `vote_k_sur_n` in `kit-td1/skeleton-multi-llm-en.py`, four synthetic examples, 20-question table 2-of-3 against 3-of-5 (step 1 above) |
| B | Matéo, Thomas | 2. Wrong consensus | C02 found in the 100 cells, faulty SQL clauses, delta query, votes counted by hand ([`../wrong-consensus/`](../wrong-consensus/case-C02.md)); cross-review of pairs A and C |
| C | Christophe, Pierre-Louis, Robin | 3. Routing rule | TD1 rates per family and level, one-page rule, adapted simulator, priority analysis ([`../routing/`](../routing/routing-rule-td2.md)); cross-review of pairs A and B |

Written cross-reviews: pair B reviewed pairs A and C, pair C reviewed pairs A and B (section above).

## Successes and failures

**Successes**
- The vote abstains rather than inventing a value: on the 20 questions, 0 wrong consensus for both the
  fixed 2-of-3 panel (16 correct, 4 abstentions) and 3-of-5 (15 correct, 5 abstentions).
- A real wrong consensus is proven in SQL: on C02, gpt-oss-20b and Cohere both return 0 for two
  different bugs; the delta query finds the 6 customers aged 25 that both miss (590320 cents).
- Every model choice of the routing rule cites its TD1 cells, and every check matches the cost of an
  error (dashboard, customer figure, payout).
- The two cross-reviews recomputed each pair's numbers from the TD1 traces with their own code: all
  figures match and every output is reproducible.

**Failures and open points**
- Pair A's branch `td2-benchmarking-A` had no common history with `master` and would have deleted the
  TD1 files; its two changes were carried over by hand. It must not be merged.
- C17 is missing from pair A's "Changes" list, and C19 (71640 shared by Cohere and Dots) is found but
  not analysed.
- No single model is correct on all six hardest questions (C10, C15-C19); the routing rule needs a
  2-of-3 panel there, and that panel holds two gpt-oss models on the same provider (Groq).

## Causes and hypotheses

- 24 of the 25 TD1 failures break the completed-age convention: age questions are the weak point of
  every model. Hypothesis: the models compute an age from the year difference or a wrongly placed
  date window instead of the anniversary rule given in the prompt.
- Two models can return the same wrong value for different reasons (C02: a window shifted by 25 years,
  and two reversed comparisons). A vote only sees the value, so a quorum cannot detect it.
- A higher threshold (3-of-5) only adds abstentions on questions with an age filter (C02, C11, C15, C17,
  C19): it protects against a wrong answer but does not produce the right one.

## Limits

Twenty questions, one sample per cell at temperature 0, one batch per model: the rates, levels and
panels are a hypothesis for this batch, not a general error rate, a permanent ranking or a guarantee
from quorum voting. Availability and refill times in the routing scenarios are supplied, not measured.
The synthetic examples of step 1 and the simulator scenarios of step 3 are labelled as simulations.

## Prompts

No new model call in TD2. The experiment prompt is unchanged since TD1 ([`../../td1/prompts-en.md`](../../td1/prompts-en.md)).

## Step 4 --- plenary note

Questions where no single free model is sufficient alone in our batch: C10, C15, C16, C17, C18, C19
(age at the order, and age combined with other filters). They need a 2-of-3 panel or the reference SQL,
and they set the cost of checking for TD3.

## Next steps (TD3)

- Configuration table: cheapest single model per family, best single model, fixed 2-of-3, 3-of-5 and our
  routing rule, with calls, tokens and API-equivalent cost (N/A with coverage for Cohere and Dots).
- Price the check of C10 and C15-C19 (panel calls, reference SQL, human review).
- Apply the cross-review remarks: C17 in pair A's list, analysis of C19, version numbers on the voting
  policy and the routing rule, a provider-diverse fallback for the L3 panel.
