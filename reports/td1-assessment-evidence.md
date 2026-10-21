# TD1 assessment evidence (R1, R2, R3)

What we show for each TD1 outcome of the assessment sheet, with the exact file and line behind each claim.
Trace rows are identified by `cell_id` and `attempts` in [`traces-td1.csv`](../traces-td1.csv) (all rows
`nature = real`; no replayed or synthetic example is used for R1-R3).

## R1 --- An independent, checked reference

**On screen:** [`reference-td1.csv`](../reference-td1.csv), twenty rows, each with the query that produced its value.

**Conventions, applied in every query** (protocol section 1, repeated in the prompt):

| Convention | How the query applies it | Where it matters |
|---|---|---|
| Period closed left, open right | `o.date >= 'S' AND o.date < 'E'` on the text timestamps | Orders at `2026-03-01 00:00:00` count in C01; the order at `2026-06-01 00:00:00` is out of C01 and C07 but in C05 and C20; the order at `2026-05-31 23:59:59` is in C07 |
| Completed age from month and day | `year(ref) - year(birth) - (strftime('%m-%d', ref) < strftime('%m-%d', birth)) = 25` | Customers born 2001-09-24, 2001-09-25 and 2001-09-26 make C02, C08 and C09 three different values |
| Age at the time of the order | Same formula with `o.date` instead of the reference date | C10, C18 |
| Product list | `o.product_id IN ('a', 'b', 'c')` (C13: `'a', 'c'`; C19: `'d'`) | C03, C12-C14, C16, C17, C19 |
| Amount | `COALESCE(SUM(o.quantity_product * p.price), 0)`, integer cents excluding VAT | C06 (no order in 2025) and C14 (none in Oct-Nov 2026) are 0, not NULL |

Worked example, C02 (reference date 2026-09-25): the six customers aged exactly 25 are born between
2000-09-26 and 2001-09-25 (C005, C007, C009, C008, C002, C001); their orders total 590320.

**Independent checks:**

- The value of each query is recomputed without SQL, in pure Python on `orders.csv`, `customers.csv` and
  `product.csv`, by [`references/compute_references.py`](../references/compute_references.py): 20/20 equal.
- Members wrote their own queries separately: C01-C04 by Robin
  ([`crosscheck-C01-C04.md`](../references/crosscheck-C01-C04.md)), C05-C08 by Raphaël
  ([`refs-raph.csv`](../references/refs-raph.csv), with a pure-Python check in
  [`check_raph.py`](../references/check_raph.py)), C09-C12 by Thomas
  ([`crosscheck-C09-C12.md`](../references/crosscheck-C09-C12.md)): all equal.
- The instructor compared the twenty values with the answer key before any model call: no difference, first
  attempt.
- No reference comes from a model: the twenty values were fixed before the first batch (first trace row
  2026-10-21 12:39:38 UTC).

## R2 --- One trace line per call

**Selected trace: Qwen on C06** (`cell_id = groq:qwen/qwen3.8-27b:C06`), two rows in `traces-td1.csv`:

| attempts | date_utc | http_status | verdict | sql / value | tokens_prompt / completion | latency_ms |
|---|---|---|---|---|---|---|
| 1 | 2026-10-21 12:39:55 | 429 | `not_executed` | empty / empty | empty / empty | 97.1 |
| 2 | 2026-10-21 12:40:11 | 200 | `correct` | period query / 0 | 630 / 95 | 493.4 |

- **Why two rows:** the first call was refused by Groq, `error` = "Rate limit reached ... on output tokens per
  minute"; the skeleton retried the cell once (its maximum) and the retry succeeded. Both attempts stay in the
  trace; the final result is the last attempt.
- **Common fingerprint:** both rows carry `prompt_sha256 = e10af719...923258`, the same as the four other
  models' rows for C06. Across the 106 rows there are exactly 20 distinct fingerprints, one per question: every
  model received the same system message and user template ([`prompts-en.md`](../prompts-en.md)), so a gap
  between models is attributable to the model, not to the wording.
- **Missing measurement versus zero:** on attempt 1 the tokens are empty because no answer came back, not
  because zero tokens were used. `cost_native` is empty on every Groq row (the provider does not return it) but
  `0` on every OpenRouter row (a value the provider returned for its free route). `tokens_reasoning` is empty
  for Qwen (reasoning disabled, not reported) and `0` for Cohere and Dots (reported as zero).
- **One row per call, written automatically:** the five operator files in [`traces/raw/`](../traces/raw/) are
  kept unmodified; [`traces/merge_traces.py`](../traces/merge_traces.py) checks each CSV against its JSONL state
  file and merges them ([`traces/merge-report.md`](../traces/merge-report.md): 100/100 cells, 6 retries, no
  blocking problem). Six retries in total, all after HTTP 429 on Groq: B on C19 and C20, D on C06, C18, C19
  and C20 ([`traces/run-log-td1.csv`](../traces/run-log-td1.csv)).

## R3 --- The cause of a failure, read from the trace

**Wrong answer: gpt-oss-120b on C17** (`cell_id = groq:openai/gpt-oss-120b:C17`, attempt 1, HTTP 200,
`verdict = incorrect`, value 80190, reference 258180). The returned SQL filters the period and the products
correctly, then ends with `c.birth_date = DATE('2026-09-25', '-25 years')`: it keeps only customers born on
2001-09-25 (customer C001) instead of everyone whose completed age is 25 on that date (born 2000-09-26 to
2001-09-25, six customers). The call worked; the convention was broken.

**Failed access: Qwen on C06, attempt 1** (above): HTTP 429, no SQL, no value, `verdict = not_executed`. The
model never answered, so nothing can be said about its reasoning on that attempt; the cause is the provider's
rate limit on the free plan, read from `http_status` and `error`. It is not counted as a wrong answer, and the
retry shows the model answers correctly once access is granted.

**Invalid SQL, a third category: Dots on C17** (attempt 1, HTTP 200, `verdict = sql_invalid`): the query
contains `CAST((STRFTIME('%Y', '2026-09-25') AS INTEGER)`, a misplaced parenthesis; the sandbox reports
`syntax error near "AS"` and no value is produced.

All 25 failing cells carry their cause in the `explanation` column of
[`model-question-comparison-en.csv`](../model-question-comparison-en.csv): 24 break the completed-age
convention, 1 is invalid SQL; the 6 access failures were all recovered by their retry.
