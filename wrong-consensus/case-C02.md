# Wrong consensus C02 --- DIA3-G5, TD2 step 2 (pair B)

**Nature of the case:** real case from our own TD1 batch (`traces-td1.csv`, merged traces), not a
synthetic or supplied example.

**Question C02:** revenue excluding VAT, in euro cents, of the orders of customers aged exactly 25
(completed years) on 2026-09-25. Reference (`reference-td1.csv`): **590320**.

Found with `python wrong-consensus/scan.py`, details with `python wrong-consensus/scan.py C02`.
Each model has a single attempt on C02, so that attempt is its final one.

## 1. Identification and quorum verdict

| Model | In the fixed 2-of-3 panel? | Verdict | Value (cents) |
|---|---|---|---|
| openai/gpt-oss-120b (Groq) | yes | correct | 590320 |
| cohere/north-mini-code:free (OpenRouter) | yes | incorrect | **0** |
| qwen/qwen3.8-27b (Groq) | yes | correct | 590320 |
| openai/gpt-oss-20b (Groq) | no | incorrect | **0** |
| dots-studio/dots-3-note-preview:free (OpenRouter) | no | incorrect | 135000 |

**Shared wrong value:** `0`, returned by `openai/gpt-oss-20b` and `cohere/north-mini-code:free`
(two models from two different families and providers). Reference: 590320.

### Vote count (by hand, to be checked against pair A's `vote_k_sur_n`)

**Fixed 2-of-3 panel** (n = 3, k = 2: gpt-oss-120b, north-mini-code, qwen3.8-27b)

| Value | Votes | Models |
|---|---|---|
| 590320 | 2 | gpt-oss-120b, qwen3.8-27b |
| 0 | 1 | north-mini-code |

Result: **consensus 590320 (2/3), correct**. The shared wrong value is **outvoted**: only one of its
two models (Cohere) is in the panel; gpt-oss-20b is not a member.

**3-of-5 quorum** (n = 5, k = 3: the five TD1 models)

| Value | Votes | Models |
|---|---|---|
| 590320 | 2 | gpt-oss-120b, qwen3.8-27b |
| 0 | 2 | north-mini-code, gpt-oss-20b |
| 135000 | 1 | dots-3-note-preview |

Result: **abstention** (`consensus: False`, `value: None`, `votes: 2`). No value reaches 3 votes. The
wrong 0 does not win, but it ties the right value at 2 votes and so blocks the correct answer.

**Reading.** Here the larger quorum is not safer: going from 2-of-3 to 3-of-5 turns a correct
consensus into an abstention, because the two added models (gpt-oss-20b, Dots) are both wrong on this
age question. The 2-of-3 panel is right only because the shared error falls on a single panel member;
had gpt-oss-20b replaced qwen3.8-27b in the panel, the 2-of-3 vote would have returned the wrong 0
as a consensus.

## 2. Faulty SQL diagnosis

To be exactly 25 on 2026-09-25, a customer must be born **between 2000-09-26 and 2001-09-25
(both included)**. The reference query keeps these customers and gets 590320.

I ran the two wrong queries on `kit-td1/data/boutique.sqlite` with `run_sql.py`: both return 0, and
the reference returns 590320, so the TD1 error is reproduced.

### gpt-oss-20b: the window is in the wrong place

Query: [`m1-gpt-oss-20b.sql`](m1-gpt-oss-20b.sql)

```sql
WHERE c.birth_date > '2025-09-25' AND c.birth_date <= '2026-09-25'
```

This keeps people born between 2025-09-26 and 2026-09-25. On 2026-09-25 they are **0 years old**
(babies). The model went back 1 year instead of 25 years: the window has the right width (one year)
but it is shifted by 25 years. No customer of the shop is born in that window, so the sum is 0.

### north-mini-code (Cohere): the two comparisons are reversed

Query: [`m2-cohere.sql`](m2-cohere.sql)

```sql
WHERE c.birth_date <= '2026-09-25'
  AND date(c.birth_date, '+25 years') > '2026-09-25'   -- (A)
  AND date(c.birth_date, '+26 years') <= '2026-09-25'  -- (B)
```

- (A) means "has not had his 25th birthday yet", so the customer is **under 25**.
- (B) means "has already had his 26th birthday", so the customer is **26 or older**.

Nobody can be both, so the `WHERE` is always false. Example with a customer born on 2001-01-01:
(A) 2026-01-01 > 2026-09-25 is false, and (B) 2027-01-01 <= 2026-09-25 is false too. No row is
kept and the sum is 0. The correct version would flip both comparisons:

```sql
date(c.birth_date, '+25 years') <= '2026-09-25'   -- already 25
AND date(c.birth_date, '+26 years') > '2026-09-25' -- not 26 yet
```

### What this shows

