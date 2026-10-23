# Project status --- DIA3-G5

Updated 23 October 2026, pack `2026-10-18-students-1`.

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
| `model-question-comparison-en.csv` | Done: 100 rows, a cause for each of the 25 failures, reviewed ([`td1-review.md`](reports/td1-review.md)) |
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

## TD2 --- 18 November --- vote and route (to do; hand-in by Sunday 22 November)

No new model call: everything runs on `traces-td1.csv`. The kit code is already in `kit-td1/`.

| Step | To do | Marked by |
|---|---|---|
| Prepare | Designate who reads `kit-td1/atelier-vote.py` and the routing worksheet before the session; operators note their allowance before any optional call | --- |
| 1. k-of-n vote | Write `Orchestrateur.vote_k_sur_n` in `kit-td1/skeleton-multi-llm-en.py` (only executed values vote; errors stay in n; strict majority `n//2 < k <= n`; duplicate pair refused; abstain without inventing a value). Run `atelier-vote.py` (4 synthetic examples) then `--traces traces-td1.csv --case Cxx` on the 20 questions; table of the 20 decisions (consensus or abstention, value, votes, agreement with the reference) | Q1: show an abstention |
| 2. Wrong consensus | Use C02 or C19: check what the fixed panel (gpt-oss-120b, Cohere, Qwen, 2 of 3) actually returns, explain the shared error from the SQL, and the check that would catch it; DEMO-VOTE synthetic case as fallback, labelled as such | Q2 |
| 3. Routing rule | One page from the kit's `templates/routing-rule-en.md`: per family, the cheapest model correct on it in our table, the check according to the cost of an error (dashboard, figure shown to a customer, amount paid out), the fallback; each line cites TD1 cells. Run `atelier-routage.py` before and after adapting `RESOURCES` and `choose` | Q3 |
| Quiz | Individual, 17:45-18:00, on the TD2 lecture and lab | 30 % (with TD1, TD3) |
| Hand-in | `reports/td2.md`, vote tests (`templates/voting-tests-en.csv`), outputs saved; new Moodle entry with the TD2 commit | --- |

## TD3 --- 11 December --- quantify and decide (to do; hand-in by Sunday 13 December)

| Step | To do | Marked by |
|---|---|---|
| 1. Configuration table | Cheapest single model per family, best single model, 2-of-3 quorum, 3-of-5 quorum, our routing rule: calls, tokens, API-equivalent cost (tokens x dated price, `methode-cout-en.md`) and real spend in two separate columns; N/A with coverage when a price is missing (Cohere, Dots) | C1 |
| 2. Decision | Name a use case, the cost of an error in it, the configuration chosen and its cost per question | C2 |
| 3. Three slides | Models compared; quorum and wrong consensus; recommended configuration and written limits; shown on screen at the table, every figure traced back to a line | C3 |
| Quiz | Individual, 17:45-18:00 | 30 % (with TD1, TD2) |
| Hand-in | Complete repository, `reports/td3.md`; Moodle entry with the TD3 commit | --- |
