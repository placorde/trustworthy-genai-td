# TD1 review of the comparison and summary (G task)

Review of `model-question-comparison-en.csv` and `five-model-summary-en.csv` before closing TD1. Florentin (G)
was not available to do it; it was done by Pierre-Louis (F) with coding assistance (declared in
`prompts-en.md`). Method: each failing query of `traces-td1.csv` is executed again on `boutique.sqlite`
(read-only), then executed a second time returning the distinct birth dates it selects instead of the sum, so
the written cause can be checked against what the query actually keeps.

Customers aged exactly 25 on 2026-09-25 are born 2000-09-26 to 2001-09-25.

| Cell | Value re-run = trace | Birth dates the query keeps | Cause in the CSV |
|---|---|---|---|
| `groq:openai/gpt-oss-120b:C17` | yes (80190) | 2001-09-25 | confirmed |
| `groq:openai/gpt-oss-20b:C02` | yes (0) | none | confirmed |
| `groq:openai/gpt-oss-20b:C08` | yes (25920) | 2001-09-24 | confirmed |
| `groq:openai/gpt-oss-20b:C11` | yes (322160) | 2001-12-08, 2004-07-12, 2005-11-20, 2006-08-15 | confirmed |
| `openrouter:cohere/north-mini-code:free:C02` | yes (0) | none | confirmed |
| `openrouter:cohere/north-mini-code:free:C08` | yes (1188090) | 13 dates, 2000-09-25 to 2006-08-15 | confirmed |
| `openrouter:cohere/north-mini-code:free:C09` | yes (1901780) | 35 dates, 1958-06-08 to 2001-09-26 | confirmed |
| `openrouter:cohere/north-mini-code:free:C10` | yes (219930) | 2004-07-12, 2005-11-20, 2006-08-15 | confirmed |
| `openrouter:cohere/north-mini-code:free:C11` | yes (768850) | 10 dates, 2001-03-10 to 2006-08-15 | confirmed |
| `openrouter:cohere/north-mini-code:free:C15` | yes (314020) | 10 dates, 2000-09-26 to 2006-08-15 | confirmed |
| `openrouter:cohere/north-mini-code:free:C17` | yes (197080) | 2000-11-30, 2001-03-10, 2001-05-15, 2001-09-24, 2001-09-25, 2001-09-26 | made precise |
| `openrouter:cohere/north-mini-code:free:C18` | yes (67150) | 1969-02-04, 1972-04-27, 1975-01-20, 1983-02-19, 1985-03-21, 1995-01-04 | made precise |
| `openrouter:cohere/north-mini-code:free:C19` | yes (71640) | 9 dates, 1958-06-08 to 2001-09-24 | confirmed |
| `groq:qwen/qwen3.8-27b:C10` | yes (119410) | 2001-03-10, 2001-05-15 | confirmed |
| `groq:qwen/qwen3.8-27b:C15` | yes (0) | none | confirmed |
| `groq:qwen/qwen3.8-27b:C16` | yes (208520) | 2000-08-14, 2001-09-25, 2001-09-26, 2001-11-30, 2001-12-08 | confirmed |
| `groq:qwen/qwen3.8-27b:C17` | yes (248490) | 2000-09-25, 2000-09-26, 2000-11-30, 2001-03-10, 2001-05-15, 2001-09-24 | confirmed |
| `groq:qwen/qwen3.8-27b:C19` | yes (83580) | 10 dates, 1958-06-08 to 2001-12-08 | confirmed |
| `openrouter:dots-studio/dots-3-note-preview:free:C02` | yes (135000) | 2001-09-25 | confirmed |
| `openrouter:dots-studio/dots-3-note-preview:free:C09` | yes (47900) | 2001-09-26 | confirmed |
| `openrouter:dots-studio/dots-3-note-preview:free:C11` | yes (0) | none | confirmed |
| `openrouter:dots-studio/dots-3-note-preview:free:C15` | yes (138920) | 2001-05-15, 2001-09-24, 2001-09-25 | confirmed |
| `openrouter:dots-studio/dots-3-note-preview:free:C18` | yes (39580) | 2001-05-15 | confirmed |
| `openrouter:dots-studio/dots-3-note-preview:free:C19` | yes (71640) | 9 dates, 1958-06-08 to 2001-09-24 | confirmed |

The `sql_invalid` cell (`openrouter:dots-studio/dots-3-note-preview:free:C17`) fails to parse again with the
same `syntax error near "AS"`. Two explanations were made more precise from this check (Cohere C17: it keeps
2001-09-26 and drops 2000-09-26; Cohere C18: it keeps only customers aged 31 or more). Example of a
quantitative check: Dots C15 misses exactly the customers born 2000-09-26 and 2000-11-30 (17540 + 12220 =
29760 = 168680 - 138920).

**Summary rows.** Index values (gpt-oss-120b 11.6, gpt-oss-20b 9, qwen3.8-27b 33.7) match
`portefeuille-modeles-2026-09-28.csv`; billed prices (0.15/0.60, 0.075/0.30, 0.80/4.00 USD per million
tokens) match `methode-cout-en.md` step 2; Cohere and Dots are N/A with the reason given there. Per-family
counts match the pivot view [`results-pivot-td1.md`](../results-pivot-td1.md), regenerated from the CSV.
