# Assignment 14 — Can LLMs Discover Missed Peephole Optimizations in LLVM IR?

## Abstract

This repository implements a controlled evaluation of LLM‑generated peephole rewrites for LLVM IR and MLIR. The workflow combines (1) a curated dataset of small patterns, (2) candidate rewrites, (3) formal or bounded correctness checks, and (4) a baseline comparison against LLVM’s local optimization passes. The goal is to determine whether LLMs can surface valid, missed peephole optimizations and to quantify the rate of invalid or hallucinated rewrites.

**Required documents:** `DESIGN`, `IMPLEMENTATION`, `EVALUATION`.

## Problem statement (from the assignment)

LLVM already performs many optimizations, but no optimizer is perfect. This project tests whether an LLM can suggest *valid* missed peephole optimizations and how those suggestions can be formally validated. The expected deliverables include a dataset of patterns, LLM candidate rewrites, a validation framework, and analysis of valid vs invalid suggestions.

## What this repository delivers

1. **Curated dataset** of LLVM IR and MLIR peephole patterns with metadata.
2. **Candidate rewrites** (LLM‑style proposals) for every pattern.
3. **Validation framework**:
   - LLVM IR: Alive2 equivalence checking.
   - MLIR: bounded equivalence checking with a small interpreter.
4. **Baseline comparison**:
   - LLVM IR: `instcombine` + `simplifycfg`.
   - MLIR: rule‑based canonicalization simulation.
5. **Evaluation reports**:
   - Per‑case diffs and validation logs.
   - Aggregate metrics and classification tables.

## Build and run

```bash
./scripts/build.sh
./scripts/run.sh
```

Outputs:

- `results/summary.md` and `results/summary.json` (LLVM IR)
- `results_mlir/summary.md` and `results_mlir/summary.json` (MLIR)

## Results snapshot (current repo outputs)

| Track | Total | Confirmed missed | Baseline optimizes | Hallucinated | Invalid | Profitability (valid only) |
|---|---:|---:|---:|---:|---:|---|
| LLVM IR | 48 | 4 | 31 | 4 | 0 | 30 better / 12 neutral / 2 worse |
| MLIR | 8 | 2 | 4 | 2 | 0 | 4 better / 2 neutral / 0 worse |

Per‑case analyses and diffs are in `results/summary.md` and `results_mlir/summary.md`.

## Method overview

1. **Dataset**: source/candidate pairs in `testcases/llvm_ir` and `testcases/mlir`.
2. **Correctness**:
   - LLVM IR: Alive2 (`alive-tv`).
   - MLIR: bounded equivalence over sampled inputs.
3. **Baseline comparison**:
   - LLVM IR: `opt -passes=instcombine,simplifycfg` + `llvm-diff`.
   - MLIR: rule‑based canonicalization simulation.
4. **Classification**: confirmed missed, baseline optimizes, invalid/hallucinated, and profitability proxy.

## Classification definitions

- **confirmed_missed**: candidate is valid and differs from the baseline output.
- **baseline_optimizes**: baseline already performs the simplification.
- **invalid_candidate**: candidate fails formal/bounded validation.
- **hallucinated_candidate**: intentionally incorrect candidate rejected by validation.
- **different_but_not_missed**: baseline changes IR but candidate still differs; requires manual review.

## Profitability proxy

The pipeline computes a simple profitability proxy: value‑producing instruction count in the candidate vs the source. This yields three labels:

- **better**: fewer value‑producing instructions.
- **neutral**: same count.
- **worse**: higher count.

This is a proxy metric, not a full LLVM cost model.

## Repository structure

```text
assignment14-llm-peephole-llvmir/
├── README.md
├── DESIGN
├── IMPLEMENTATION
├── EVALUATION
├── src/
│   ├── run_experiments.py
│   └── run_mlir_experiments.py
├── scripts/
│   ├── build.sh
│   ├── run.sh
│   ├── run_all.sh
│   └── check_env.sh
├── testcases/
│   ├── llvm_ir/
│   └── mlir/
├── results/
└── results_mlir/
```

## Testcase format

### LLVM IR

Each testcase has:

- `<name>.ll` (source)
- `<name>.candidate.ll` (candidate rewrite)

Metadata is embedded at the top of the source file:

```llvm
; TITLE: My optimization idea
; EXPECTED: missed
; CATEGORY: llm-candidate
; FAMILY: my_pattern_family
; VARIANT: v1
```

### MLIR

Each testcase has:

- `<name>.mlir` (source)
- `<name>.candidate.mlir` (candidate rewrite)

Metadata is embedded at the top of the source file:

```mlir
// TITLE: My MLIR optimization idea
// EXPECTED: missed
// CATEGORY: llm-candidate
// FAMILY: my_mlir_family
// VARIANT: v1
```

## Reproducibility and environment

Prerequisites:

- LLVM tools: `opt`, `llvm-diff`, `llvm-as`, `llvm-dis`, `llc`
- Alive2: `alive-tv`
- Python 3

Default paths (override via environment variables):

- `LLVM_BIN=/home/boss/llvm/llvm-build-debug/bin`
- `ALIVE_TV=/usr/local/bin/alive-tv`

The environment check in `scripts/check_env.sh` validates tool availability and versions.

## Limitations

- The MLIR validator is bounded and only supports a small subset of `arith.*` operations.
- Profitability uses instruction count and does not account for micro‑architectural costs.
- The baseline pass set is intentionally minimal to isolate peephole behavior.
