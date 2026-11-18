# TD 2 — Pair A — k-of-n vote

We used the last real attempt per model and question from the merged TD 1 CSV, keeping unsuccessful attempts in the panel size. Both `correct` and `incorrect` rows can vote when they contain an executed value. We compared the decision with `reference-td1.csv` only after the vote. All amounts are in cents.

The fixed panel uses GPT-OSS 120B (Groq), North Mini Code (OpenRouter), and Qwen 27B (Groq). The five-model quorum adds GPT-OSS 20B (Groq) and Dots 3 Note (OpenRouter).

## Voting policy

1. Fix the panel before voting and use each member's last real attempt for the question. The two configurations use a strict majority of the full panel, with two votes out of three or three votes out of five. Reject thresholds outside `n // 2 < k <= n` and reject duplicate `(provider, model_requested)` pairs.
2. Count one vote for the exact integer value (in cents) of each executed proposal, including zero. Failed or unavailable members stay in the denominator and cast no vote.
3. Return a value only if it reaches the threshold, along with the vote count and agreeing members. Otherwise abstain, record the highest vote count (zero if there were no votes), and leave the value and agreeing-member list empty. There is no tie-break or fallback value.
4. Compare the result with the independent TD 1 reference only after the decision. A consensus can still be wrong, as the synthetic case with two votes for zero shows.

## Synthetic examples

| Example | Proposals | Decision | Reference | Matches |
| --- | --- | --- | ---: | --- |
| Agreement | 100, 100, 120 | 100 (2/3) | 100 | Yes |
| Disagreement | 100, 110, 120 | Abstain (best 1/3) | 100 | — |
| Unavailable | 100, unavailable, unavailable | Abstain (best 1/3) | 100 | — |
| Wrong consensus | 0, 0, 100 | 0 (2/3) | 100 | No |

## Comparison on the twenty TD 1 questions

| Question | Reference | 2-of-3 | Matches | 3-of-5 | Matches |
| --- | ---: | --- | --- | --- | --- |
| C01 | 792800 | 792800 (3/3) | Yes | 792800 (5/5) | Yes |
| C02 | 590320 | 590320 (2/3) | Yes | Abstain (best 2/5) | — |
| C03 | 936350 | 936350 (3/3) | Yes | 936350 (5/5) | Yes |
| C04 | 2826250 | 2826250 (3/3) | Yes | 2826250 (5/5) | Yes |
| C05 | 38480 | 38480 (3/3) | Yes | 38480 (5/5) | Yes |
| C06 | 0 | 0 (3/3) | Yes | 0 (5/5) | Yes |
| C07 | 13970 | 13970 (3/3) | Yes | 13970 (5/5) | Yes |
| C08 | 605580 | 605580 (2/3) | Yes | 605580 (3/5) | Yes |
| C09 | 487980 | 487980 (2/3) | Yes | 487980 (3/5) | Yes |
| C10 | 558980 | Abstain (best 1/3) | — | 558980 (3/5) | Yes |
| C11 | 446690 | 446690 (2/3) | Yes | Abstain (best 2/5) | — |
| C12 | 1666490 | 1666490 (3/3) | Yes | 1666490 (5/5) | Yes |
| C13 | 107740 | 107740 (3/3) | Yes | 107740 (5/5) | Yes |
| C14 | 0 | 0 (3/3) | Yes | 0 (5/5) | Yes |
| C15 | 168680 | Abstain (best 1/3) | — | Abstain (best 2/5) | — |
| C16 | 376740 | 376740 (2/3) | Yes | 376740 (4/5) | Yes |
| C17 | 258180 | Abstain (best 1/3) | — | Abstain (best 1/5) | — |
| C18 | 62480 | 62480 (2/3) | Yes | 62480 (3/5) | Yes |
| C19 | 1990 | Abstain (best 1/3) | — | Abstain (best 2/5) | — |
| C20 | 1106090 | 1106090 (3/3) | Yes | 1106090 (5/5) | Yes |

- **2-of-3** yielded 16 correct consensuses, 0 incorrect consensuses and 4 abstentions.
- **3-of-5** yielded 15 correct consensuses, 0 incorrect consensuses and 5 abstentions.

## Changes in the decision or vote count

