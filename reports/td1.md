# TD1 report --- compare

Session of 21 October 2026. Pack `2026-10-14-students-1`. Every figure below comes from the files of this
repository; all trace rows are of nature `real` (no replayed or simulated row was used).

## What we attempted and what we completed

- **Step 1, references.** Twenty SQLite queries returning one `revenue_cents` column, executed on
  `data/boutique.sqlite` opened read-only: [`reference-td1.csv`](../reference-td1.csv), produced by
  [`references/compute_references.py`](../references/compute_references.py), which also recomputes each value in
  pure Python on the three CSV files (20/20 equal). Independent cross-checks by members: C01-C04 (Robin,
  [`crosscheck-C01-C04.md`](../references/crosscheck-C01-C04.md)), C05-C08 (Raphaël,
  [`refs-raph.csv`](../references/refs-raph.csv)), C09-C12 (Thomas,
  [`crosscheck-C09-C12.md`](../references/crosscheck-C09-C12.md)). The instructor confirmed the twenty values
  against the answer key before any model call.
- **Step 2, the five models.** 100 base cells, one operator at a time, each with their own state file:
  60 initial Groq calls (A, B, D) and 40 initial OpenRouter calls (C, E), plus 6 retries. All attempts are
  merged in [`traces-td1.csv`](../traces-td1.csv) / [`traces-td1.jsonl`](../traces-td1.jsonl) (106 rows) from the
  unmodified operator files in [`traces/raw/`](../traces/raw/). The merge check
  ([`traces/merge-report.md`](../traces/merge-report.md)) reports 100/100 cells, one prompt fingerprint per
  question, trace references equal to `reference-td1.csv`, at most one retry per cell: no blocking problem.
- **Step 3, summaries.** [`model-question-comparison-en.csv`](../model-question-comparison-en.csv) (100 rows,
  one cause per failure), [`five-model-summary-en.csv`](../five-model-summary-en.csv) (five rows), and the
  models x questions view [`results-pivot-td1.md`](../results-pivot-td1.md) generated from the comparison CSV.
- **Prompt.** System message and user template exactly as used: [`prompts-en.md`](../prompts-en.md); the C01
  fingerprint recomputed from that file (`d25f6373...b1bdd`) equals the `prompt_sha256` of every C01 trace row.

## What worked

| Model (operator) | Correct (final attempt) | Pure period (6) | Pure age (5) | Pure product (4) | Combined (5) |
|---|---|---|---|---|---|
| `groq:openai/gpt-oss-120b` (A) | 19/20 | 6/6 | 5/5 | 4/4 | 4/5 |
| `groq:openai/gpt-oss-20b` (B) | 17/20 | 6/6 | 2/5 | 4/4 | 5/5 |
| `groq:qwen/qwen3.8-27b` (D) | 15/20 | 6/6 | 4/5 | 4/4 | 1/5 |
| `openrouter:dots-studio/dots-3-note-preview:free` (E) | 13/20 | 6/6 | 2/5 | 4/4 | 1/5 |
| `openrouter:cohere/north-mini-code:free` (C) | 11/20 | 6/6 | 0/5 | 4/4 | 1/5 |

Source: [`results-pivot-td1.md`](../results-pivot-td1.md) and the `*_results` columns of
[`five-model-summary-en.csv`](../five-model-summary-en.csv).

- Every model is correct on every pure period question (including the boundary orders at
  `2026-03-01 00:00:00`, `2026-05-31 23:59:59` and `2026-06-01 00:00:00`) and on every pure product question,
  including the two empty results (C06, C14) where all models returned 0 and not NULL.
- Every model returned the exact model requested (`model_returned` = `model_requested` on all 100 cells).
- Every model produced runnable SQL on 99 of its 100 cells; only one query failed to parse.

## What failed or remains incomplete

**Wrong answers (observed in the returned SQL).** 25 of the 100 final cells are not correct. 24 are
`incorrect` and all of them break the completed-age convention; the period and product filters in those
queries are right. Recurrent patterns, each cited in the `explanation` column of the comparison CSV:

- keeping only the customers born exactly on the reference date minus 25 years
  (A C17, B C08, E C02, E C09);
- a birth-date window shifted or of the wrong width (B C02, B C11);
- contradictory or always-true conditions (C C02 and D C15 give 0; C C08 and C C11 keep ages 0-25);
- an off-by-one on the anniversary or a year difference of 24/26 swapped (D C10, D C16, D C17, E C18);
- no age bound at all (C C09, C C19, D C19, E C19).

