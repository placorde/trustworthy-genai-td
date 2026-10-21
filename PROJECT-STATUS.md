# Project status --- sub-group 5

Updated 21 October 2026, after the TD1 hand-in. The mark is 9 outcomes x 2 points (3 per session) plus 2
hand-in points (H1 repository, H2 video); an outcome marked 2 whose evidence is missing from the final
repository drops to 1, so every piece of evidence must stay here until TD3.

## TD1 --- 21 October --- compare (done)

Handed in: tag [`td1-submission`](https://github.com/placorde/trustworthy-genai-td/tree/td1-submission),
commit `d899587fc120ecc5152a65d5752be26f7af3351c`.

| Deliverable | Status |
|---|---|
| `reference-td1.csv` | Done: 20/20, equal to the answer key; member checks C01-C12, CSV recomputation 20/20 |
| `traces-td1.csv` / `.jsonl` | Done: 100 cells + 6 retries, merge check without blocking problem |
| `model-question-comparison-en.csv` | Done: 100 rows, a cause for each of the 25 failures, reviewed ([`td1-review.md`](reports/td1-review.md)) |
| `five-model-summary-en.csv` | Done: 5 rows, N/A with reason for Cohere and Dots |
| `prompts-en.md` | Done: experiment prompt verbatim, coding-assistance prompts declared |
| `reports/td1.md` + R1-R3 evidence | Done |
| `traces/run-log-td1.csv` | Calls and retries filled; allowances N/A (not recorded at run time) |

After the tag: review of the comparison (G task) and the sub-group number added. If the Moodle entry is not
submitted yet, submit the newer commit; otherwise keep the tagged one.

Results to reuse: gpt-oss-120b 19/20, gpt-oss-20b 17/20, Qwen 15/20, Dots 13/20, Cohere 11/20. Every
model is right on all period and product questions; 24 of 25 failures break the completed-age convention.
Shared wrong values: C02 = 0 (gpt-oss-20b, Cohere), C19 = 71640 (Cohere, Dots).

## TD2 --- 18 November --- vote and route (to do)

No new model call: everything runs on `traces-td1.csv`.

| Step | To do | Marked by |
|---|---|---|
| Prepare | Copy `skeleton-multi-llm-en.py`, `sandbox_sqlite.py`, `atelier-vote.py`, `atelier-routage.py` from the kit into the repo; designate who reads `atelier-vote.py` and the routing worksheet before the session | --- |
| 1. k-of-n vote | Write `Orchestrateur.vote_k_sur_n` (only executed values vote; errors stay in n; strict majority `n//2 < k <= n`; duplicate pair refused; abstain without inventing a value). Run `atelier-vote.py` (4 synthetic examples) then `--traces traces-td1.csv --case Cxx` on the 20 questions; table of the 20 decisions (consensus or abstention, value, votes, agreement with the reference) | Q1: show an abstention |
| 2. Wrong consensus | Use C02 or C19: check what the fixed panel (gpt-oss-120b, Cohere, Qwen, 2 of 3) actually returns, explain the shared error from the SQL, and the check that would catch it; DEMO-VOTE synthetic case as fallback, labelled as such | Q2 |
| 3. Routing rule | One page from `templates/routing-rule-en.md`: per family, the cheapest model correct on it in our table, the check according to the cost of an error (dashboard, figure shown to a customer, amount paid out), the fallback; each line cites TD1 cells. Run `atelier-routage.py` before and after adapting `RESOURCES` and `choose` | Q3 |
| Hand-in | `reports/td2.md`, vote tests (`templates/voting-tests-en.csv`), outputs saved; new Moodle entry with the TD2 commit hash | --- |

## TD3 --- 11 December --- quantify and decide (to do)

| Step | To do | Marked by |
|---|---|---|
| 1. Configuration table | Cheapest single model per family, best single model, 2-of-3 quorum, 3-of-5 quorum, our routing rule: calls, tokens, API-equivalent cost (tokens x dated price, `methode-cout-en.md`) and real spend in two separate columns; N/A with coverage when a price is missing (Cohere, Dots) | C1 |
| 2. Decision | Name a use case, the cost of an error in it, the configuration chosen and its cost per question | C2 |
| 3. Three slides | Models compared; quorum and wrong consensus; recommended configuration and written limits | C3 |
| Oral | 20 minutes, each member presents one part; every figure traced back to a line | +/-1 |
| Final hand-in | Video of one call, its verdict and the vote; complete repository replayable from a fresh clone; `reports/td3.md` | H1, H2 |
