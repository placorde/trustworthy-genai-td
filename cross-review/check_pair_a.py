"""TD2 cross-review by pair B: check pair A's `vote_k_sur_n` and its 20-question table.

Run from the repository root (no network, standard library only):
    python cross-review/check_pair_a.py --skeleton kit-td1/skeleton-multi-llm-en.py --report reports/td2.md

What it does:
1. contract tests on pair A's method (threshold, duplicates, unavailable members, abstention);
2. replays 2-of-3 (fixed panel) and 3-of-5 (all five TD1 models) on C01-C20 with pair A's method,
   using the last attempt of each model (latest `date_utc`);
3. recounts the same votes with an independent counter written here (not pair A's code);
4. compares both with the table in pair A's report and with `reference-td1.csv`.
"""
import argparse
import collections
import csv
import importlib.util
import re
import sys
from pathlib import Path
from types import SimpleNamespace

PANEL3 = [("groq", "openai/gpt-oss-120b"), ("openrouter", "cohere/north-mini-code:free"),
          ("groq", "qwen/qwen3.8-27b")]
PANEL5 = PANEL3 + [("groq", "openai/gpt-oss-20b"), ("openrouter", "dots-studio/dots-3-note-preview:free")]


def load_vote(path):
    spec = importlib.util.spec_from_file_location("pair_a_skeleton", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return lambda proposals, k: module.Orchestrateur.vote_k_sur_n(None, proposals, k)


def p(provider, model, value, verdict="executed"):
    return SimpleNamespace(provider=provider, model_requested=model, value=value, verdict=verdict)


def contract_tests(vote):
    a, b, c = PANEL3
    d, e = PANEL5[3], PANEL5[4]
    tests = []

    def expect(name, fn, check):
        try:
            out = fn()
            ok = check(out)
            tests.append((name, ok, out))
        except Exception as exc:  # a refusal is an exception
            ok = check(exc)
            tests.append((name, ok, f"{type(exc).__name__}: {exc}"))

    three = [p(*a, 100), p(*b, 100), p(*c, 120)]
    expect("agreement 100,100,120 k=2 -> consensus 100 (2 votes)", lambda: vote(three, 2),
           lambda o: isinstance(o, dict) and o["consensus"] and o["value"] == 100 and o["votes"] == 2)
    expect("k=1 of n=3 is refused (not a strict majority)", lambda: vote(three, 1),
           lambda o: isinstance(o, ValueError))
    expect("k=4 of n=3 is refused (k > n)", lambda: vote(three, 4), lambda o: isinstance(o, ValueError))
    four = three + [p(*d, 100)]
    expect("k=2 of n=4 is refused (2 is not > 4//2)", lambda: vote(four, 2), lambda o: isinstance(o, ValueError))
    dup = [p(*a, 100), p(*a, 100), p(*c, 120)]
    expect("duplicate (provider, model) is refused", lambda: vote(dup, 2), lambda o: isinstance(o, ValueError))
    unav = [p(*a, 100), p(*b, None, "error"), p(*c, None, "error")]
    expect("100 + 2 unavailable, k=2 -> abstain, unavailable stay in n", lambda: vote(unav, 2),
           lambda o: isinstance(o, dict) and not o["consensus"] and o["value"] is None and o["votes"] == 1)
    allerr = [p(*a, None, "error"), p(*b, None, "error"), p(*c, None, "error")]
    expect("all unavailable -> abstain with 0 votes", lambda: vote(allerr, 2),
           lambda o: isinstance(o, dict) and not o["consensus"] and o["votes"] == 0 and o["models"] == [])
    zeros = [p(*a, 0), p(*b, 0), p(*c, 100)]
    expect("0 is a real value: 0,0,100 k=2 -> consensus 0", lambda: vote(zeros, 2),
           lambda o: isinstance(o, dict) and o["consensus"] and o["value"] == 0)
    tie5 = [p(*a, 1), p(*b, 1), p(*c, 2), p(*d, 2), p(*e, 3)]
    expect("tie 2-2-1 of n=5, k=3 -> abstain with votes=2", lambda: vote(tie5, 3),
           lambda o: isinstance(o, dict) and not o["consensus"] and o["value"] is None and o["votes"] == 2)
    err_with_value = [p(*a, 100), p(*b, 100, "error"), p(*c, 120)]
    expect("an `error` proposal does not vote even if it carries a value", lambda: vote(err_with_value, 2),
           lambda o: isinstance(o, dict) and not o["consensus"] and o["votes"] == 1)
    return tests


def last_attempts(rows):
    """(case, provider, model) -> row with the latest date_utc; also report if CSV order disagrees."""
    by_date, by_order = {}, {}
    for r in rows:
        key = (r["case_id"], r["provider"], r["model_requested"])
        by_order[key] = r
        if key not in by_date or r["date_utc"] >= by_date[key]["date_utc"]:
            by_date[key] = r
    disagree = [k for k in by_date if by_date[k] is not by_order[k]]
    return by_date, disagree


def proposals(last, case, panel):
    out = []
    for provider, model in panel:
        r = last.get((case, provider, model), {})
        valid = r.get("verdict") in {"correct", "incorrect"} and r.get("value", "") != ""
        out.append(p(provider, model, int(r["value"]) if valid else None, "executed" if valid else "error"))
    return out


def own_count(props, k):
    """Independent counter (pair B), same contract, not pair A's code."""
    counts = collections.Counter(x.value for x in props if x.verdict == "executed" and x.value is not None)
    if not counts:
        return {"consensus": False, "value": None, "votes": 0}
    value, votes = counts.most_common(1)[0]
    if votes >= k:
        return {"consensus": True, "value": value, "votes": votes}
    return {"consensus": False, "value": None, "votes": votes}


def fmt(d, n):
    return f"{d['value']} ({d['votes']}/{n})" if d["consensus"] else f"Abstain (best {d['votes']}/{n})"


def report_table(path):
    """Parse pair A's table: | Cxx | ref | 2-of-3 | matches | 3-of-5 | matches |"""
    table = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(C\d\d)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*[^|]*\|\s*([^|]+?)\s*\|", line)
        if m:
            table[m.group(1)] = (int(m.group(2)), m.group(3), m.group(4))
    return table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skeleton", default="kit-td1/skeleton-multi-llm-en.py")
    ap.add_argument("--report", default="reports/td2.md")
    ap.add_argument("--traces", default="traces-td1.csv")
    ap.add_argument("--reference", default="reference-td1.csv")
    args = ap.parse_args()

    vote = load_vote(args.skeleton)
    print("## 1. Contract tests on pair A's vote_k_sur_n\n")
    print("| Test | Result | Output |\n|---|---|---|")
    tests = contract_tests(vote)
    for name, ok, out in tests:
        print(f"| {name} | {'PASS' if ok else 'FAIL'} | `{out}` |")
    print(f"\n{sum(ok for _, ok, _ in tests)}/{len(tests)} tests pass.\n")

    rows = list(csv.DictReader(open(args.traces, encoding="utf-8")))
    refs = {r["case_id"]: int(r["revenue_cents"]) for r in csv.DictReader(open(args.reference, encoding="utf-8"))}
    last, disagree = last_attempts(rows)
    table = report_table(args.report)

    print("## 2. Replay on C01-C20 (pair A's method vs independent recount vs pair A's report)\n")
    print(f"Last attempt = latest `date_utc` per model and question; CSV order and date order "
          f"{'agree on every cell' if not disagree else 'DISAGREE on ' + str(disagree)}.\n")
    print("| Q | Ref | 2-of-3 (A's method) | 2-of-3 (recount) | 2-of-3 in A's report | 3-of-5 (A's method) "
          "| 3-of-5 (recount) | 3-of-5 in A's report | Same everywhere? |")
    print("|---|---:|---|---|---|---|---|---|---|")
    mismatches, tally = [], {"2-of-3": collections.Counter(), "3-of-5": collections.Counter()}
    for i in range(1, 21):
        q = f"C{i:02d}"
        a3, a5 = vote(proposals(last, q, PANEL3), 2), vote(proposals(last, q, PANEL5), 3)
        o3, o5 = own_count(proposals(last, q, PANEL3), 2), own_count(proposals(last, q, PANEL5), 3)
        r3, r5 = (table.get(q, (None, "missing", "missing"))[1:])
        same = fmt(a3, 3) == fmt(o3, 3) == r3 and fmt(a5, 5) == fmt(o5, 5) == r5
        if not same:
            mismatches.append(q)
        for label, d in (("2-of-3", a3), ("3-of-5", a5)):
            tally[label]["abstain" if not d["consensus"] else
                         ("correct" if d["value"] == refs[q] else "WRONG")] += 1
        print(f"| {q} | {refs[q]} | {fmt(a3, 3)} | {fmt(o3, 3)} | {r3} | {fmt(a5, 5)} | {fmt(o5, 5)} | {r5} "
              f"| {'yes' if same else '**NO**'} |")
    print()
    for label, c in tally.items():
        print(f"- {label}: {c['correct']} correct, {c['WRONG']} wrong consensus, {c['abstain']} abstentions")
    print(f"- Questions where something differs: {mismatches if mismatches else 'none'}")


if __name__ == "__main__":
    main()
