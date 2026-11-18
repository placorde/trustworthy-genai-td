#!/usr/bin/env python3
"""TD2 cross-review by pair C: recheck pairs A and B independently, offline.

Run from the repository root (needs git and the branches fetched; standard library only):
    git fetch origin
    python td2/cross-review/check_pairs_a_b.py

Pair A's code and report are read from origin/td2-benchmarking-A, pair B's files from
origin/td2-wrong-consensus-b (git show), without merging them. Every number is recomputed from
traces-td1.csv, reference-td1.csv and the CSV files of the shop, not from the pairs' outputs.
Writes cross-review/check-pairs-a-b-output.md.
"""
import csv
import importlib.util
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
BRANCH_A = "origin/td2-benchmarking-A"
BRANCH_B = "origin/td2-wrong-consensus-b"
DB = ROOT / "kit-td1" / "data" / "boutique.sqlite"
OUT = []


def say(line=""):
    OUT.append(line)


def git_show(ref, path):
    return subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8", check=True).stdout


def check(label, ok, detail=""):
    say(f"| {label} | {'OK' if ok else '**FAIL**'} | {detail} |")
    return ok


def final_attempts():
    last = {}
    for r in csv.DictReader(open(ROOT / "td1" / "traces-td1.csv", encoding="utf-8")):
        key = (r["provider"], r["model_requested"], r["case_id"])
        if key not in last or int(r["attempts"]) > int(last[key]["attempts"]):
            last[key] = r
    return last