The 25th failure is `sql_invalid`: Dots on C17 returned `CAST((STRFTIME(...) AS INTEGER)`, a misplaced
parenthesis; the sandbox reports `syntax error near "AS"` and no value.

**Access failures (observed in the HTTP status), distinct from wrong answers.** Six first attempts on Groq
ended with HTTP 429 and an empty answer: B on C19 and C20, D on C06, C18, C19 and C20. The provider message
names the limit: output tokens per minute, 1000 on the Free plan. The skeleton retried each cell once; all six
retries returned HTTP 200 (five correct, D C19 incorrect). These rows have `verdict = not_executed`, no SQL and
empty token counts. Hypothesis, not verified: with a 3-second pause, about 20 requests per minute of 100 to 250
output tokens each exceed 1000 output tokens per minute on the later questions of a batch.

**Shared wrong values.** On C02, gpt-oss-20b and Cohere both return 0 (reference 590320); on C19, Cohere and
Dots both return 71640 (reference 1990). Both are candidates for the wrong-consensus analysis of TD2; in each
case the two models reach the same value by different wrong SQL.

**Open points recorded at hand-in.**

- Remaining account allowances before and after each batch were not written down at run time, and the traces
  carry no account counter: they are `N/A` with that reason in
  [`traces/run-log-td1.csv`](../traces/run-log-td1.csv). Calls, retries and incidents per operator are filled
  from the traces.
- References C13-C20 have no cross-check file from a member in the repository; they rest on the pure-Python
  recomputation and the instructor's confirmation against the answer key.
- The causes for models B-E were drafted with coding assistance (declared in `prompts-en.md`); G (Florentin) checks them
  against the returned SQL before the hand-in commit.

## Decisions, limits and uncertainty

- **Measurements.** Missing is not zero: `tokens_prompt` and `tokens_completion` are empty on the six HTTP 429
  rows (no answer); `cost_native` is empty on all Groq rows (not returned) and `0` on all OpenRouter rows (a value
  returned by the provider for the free route). Median latency on HTTP 200 calls: about 0.5-0.9 s on Groq and
  3.2-3.6 s on OpenRouter.
- **Prices and index.** gpt-oss-120b, gpt-oss-20b and Qwen have a public index (portfolio snapshot of
  28 September 2026) and dated billed prices for the same model (Groq Developer, 5 October 2026). Cohere North
  Mini Code and Dots 3 Note Preview are absent from the snapshot and have no documented paid route for the exact
  same model: index and prices are N/A with that reason, not zero.
- **Scope.** One sample per cell at temperature 0, twenty questions on one small database. The counts above
  describe this batch; they support a routing hypothesis (any of the five models is enough for period and
  product questions here; age questions need gpt-oss-120b or a check), not a general error rate or a permanent
  ranking.
- **Prompt.** Unchanged during the session; no second experiment was started.

## Assessment evidence

The evidence shown for R1, R2 and R3 (conventions, independent checks, the selected trace with its
retry and fingerprint, a wrong answer versus a failed access) is gathered with file and row references in
[`td1-assessment-evidence.md`](td1-assessment-evidence.md).

## Division of labour

| Member | Role in TD1 |
|---|---|
| A, Robin | Batch gpt-oss-120b (Groq); cross-check C01-C04; comparison and summary rows of his model |
| B, Raphaël | Batch gpt-oss-20b (Groq); cross-check C05-C08 |
| C, Thomas | Batch Cohere North Mini Code (OpenRouter); cross-check C09-C12 |
| D, Matéo | Batch Qwen 3.8 27B (Groq) |
| E, Christophe | Batch Dots 3 Note Preview (OpenRouter) |
| F + H, Pierre-Louis | Reference queries; validation with the instructor; run coordination and counting; trace merge and checks; comparison rows and causes B-E; summary rows B-E; repository organisation |
| G, Florentin | Review of the five-model summary and comparison; pivot for the plenary |

Details and cross-checkers: [`contributions-en.csv`](../contributions-en.csv).

## Next steps / help needed

- From TD2 on, each operator writes their remaining allowance in the run log before and after any call.
- TD2: complete `vote_k_sur_n`, run `atelier-vote.py --traces traces-td1.csv` on the twenty questions, and use
  C02 or C19 for the wrong-consensus case; note that Cohere is in the fixed panel, Dots is not.
- TD2 routing rule: start from the per-family results above (period and product: cheapest model; age: quorum
  or reference check).

---
Pack version used: `2026-10-14-students-1`. Commit of this report: the commit tagged `td1-submission`; its full hash is recorded in the Moodle hand-in entry.
