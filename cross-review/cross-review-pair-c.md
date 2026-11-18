# TD2 internal cross-review --- DIA3-G5 (done by pair C)

Date: 18 November 2026. No new model call: everything is replayed offline from the TD1 traces.

| Pair | Branch | Commit reviewed |
|---|---|---|
| A (vote) | `td2-benchmarking-A` | `9b4180a` |
| B (wrong consensus) | `td2-wrong-consensus-b` | `138488f` (and pair B's own cross-review `01a58e5`) |

Method: pair A's skeleton and report and pair B's SQL files are read from their branches with
`git show`, without merging anything. Every number is recomputed from `traces-td1.csv`,
`reference-td1.csv` and the shop's CSV files with my own code, then compared with what the pair wrote.

Script and raw output: [`check_pairs_a_b.py`](check_pairs_a_b.py) →
[`check-pairs-a-b-output.md`](check-pairs-a-b-output.md).

```bash
git fetch origin
python cross-review/check_pairs_a_b.py
```

## Pair A --- the k-of-n vote

**What I checked**

1. Eight contract tests on pair A's `vote_k_sur_n`: **8/8 pass**. k = 1 of 3, k = 2 of 4 and k = 4 of 3
   are refused; a duplicate (provider, model) is refused; 0 is a real value and can win; an `error`
   proposal does not vote; nobody available gives an abstention with 0 votes; a 2-2-1 split of 5 with
   k = 3 abstains.
2. Replay of the fixed 2-of-3 panel (gpt-oss-120b, Cohere, Qwen) and of 3-of-5 on C01-C20, three ways:
   pair A's code, my own counter, and the table of pair A's report. **The three agree on all 20 rows.**
   - 2-of-3: 16 correct, 0 wrong consensus, 4 abstentions (C10, C15, C17, C19).
   - 3-of-5: 15 correct, 0 wrong consensus, 5 abstentions (C02, C11, C15, C17, C19).

**Verdict: the method and the table are correct.**

**To fix before the merge**

1. **The branch has no common history with `master`** (`git merge-base` finds nothing) and holds only
   two files: a pull request would delete every TD1 file. Pair A should start a new branch from
   `master` and copy its two changes onto it (same remark as pair B).
2. **C17 is missing from the "Changes" list** (19 of 20 questions commented). C17 is the invalid-SQL
   case: Dots stays in n = 5 without a vote, the four other values all differ, best 1/5, abstain.
3. The "Changes" list says "reach 2" for 2-of-3 while naming three models (e.g. C01, where the vote
   is 3/3), and it lists questions where nothing changes. It should keep only the questions whose
   decision changes between 2-of-3 and 3-of-5 (C02, C10, C11) and explain each in one sentence.
4. Pair A's `reports/td2.md` is a separate file: it conflicts with the `reports/td2.md` of pair C,
   which already has an empty "Step 1 (pair A)" section. Paste the text into that section instead.

## Pair B --- the wrong consensus C02

**What I checked**

1. `m1-gpt-oss-20b.sql` and `m2-cohere.sql` are exactly the SQL stored in the TD1 traces, and both
   return 0 on `kit-td1/data/boutique.sqlite`; `ref.sql` returns 590320.
2. The delta query lists 6 customers. I recomputed the completed age on 2026-09-25 in Python from
   `customers.csv` (not with a date window): the same 6 customers (C001, C002, C005, C007, C008, C009).
   Their total is 590320, the reference.
3. Dots' 135000 is exactly C001's revenue, as written.
4. With gpt-oss-20b in place of Qwen, the 2-of-3 panel returns the wrong 0 (2/3); 3-of-5 abstains
   (2 against 2). Both statements of section 4 are right.

**Verdict: the case, the SQL diagnosis and the delta query are correct.**

**Remarks**

1. C19 (71640, Cohere and Dots) is found by `scan.py` but not analysed; pair B says so. One line in the
   report is enough.
2. The rows of the delta query are found by a birth-date window. My check by completed age gives the
   same customers, which confirms the window's boundaries (C001 and C005).

## Pair B's remarks on pair C --- our answer

I rechecked pair B's two numerical claims on our rule: both are **true**.
- The L1 panel (Cohere, Dots, gpt-oss-20b) gives wrong consensuses on exactly C02 (0) and C19 (71640)
  over the 20 questions.
- The L3 panel (gpt-oss-20b, gpt-oss-120b, Dots) gives 17 correct, 3 abstentions, 0 wrong.

| Pair B's remark | Pair C's answer |
|---|---|
| L3 panel: two gpt-oss models on Groq | True. Among the ten 2-of-3 panels, only those holding both gpt-oss models reach 0 wrong and one abstention on L3 (`routing/quorum-check-td1.md`); a mixed panel would abstain on 3 or 4 of the 6 L3 cells. The shared-error risk is why the rule adds the reference SQL for customer figures and payouts. The single-provider risk (one Groq quota) is real; to be written in the rule. **To decide by pair C.** |
| L1 panel wrong on C02 and C19 if an age question is misclassified | True: the rule is only safe if the family is identified correctly. One line to add to the rule. **To decide by pair C.** |
| "Normalised by code" is a rule for later | True: in TD2 the values are already integers in cents in the traces. To be reworded. **To decide by pair C.** |
| No version number on the retry policy | To add ("routing rule v1"). **To decide by pair C.** |
| `reports/td2.md` conflict with pair A | Agreed: pair C's file is the base, pair A pastes its text into step 1. |

## Consistency between the three pairs

| Point | A | B | C | OK? |
|---|---|---|---|---|
| C02, fixed 2-of-3 | 590320 (2/3) | 590320 (2/3) | --- | yes |
| C02, 3-of-5 | abstain (2/5) | abstain (2/5) | "a higher threshold only adds abstentions" | yes |
| Shared wrong values | --- | C02 (0), C19 (71640) | L1 panel would be wrong on exactly C02 and C19 | yes |
| C10, C15, C19 | fixed panel abstains | --- | L3 panel gives the right value | yes, different panels (fixed vs per family): to say in the report |
| Age questions are the weak point | 3-of-5 abstains on C02, C11 | two different SQL bugs give the same 0 | F2 needs L2; L3 always votes | yes |