def load_vote_from_branch():
    code = git_show(BRANCH_A, "kit-td1/skeleton-multi-llm-en.py")
    kit = Path(tempfile.mkdtemp()) / "kit-td1"
    shutil.copytree(ROOT / "kit-td1", kit)  # the skeleton needs the kit files beside it
    tmp = kit / "skeleton_pair_a.py"
    tmp.write_text(code, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("skeleton_pair_a", tmp)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return lambda proposals, k: module.Orchestrateur.vote_k_sur_n(None, proposals, k)


def p(provider, model, value, verdict="executed"):
    return SimpleNamespace(provider=provider, model_requested=model, value=value, verdict=verdict)


def independent_vote(values, k):
    """Own counter: values = list of int or None (no vote)."""
    counts = Counter(v for v in values if v is not None)
    if not counts:
        return None, 0
    value, n = counts.most_common(1)[0]
    if list(counts.values()).count(n) > 1:
        return None, n
    return (value, n) if n >= k else (None, n)


def pair_a(last, ref):
    vote = load_vote_from_branch()
    say("## Pair A --- `vote_k_sur_n` and the 20-question table")
    say()
    say(f"Code read from `{BRANCH_A}:kit-td1/skeleton-multi-llm-en.py`.")
    say()
    say("| Contract test | Result | Detail |")
    say("|---|---|---|")
    three = [("g", "m1"), ("o", "m2"), ("g", "m3")]

    def refused(proposals, k):
        try:
            vote(proposals, k)
            return False
        except ValueError:
            return True

    check("k = 1 of 3 refused", refused([p(a, b, 1) for a, b in three], 1))
    check("k = 2 of 4 refused", refused([p(a, b, 1) for a, b in three + [("g", "m4")]], 2))
    check("k = 4 of 3 refused", refused([p(a, b, 1) for a, b in three], 4))
    check("duplicate (provider, model) refused", refused([p("g", "m1", 1), p("g", "m1", 1), p("o", "m2", 1)], 2))
    d = vote([p("g", "m1", 0), p("o", "m2", 0), p("g", "m3", 5)], 2)
    check("0 is a real value and can win", d["consensus"] and d["value"] == 0, str(d))
    d = vote([p("g", "m1", 7, "error"), p("o", "m2", 7, "error"), p("g", "m3", 7)], 2)
    check("an `error` proposal does not vote", not d["consensus"], str(d))
    d = vote([p("g", "m1", None, "error")] * 1 + [p("o", "m2", None, "error"), p("g", "m3", None, "error")], 2)
    check("nobody available: abstain, 0 votes", not d["consensus"] and d["votes"] == 0 and d["value"] is None, str(d))
    five = three + [("o", "m4"), ("g", "m5")]
    d = vote([p(a, b, v) for (a, b), v in zip(five, [1, 1, 2, 2, 3])], 3)
    check("2-2-1 of 5 with k = 3 abstains", not d["consensus"], str(d))
    say()

    p3 = [("groq", "openai/gpt-oss-120b"), ("openrouter", "cohere/north-mini-code:free"), ("groq", "qwen/qwen3.8-27b")]
    p5 = p3 + [("groq", "openai/gpt-oss-20b"), ("openrouter", "dots-studio/dots-3-note-preview:free")]

    def proposals(panel, case):
        out = []
        for prov, model in panel:
            r = last[(prov, model, case)]
            ok = r["verdict"] in ("correct", "incorrect") and r["value"] != ""
            out.append(p(prov, model, int(r["value"]) if ok else None, "executed" if ok else "error"))
        return out

    def fmt(consensus, value, votes, n):
        return f"{value} ({votes}/{n})" if consensus else f"Abstain (best {votes}/{n})"

    report = git_show(BRANCH_A, "reports/td2.md")
    say("Replay on C01-C20: pair A's code, my own counter, and the table of pair A's report.")
    say()
    say("| Question | Reference | 2-of-3 (code) | own | report | 3-of-5 (code) | own | report | Agree |")
    say("|---|---|---|---|---|---|---|---|---|")
    totals = {3: Counter(), 5: Counter()}
    all_agree = True
    for case in sorted(ref):
        cells = []
        for panel, k in ((p3, 2), (p5, 3)):
            n = len(panel)
            d = vote(proposals(panel, case), k)
            own_value, own_votes = independent_vote([x.value for x in proposals(panel, case)], k)
            code = fmt(d["consensus"], d["value"], d["votes"], n)
            own = fmt(own_value is not None, own_value, own_votes, n)
            totals[n]["correct" if d["consensus"] and d["value"] == ref[case] else
                      "wrong" if d["consensus"] else "abstain"] += 1
            cells.append((code, own))
        m = re.search(rf"^\| {case} \| \d+ \| ([^|]+) \| [^|]+ \| ([^|]+) \|", report, re.M)
        rep = (m.group(1).strip(), m.group(2).strip()) if m else ("missing", "missing")
        agree = cells[0][0] == cells[0][1] == rep[0] and cells[1][0] == cells[1][1] == rep[1]
        all_agree &= agree
        say(f"| {case} | {ref[case]} | {cells[0][0]} | {cells[0][1]} | {rep[0]} | {cells[1][0]} | {cells[1][1]} | {rep[1]} | {'yes' if agree else '**no**'} |")
    say()
    say(f"2-of-3: {totals[3]['correct']} correct, {totals[3]['wrong']} wrong, {totals[3]['abstain']} abstain. "
        f"3-of-5: {totals[5]['correct']} correct, {totals[5]['wrong']} wrong, {totals[5]['abstain']} abstain. "
        f"All 20 rows agree: {'yes' if all_agree else 'NO'}.")
    commented = sorted(set(re.findall(r"^- \*\*(C\d\d)\*\*", report, re.M)))
    missing = sorted(set(ref) - set(commented))
    say(f"Questions commented in \"Changes\": {len(commented)}/20; missing: {', '.join(missing) or 'none'}.")
    say()


def completed_age(born, on):
    return on.year - born.year - ((on.month, on.day) < (born.month, born.day))


def pair_b(last, ref):
    say("## Pair B --- wrong consensus C02")
    say()
    say(f"Files read from `{BRANCH_B}:wrong-consensus/`.")
    say()
    say("| Check | Result | Detail |")
    say("|---|---|---|")
    con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)

    def run(sql):
        return con.execute(sql).fetchall()

    trace = {m: last[(prov, m, "C02")] for prov, m in [
        ("groq", "openai/gpt-oss-20b"), ("openrouter", "cohere/north-mini-code:free"),
        ("groq", "openai/gpt-oss-120b"), ("groq", "qwen/qwen3.8-27b"),
        ("openrouter", "dots-studio/dots-3-note-preview:free")]}
    for f, model in (("m1-gpt-oss-20b.sql", "openai/gpt-oss-20b"), ("m2-cohere.sql", "cohere/north-mini-code:free")):
        sql = git_show(BRANCH_B, f"wrong-consensus/{f}")
        body = "\n".join(l for l in sql.splitlines() if not l.startswith("--"))
        same = " ".join(body.split()).rstrip(";") == " ".join(trace[model]["sql"].split()).rstrip(";")
        check(f"`{f}` is the SQL stored in the TD1 trace", same)
        value = run(body)[0][0]
        check(f"`{f}` returns 0 (trace value {trace[model]['value']})", value == 0 and trace[model]["value"] == "0", str(value))
    value = run(git_show(BRANCH_B, "wrong-consensus/ref.sql"))[0][0]
    check("`ref.sql` returns the reference", value == ref["C02"] == 590320, str(value))

    rows = run(git_show(BRANCH_B, "wrong-consensus/delta.sql"))
    on = date(2026, 9, 25)
    customers = list(csv.DictReader(open(ROOT / "kit-td1" / "data" / "customers.csv", encoding="utf-8")))
    aged_25 = sorted(c["customer_id"] for c in customers
                     if completed_age(date.fromisoformat(c["birth_date"]), on) == 25)
    check("delta rows = customers of completed age 25 (computed in Python from customers.csv)",
          sorted(r[0] for r in rows) == aged_25, f"{len(rows)} rows: {', '.join(aged_25)}")
    check("delta total = reference 590320", sum(r[2] for r in rows) == 590320, str(sum(r[2] for r in rows)))
    c001 = next(r[2] for r in rows if r[0] == "C001")
    check("Dots' 135000 is exactly C001's revenue", c001 == 135000 and trace["dots-studio/dots-3-note-preview:free"]["value"] == "135000")

    def decide(models, k):
        return independent_vote([int(trace[m]["value"]) for m in models], k)

    v, n = decide(["openai/gpt-oss-120b", "cohere/north-mini-code:free", "openai/gpt-oss-20b"], 2)
    check("with gpt-oss-20b instead of Qwen, 2-of-3 returns the wrong 0", v == 0, f"{v} ({n}/3)")
    v, n = decide(list(trace), 3)
    check("3-of-5 abstains on C02 (2 against 2)", v is None and n == 2, f"best {n}/5")
    say()


