#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import difflib
import itertools
import json
import re
import shutil
from pathlib import Path


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


@dataclass
class MlirFunction:
    name: str
    arg_names: list[str]
    arg_bits: list[int]
    ret_bits: int
    ops: list[tuple]
    return_var: str


def parse_case_metadata(case_file: Path) -> tuple[str, str, str, str, str]:
    title = case_file.stem
    expected = "unknown"
    category = "llm-candidate"
    family = ""
    variant = ""

    text = read_text(case_file)
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith(";"):
            line = line[1:].strip()
        elif line.startswith("//"):
            line = line[2:].strip()
        else:
            continue
        if line.startswith("TITLE:"):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("EXPECTED:"):
            expected = line.split(":", 1)[1].strip().lower()
        elif line.startswith("CATEGORY:"):
            category = line.split(":", 1)[1].strip().lower()
        elif line.startswith("FAMILY:"):
            family = line.split(":", 1)[1].strip().lower()
        elif line.startswith("VARIANT:"):
            variant = line.split(":", 1)[1].strip().lower()

    return title, expected, category, family, variant


def normalize_mlir(text: str) -> str:
    cleaned_lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("//") or line.startswith(";"):
            continue
        cleaned_lines.append(re.sub(r"\s+", " ", line))
    return "\n".join(cleaned_lines)


def unified_diff(a: str, b: str, from_name: str, to_name: str) -> str:
    return "".join(
        difflib.unified_diff(
            a.splitlines(keepends=True),
            b.splitlines(keepends=True),
            fromfile=from_name,
            tofile=to_name,
        )
    )


def parse_mlir_function(text: str) -> MlirFunction:
    lines = [ln.rstrip() for ln in text.splitlines()]

    func_header_idx = -1
    for i, line in enumerate(lines):
        if "func.func @" in line:
            func_header_idx = i
            break
    if func_header_idx < 0:
        raise ValueError("Missing func.func declaration")

    header = lines[func_header_idx].strip()
    m = re.search(r"func\.func\s+@([A-Za-z_][A-Za-z0-9_]*)\((.*)\)\s*->\s*i(\d+)\s*\{", header)
    if not m:
        raise ValueError("Unsupported function signature format")
    fn_name = m.group(1)
    args_raw = m.group(2).strip()
    ret_bits = int(m.group(3))

    arg_names: list[str] = []
    arg_bits: list[int] = []
    if args_raw:
        for piece in args_raw.split(","):
            arg_m = re.match(r"\s*(%[A-Za-z0-9_]+)\s*:\s*i(\d+)\s*", piece)
            if not arg_m:
                raise ValueError(f"Unsupported argument format: {piece}")
            arg_names.append(arg_m.group(1))
            arg_bits.append(int(arg_m.group(2)))

    in_func = False
    brace_depth = 0
    body_lines: list[str] = []
    for line in lines[func_header_idx:]:
        stripped = line.strip()
        if not in_func:
            if "func.func @" in stripped and stripped.endswith("{"):
                in_func = True
                brace_depth = 1
            continue
        else:
            brace_depth += stripped.count("{")
            brace_depth -= stripped.count("}")
            if brace_depth <= 0:
                break
            if not stripped or stripped.startswith("//") or stripped.startswith(";"):
                continue
            body_lines.append(stripped)

    ops: list[tuple] = []
    return_var = ""
    for line in body_lines:
        const_m = re.match(r"(%[A-Za-z0-9_]+)\s*=\s*arith\.constant\s+(-?\d+)\s*:\s*i(\d+)", line)
        if const_m:
            ops.append(("const", const_m.group(1), int(const_m.group(2)), int(const_m.group(3))))
            continue
        bin_m = re.match(
            r"(%[A-Za-z0-9_]+)\s*=\s*arith\.(addi|muli|subi|andi|ori|xori|shli|shrui)\s+"
            r"(%[A-Za-z0-9_]+)\s*,\s*(%[A-Za-z0-9_]+)\s*:\s*i(\d+)",
            line,
        )
        if bin_m:
            ops.append(
                (
                    "bin",
                    bin_m.group(1),
                    bin_m.group(2),
                    bin_m.group(3),
                    bin_m.group(4),
                    int(bin_m.group(5)),
                )
            )
            continue
        ret_m = re.match(r"return\s+(%[A-Za-z0-9_]+)\s*:\s*i(\d+)", line)
        if ret_m:
            return_var = ret_m.group(1)
            if int(ret_m.group(2)) != ret_bits:
                raise ValueError("Return type does not match function signature")
            continue
        raise ValueError(f"Unsupported MLIR line: {line}")

    if not return_var:
        raise ValueError("Missing return operation")

    return MlirFunction(
        name=fn_name,
        arg_names=arg_names,
        arg_bits=arg_bits,
        ret_bits=ret_bits,
        ops=ops,
        return_var=return_var,
    )


