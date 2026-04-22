#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
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
    category: str
    family: str
    variant: str
    alive_status: str
    alive_correct: int
    alive_incorrect: int
    alive_errors: int
    source_inst_count: int
    candidate_inst_count: int
    baseline_inst_count: int
    candidate_profitability: str
    baseline_profitability: str
    baseline_changed: bool
    candidate_differs_from_baseline: bool
    classification: str
    quality_bucket: str
    notes: str


def parse_case_metadata(case_file: Path) -> tuple[str, str, str, str, str]:
    title = case_file.stem
    expected = "unknown"
    category = "llm-candidate"
    family = ""
    variant = ""

    text = read_text(case_file)
    for line in text.splitlines():
        if line.startswith("; TITLE:"):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("; EXPECTED:"):
            expected = line.split(":", 1)[1].strip().lower()
        elif line.startswith("; CATEGORY:"):
            category = line.split(":", 1)[1].strip().lower()
        elif line.startswith("; FAMILY:"):
            family = line.split(":", 1)[1].strip().lower()
        elif line.startswith("; VARIANT:"):
            variant = line.split(":", 1)[1].strip().lower()

    return title, expected, category, family, variant


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


def count_value_instructions(ir_text: str) -> int:
    in_function = False
    count = 0
    for raw_line in ir_text.splitlines():
        line = raw_line.split(";", 1)[0].strip()
        if not line:
            continue
        if line.startswith("define "):
            in_function = True
            continue
        if in_function and line.startswith("}"):
            in_function = False
            continue
        if not in_function:
            continue
        if line.endswith(":"):
            continue
        if " = " in line:
            count += 1
    return count


def profitability_label(source_inst_count: int, rewritten_inst_count: int) -> str:
    if rewritten_inst_count < source_inst_count:
        return "better"
    if rewritten_inst_count == source_inst_count:
        return "neutral"
    return "worse"


def classify(
    expected: str,
    category: str,
    alive_ok: bool,
    baseline_changed: bool,
    cand_diff_baseline: bool,
) -> str:
    if not alive_ok:
        if category == "hallucination":
            return "hallucinated_candidate"
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


