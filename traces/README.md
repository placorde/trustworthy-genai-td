# TD1 traces

## Run order (step 2)

One operator at a time for the whole sub-group. Each operator, from their own `kit-td1` with the validated
`reference-td1.csv` copied in, runs exactly one command and never changes `--state` / `--out` between resumptions:

| Op. | Member | Command |
|---|---|---|
| A | Robin | `python skeleton-multi-llm-en.py --run --models groq:openai/gpt-oss-120b --state state-A.jsonl --out traces-A.csv` |
| B | Raphaël | `python skeleton-multi-llm-en.py --run --models groq:openai/gpt-oss-20b --state state-B.jsonl --out traces-B.csv` |
| C | Thomas | `python skeleton-multi-llm-en.py --run --models openrouter:cohere/north-mini-code:free --state state-C.jsonl --out traces-C.csv` |
| D | Matéo | `python skeleton-multi-llm-en.py --run --models groq:qwen/qwen3.8-27b --state state-D.jsonl --out traces-D.csv` |
| E | Christophe | `python skeleton-multi-llm-en.py --run --models openrouter:dots-studio/dots-3-note-preview:free --state state-E.jsonl --out traces-E.csv` |

If a run stops, rerun the same command: verified cells are not replayed and each cell gets at most two attempts.

## Counting sheet

`run-log-td1.csv`: before running, each operator gives their remaining allowance (and when it was read);
after running, the initial calls, retries, extra checks and remaining allowance. Retries and checks are
counted apart from the 100 initial calls (60 Groq, 40 OpenRouter).

## Merge and checks

Drop each operator's `traces-X.csv` **and** `state-X.jsonl`, unmodified, into `traces/raw/`, then from the
repository root:

```
python traces/merge_traces.py
```

It writes `traces-td1.csv` and `traces-td1.jsonl` at the root and `traces/merge-report.md`, and exits with
code 1 if a blocking problem is found:

- a CSV header that differs from the skeleton columns, or a CSV that does not match its JSONL;
- a file holding another model than its operator's;
- a missing cell among the 5 x 20 expected;
- more than one retry for a cell;
- several prompt fingerprints for one question;
- a trace reference that differs from `reference-td1.csv`.

It also reports rows by nature, call counts per provider, the final verdict per model and the measurements
left empty versus zero. The merge can be run after each operator finishes: missing cells are expected until
all five have run.