def to_unsigned(value: int, bits: int) -> int:
    return value & ((1 << bits) - 1)


def eval_mlir_function(fn: MlirFunction, inputs: list[int]) -> int:
    if len(inputs) != len(fn.arg_names):
        raise ValueError("Incorrect argument count for evaluation")
    env: dict[str, int] = {}
    type_map: dict[str, int] = {}

    for name, bits, value in zip(fn.arg_names, fn.arg_bits, inputs):
        env[name] = to_unsigned(value, bits)
        type_map[name] = bits

    for op in fn.ops:
        if op[0] == "const":
            _, dst, cst, bits = op
            env[dst] = to_unsigned(cst, bits)
            type_map[dst] = bits
            continue
        _, dst, opname, lhs, rhs, bits = op
        if lhs not in env or rhs not in env:
            raise ValueError(f"Unknown SSA value in op {opname}: {lhs}, {rhs}")
        mask = (1 << bits) - 1
        lval = env[lhs] & mask
        rval = env[rhs] & mask
        if opname == "addi":
            out = (lval + rval) & mask
        elif opname == "muli":
            out = (lval * rval) & mask
        elif opname == "subi":
            out = (lval - rval) & mask
        elif opname == "andi":
            out = (lval & rval) & mask
        elif opname == "ori":
            out = (lval | rval) & mask
        elif opname == "xori":
            out = (lval ^ rval) & mask
        elif opname == "shli":
            out = (lval << (rval % bits)) & mask
        elif opname == "shrui":
            out = (lval >> (rval % bits)) & mask
        else:
            raise ValueError(f"Unsupported op: {opname}")
        env[dst] = out
        type_map[dst] = bits

    if fn.return_var not in env:
        raise ValueError(f"Unknown return value: {fn.return_var}")
    return env[fn.return_var] & ((1 << fn.ret_bits) - 1)


def sample_values(bits: int) -> list[int]:
    mask = (1 << bits) - 1
    values = [0, 1, 2, 3, 5, 7, mask, max(0, mask - 1), 1 << max(0, bits - 1)]
    deduped = sorted({v & mask for v in values})
    return deduped


def bounded_equivalence(src: MlirFunction, cand: MlirFunction) -> tuple[bool, str]:
    if src.arg_bits != cand.arg_bits or src.ret_bits != cand.ret_bits:
        return False, "Function signature mismatch between source and candidate."
    vectors = [sample_values(bits) for bits in src.arg_bits]
    if not vectors:
        vectors = [[0]]
    for combo in itertools.product(*vectors):
        src_out = eval_mlir_function(src, list(combo))
        cand_out = eval_mlir_function(cand, list(combo))
        if src_out != cand_out:
            pretty_inputs = ", ".join(str(x) for x in combo)
            return (
                False,
                f"Bounded check failed on inputs ({pretty_inputs}): source={src_out}, candidate={cand_out}",
            )
    return True, "Bounded check passed for sampled inputs."


