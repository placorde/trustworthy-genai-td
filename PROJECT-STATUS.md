# Project status --- DIA3-G5

Updated 18 November 2026, pack `2026-10-18-students-1`. Since TD2 the repository is grouped by session:
TD1 files in [`td1/`](td1/README.md), TD2 files in [`td2/`](td2/README.md); `kit-td1/` stays at the root.

**How the mark works.** Sub-group mark = the nine session outcomes (R1-R3, Q1-Q3, C1-C3, each 0/1/2) out of
18, brought to 20. Final mark = 70 % sub-group mark + 30 % mean of the three individual Moodle quizzes
(10 questions, 15 minutes, no AI, at the end of each TD). No video, no oral, no hand-in points. An outcome
marked 2 whose evidence is missing from the session's repository drops to 1. A blocking bug or missing code
basics (configuration-driven models, one client interface, error handling, one trace line per call,
replayable README, no secret) cost points.

**Hand-in after each TD**, by 23:59 Paris time on the following Sunday: commit recorded in Moodle with the
repository URL and a link to the report at that commit.

## TD1 --- 21 October --- compare (done; hand-in by Sunday 25 October)

The Moodle entry records the commit tagged
[`td1-submission`](https://github.com/placorde/trustworthy-genai-td/tree/td1-submission).

| Deliverable | Status |
|---|---|
| `reference-td1.csv` | Done: 20/20, equal to the published values; member checks C01-C12, CSV recomputation 20/20 |
| Configuration file | Done: `kit-td1/modeles-autorises.json`, read by `kit-td1/skeleton-multi-llm-en.py` |
| `traces-td1.csv` / `.jsonl` | Done: 100 cells + 6 retries, merge check without blocking problem; offline replay reproduces every verdict |
| `model-question-comparison-en.csv` | Done: 100 rows, a cause for each of the 25 failures, reviewed ([`td1-review.md`](td1/reports/td1-review.md)) |
| `five-model-summary-en.csv` | Done: 5 rows, N/A with reason for Cohere and Dots |
| `prompts-en.md` | Done: experiment prompt verbatim, coding-assistance prompts declared |
| `README.md` | Done: DIA3 / DIA3-G5 header, members, pack, replay commands |
| `reports/td1.md` + R1-R3 evidence | Done |
| `traces/run-log-td1.csv` | Calls and retries filled; allowances N/A (not recorded at run time) |

Each member also registers their DIA class and sub-group number in the Moodle quiz "TD 1 sub-group
registration".

Results to reuse: gpt-oss-120b 19/20, gpt-oss-20b 17/20, Qwen 15/20, Dots 13/20, Cohere 11/20. Every
model is right on all period and product questions; 24 of 25 failures break the completed-age convention.
Shared wrong values: C02 = 0 (gpt-oss-20b, Cohere), C19 = 71640 (Cohere, Dots).

## TD2 --- 18 November --- vote and route (done; hand-in by Sunday 22 November)

No new model call: everything runs on `td1/traces-td1.csv`. Report:
[`td2/reports/td2.md`](td2/reports/td2.md).

| Step | Status | Marked by |
|---|---|---|
| 1. k-of-n vote (pair A: Raphaël, Florentin) | Done: `Orchestrateur.vote_k_sur_n` in `kit-td1/skeleton-multi-llm-en.py`; four synthetic examples; 20-question table, fixed 2-of-3: 16 correct, 0 wrong, 4 abstentions; 3-of-5: 15 correct, 0 wrong, 5 abstentions | Q1: show an abstention |
| 2. Wrong consensus (pair B: Matéo, Thomas) | Done: C02, gpt-oss-20b and Cohere both return 0 (reference 590320); faulty SQL clauses and delta query in [`td2/wrong-consensus/`](td2/wrong-consensus/case-C02.md); C19 found, not analysed | Q2 |
| 3. Routing rule (pair C: Christophe, Pierre-Louis, Robin) | Done: TD1 rates per family and level, one-page rule, adapted `RESOURCES` and `choose`, simulator outputs before and after, priority analysis in [`td2/routing/`](td2/routing/routing-rule-td2.md) | Q3 |
| Internal cross-review | Done: pair B reviewed A and C, pair C reviewed A and B, in [`td2/cross-review/`](td2/cross-review/); all figures reproduced | --- |
| Quiz | Individual, 17:45-18:00, on the TD2 lecture and lab | 30 % (with TD1, TD3) |
| Hand-in | `td2/reports/td2.md` complete; vote tests in [`td2/vote/voting-tests-en.csv`](td2/vote/voting-tests-en.csv) (14/14 pass) and the driver `td2/vote/vote_driver.py` that rebuilds the 20-question table; to do: new Moodle entry with the TD2 commit | --- |

Open points from the cross-reviews (not blocking): C17 missing from pair A's "Changes" list, C19 not
analysed, version numbers on the voting policy and the routing rule, the L3 panel relies on one provider
(Groq). Branch `td2-benchmarking-A` must not be merged: its content is already in `master`.

## TD3 --- 11 December --- quantify and decide (to do; hand-in by Sunday 13 December)

| Step | To do | Marked by |
|---|---|---|
| 1. Configuration table | Cheapest single model per family, best single model, 2-of-3 quorum, 3-of-5 quorum, our routing rule: calls, tokens, API-equivalent cost (tokens x dated price, `methode-cout-en.md`) and real spend in two separate columns; N/A with coverage when a price is missing (Cohere, Dots) | C1 |
| 2. Decision | Name a use case, the cost of an error in it, the configuration chosen and its cost per question | C2 |
| 3. Three slides | Models compared; quorum and wrong consensus; recommended configuration and written limits; shown on screen at the table, every figure traced back to a line | C3 |
| Quiz | Individual, 17:45-18:00 | 30 % (with TD1, TD2) |
| Hand-in | Complete repository, `reports/td3.md`; Moodle entry with the TD3 commit | --- |
