# Cross-review by pair C --- raw output of `cross-review/check_pairs_a_b.py`

## Pair A --- `vote_k_sur_n` and the 20-question table

Code read from `origin/td2-benchmarking-A:kit-td1/skeleton-multi-llm-en.py`.

| Contract test | Result | Detail |
|---|---|---|
| k = 1 of 3 refused | OK |  |
| k = 2 of 4 refused | OK |  |
| k = 4 of 3 refused | OK |  |
| duplicate (provider, model) refused | OK |  |
| 0 is a real value and can win | OK | {'consensus': True, 'value': 0, 'votes': 2, 'models': ['g:m1', 'o:m2']} |
| an `error` proposal does not vote | OK | {'consensus': False, 'value': None, 'votes': 1, 'models': []} |
| nobody available: abstain, 0 votes | OK | {'consensus': False, 'value': None, 'votes': 0, 'models': []} |
| 2-2-1 of 5 with k = 3 abstains | OK | {'consensus': False, 'value': None, 'votes': 2, 'models': []} |

Replay on C01-C20: pair A's code, my own counter, and the table of pair A's report.

| Question | Reference | 2-of-3 (code) | own | report | 3-of-5 (code) | own | report | Agree |
|---|---|---|---|---|---|---|---|---|
| C01 | 792800 | 792800 (3/3) | 792800 (3/3) | 792800 (3/3) | 792800 (5/5) | 792800 (5/5) | 792800 (5/5) | yes |
| C02 | 590320 | 590320 (2/3) | 590320 (2/3) | 590320 (2/3) | Abstain (best 2/5) | Abstain (best 2/5) | Abstain (best 2/5) | yes |
| C03 | 936350 | 936350 (3/3) | 936350 (3/3) | 936350 (3/3) | 936350 (5/5) | 936350 (5/5) | 936350 (5/5) | yes |
| C04 | 2826250 | 2826250 (3/3) | 2826250 (3/3) | 2826250 (3/3) | 2826250 (5/5) | 2826250 (5/5) | 2826250 (5/5) | yes |
| C05 | 38480 | 38480 (3/3) | 38480 (3/3) | 38480 (3/3) | 38480 (5/5) | 38480 (5/5) | 38480 (5/5) | yes |
| C06 | 0 | 0 (3/3) | 0 (3/3) | 0 (3/3) | 0 (5/5) | 0 (5/5) | 0 (5/5) | yes |
| C07 | 13970 | 13970 (3/3) | 13970 (3/3) | 13970 (3/3) | 13970 (5/5) | 13970 (5/5) | 13970 (5/5) | yes |
| C08 | 605580 | 605580 (2/3) | 605580 (2/3) | 605580 (2/3) | 605580 (3/5) | 605580 (3/5) | 605580 (3/5) | yes |
| C09 | 487980 | 487980 (2/3) | 487980 (2/3) | 487980 (2/3) | 487980 (3/5) | 487980 (3/5) | 487980 (3/5) | yes |
| C10 | 558980 | Abstain (best 1/3) | Abstain (best 1/3) | Abstain (best 1/3) | 558980 (3/5) | 558980 (3/5) | 558980 (3/5) | yes |
| C11 | 446690 | 446690 (2/3) | 446690 (2/3) | 446690 (2/3) | Abstain (best 2/5) | Abstain (best 2/5) | Abstain (best 2/5) | yes |
| C12 | 1666490 | 1666490 (3/3) | 1666490 (3/3) | 1666490 (3/3) | 1666490 (5/5) | 1666490 (5/5) | 1666490 (5/5) | yes |
| C13 | 107740 | 107740 (3/3) | 107740 (3/3) | 107740 (3/3) | 107740 (5/5) | 107740 (5/5) | 107740 (5/5) | yes |
| C14 | 0 | 0 (3/3) | 0 (3/3) | 0 (3/3) | 0 (5/5) | 0 (5/5) | 0 (5/5) | yes |
| C15 | 168680 | Abstain (best 1/3) | Abstain (best 1/3) | Abstain (best 1/3) | Abstain (best 2/5) | Abstain (best 2/5) | Abstain (best 2/5) | yes |
| C16 | 376740 | 376740 (2/3) | 376740 (2/3) | 376740 (2/3) | 376740 (4/5) | 376740 (4/5) | 376740 (4/5) | yes |
| C17 | 258180 | Abstain (best 1/3) | Abstain (best 1/3) | Abstain (best 1/3) | Abstain (best 1/5) | Abstain (best 1/5) | Abstain (best 1/5) | yes |
| C18 | 62480 | 62480 (2/3) | 62480 (2/3) | 62480 (2/3) | 62480 (3/5) | 62480 (3/5) | 62480 (3/5) | yes |
| C19 | 1990 | Abstain (best 1/3) | Abstain (best 1/3) | Abstain (best 1/3) | Abstain (best 2/5) | Abstain (best 2/5) | Abstain (best 2/5) | yes |
| C20 | 1106090 | 1106090 (3/3) | 1106090 (3/3) | 1106090 (3/3) | 1106090 (5/5) | 1106090 (5/5) | 1106090 (5/5) | yes |

2-of-3: 16 correct, 0 wrong, 4 abstain. 3-of-5: 15 correct, 0 wrong, 5 abstain. All 20 rows agree: yes.
Questions commented in "Changes": 19/20; missing: C17.

## Pair B --- wrong consensus C02

Files read from `origin/td2-wrong-consensus-b:wrong-consensus/`.

| Check | Result | Detail |
|---|---|---|
| `m1-gpt-oss-20b.sql` is the SQL stored in the TD1 trace | OK |  |
| `m1-gpt-oss-20b.sql` returns 0 (trace value 0) | OK | 0 |
| `m2-cohere.sql` is the SQL stored in the TD1 trace | OK |  |
| `m2-cohere.sql` returns 0 (trace value 0) | OK | 0 |
| `ref.sql` returns the reference | OK | 590320 |
| delta rows = customers of completed age 25 (computed in Python from customers.csv) | OK | 6 rows: C001, C002, C005, C007, C008, C009 |
| delta total = reference 590320 | OK | 590320 |
| Dots' 135000 is exactly C001's revenue | OK |  |
| with gpt-oss-20b instead of Qwen, 2-of-3 returns the wrong 0 | OK | 0 (2/3) |
| 3-of-5 abstains on C02 (2 against 2) | OK | best 2/5 |

## Pair B's remarks on pair C, rechecked

| Claim | Result | Detail |
|---|---|---|
| L1 panel would give wrong consensuses only on C02 and C19 over the 20 questions | OK | C02=0, C19=71640 |
| L3 panel on the 20 questions: 17 correct, 3 abstain, 0 wrong | OK | {'correct': 17, 'abstain': 3} |