def render_canonical_module(fn: MlirFunction, return_var: str) -> str:
    args = ", ".join(f"{name}: i{bits}" for name, bits in zip(fn.arg_names, fn.arg_bits))
    lines = [
        "module {",
        f"  func.func @{fn.name}({args}) -> i{fn.ret_bits} {{",
        f"    return {return_var} : i{fn.ret_bits}",
        "  }",
        "}",
        "",
    ]
    return "\n".join(lines)


def try_rule_based_baseline(source_text: str) -> tuple[bool, str, str]:
    try:
        fn = parse_mlir_function(source_text)
    except ValueError as exc:
        return False, source_text, f"Could not parse source for baseline simulation: {exc}"

    if len(fn.ops) != 2:
        return False, source_text, "No simulated baseline rule matched."
    if fn.ops[0][0] != "const" or fn.ops[1][0] != "bin":
        return False, source_text, "No simulated baseline rule matched."
    _, c_dst, cst, c_bits = fn.ops[0]
    _, b_dst, op_name, lhs, rhs, b_bits = fn.ops[1]
    if c_bits != b_bits:
        return False, source_text, "No simulated baseline rule matched."
    if fn.return_var != b_dst:
        return False, source_text, "No simulated baseline rule matched."

    arg_side = None
    const_side = None
    if lhs in fn.arg_names and rhs == c_dst:
        arg_side = lhs
        const_side = cst
    elif rhs in fn.arg_names and lhs == c_dst:
        arg_side = rhs
        const_side = cst
    else:
        return False, source_text, "No simulated baseline rule matched."

    mask = (1 << b_bits) - 1
    const_unsigned = const_side & mask

    if op_name == "addi" and const_unsigned == 0:
        return True, render_canonical_module(fn, arg_side), "Simulated baseline matched addi-by-zero."
    if op_name == "muli" and const_unsigned == 1:
        return True, render_canonical_module(fn, arg_side), "Simulated baseline matched muli-by-one."
    if op_name == "ori" and const_unsigned == 0:
        return True, render_canonical_module(fn, arg_side), "Simulated baseline matched or-with-zero."
    if op_name == "andi" and const_unsigned == mask:
        return True, render_canonical_module(fn, arg_side), "Simulated baseline matched and-with-all-ones."
    return False, source_text, "No simulated baseline rule matched."