def pair_b_on_c(last, ref):
    say("## Pair B's remarks on pair C, rechecked")
    say()
    say("| Claim | Result | Detail |")
    say("|---|---|---|")
    l1 = [("openrouter", "cohere/north-mini-code:free"), ("openrouter", "dots-studio/dots-3-note-preview:free"),
          ("groq", "openai/gpt-oss-20b")]
    wrong = []
    for case in sorted(ref):
        v, _ = independent_vote([int(last[(a, b, case)]["value"]) if last[(a, b, case)]["value"] else None
                                 for a, b in l1], 2)
        if v is not None and v != ref[case]:
            wrong.append(f"{case}={v}")
    check("L1 panel would give wrong consensuses only on C02 and C19 over the 20 questions",
          [w.split("=")[0] for w in wrong] == ["C02", "C19"], ", ".join(wrong))
    l3 = [("groq", "openai/gpt-oss-20b"), ("groq", "openai/gpt-oss-120b"), ("openrouter", "dots-studio/dots-3-note-preview:free")]
    res = Counter()
    for case in sorted(ref):
        vals = []
        for a, b in l3:
            r = last[(a, b, case)]
            vals.append(int(r["value"]) if r["verdict"] in ("correct", "incorrect") and r["value"] != "" else None)
        v, _ = independent_vote(vals, 2)
        res["abstain" if v is None else "correct" if v == ref[case] else "wrong"] += 1
    check("L3 panel on the 20 questions: 17 correct, 3 abstain, 0 wrong",
          (res["correct"], res["abstain"], res["wrong"]) == (17, 3, 0), dict(res).__repr__())
    say()


def main():
    last = final_attempts()
    ref = {r["case_id"]: int(r["revenue_cents"]) for r in csv.DictReader(open(ROOT / "td1" / "reference-td1.csv", encoding="utf-8"))}
    say("# Cross-review by pair C --- raw output of `cross-review/check_pairs_a_b.py`")
    say()
    pair_a(last, ref)
    pair_b(last, ref)
    pair_b_on_c(last, ref)
    (ROOT / "td2" / "cross-review" / "check-pairs-a-b-output.md").write_text("\n".join(OUT) + "\n", encoding="utf-8")
    print("\n".join(OUT))


if __name__ == "__main__":
    main()
