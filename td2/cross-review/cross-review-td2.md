# TD2 internal cross-review --- DIA3-G5 (done by pair B)

Date: 18 November 2026. No new model call: everything is replayed offline from the TD1 traces.

Commits reviewed:

| Pair | Branch | Commit |
|---|---|---|
| A (vote) | `td2-benchmarking-A` | `9b4180a` |
| B (wrong consensus) | `td2-wrong-consensus-b` | `138488f` |
| C (routing) | `td2-routing-c` | `1db815e` |

Method: for each pair I (1) re-ran their code on a clean copy of their branch, (2) recomputed their
numbers with my own script starting from `traces-td1.csv`, not from their files, and (3) compared.

Scripts and raw outputs in this folder:
- [`check_pair_a.py`](check_pair_a.py) -> [`check-pair-a-output.md`](check-pair-a-output.md)
- [`check_pair_c.py`](check_pair_c.py) -> [`check-pair-c-output.md`](check-pair-c-output.md)

## Pair A --- the k-of-n vote

**What I checked**

1. `python kit-td1/atelier-vote.py` with pair A's skeleton: the four synthetic examples give the
   expected decisions (agreement 100, disagreement abstain, unavailable abstain, wrong consensus 0).
2. 10 contract tests on `vote_k_sur_n` (`check_pair_a.py`, part 1): **10/10 pass**. Tested: k = 1 of 3,
   k = 4 of 3 and k = 2 of 4 are refused; a duplicate (provider, model) is refused; unavailable members
   stay in n; all unavailable gives 0 votes; 0 counts as a real value; a 2-2-1 tie of 5 abstains; an
   `error` proposal does not vote even if it carries a value.
3. Replay of 2-of-3 and 3-of-5 on C01-C20 (part 2), three ways: pair A's method, my own independent
   counter, and the table in pair A's report. **The three agree on all 20 questions.**
   - 2-of-3: 16 correct, 0 wrong consensus, 4 abstentions (C10, C15, C17, C19).
   - 3-of-5: 15 correct, 0 wrong consensus, 5 abstentions (C02, C11, C15, C17, C19).
4. "Last attempt": I took the latest `date_utc` per model and question; it is the same as the last
   CSV row on every cell, so pair A's choice is safe.
5. C02 matches my hand count from step 2 (590320 2/3, then abstain 2/5).

**Verdict: the method and the table are correct.**

**To fix before the merge**

1. **The branch has no common history with `master`** (`git merge-base` finds nothing). It only holds
   two files and no `traces-td1.csv`, so the commands in the report cannot be replayed from it, and a
   pull request into `master` will not merge cleanly. Pair A should create a new branch from `master`
   and put their two files on it.
2. **C17 is missing from the "Changes" list** (19 questions commented out of 20). C17 is exactly the
   case the assignment asks about ("margin shift caused by invalid SQL"): Dots returned invalid SQL
   (`syntax error near "AS"`), so it stays in n = 5 but does not vote; the four other values are all
   different (80190, 258180, 197080, 248490), best 1/5, abstain.
3. The decisions that change between 2-of-3 and 3-of-5 (C02, C10, C11) should be explained in one
   sentence each, not only listed with values. Example for C10: the 2-of-3 panel abstains (1/3) because
   Cohere and Qwen are both wrong, and 3-of-5 reaches 3 because the two added models (gpt-oss-20b, Dots)
   are right.
4. The test outputs asked by the hand-in page are missing for **duplicate routes** (agreement,
   disagreement and unavailable are in the synthetic table). `check-pair-a-output.md` can be used.
5. The driver that produced the 3-of-5 column is not in the branch (only the skeleton is). The
   hand-in page asks for "the small driver that calls it". `check_pair_a.py` does the same replay and
   can be cited, but pair A should say which code they ran.
6. Small: the "Voting policy" section has no version number (Lecture 2: a policy is written rules with
   a version, e.g. "voting policy v1").

## Pair C --- the routing rule

**What I checked**

1. Re-ran all their commands on a clean copy of their branch (`family_rates.py`, `quorum_check.py`,
   `priority_check.py`, `kit-td1/atelier-routage.py`, `routing/atelier-routage.py`): **every output
   file is byte-identical** to the committed one (`simulator-before.jsonl`, `simulator-after.jsonl`,
   `family-rates-td1.md`, `quorum-check-td1.md`, `priority-check.jsonl`).
