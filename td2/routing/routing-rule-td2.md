# Routing rule --- DIA3-G5, TD2 step 3 (pair C)

Rates: [`family-rates-td1.md`](family-rates-td1.md). Panel replays: [`quorum-check-td1.md`](quorum-check-td1.md).
Machine form read by the simulator: [`routing-rule.json`](routing-rule.json). The rule applies the four lecture
factors in order (**difficulty → minimum level, stakes → check, deadline → wait or pay, budget → which paid
route**), then "filter then cheapest". Twenty questions support a hypothesis for this batch only: not a general
error rate, not a permanent ranking, not a guarantee from quorum voting.

**Difficulty.** L1 = F1 period + F3 product list (all 50 model-cells correct in TD1). L2 = F2 completed age at
a date (10/20 model-cells correct). L3 = F2b age at the order (3/5, one cell only, age moves with each order date)
and F4 combinations (12/25 correct). **Model level** = highest L with every TD1 cell up to L correct: Cohere,
Dots, gpt-oss-20b = L1; gpt-oss-120b, Qwen = L2; **no single model reaches L3**.

**Cheapest.** Every TD1 route was free. Ties on cash are broken by the billed-equivalent cost of one request
(dated price × median TD1 tokens): Cohere and Dots 0 (free-only route), gpt-oss-20b 0.000106, gpt-oss-120b
0.000207, Qwen 0.000984 USD.

| Family (TD1 cells) | L | Rate 120b / 20b / Cohere / Qwen / Dots | First model | Check: dashboard / customer figure / payout | If unavailable |
|---|---|---|---|---|---|
| **F1 period** (C01, C04, C05, C06, C07, C20) | 1 | 6/6 / 6/6 / 6/6 / 6/6 / 6/6 | Cohere free (L1, 10/10 L1 cells, 0 USD) | none / 2-of-3 panel L1 (Cohere, Dots, 20b: 10 correct, 0 wrong) / reference SQL re-run by code + human review if different | Dots, then 20b (other provider), 120b, Qwen; else defer ≤ 10 × 1 min; else billed 120b within budget; else abstain |
| **F3 product list** (C03, C12, C13, C14) | 1 | 4/4 / 4/4 / 4/4 / 4/4 / 4/4 | Cohere free (as F1) | as F1 | as F1 |
| **F2 completed age at a date** (C02, C08, C09, C11) | 2 | 4/4 / 1/4 / 0/4 / 4/4 / 1/4 | gpt-oss-120b free (L2, 14/14 cells up to L2) | none / 2-of-3 panel L2 (120b, Qwen, Dots: 4 correct, 0 wrong) / reference SQL + review | Qwen (L2); else defer ≤ 10 × 1 min; else billed 120b (0.000207 USD); else abstain. Never an L1 model alone |
| **F2b age at the order** (C10) | 3 | 1/1 / 1/1 / 0/1 / 0/1 / 1/1 | panel L3, first call gpt-oss-20b (1/1, cheapest) | panel vote / vote + reference SQL / reference SQL + review | defer the panel ≤ 10 × 1 min; else abstain |
| **F4 combinations** (C15-C19) | 3 | 4/5 / 5/5 / 1/5 / 1/5 / 1/5 | panel L3, first call gpt-oss-20b (5/5, cheapest) | panel vote / vote + reference SQL / reference SQL + review | as F2b |
| Unseen family | 4 | no cell | none | --- | abstain |

**Panel L3** = gpt-oss-20b, gpt-oss-120b, Dots (2 of 3, strict majority). On the 20 TD1 cells it is never wrong:
L1 10 correct; L2 2 correct, 2 abstain (C02, C11); L3 5 correct, 1 abstain (C17: 258180, 80190, invalid SQL).
Among the ten 2-of-3 panels, only those holding both gpt-oss models reach 5 correct and 0 wrong on L3; Dots is
the third member because it is 1/1 on C10, free, and on another provider (OpenRouter).

**Consistency.** "None" appears only for the dashboard and only for a model correct on 100 % of its family
(F1, F3 for L1 models; F2 for gpt-oss-120b). F2b rests on one cell and every model misses at least one L3 cell,
so L3 always votes. A customer figure gets a quorum (plus the reference SQL at L3); a payout always gets the
deterministic check by code and human review.

**Vote hygiene (lecture).** A value counts only with its SQL; refused calls (429) and broken SQL stay in n
without a vote; one vote per model, final attempt; values normalised by code before the vote.

**Unavailability.** TD1 saw six HTTP 429 (output tokens per minute) on Groq, all served on retry. Rule: take the
next eligible model that is up now; if none, wait for the free quota (up to 10 attempts, 1 min apart, availability
re-measured at wake-up), then the billed route within budget, then abstain.

**Risks kept.** The L3 panel holds two models of the same family (gpt-oss): a shared error would pass the vote,
hence the reference SQL for customer figures and payouts. A higher threshold (3-of-5) would only add abstentions.
A new model joins in shadow mode (logged, no vote) until it has its own TD1-style record. **No free model is
sufficient alone on C10 and C15-C19**: these set the cost of checking in TD3.

Scenario outputs: [`simulator-before.jsonl`](simulator-before.jsonl) (kit rule) and
[`simulator-after.jsonl`](simulator-after.jsonl) (this rule, `td2/routing/atelier-routage.py`).
