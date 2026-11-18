# TD1 trace merge report

Merged 106 rows from 5 files into `traces-td1.csv` and `traces-td1.jsonl`.

| File | Operator | Rows |
|---|---|---|
| traces-A.csv | A | 20 |
| traces-B.csv | B | 22 |
| traces-C.csv | C | 20 |
| traces-D.csv | D | 24 |
| traces-E.csv | E | 20 |

Rows by nature: real=106
Cells (real): 100 found / 100 expected

## Call counts

| Provider | Initial calls | Retries | Total |
|---|---|---|---|
| groq | 60 | 6 | 66 |
| openrouter | 40 | 0 | 40 |

## Final verdict per model (last attempt of each cell)

| Model | correct | incorrect | sql_invalid |
|---|---|---|---|
| groq:openai/gpt-oss-120b | 19 | 1 | 0 |
| groq:openai/gpt-oss-20b | 17 | 3 | 0 |
| groq:qwen/qwen3.8-27b | 15 | 5 | 0 |
| openrouter:cohere/north-mini-code:free | 11 | 9 | 0 |
| openrouter:dots-studio/dots-3-note-preview:free | 13 | 6 | 1 |

## Measurements left empty (empty is not zero)

| Column | Empty | Zero |
|---|---|---|
| http_status | 0 | 0 |
| latency_ms | 0 | 0 |
| tokens_prompt | 6 | 0 |
| tokens_completion | 6 | 0 |
| tokens_reasoning | 26 | 40 |
| cost_native | 66 | 40 |

## Blocking problems (0)
- none

## Warnings (0)
- none
