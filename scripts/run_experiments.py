#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=False, text=True, capture_output=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


@dataclass
class CaseResult:
    name: str
    title: str
    expected: str
    alive_status: str
    alive_correct: int
    alive_incorrect: int
    alive_errors: int
    baseline_changed: bool
    candidate_differs_from_baseline: bool
    classification: str
    notes: str


def parse_info(case_file: Path) -> tuple[str, str]:
    title = case_file.stem
    expected = "unknown"
    text = read_text(case_file)
    for line in text.splitlines():
        if line.startswith("; TITLE:"):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("; EXPECTED:"):
            expected = line.split(":", 1)[1].strip().lower()
    return title, expected


def parse_alive_summary(text: str) -> tuple[int, int, int]:
    correct = incorrect = errors = 0
    m = re.search(r"(\d+)\s+correct transformations", text)
    if m:
        correct = int(m.group(1))
    m = re.search(r"(\d+)\s+incorrect transformations", text)
    if m:
        incorrect = int(m.group(1))
    m = re.search(r"(\d+)\s+Alive2 errors", text)
    if m:
        errors = int(m.group(1))
    return correct, incorrect, errors


def has_functional_diff(llvm_diff_output: str) -> bool:
    content = llvm_diff_output.strip()
    if not content:
        return False
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        # Ignore pure naming/noise lines if any appear.
        if stripped.startswith("in function"):
            continue
        return True
    return False


