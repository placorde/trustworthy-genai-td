import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

COLUMNS = ["cell_id", "provider", "model_requested", "model_returned", "case_id", "question", "prompt_sha256",
           "sql", "value", "reference", "verdict", "verdict_detail", "http_status", "error", "latency_ms",
           "tokens_prompt", "tokens_completion", "tokens_reasoning", "cost_native", "attempts", "date_utc", "nature"]

OPERATORS = {
    "A": "groq:openai/gpt-oss-120b",
    "B": "groq:openai/gpt-oss-20b",
    "C": "openrouter:cohere/north-mini-code:free",
    "D": "groq:qwen/qwen3.8-27b",
    "E": "openrouter:dots-studio/dots-3-note-preview:free",
}

MEASURES = ["http_status", "latency_ms", "tokens_prompt", "tokens_completion", "tokens_reasoning", "cost_native"]
CASES = [f"C{i:02d}" for i in range(1, 21)]


class Report:
    def __init__(self):
        self.errors, self.warnings, self.lines = [], [], []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def info(self, msg=""):
        self.lines.append(msg)

    def render(self):
        out = list(self.lines)
        out += ["", f"## Blocking problems ({len(self.errors)})"] + [f"- {e}" for e in self.errors or ["none"]]
        out += ["", f"## Warnings ({len(self.warnings)})"] + [f"- {w}" for w in self.warnings or ["none"]]
        return "\n".join(out)


def operator_of(path):
    match = re.fullmatch(r"(?:traces|state)-([A-Za-z0-9]+)\.(?:csv|jsonl)", path.name)
    return match.group(1).upper() if match else None


