# Trustworthy Generative AI --- Sub-group repository (TD1 -> TD3)

ESILV, Next-Generation AI module (Data & AI major, year 4). Shared repository for one sub-group, kept
public and read-accessible without sign-in from TD1 through TD3.

## Sub-group and members

<!-- TODO: fill in before the first hand-in -->
- Member A --- role (e.g. Groq: openai/gpt-oss-120b)
- Member B --- role (e.g. Groq: openai/gpt-oss-20b)
- Member C --- role (e.g. OpenRouter: cohere/north-mini-code:free)
- Member D --- role (e.g. Groq: qwen/qwen3.8-27b)
- Member E --- role (e.g. OpenRouter: dots-studio/dots-3-note-preview:free)
- Members F, G, H --- reference-checking, trace merging, synthesis

## Course pack and environment

- Pack version: `2026-10-14-students-1` (14 October 2026) --- see `modeles-autorises.json` in the kit.
- Python 3.10+ (tested with 3.14.7), virtual environment in `kit-td1/.venv`.
- Dependency: `requests` (see `kit-td1/requirements` section of the environment guide).

## Reproducing the setup check

```powershell
cd kit-td1
.venv\Scripts\Activate.ps1
python check_access.py | Tee-Object ready-for-td1.txt
```

`modeles-autorises.json` must be dated `2026-10-14`; a passing run reports 5/5 required models `[OK]`.

## Repository layout

- `reports/` --- one Markdown report per session (`td1.md`, `td2.md`, `td3.md`), added after each TD.
- `.gitignore` --- copied from the student kit; keeps API keys, `.env` files and local caches out of this
  public repository.

## Hand-in

For each TD, the Moodle submission records: this repository's URL, the sub-group and member names, the
exact commit hash of the submitted version, and a direct link to that session's report at that commit.
