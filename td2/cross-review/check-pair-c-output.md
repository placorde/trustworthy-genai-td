## 1. Rates per family, recomputed from traces-td1.csv

| Family | gpt-oss-120b | gpt-oss-20b | north-mini-code:free | qwen3.8-27b | dots-3-note-preview:free | Same as pair C? |
|---|---|---|---|---|---|---|
| F1 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | yes |
| F3 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | yes |
| F2 | 4/4 | 1/4 | 0/4 | 4/4 | 1/4 | yes |
| F2b | 1/1 | 1/1 | 0/1 | 0/1 | 1/1 | yes |
| F4 | 4/5 | 5/5 | 1/5 | 1/5 | 1/5 | yes |

| Model | Level recomputed | Level by pair C | Same? |
|---|---|---|---|
| openai/gpt-oss-120b | L2 | L2 | yes |
| openai/gpt-oss-20b | L1 | L1 | yes |
| cohere/north-mini-code:free | L1 | L1 | yes |
| qwen/qwen3.8-27b | L2 | L2 | yes |
| dots-studio/dots-3-note-preview:free | L1 | L1 | yes |

## 2. Pair C's 2-of-3 panels replayed on the 20 questions

| Panel | Members | Correct | Abstain | Wrong | Abstentions |
|---|---|---|---|---|---|
| L1 | north-mini-code:free, dots-3-note-preview:free, gpt-oss-20b | 12 | 6 | 2 | C08, C09, C11, C15, C17, C18 |
| L2 | gpt-oss-120b, qwen3.8-27b, dots-3-note-preview:free | 17 | 3 | 0 | C15, C17, C19 |
| L3 | gpt-oss-20b, gpt-oss-120b, dots-3-note-preview:free | 17 | 3 | 0 | C02, C11, C17 |

## 3. Consistency constraint ("none" only if the first model is 100 % on the family)

| Family | First model | Dashboard check | First model rate | Constraint respected? |
|---|---|---|---|---|
| F1 | cohere/north-mini-code:free | none | 6/6 | yes |
| F3 | cohere/north-mini-code:free | none | 4/4 | yes |
| F2 | openai/gpt-oss-120b | none | 4/4 | yes |
| F2b | panel L3 | panel vote | (panel, not a single model) | yes (no single model alone) |
| F4 | panel L3 | panel vote | (panel, not a single model) | yes (no single model alone) |

Everything matches pair C's files: yes