def read_csv(path, report):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            report.error(f"{path.name}: header differs from the skeleton columns: {reader.fieldnames}")
        return list(reader)


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_references(path):
    with open(path, newline="", encoding="utf-8") as f:
        return {r["case_id"]: r["revenue_cents"].strip() for r in csv.DictReader(f)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=ROOT / "traces" / "raw")
    parser.add_argument("--out-csv", type=Path, default=ROOT / "traces-td1.csv")
    parser.add_argument("--out-jsonl", type=Path, default=ROOT / "traces-td1.jsonl")
    parser.add_argument("--reference", type=Path, default=ROOT / "reference-td1.csv")
    parser.add_argument("--report", type=Path, default=ROOT / "traces" / "merge-report.md")
    parser.add_argument("--nature", default="real")
    parser.add_argument("--expect", nargs="*", default=None,
                        help="OPERATOR=provider:model pairs, default: the five TD1 operators A-E")
    args = parser.parse_args()

    expected = dict(e.split("=", 1) for e in args.expect) if args.expect else OPERATORS
    report = Report()
    references = load_references(args.reference)

    csv_files = sorted(args.raw.glob("traces-*.csv"))
    if not csv_files:
        sys.exit(f"No traces-*.csv in {args.raw}")

    merged_rows, merged_jsonl = [], []
    per_file = []
    for path in csv_files:
        op = operator_of(path)
        rows = read_csv(path, report)
        state = path.with_name(f"state-{path.stem.split('-', 1)[1]}.jsonl")
        records = read_jsonl(state) if state.exists() else None
        if records is None:
            report.error(f"{path.name}: matching {state.name} missing (keep the original JSONL)")
        elif len(records) != len(rows):
            report.error(f"{path.name}: {len(rows)} CSV rows but {len(records)} lines in {state.name}")
        else:
            for row, record in zip(rows, records):
                if row["cell_id"] != record.get("cell_id") or row["date_utc"] != record.get("date_utc"):
                    report.error(f"{path.name}: CSV and {state.name} disagree at cell {row['cell_id']}")
                    break
        models = {f"{r['provider']}:{r['model_requested']}" for r in rows}
        if op in expected and models - {expected[op]}:
            report.error(f"{path.name}: operator {op} should only hold {expected[op]}, found {sorted(models)}")
        if op not in expected:
            report.warn(f"{path.name}: operator '{op}' not in the expected allocation")
        per_file.append((path.name, op, len(rows)))
        merged_rows += rows
        merged_jsonl += records or []

    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged_rows)
    with open(args.out_jsonl, "w", encoding="utf-8") as f:
        for record in merged_jsonl:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    report.info("# TD1 trace merge report")
    report.info()
    report.info(f"Merged {len(merged_rows)} rows from {len(csv_files)} files into `{args.out_csv.name}` "
                f"and `{args.out_jsonl.name}`.")
    report.info()
    report.info("| File | Operator | Rows |")
    report.info("|---|---|---|")
    for name, op, n in per_file:
        report.info(f"| {name} | {op} | {n} |")

    natures = Counter(r["nature"] for r in merged_rows)
    report.info()
    report.info("Rows by nature: " + ", ".join(f"{k}={v}" for k, v in sorted(natures.items())))
    for nature in natures:
        if nature != args.nature:
            report.warn(f"{natures[nature]} rows of nature '{nature}': never count them with '{args.nature}' rows")

    rows = [r for r in merged_rows if r["nature"] == args.nature]
    by_cell = defaultdict(list)
    for r in rows:
        by_cell[r["cell_id"]].append(r)

    expected_cells = {f"{m}:{c}" for m in expected.values() for c in CASES}
    missing = sorted(expected_cells - set(by_cell))
    extra = sorted(set(by_cell) - expected_cells)
    report.info(f"Cells ({args.nature}): {len(by_cell)} found / {len(expected_cells)} expected")
    if missing:
        report.error(f"{len(missing)} expected cells have no attempt: {', '.join(missing)}")
    if extra:
        report.warn(f"{len(extra)} cells outside the allocation: {', '.join(extra)}")

    for cell, attempts in by_cell.items():
        numbers = [int(a["attempts"] or 0) for a in attempts]
        if len(attempts) > 2 or max(numbers) > 2:
            report.error(f"{cell}: {len(attempts)} rows, attempts {numbers} (at most one retry per cell)")
        if numbers != sorted(numbers):
            report.warn(f"{cell}: attempt numbers not in chronological order {numbers}")

    sha_by_case = defaultdict(set)
    for r in rows:
        sha_by_case[r["case_id"]].add(r["prompt_sha256"])
    for case, shas in sorted(sha_by_case.items()):
        if len(shas) > 1:
            report.error(f"{case}: {len(shas)} different prompt fingerprints across models "
                         f"(changed prompt or reference = separate experiment)")

    for r in rows:
        ref = references.get(r["case_id"], "")
        if r["reference"] != ref:
            report.error(f"{r['cell_id']}: trace reference '{r['reference']}' differs from reference-td1.csv '{ref}'")

    initial = Counter()
    retries = Counter()
    for r in rows:
        provider = r["provider"]
        (initial if r["attempts"] in ("1", "") else retries)[provider] += 1
    report.info()
    report.info("## Call counts")
    report.info()
    report.info("| Provider | Initial calls | Retries | Total |")
    report.info("|---|---|---|---|")
    for provider in sorted(set(initial) | set(retries)):
        report.info(f"| {provider} | {initial[provider]} | {retries[provider]} | {initial[provider] + retries[provider]} |")

    report.info()
    report.info("## Final verdict per model (last attempt of each cell)")
    report.info()
    verdicts = sorted({cell[-1]["verdict"] or "(empty)" for cell in by_cell.values()})
    report.info("| Model | " + " | ".join(verdicts) + " |")
    report.info("|---|" + "---|" * len(verdicts))
    table = defaultdict(Counter)
    for cell in by_cell.values():
        last = cell[-1]
        table[f"{last['provider']}:{last['model_requested']}"][last["verdict"] or "(empty)"] += 1
    for model in sorted(table):
        report.info(f"| {model} | " + " | ".join(str(table[model][v]) for v in verdicts) + " |")

    report.info()
    report.info("## Measurements left empty (empty is not zero)")
    report.info()
    report.info("| Column | Empty | Zero |")
    report.info("|---|---|---|")
    for col in MEASURES:
        empty = sum(1 for r in rows if r[col] == "")
        zero = sum(1 for r in rows if r[col] != "" and float(r[col]) == 0)
        report.info(f"| {col} | {empty} | {zero} |")
        if zero and col in ("tokens_prompt", "tokens_completion", "latency_ms"):
            report.warn(f"{zero} rows with {col} = 0: check it is a measurement, not a missing value")

    text = report.render()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(text + "\n", encoding="utf-8")
    print(text)
    sys.exit(1 if report.errors else 0)


if __name__ == "__main__":
    main()