The two models give **the same 0 for two different reasons** (a shifted window for gpt-oss-20b,
an impossible condition for Cohere). The vote cannot see that: it only sees "0" twice. So two models
agreeing on a value does not mean the value is right.

## 3. Delta query on `data/boutique.sqlite`

Query: [`delta.sql`](delta.sql). It lists the customers born between 2000-09-26 and 2001-09-25 (so
aged exactly 25 on 2026-09-25) with their revenue excluding VAT.

```bash
python wrong-consensus/run_sql.py wrong-consensus/delta.sql
```

| customer_id | birth_date | revenue_cents |
|---|---|---|
| C001 | 2001-09-25 | 135000 |
| C002 | 2001-09-24 | 25920 |
| C005 | 2000-09-26 | 150240 |
| C007 | 2000-11-30 | 118740 |
| C008 | 2001-05-15 | 99090 |
| C009 | 2001-03-10 | 61330 |
| **Total** | | **590320** |

The total is exactly the reference (590320). Both faulty queries keep **none** of these 6 customers
(I checked: 0 customers in the gpt-oss-20b window, 0 customers match the Cohere `WHERE`), so the gap
is the whole amount: **590320 - 0 = 590320 cents**, i.e. 6 customers missed.

Two of these rows are the boundaries of the window: C001 has his 25th birthday on the day itself
(2001-09-25), and C005 turns 26 the next day (2000-09-26). These are the rows a wrong `<` / `<=`
would lose first.

Side note: Dots (the third wrong value, 135000) used `birth_date = '2001-09-25'`, so it only kept C001.
Its 135000 is exactly C001's line in the table.

## 4. Consequence for checking

- **The vote alone is not enough on age questions.** On C02, 2-of-3 gives the right answer only
  because one of the two wrong models (gpt-oss-20b) is not in the panel. With gpt-oss-20b instead of
  Qwen, the 2-of-3 panel would return the wrong 0 as a consensus. 3-of-5 does not help either: it
  abstains (2 votes against 2).
- **A different panel is not a guarantee.** It can move the problem, not remove it: models from
  different families made the same kind of age mistake here.
- **The independent check I would use:** a deterministic reference query for "age at a date",
  written once and tested (the birth-date window is computed by code: born after D - 26 years and on
  or before D - 25 years), and the model's answer is compared to it. For a figure shown to a customer or
  an amount paid out, a mismatch goes to human review.
- **Cheap warning signs** that would have caught this case even without the reference:
  - the `WHERE` keeps 0 customers while the table has customers of that age: a result of 0 on an
    age question should be flagged, not trusted;
  - testing the model's `WHERE` on the boundary customers (C001 and C005 above) shows if the window
    is shifted or reversed.
- This matches pair C's routing rule: for F2 (age at a date), a customer figure or a payout needs a
  reference SQL check, not only a quorum.

**Limits.** This is one question out of 20 in one TD1 batch. It shows that a shared wrong value can
happen, not how often it happens. The other shared wrong value in our traces (C19, 71640, Cohere and
Dots) has not been analysed here.

## 5. Link with Lecture 2 (18 November)

What we saw on C02 matches several points of this morning's lecture:

| Lecture 2 idea | What C02 shows |
|---|---|
| Three kinds of failure: refused call (429), broken answer (query that cannot run), **wrong value** (query runs but computes the wrong result) | C02 is a **wrong value**: both queries run without error and return 0. This is the hardest kind to catch, because nothing looks broken. |
| Mixing model families reduces the risk of a shared mistake but does not remove it | gpt-oss-20b (OpenAI family, Groq) and north-mini-code (Cohere family, OpenRouter) are different families on different providers, and they still return the same 0. |
| A stricter threshold (higher K) gives more abstentions and does not guarantee the truth | Going from 2-of-3 to 3-of-5 turns a correct consensus into an abstention (2 votes against 2). |
| Deterministic checks are done by code, not by a model, before trusting a vote | Our consequence (section 4): a tested reference query for "age at a date", plus simple code checks (0 on an age question, boundary customers). |
| The same model counts as one vote, and only its last attempt is kept | I checked it: each model has a single attempt on C02, so one vote per model. |
| A value without its SQL query is not a vote | Every value in the table comes with its SQL in `traces-td1.csv`, which is how I could find the faulty `WHERE` clauses. |
| A new model is tested in shadow mode (logged, not voting) before joining a panel | gpt-oss-20b is right on only 1 out of 4 age questions (F2) in TD1. On age questions it should stay in shadow mode instead of voting; otherwise, with it in the 2-of-3 panel, the wrong 0 wins. |

Main takeaway for me: a quorum only helps when the models make **independent** mistakes. Here they
make two different mistakes that happen to give the same number, and the vote cannot tell the
difference. Only a check that looks at the data itself (the reference query, the delta query) can.
