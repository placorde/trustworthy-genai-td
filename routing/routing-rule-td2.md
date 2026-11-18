# Routing rule --- DIA3-G5, TD2 step 3 (pair C)

Machine-readable form read by the simulator: [`routing-rule.json`](routing-rule.json). Rates:
[`family-rates-td1.md`](family-rates-td1.md) (from `model-question-comparison-en.csv`, final TD1 attempts).
Cost basis: every TD1 route is free (Groq Free plan, OpenRouter `:free`); "cheapest" is ranked by the dated
billed price of the same model (gpt-oss-20b 0.075/0.30 < gpt-oss-120b 0.15/0.60 < Qwen 0.80/4.00 USD per
million tokens), Cohere and Dots last (free route only, no documented paid price: N/A). Twenty questions
support a hypothesis for this batch, not a general error rate, a permanent ranking or a quorum guarantee.

## Rule

| Family (TD1 cells) | TD1 rate per model: 120b / 20b / Cohere / Qwen / Dots | First model | Check: dashboard / customer figure / payout | If unavailable |
|---|---|---|---|---|
| **F1 period** (C01, C04, C05, C06, C07, C20) | 6/6 / 6/6 / 6/6 / 6/6 / 6/6 | gpt-oss-20b (Groq), cheapest at 6/6 | none / 2-of-3 fixed panel / 3-of-5 + reference SQL template, review if they differ | 120b, Qwen, then Cohere, Dots (other provider); defer if the Groq quota refills before the deadline; abstain |
| **F2 completed age at a date** (C02, C08, C09, C11) | 4/4 / 1/4 / 0/4 / 4/4 / 1/4 | gpt-oss-120b (Groq), cheapest at 4/4 | none / 2-of-3 (120b, Qwen, Cohere: needs both 4/4 models) / reference age SQL + review; 3-of-5 never (three models at 0-1/4) | Qwen; defer; billed 120b on OpenRouter within budget; abstain. Never a model below 4/4 |
| **F2b age at the order** (C10) | 1/1 / 1/1 / 0/1 / 0/1 / 1/1 | gpt-oss-20b, cheapest at 1/1 | 2-of-3 (20b, 120b, Dots) for every use: one cell only / + reference SQL / reference SQL + review | 120b, Dots; defer; abstain |
| **F3 product list** (C03, C12, C13, C14) | 4/4 / 4/4 / 4/4 / 4/4 / 4/4 | gpt-oss-20b, cheapest at 4/4 | none / 2-of-3 fixed panel / 3-of-5 + reference SQL template, review if they differ | as F1 |
| **F4 combinations** (C15-C19) | 4/5 (C17) / 5/5 / 1/5 / 1/5 / 1/5 | gpt-oss-20b, cheapest at 5/5 | 2-of-3 (20b, 120b, Qwen), abstain without majority / + reference SQL / reference SQL + review | 120b; defer; abstain |
| Unseen family (no TD1 cell) | --- | none | --- | abstain |

**Consistency constraint applied.** "None" appears only for the dashboard on F1, F2 and F3, where the first
model is 100 % in TD1. F2b is 1/1 on a single cell and F4 mixes filters, so they always vote. A customer
figure or a payout always gets a quorum or a deterministic check.

**Judgement on F4.** gpt-oss-20b is 5/5 on combinations but 1/4 on pure age questions, although every
combination holds an age filter: five cells are too few to trust it alone, so it is first only inside a quorum.
Replayed on the TD1 traces, the rule's quorums give 19 correct, 1 abstention (C17: 258180, 80190, 248490, no
majority) and 0 wrong answers ([`quorum-check-td1.md`](quorum-check-td1.md)).

**Unavailability.** Observed in TD1: six Groq calls returned HTTP 429 on output tokens per minute and all
succeeded on retry. The rule defers to the same free model when its quota refills before the deadline
(rechecking at wake-up), uses the next model of the family order otherwise, then the billed route of the same
model within budget, then abstains.

## Scenario outcomes (simulator after adaptation)

| ID | Situation (simulator scenario) | Selected action | Reason tied to the rule | Evidence or explicit assumption |
|---|---|---|---|---|
| R1 | Ordinary F1 question, dashboard (`simple`) | run gpt-oss-20b free | first of F1, check none | 20b 6/6 on C01, C04, C05, C06, C07, C20 |
| R2 | Groq down, F1 (`provider unavailable`) | run Cohere free | next eligible on another provider | Cohere 6/6 on F1 |
| R3 | F2 customer figure, Groq free quota exhausted, refill in 1 min (`deferrable`) | defer gpt-oss-120b, wake in 1 min | free quota refills before the deadline | 120b 4/4 on C02, C08, C09, C11; refill time assumed from the TD1 429 retries |
| R4 | Same, urgent (`urgent`), then budget 0 (`budget exhausted`) | run billed 120b (0.00021 USD); abstain | same model on a billed route; nothing eligible within budget | 0.15/0.60 USD per M tokens x 638/185.5 median TD1 tokens |
| R5 | F4 payout (`high impact`) | run gpt-oss-20b, deterministic check + review | high consequence: a quorum agreeing is not enough | 20b 5/5 on C15-C19; wrong consensus possible (C02, C19 in TD1) |
| --- | F2b dashboard (`age at the order`); unseen family F5 (`unknown capability`) | run 20b with 2-of-3; abstain | one TD1 cell; no evidence | 20b 1/1 on C10; no cell |

Outputs: [`simulator-before.jsonl`](simulator-before.jsonl) (supplied rule, 7 scenarios) and
[`simulator-after.jsonl`](simulator-after.jsonl) (our rule, 9 scenarios); every reason string cites its TD1 cells.

## Priority order in the supplied `choose`

`choose` tests three lists in a fixed order and returns at the first non-empty one: (1) `included`, every
eligible resource that is available now with `cash == 0` (free and subscription alike, ranked by allocation,
so a free route beats a subscription when both are up); (2) `waiting`, eligible resources with `cash == 0` that
are unavailable but reset before `deadline_minutes`, only if the request `can_wait`; (3) `paid`, available
routes whose `cash` fits the budget; else abstain. So an available subscription (`cash == 0`,
`allocation > 0`) is chosen **before** deferring to an exhausted free route that would refill in time
(checked: free exhausted with reset 30 min, subscription up gives `run senior-subscription`; with the
subscription gone the same request gives `defer free-senior`).

Why: both cost zero cash, but the subscription answers now, while waiting adds delay and is not guaranteed
(the docstring: reaching a reset time does not prove capacity is back); the subscription is already paid, so
unused allocation is lost value.

When to reverse it: when the subscription allocation is scarce and has an opportunity cost, i.e. it is close to
its cap or reserved for urgent or high-impact requests that cannot wait, and the request is deferrable with a
refill well inside its deadline. Then consuming the allocation now would force a later urgent request onto
paid tokens or into abstention, so deferring to the free route is cheaper overall. The reversal needs the
remaining allocation to be measured, not assumed.