def count_mlir_value_instructions(text: str) -> int:
    in_func = False
    depth = 0
    count = 0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("//") or line.startswith(";"):
            continue
        if not in_func and line.startswith("func.func "):
            in_func = True
            depth = 1
            continue
        if not in_func:
            continue
        depth += line.count("{")
        depth -= line.count("}")
        if line.startswith("return "):
            if depth <= 0:
                in_func = False
            continue
        if " = " in line:
            count += 1
        if depth <= 0:
            in_func = False
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
    parser = argparse.ArgumentParser(description="Run MLIR peephole assignment experiments.")
    parser.add_argument("--cases-dir", required=True)
    parser.add_argument("--results-dir", required=True)
    args = parser.parse_args()

    cases_dir = Path(args.cases_dir)
    results_dir = Path(args.results_dir)

    if not cases_dir.exists():
        raise SystemExit(f"Missing MLIR cases directory: {cases_dir}")
    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    cases = sorted(p for p in cases_dir.glob("*.mlir") if not p.name.endswith(".candidate.mlir"))
    if not cases:
        raise SystemExit(f"No .mlir cases found in {cases_dir}")

    all_results: list[CaseResult] = []

    for case in cases:
        name = case.stem
        title, expected, category, family, variant = parse_case_metadata(case)
        src_file = case
        candidate_file = cases_dir / f"{name}.candidate.mlir"
        if not candidate_file.exists():
            raise SystemExit(f"Missing candidate file for {name}: {candidate_file}")

        src_text = read_text(src_file)
        cand_text = read_text(candidate_file)
        out_dir = results_dir / name
        out_dir.mkdir(parents=True, exist_ok=True)

        baseline_changed, baseline_text, baseline_reason = try_rule_based_baseline(src_text)
        write_text(out_dir / "baseline.mlir", baseline_text)
        write_text(out_dir / "validator.txt", baseline_reason + "\n")

        baseline_diff = unified_diff(src_text, baseline_text, "source.mlir", "baseline.mlir")
        write_text(out_dir / "baseline.diff.txt", baseline_diff)

        cand_vs_base = unified_diff(cand_text, baseline_text, "candidate.mlir", "baseline.mlir")
        write_text(out_dir / "candidate_vs_baseline.diff.txt", cand_vs_base)
        candidate_differs_from_baseline = normalize_mlir(cand_text) != normalize_mlir(baseline_text)

        parse_error = ""
        alive_ok = False
        try:
            src_fn = parse_mlir_function(src_text)
            cand_fn = parse_mlir_function(cand_text)
            alive_ok, eq_note = bounded_equivalence(src_fn, cand_fn)
            write_text(out_dir / "validator.txt", baseline_reason + "\n" + eq_note + "\n")
        except ValueError as exc:
            parse_error = str(exc)
            write_text(
                out_dir / "validator.txt",
                baseline_reason + "\n" + f"Bounded check failed to parse MLIR: {parse_error}\n",
            )

        correct = 1 if alive_ok else 0
        incorrect = 0 if alive_ok else 1
        errors = 0

        source_inst_count = count_mlir_value_instructions(src_text)
        candidate_inst_count = count_mlir_value_instructions(cand_text)
        baseline_inst_count = count_mlir_value_instructions(baseline_text)
        candidate_profitability = profitability_label(source_inst_count, candidate_inst_count)
        baseline_profitability = profitability_label(source_inst_count, baseline_inst_count)

        cls = classify(expected, category, alive_ok, baseline_changed, candidate_differs_from_baseline)
        q_bucket = quality_bucket(category, alive_ok, candidate_profitability)
        if cls == "confirmed_missed":
            notes = "Candidate passed bounded equivalence and differs from simulated baseline."
        elif cls == "hallucinated_candidate":
            notes = "Intentional hallucination candidate failed bounded equivalence."
        elif cls == "invalid_candidate":
            notes = "Candidate failed bounded equivalence."
        elif cls == "baseline_optimizes":
            notes = "Simulated MLIR baseline already performs an equivalent transform."
        elif cls == "different_but_not_missed":
            notes = "Candidate differs while baseline changed; review canonical forms."
        elif cls == "not_missed":
            notes = "Candidate does not provide a distinct simplification over baseline output."
        else:
            notes = "Review generated diffs and validator output manually."
        if parse_error:
            notes += f" Parser error: {parse_error}."
        notes += (
            f" Candidate value-inst count is {candidate_inst_count} vs source {source_inst_count} "
            f"({candidate_profitability})."
        )

        all_results.append(
            CaseResult(
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
        )

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
    lines.append("# MLIR Experiment Summary")
    lines.append("")
    lines.append("- Validation mode: **bounded equivalence + rule-based baseline simulation**")
    lines.append(f"- Total cases: **{summary['total_cases']}**")
    lines.append(f"- Confirmed missed opportunities: **{summary['confirmed_missed']}**")
    lines.append(f"- Invalid candidate rewrites: **{summary['invalid_candidates']}**")
    lines.append(f"- Hallucinated candidate rewrites: **{summary['hallucinated_candidates']}**")
    lines.append(f"- Already optimized by baseline: **{summary['baseline_optimizes']}**")
    lines.append(
        "- Candidate profitability vs source (value-inst count, validator-valid only): "
        f"better **{profitability_counts['better']}**, "
        f"neutral **{profitability_counts['neutral']}**, "
        f"worse **{profitability_counts['worse']}**"
    )
    lines.append("")
    lines.append(
        "| Case | Expected | Category | Family | Validator | Cand inst count | Cand profitability | "
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
            "| Family | Variants | Valid | Invalid/Hallucinated | Confirmed missed | "
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
    lines.append("Each MLIR case has detailed outputs under `results_mlir/<case>/`.")
    write_text(results_dir / "summary.md", "\n".join(lines))

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