- **C01**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 792800. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 792800. GPT-OSS 120B 792800 (`correct`), North Mini Code 792800 (`correct`), Qwen 27B 792800 (`correct`), GPT-OSS 20B 792800 (`correct`), Dots 3 Note 792800 (`correct`).
- **C02**. For 2-of-3, GPT-OSS 120B, Qwen 27B reach 2 for 590320. For 3-of-5, the largest bloc of 2 in the 5-model panel falls short of 3. GPT-OSS 120B 590320 (`correct`), North Mini Code 0 (`incorrect`), Qwen 27B 590320 (`correct`), GPT-OSS 20B 0 (`incorrect`), Dots 3 Note 135000 (`incorrect`).
- **C03**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 936350. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 936350. GPT-OSS 120B 936350 (`correct`), North Mini Code 936350 (`correct`), Qwen 27B 936350 (`correct`), GPT-OSS 20B 936350 (`correct`), Dots 3 Note 936350 (`correct`).
- **C04**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 2826250. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 2826250. GPT-OSS 120B 2826250 (`correct`), North Mini Code 2826250 (`correct`), Qwen 27B 2826250 (`correct`), GPT-OSS 20B 2826250 (`correct`), Dots 3 Note 2826250 (`correct`).
- **C05**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 38480. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 38480. GPT-OSS 120B 38480 (`correct`), North Mini Code 38480 (`correct`), Qwen 27B 38480 (`correct`), GPT-OSS 20B 38480 (`correct`), Dots 3 Note 38480 (`correct`).
- **C06**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 0. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 0. GPT-OSS 120B 0 (`correct`), North Mini Code 0 (`correct`), Qwen 27B 0 (`correct`), GPT-OSS 20B 0 (`correct`), Dots 3 Note 0 (`correct`).
- **C07**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 13970. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 13970. GPT-OSS 120B 13970 (`correct`), North Mini Code 13970 (`correct`), Qwen 27B 13970 (`correct`), GPT-OSS 20B 13970 (`correct`), Dots 3 Note 13970 (`correct`).
- **C08**. For 2-of-3, GPT-OSS 120B, Qwen 27B reach 2 for 605580. For 3-of-5, GPT-OSS 120B, Qwen 27B, Dots 3 Note reach 3 for 605580. GPT-OSS 120B 605580 (`correct`), North Mini Code 1188090 (`incorrect`), Qwen 27B 605580 (`correct`), GPT-OSS 20B 25920 (`incorrect`), Dots 3 Note 605580 (`correct`).
- **C09**. For 2-of-3, GPT-OSS 120B, Qwen 27B reach 2 for 487980. For 3-of-5, GPT-OSS 120B, Qwen 27B, GPT-OSS 20B reach 3 for 487980. GPT-OSS 120B 487980 (`correct`), North Mini Code 1901780 (`incorrect`), Qwen 27B 487980 (`correct`), GPT-OSS 20B 487980 (`correct`), Dots 3 Note 47900 (`incorrect`).
- **C10**. For 2-of-3, the largest bloc of 1 in the 3-model panel falls short of 2. For 3-of-5, GPT-OSS 120B, GPT-OSS 20B, Dots 3 Note reach 3 for 558980. GPT-OSS 120B 558980 (`correct`), North Mini Code 219930 (`incorrect`), Qwen 27B 119410 (`incorrect`), GPT-OSS 20B 558980 (`correct`), Dots 3 Note 558980 (`correct`).
- **C11**. For 2-of-3, GPT-OSS 120B, Qwen 27B reach 2 for 446690. For 3-of-5, the largest bloc of 2 in the 5-model panel falls short of 3. GPT-OSS 120B 446690 (`correct`), North Mini Code 768850 (`incorrect`), Qwen 27B 446690 (`correct`), GPT-OSS 20B 322160 (`incorrect`), Dots 3 Note 0 (`incorrect`).
- **C12**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 1666490. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 1666490. GPT-OSS 120B 1666490 (`correct`), North Mini Code 1666490 (`correct`), Qwen 27B 1666490 (`correct`), GPT-OSS 20B 1666490 (`correct`), Dots 3 Note 1666490 (`correct`).
- **C13**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 107740. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 107740. GPT-OSS 120B 107740 (`correct`), North Mini Code 107740 (`correct`), Qwen 27B 107740 (`correct`), GPT-OSS 20B 107740 (`correct`), Dots 3 Note 107740 (`correct`).
- **C14**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 0. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 0. GPT-OSS 120B 0 (`correct`), North Mini Code 0 (`correct`), Qwen 27B 0 (`correct`), GPT-OSS 20B 0 (`correct`), Dots 3 Note 0 (`correct`).
- **C15**. For 2-of-3, the largest bloc of 1 in the 3-model panel falls short of 2. For 3-of-5, the largest bloc of 2 in the 5-model panel falls short of 3. GPT-OSS 120B 168680 (`correct`), North Mini Code 314020 (`incorrect`), Qwen 27B 0 (`incorrect`), GPT-OSS 20B 168680 (`correct`), Dots 3 Note 138920 (`incorrect`).
- **C16**. For 2-of-3, GPT-OSS 120B, North Mini Code reach 2 for 376740. For 3-of-5, GPT-OSS 120B, North Mini Code, GPT-OSS 20B, Dots 3 Note reach 3 for 376740. GPT-OSS 120B 376740 (`correct`), North Mini Code 376740 (`correct`), Qwen 27B 208520 (`incorrect`), GPT-OSS 20B 376740 (`correct`), Dots 3 Note 376740 (`correct`).
- **C18**. For 2-of-3, GPT-OSS 120B, Qwen 27B reach 2 for 62480. For 3-of-5, GPT-OSS 120B, Qwen 27B, GPT-OSS 20B reach 3 for 62480. GPT-OSS 120B 62480 (`correct`), North Mini Code 67150 (`incorrect`), Qwen 27B 62480 (`correct`), GPT-OSS 20B 62480 (`correct`), Dots 3 Note 39580 (`incorrect`).
- **C19**. For 2-of-3, the largest bloc of 1 in the 3-model panel falls short of 2. For 3-of-5, the largest bloc of 2 in the 5-model panel falls short of 3. GPT-OSS 120B 1990 (`correct`), North Mini Code 71640 (`incorrect`), Qwen 27B 83580 (`incorrect`), GPT-OSS 20B 1990 (`correct`), Dots 3 Note 71640 (`incorrect`).
- **C20**. For 2-of-3, GPT-OSS 120B, North Mini Code, Qwen 27B reach 2 for 1106090. For 3-of-5, GPT-OSS 120B, North Mini Code, Qwen 27B, GPT-OSS 20B, Dots 3 Note reach 3 for 1106090. GPT-OSS 120B 1106090 (`correct`), North Mini Code 1106090 (`correct`), Qwen 27B 1106090 (`correct`), GPT-OSS 20B 1106090 (`correct`), Dots 3 Note 1106090 (`correct`).