def quality_bucket(category: str, alive_ok: bool, candidate_profitability: str) -> str:
    if category == "hallucination":
        return "hallucinated" if not alive_ok else "hallucination_valid"
    if category == "ambiguous":
        return "ambiguous_invalid" if not alive_ok else "ambiguous_valid"
    if not alive_ok:
        return "invalid"
    if candidate_profitability == "better":
        return "valid_profitable"
    if candidate_profitability == "worse":
        return "valid_unprofitable"
    return "valid_neutral"


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
        title, expected, category, family, variant = parse_case_metadata(case)
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

        source_inst_count = count_value_instructions(read_text(src_file))
        candidate_inst_count = count_value_instructions(read_text(candidate_file))
        baseline_inst_count = count_value_instructions(read_text(baseline_file))
        candidate_profitability = profitability_label(source_inst_count, candidate_inst_count)
        baseline_profitability = profitability_label(source_inst_count, baseline_inst_count)

        cls = classify(expected, category, alive_ok, baseline_changed, candidate_differs_from_baseline)
        q_bucket = quality_bucket(category, alive_ok, candidate_profitability)
        notes = ""
        if cls == "confirmed_missed":
            notes = "Candidate is Alive2-valid and differs from baseline; baseline did not apply equivalent simplification."
        elif cls == "hallucinated_candidate":
            notes = "Intentional hallucination candidate was rejected by Alive2."
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
        notes += (
            f" Candidate value-inst count is {candidate_inst_count} vs source {source_inst_count} "
            f"({candidate_profitability})."
        )

        result = CaseResult(
            name=name,
            title=title,
            expected=expected,
            category=category,
            family=family,
            variant=variant,
            alive_status="valid" if alive_ok else "invalid",
            alive_correct=correct,
            alive_incorrect=incorrect,
            alive_errors=errors,
            source_inst_count=source_inst_count,
            candidate_inst_count=candidate_inst_count,
            baseline_inst_count=baseline_inst_count,
            candidate_profitability=candidate_profitability,
            baseline_profitability=baseline_profitability,
            baseline_changed=baseline_changed,
            candidate_differs_from_baseline=candidate_differs_from_baseline,
            classification=cls,
            quality_bucket=q_bucket,
            notes=notes,
        )
        all_results.append(result)

    families: dict[str, list[CaseResult]] = defaultdict(list)
    for r in all_results:
        if r.family:
            families[r.family].append(r)

    family_generalization: list[dict[str, object]] = []
    for family_name in sorted(families):
        items = families[family_name]
        if len(items) < 2:
            continue
        confirmed_missed = sum(1 for r in items if r.classification == "confirmed_missed")
        alive_valid = sum(1 for r in items if r.alive_status == "valid")
        invalid = sum(1 for r in items if r.classification in {"invalid_candidate", "hallucinated_candidate"})
        hallucinated = sum(1 for r in items if r.classification == "hallucinated_candidate")
        better = sum(1 for r in items if r.alive_status == "valid" and r.candidate_profitability == "better")
        worse = sum(1 for r in items if r.alive_status == "valid" and r.candidate_profitability == "worse")

        if confirmed_missed >= 2:
            conclusion = "generalizes"
        elif confirmed_missed == 1 and alive_valid >= 2:
            conclusion = "possibly_overfitted"
        elif hallucinated == len(items):
            conclusion = "hallucinated_family"
        elif alive_valid == len(items):
            conclusion = "valid_but_no_missed_evidence"
        else:
            conclusion = "mixed_results"

        family_generalization.append(
            {
                "family": family_name,
                "variants": len(items),
                "alive_valid": alive_valid,
                "invalid_or_hallucinated": invalid,
                "confirmed_missed": confirmed_missed,
                "profitable_variants": better,
                "unprofitable_variants": worse,
                "conclusion": conclusion,
            }
        )

    profitability_counts = {
        "better": sum(
            1 for r in all_results if r.alive_status == "valid" and r.candidate_profitability == "better"
        ),
        "neutral": sum(
            1 for r in all_results if r.alive_status == "valid" and r.candidate_profitability == "neutral"
        ),
        "worse": sum(
            1 for r in all_results if r.alive_status == "valid" and r.candidate_profitability == "worse"
        ),
    }
    quality_bucket_counts: dict[str, int] = defaultdict(int)
    for r in all_results:
        quality_bucket_counts[r.quality_bucket] += 1

    summary = {
        "total_cases": len(all_results),
        "confirmed_missed": sum(1 for r in all_results if r.classification == "confirmed_missed"),
        "invalid_candidates": sum(1 for r in all_results if r.classification == "invalid_candidate"),
        "hallucinated_candidates": sum(1 for r in all_results if r.classification == "hallucinated_candidate"),
        "baseline_optimizes": sum(1 for r in all_results if r.classification == "baseline_optimizes"),
        "candidate_profitability": profitability_counts,
        "quality_buckets": dict(sorted(quality_bucket_counts.items())),
        "family_generalization": family_generalization,
        "results": [r.__dict__ for r in all_results],
    }
    write_text(results_dir / "summary.json", json.dumps(summary, indent=2))

    lines = []
    lines.append("# Experiment Summary")
    lines.append("")
    lines.append(f"- Total cases: **{summary['total_cases']}**")
    lines.append(f"- Confirmed missed opportunities: **{summary['confirmed_missed']}**")
    lines.append(f"- Invalid candidate rewrites: **{summary['invalid_candidates']}**")
    lines.append(f"- Hallucinated candidate rewrites: **{summary['hallucinated_candidates']}**")
    lines.append(f"- Already optimized by baseline: **{summary['baseline_optimizes']}**")
    lines.append(
        "- Candidate profitability vs source (value-inst count, Alive-valid only): "
        f"better **{profitability_counts['better']}**, "
        f"neutral **{profitability_counts['neutral']}**, "
        f"worse **{profitability_counts['worse']}**"
    )
    lines.append("")
    lines.append(
        "| Case | Expected | Category | Family | Alive2 | Cand inst count | Cand profitability | "
        "Baseline changed? | Candidate vs baseline | Classification |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in all_results:
        family_cell = r.family if r.family else "-"
        lines.append(
            f"| `{r.name}` | `{r.expected}` | `{r.category}` | `{family_cell}` | `{r.alive_status}` | "
            f"`{r.candidate_inst_count}/{r.source_inst_count}` | `{r.candidate_profitability}` | "
            f"`{r.baseline_changed}` | `{r.candidate_differs_from_baseline}` | `{r.classification}` |"
        )
    lines.append("")
    lines.append("## Family Generalization (>=2 variants)")
    lines.append("")
    if family_generalization:
        lines.append(
            "| Family | Variants | Alive-valid | Invalid/Hallucinated | Confirmed missed | "
            "Profitable | Unprofitable | Conclusion |"
        )
        lines.append("|---|---|---|---|---|---|---|---|")
        for fam in family_generalization:
            lines.append(
                f"| `{fam['family']}` | `{fam['variants']}` | `{fam['alive_valid']}` | "
                f"`{fam['invalid_or_hallucinated']}` | `{fam['confirmed_missed']}` | "
                f"`{fam['profitable_variants']}` | `{fam['unprofitable_variants']}` | `{fam['conclusion']}` |"
            )
    else:
        lines.append("No multi-variant families found.")
    lines.append("")
    lines.append("## Candidate Quality Buckets")
    lines.append("")
    lines.append("| Bucket | Count |")
    lines.append("|---|---|")
    for bucket, count in sorted(quality_bucket_counts.items()):
        lines.append(f"| `{bucket}` | `{count}` |")
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