2. Recomputed the rates per family from `traces-td1.csv` (they used `model-question-comparison-en.csv`):
   **all 25 cells and all 5 model levels match** (`check_pair_c.py`, part 1).
3. Replayed their three 2-of-3 panels (part 2): L2 panel (120b, Qwen, Dots) 0 wrong; L3 panel (20b,
   120b, Dots) 17 correct, 3 abstain (C02, C11, C17), 0 wrong. Matches what they wrote.
4. Consistency constraint (part 3): "none" is only used for the dashboard, and only where the first
   model is 100 % on the family (Cohere 6/6 on F1, 4/4 on F3; gpt-oss-120b 4/4 on F2). **Respected.**
5. The priority analysis of the kit's `choose` is present and checked by `priority_check.py`
   (subscription up -> run subscription; subscription down -> defer free, wake in 30 min), with
   conditions to reverse it.
6. The retry policy of the lecture (10 attempts, 1 min apart) is now in `routing-rule.json`.

**Verdict: the numbers are correct and reproducible.**

**Points to discuss or fix**

1. **The L3 panel has two models of the same family on the same provider** (gpt-oss-20b and
   gpt-oss-120b, both on Groq). The assignment asks for "a panel of distinct families". Pair C writes
   the risk down, which is good, but it also means one Groq quota problem removes 2 of the 3 members at
   once (their scenario "hard question, quota exhausted" shows the whole panel deferring).
2. **Link with our step 2:** the L1 panel (Cohere, Dots, gpt-oss-20b) is fine on F1 and F3, but on the
   20 questions it gives **2 wrong consensuses: C02 (0) and C19 (71640)**, the two cases pair B found.
   So the rule is only safe if the question is put in the right family. A question about age sent to
   L1 by mistake would return a wrong value with a "consensus". Worth one line in the report.
3. "Vote hygiene" says values are "normalised by code before the vote". In TD2 the values are already
   integers in the traces, so this is a rule for later, not something the code does today. Better to
   say so.
4. The retry policy has no version number (same remark as pair A).
5. **Conflict with pair A:** both branches create `reports/td2.md`. Pair C's file already has empty
   sections "Step 1 (pair A)" and "Step 2 (pair B)", so it should be the base: pair A pastes its text
   into step 1 instead of adding its own file.

## Pair B --- self-check (our own work)

Re-ran everything from a clean copy of the pushed branch: `scan.py` finds C02 and C19; `m1` and `m2`
return 0, `ref` returns 590320; `delta.sql` lists 6 customers summing to 590320. Same as
`wrong-consensus/case-C02.md`. Known limit: C19 is found but not analysed.

## Consistency between the three pairs

| Point | A | B | C | OK? |
|---|---|---|---|---|
| C02, fixed 2-of-3 | 590320 (2/3) | 590320 (2/3, by hand) | --- | yes |
| C02, 3-of-5 | abstain (2/5) | abstain (2/5, by hand) | "a higher threshold only adds abstentions" | yes |
| Shared wrong values in the traces | --- | C02 (0), C19 (71640) | L1 panel would be wrong on exactly C02 and C19 | yes |
| C10, C15, C19 | 2-of-3 fixed panel abstains | --- | L3 panel gives the right value | yes, **different panels**: A uses the fixed panel (120b, Cohere, Qwen), C chooses a panel per family. Not a contradiction, but the report must say it. |
| Age questions are the weak point | 3-of-5 abstains on C02, C11 | C02 wrong consensus, two different SQL bugs | F2 needs L2, never an L1 model alone | yes |

## Merge plan (proposal)

1. Merge B (`td2-wrong-consensus-b`, then this `cross-review/` folder): new files only, no conflict.
2. Merge C (`td2-routing-c`): touches `README.md` and creates `reports/td2.md`.
3. Pair A rebuilds its branch from `master` (after 1 and 2), puts `vote_k_sur_n` in
   `kit-td1/skeleton-multi-llm-en.py`, and pastes its report into the "Step 1" section of the existing
   `reports/td2.md`.
4. Fill "Step 2" of `reports/td2.md` with a summary of `wrong-consensus/case-C02.md`, add a short
   "cross-review" section linking to this file, the members' contributions, and the AI-use lines in
   `prompts-en.md`.
