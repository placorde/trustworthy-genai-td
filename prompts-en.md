# Prompts used in TD1

Experiment prompt, identical for every model and every question, taken verbatim from
`skeleton-multi-llm-en.py` (pack `2026-10-14-students-1`, file SHA-256 `55abb7d86d40e18534b9d6b1f91e467a0eebcec55d98bdcbe9de1769e070e17d`). No variant was used
in TD1. `{schema}` is the content of `schema.sql`, `{question}` the question text of `questions-td1.json`.
The prompt fingerprint written in every trace line is `sha256(system + "
" + user)`.

## System message

````text
You write SQLite queries for a small e-commerce database. Reply with exactly one SQLite SELECT statement and nothing else: no explanation, no comments, no markdown other than an optional ```sql fence.
````

## User template

````text
Schema (SQLite):
{schema}

Conventions (binding):
- product.price is the unit price in euro cents, excluding VAT (an integer). Revenue excluding VAT is SUM(quantity_product * price), an integer number of cents.
- orders holds order lines: one row per (order_id, product_id). All lines of an order share the same customer_id and the same date.
- orders.date and customers.insert_date are UTC timestamps stored as text 'YYYY-MM-DD HH:MM:SS'. customers.birth_date is a date stored as text 'YYYY-MM-DD'. Compare them as text or with SQLite date functions.
- A period "from S to E" is closed on the left and open on the right: date >= S AND date < E.
- A customer's age on a day D is the number of completed years: someone born on B is N years old on D when the N-th anniversary of B is on or before D and the (N+1)-th anniversary is after D. "Exactly 25 years old" means completed age 25 on that day, computed from month and day, never from the year difference alone.
- Unless the question says "at the time of the order", ages are computed on the reference date given in the question.
- The query must return exactly one row and one column named revenue_cents. When no order line matches, return 0 (use COALESCE), not NULL.
- Use only the tables above. One SELECT statement, nothing else.

Question: {question}
````

## Fingerprint check

For C01, the fingerprint recomputed from this file is `d25f63730bdd4980e31c3e5a449f59f3410bcee3a2cfc132d8f38efab03b1bdd`; it must equal the `prompt_sha256` of every
C01 row in `traces-td1.csv`.

## Coding-assistance prompts

Prompts used with coding assistants for this repository (reference computation, cross-check and trace merge
scripts) are listed here as they were used.

| Date | Member | Tool | Prompt | Output used in |
|---|---|---|---|---|
| 2026-10-21 | F (Pierre-Louis) | Claude Code (Claude Opus 5.5) | "Calcule les références SQL C01 à C20 sur boutique.sqlite et remplis reference-td1.csv dans le repo." | `references/compute_references.py`, `reference-td1.csv` (values then confirmed by members' cross-checks and the instructor) |
| 2026-10-21 | F (Pierre-Louis) | Claude Code (Claude Opus 5.5) | "Prépare le script de fusion/contrôle des traces et la fiche de comptage dans le repo, sur une branche." | `traces/merge_traces.py`, `traces/run-log-td1.csv`, `traces/README.md` |
| 2026-10-21 | F (Pierre-Louis) | Claude Code (Claude Opus 5.5) | "C'est bon on a tous, peux-tu réorganiser et commencer à faire la validation" | merge of B and E, `model-question-comparison-en.csv` rows B-E with causes read from the returned SQL, `five-model-summary-en.csv` rows B-E, `traces/pivot_comparison.py`; to be reviewed by G (Florentin) |
| 2026-10-21 | F (Pierre-Louis) | Claude Code (Claude Opus 5.5) | "Fais la partie de Florentin pour clôturer le TD1" | `reports/td1-review.md` (failing queries re-executed, selected birth dates listed), two explanations made precise in `model-question-comparison-en.csv` |
| 2026-10-23 | F (Pierre-Louis) | Claude Code (Claude Opus 5.5) | "Mets le README à jour (DIAx-G5), ajoute le fichier de configuration et le code du kit, et ouvre une PR." | `kit-td1/` (kit files copied unmodified), README header and replay commands, `references/compute_references.py` default kit path |
| | | | | |
