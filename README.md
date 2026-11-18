# Trustworthy Generative AI --- DIA3 / DIA3-G5

- **DIA class:** DIA3
- **Sub-group:** DIA3-G5
- **Members:** Robin, Raphaël, Thomas, Matéo, Christophe, Pierre-Louis, Florentin

ESILV, Next-Generation AI module (Data & AI major, year 4). Shared repository for one sub-group, kept
public and read-accessible without sign-in from TD1 through TD3.

## Members and TD1 roles

Seven members, so the F-H duties are shared by F and G. Roles rotate in TD2 and TD3.

| Role | Member | TD1 task |
|---|---|---|
| A | Robin | Groq: `openai/gpt-oss-120b` |
| B | Raphaël | Groq: `openai/gpt-oss-20b` |
| C | Thomas | OpenRouter: `cohere/north-mini-code:free` |
| D | Matéo | Groq: `qwen/qwen3.8-27b` |
| E | Christophe | OpenRouter: `dots-studio/dots-3-note-preview:free` |
| F + H | Pierre-Louis | Reference cross-checks, run coordination and counting, trace merge |
| G | Florentin | Five-model summary, comparison table and pivot (TD1 review carried out by F, see `reports/td1-review.md`) |

## Course pack and environment

- Pack version: TD1 batches ran with the kit of pack `2026-10-14-students-1`; the site moved to
  `2026-10-18-students-1` (18 October 2026). The code, the database, the questions and the model selection
  are byte-identical between the two packs; `kit-td1/` holds the 18 October copy. The published reference
  values of 21 October equal our `reference-td1.csv` on all twenty questions.
- Model configuration read by the code: [`kit-td1/modeles-autorises.json`](kit-td1/modeles-autorises.json)
  (selection of 14 October 2026: providers, exact identifiers, parameters; no key). No replacement model
  was used in TD1.
- Database: `kit-td1/data/boutique.sqlite`, seed 20260925, SHA-256 `0077e235...3398fec2`, identical to
  `kit-td1/data/manifest.json` (`python kit-td1/verify-data.py`).
- Python 3.10+ (tested with 3.14.7), standard library only; `requests` only for `kit-td1/check_access.py`.
  API keys stay in the `GROQ_API_KEY` and `OPENROUTER_API_KEY` environment variables, never in the repository.

## Repository layout

The work is grouped by session. Each TD folder has its own README with its files and its replay commands.

| Path | Content |
|---|---|
| [`td1/`](td1/README.md) | TD1 --- compare (21 October 2026): references, traces of the five models, comparison, summary, prompts, contributions, report |
| [`td2/`](td2/README.md) | TD2 --- vote and route (18 November 2026): k-of-n vote (pair A), wrong consensus (pair B), routing rule (pair C), report |
| `kit-td1/` | Student kit shared by every TD: `skeleton-multi-llm-en.py` (common prompt, one client interface for both providers, error handling and retries, read-only sandbox, one trace line per call; `vote_k_sur_n` completed in TD2 by pair A), `sandbox_sqlite.py`, `modeles-autorises.json`, `check_access.py`, `atelier-vote.py`, `atelier-routage.py`, `data/`. Every other kit file is unmodified |
| `PROJECT-STATUS.md` | What is done and what remains, TD1 to TD3 |

## Reproducing

From a fresh clone, from the repository root, with no other download (offline, no key needed):

```powershell
python kit-td1/verify-data.py
```

checks the database against its manifest; then follow [`td1/README.md`](td1/README.md) and
[`td2/README.md`](td2/README.md).

## Contributing during a session

Work on your own branch from an up-to-date `master`, commit only your own files (traces go straight into
`td1/traces/raw/`), never commit keys, `.env` files or `ready-for-td1.txt`, then open a pull request.
Shared files (`td1/reference-td1.csv`, merged traces, summaries, README) are updated by F/G.

## Hand-in

For each TD, the Moodle submission records: this repository's URL, the sub-group and member names, the
exact commit hash of the submitted version, and a direct link to that session's report at that commit.