def classify(expected: str, alive_ok: bool, baseline_changed: bool, cand_diff_baseline: bool) -> str:
    if not alive_ok:
        return "invalid_candidate"
    if expected == "missed":
        if (not baseline_changed) and cand_diff_baseline:
            return "confirmed_missed"
        if baseline_changed and cand_diff_baseline:
            return "different_but_not_missed"
        return "not_missed"
    if expected == "already-optimized":
        if baseline_changed:
            return "baseline_optimizes"
        return "unexpected_baseline_behavior"
    return "needs_review"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run LLVM peephole assignment experiments.")
    parser.add_argument("--cases-dir", required=True)
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--llvm-bin", required=True)
    parser.add_argument("--alive-tv", required=True)
    args = parser.parse_args()

    cases_dir = Path(args.cases_dir)
    results_dir = Path(args.results_dir)
    llvm_bin = Path(args.llvm_bin)
    alive_tv = Path(args.alive_tv)

    for tool in ["opt", "llvm-diff", "llvm-as", "llvm-dis", "llc"]:
        p = llvm_bin / tool
        if not p.exists():
            raise SystemExit(f"Missing tool: {p}")
    if not alive_tv.exists():
        raise SystemExit(f"Missing tool: {alive_tv}")

    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    cases = sorted(
        p for p in cases_dir.glob("*.ll") if not p.name.endswith(".candidate.ll")
    )
    if not cases:
        raise SystemExit(f"No .ll cases found in {cases_dir}")

    all_results: list[CaseResult] = []

    for case in cases:
        name = case.stem
        title, expected = parse_info(case)
        src_file = case
        candidate_file = cases_dir / f"{name}.candidate.ll"
        if not candidate_file.exists():
            raise SystemExit(f"Missing candidate file for {name}: {candidate_file}")

        out_dir = results_dir / name
        out_dir.mkdir(parents=True, exist_ok=True)

        baseline_file = out_dir / "baseline.ll"
        baseline_cmd = [
            str(llvm_bin / "opt"),
            "-S",
            "-passes=instcombine,simplifycfg",
            str(src_file),
            "-o",
            str(baseline_file),
        ]
        baseline_run = run_cmd(baseline_cmd)
        write_text(out_dir / "baseline.stderr.txt", baseline_run.stderr)
        if baseline_run.returncode != 0:
            raise SystemExit(f"Baseline opt failed for {name}:\n{baseline_run.stderr}")

        alive_cmd = [str(alive_tv), str(src_file), str(candidate_file)]
        alive_run = run_cmd(alive_cmd)
        write_text(out_dir / "alive-tv.txt", alive_run.stdout + alive_run.stderr)
        correct, incorrect, errors = parse_alive_summary(alive_run.stdout + alive_run.stderr)
        alive_ok = correct > 0 and incorrect == 0 and errors == 0

        baseline_diff_run = run_cmd([str(llvm_bin / "llvm-diff"), str(src_file), str(baseline_file)])
        write_text(out_dir / "baseline.diff.txt", baseline_diff_run.stdout + baseline_diff_run.stderr)
        baseline_changed = has_functional_diff(baseline_diff_run.stdout + baseline_diff_run.stderr)

        cand_vs_base_run = run_cmd([str(llvm_bin / "llvm-diff"), str(candidate_file), str(baseline_file)])
        write_text(out_dir / "candidate_vs_baseline.diff.txt", cand_vs_base_run.stdout + cand_vs_base_run.stderr)
        candidate_differs_from_baseline = has_functional_diff(cand_vs_base_run.stdout + cand_vs_base_run.stderr)

        cls = classify(expected, alive_ok, baseline_changed, candidate_differs_from_baseline)
        notes = ""
        if cls == "confirmed_missed":
            notes = "Candidate is Alive2-valid and differs from baseline; baseline did not apply equivalent simplification."
        elif cls == "invalid_candidate":
            notes = "Candidate rewrite is unsound per Alive2."
        elif cls == "baseline_optimizes":
            notes = "Baseline InstCombine/SimplifyCFG already performs an equivalent transform."
        elif cls == "different_but_not_missed":
            notes = "Candidate differs, but baseline also changed IR; investigate semantic relation."
        elif cls == "not_missed":
            notes = "Candidate does not provide a distinct simplification over baseline output."
        else:
            notes = "Review generated diffs and Alive2 output manually."

        result = CaseResult(
            name=name,
            title=title,
            expected=expected,
            alive_status="valid" if alive_ok else "invalid",
            alive_correct=correct,
            alive_incorrect=incorrect,
            alive_errors=errors,
            baseline_changed=baseline_changed,
            candidate_differs_from_baseline=candidate_differs_from_baseline,
            classification=cls,
            notes=notes,
        )
        all_results.append(result)

    summary = {
        "total_cases": len(all_results),
        "confirmed_missed": sum(1 for r in all_results if r.classification == "confirmed_missed"),
        "invalid_candidates": sum(1 for r in all_results if r.classification == "invalid_candidate"),
        "baseline_optimizes": sum(1 for r in all_results if r.classification == "baseline_optimizes"),
        "results": [r.__dict__ for r in all_results],
    }
    write_text(results_dir / "summary.json", json.dumps(summary, indent=2))

    lines = []
    lines.append("# Experiment Summary")
    lines.append("")
    lines.append(f"- Total cases: **{summary['total_cases']}**")
    lines.append(f"- Confirmed missed opportunities: **{summary['confirmed_missed']}**")
    lines.append(f"- Invalid candidate rewrites: **{summary['invalid_candidates']}**")
    lines.append(f"- Already optimized by baseline: **{summary['baseline_optimizes']}**")
    lines.append("")
    lines.append("| Case | Expected | Alive2 | Baseline changed? | Candidate vs baseline | Classification |")
    lines.append("|---|---|---|---|---|---|")
    for r in all_results:
        lines.append(
            f"| `{r.name}` | `{r.expected}` | `{r.alive_status}` | "
            f"`{r.baseline_changed}` | `{r.candidate_differs_from_baseline}` | `{r.classification}` |"
        )
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    for r in all_results:
        lines.append(f"- **{r.name}**: {r.notes}")
    lines.append("")
    lines.append("Each case has detailed outputs under `results/<case>/`.")
    write_text(results_dir / "summary.md", "\n".join(lines))

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
