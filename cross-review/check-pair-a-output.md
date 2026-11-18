## 1. Contract tests on pair A's vote_k_sur_n

| Test | Result | Output |
|---|---|---|
| agreement 100,100,120 k=2 -> consensus 100 (2 votes) | PASS | `{'consensus': True, 'value': 100, 'votes': 2, 'models': ['groq:openai/gpt-oss-120b', 'openrouter:cohere/north-mini-code:free']}` |
| k=1 of n=3 is refused (not a strict majority) | PASS | `ValueError: k must be a strict majority for n=3, got 1` |
| k=4 of n=3 is refused (k > n) | PASS | `ValueError: k must be a strict majority for n=3, got 4` |
| k=2 of n=4 is refused (2 is not > 4//2) | PASS | `ValueError: k must be a strict majority for n=4, got 2` |
| duplicate (provider, model) is refused | PASS | `ValueError: Duplicate panel member: groq:openai/gpt-oss-120b` |
| 100 + 2 unavailable, k=2 -> abstain, unavailable stay in n | PASS | `{'consensus': False, 'value': None, 'votes': 1, 'models': []}` |
| all unavailable -> abstain with 0 votes | PASS | `{'consensus': False, 'value': None, 'votes': 0, 'models': []}` |
| 0 is a real value: 0,0,100 k=2 -> consensus 0 | PASS | `{'consensus': True, 'value': 0, 'votes': 2, 'models': ['groq:openai/gpt-oss-120b', 'openrouter:cohere/north-mini-code:free']}` |
| tie 2-2-1 of n=5, k=3 -> abstain with votes=2 | PASS | `{'consensus': False, 'value': None, 'votes': 2, 'models': []}` |
| an `error` proposal does not vote even if it carries a value | PASS | `{'consensus': False, 'value': None, 'votes': 1, 'models': []}` |

10/10 tests pass.

## 2. Replay on C01-C20 (pair A's method vs independent recount vs pair A's report)

Last attempt = latest `date_utc` per model and question; CSV order and date order agree on every cell.

| Q | Ref | 2-of-3 (A's method) | 2-of-3 (recount) | 2-of-3 in A's report | 3-of-5 (A's method) | 3-of-5 (recount) | 3-of-5 in A's report | Same everywhere? |
|---|---:|---|---|---|---|---|---|---|
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

- 2-of-3: 16 correct, 0 wrong consensus, 4 abstentions
- 3-of-5: 15 correct, 0 wrong consensus, 5 abstentions
- Questions where something differs: none
