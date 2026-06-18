# Assignment 14 — Can LLMs Discover Missed Peephole Optimizations in LLVM IR?

## Abstract

This repository implements a controlled evaluation of LLM-generated peephole rewrites for LLVM IR and MLIR. The workflow combines:

1. A curated dataset of LLVM IR / MLIR patterns.
2. Automatic candidate rewrite generation using a Large Language Model (LLM).
3. Formal or bounded correctness validation.
4. Comparison against LLVM's existing optimization passes.

The goal is to determine whether an LLM can discover valid missed peephole optimizations and to quantify how often generated rewrites are invalid, hallucinated, or already known to the compiler.

**Required documents:** `DESIGN`, `IMPLEMENTATION`, `EVALUATION`.

---

## Problem Statement

LLVM already performs many optimizations, but no optimizer is perfect. This project investigates whether an LLM can suggest valid missed peephole optimizations and how those suggestions can be formally validated.

The expected deliverables include:

- A dataset of optimization patterns.
- LLM-generated candidate rewrites.
- A validation framework.
- Analysis of valid vs invalid suggestions.
- A study of whether LLMs discover useful missed optimizations or mostly hallucinate.

---

## What This Repository Delivers

1. **Curated dataset** of LLVM IR and MLIR peephole patterns.
2. **LLM-generated candidate rewrites** using Gemini.
3. **Validation framework**
   - LLVM IR: Alive2 equivalence checking.
   - MLIR: bounded equivalence checking using a lightweight interpreter.
4. **Baseline comparison**
   - LLVM IR: `instcombine` + `simplifycfg`
   - MLIR: rule-based canonicalization simulation.
5. **Evaluation reports**
   - Per-case validation logs.
   - Aggregate metrics.
   - Failure analysis and classification tables.

---

## Workflow

```text
LLVM IR / MLIR Pattern
            │
            ▼
generate_candidates.py
            │
            ▼
LLM Candidate Rewrite
            │
            ▼
Validation
(Alive2 / Bounded Equivalence)
            │
            ▼
LLVM Baseline Comparison
            │
            ▼
Classification
            │
            ▼
Results & Reports
```

---

## Build and Run

### Build

```bash
./scripts/build.sh
```

### Configure LLM Access

Obtain a Gemini API key and export it:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

### Run Full Pipeline

```bash
./scripts/run.sh
```

Outputs:

- `results/summary.md`
- `results/summary.json`
- `results_mlir/summary.md`
- `results_mlir/summary.json`

---

## LLM Candidate Generation

Candidate rewrites are generated automatically using:

```text
src/generate_candidates.py
```

The script:

1. Reads source patterns from:

```text
testcases/llvm_ir/*.ll
testcases/mlir/*.mlir
```

2. Sends each pattern to Gemini 2.5 Flash.

3. Requests a semantically equivalent local peephole optimization.

4. Saves the generated rewrite as:

```text
<name>.candidate.ll
<name>.candidate.mlir
```

Example:

```text
c01.ll
   │
   ▼
Gemini
   │
   ▼
c01.candidate.ll
```

Generated candidates are **not trusted** and must pass validation before being considered valid optimizations.

---

## Method Overview

### 1. Dataset

Source optimization patterns are stored in:

```text
testcases/llvm_ir/
testcases/mlir/
```

### 2. Candidate Generation

Gemini 2.5 Flash generates candidate rewrites for each pattern.

### 3. Correctness Validation

#### LLVM IR

Uses Alive2:

```text
alive-tv
```

to formally prove semantic equivalence.

#### MLIR

Uses bounded equivalence checking over sampled inputs.

### 4. Baseline Comparison

#### LLVM IR

Runs:

```bash
opt -passes=instcombine,simplifycfg
```

and compares the result using:

```text
llvm-diff
```

#### MLIR

Uses a rule-based canonicalization simulation.

### 5. Classification

Each candidate is classified as:

- `confirmed_missed`
- `baseline_optimizes`
- `invalid_candidate`
- `hallucinated_candidate`
- `different_but_not_missed`

---

## Classification Definitions

### confirmed_missed

Candidate is valid and LLVM baseline does not perform the rewrite.

### baseline_optimizes

LLVM already performs the optimization.

### invalid_candidate

Candidate fails formal or bounded validation.

### hallucinated_candidate

Candidate is semantically incorrect and rejected by validation.

### different_but_not_missed

Candidate differs from baseline but requires manual review.

---

## Profitability Proxy

The pipeline estimates profitability using value-producing instruction counts.

Labels:

- **better** → fewer instructions
- **neutral** → same number of instructions
- **worse** → more instructions

This is only a proxy and not a replacement for LLVM's full cost model.

---

## Repository Structure

```text
assignment14-llm-peephole-llvmir/
├── README.md
├── DESIGN
├── IMPLEMENTATION
├── EVALUATION
├── src/
│   ├── generate_candidates.py
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

---

## Testcase Format

### LLVM IR

Each testcase contains:

```text
<name>.ll
<name>.candidate.ll
```

Metadata:

```llvm
; TITLE: My optimization idea
; EXPECTED: missed
; CATEGORY: llm-candidate
; FAMILY: my_pattern_family
; VARIANT: v1
```

### MLIR

Each testcase contains:

```text
<name>.mlir
<name>.candidate.mlir
```

Metadata:

```mlir
// TITLE: My MLIR optimization idea
// EXPECTED: missed
// CATEGORY: llm-candidate
// FAMILY: my_mlir_family
// VARIANT: v1
```

---

## Reproducibility and Environment

Prerequisites:

- LLVM tools:
  - `opt`
  - `llvm-diff`
  - `llvm-as`
  - `llvm-dis`
  - `llc`
- Alive2:
  - `alive-tv`
- Python 3.10+
- Google GenAI SDK

Install Python dependency:

```bash
pip install google-genai
```

Default paths:

```bash
LLVM_BIN=/home/boss/llvm/llvm-build-debug/bin
ALIVE_TV=/usr/local/bin/alive-tv
```

Environment variables:

```bash
export GEMINI_API_KEY=<your_api_key>
```

The environment check in `scripts/check_env.sh` validates tool availability.

---

## Results Snapshot

| Track | Total | Confirmed Missed | Baseline Optimizes | Hallucinated | Invalid |
|--------|--------|--------|--------|--------|--------|
| LLVM IR | 48 | 4 | 31 | 4 | 0 |
| MLIR | 8 | 2 | 4 | 2 | 0 |

Detailed reports:

- `results/summary.md`
- `results_mlir/summary.md`

---

## Limitations

- The MLIR validator is bounded and supports only a subset of `arith.*` operations.
- Profitability is estimated using instruction count only.
- The baseline pass set is intentionally minimal.
- LLM-generated rewrites may be invalid or hallucinated.
- Gemini acts only as a candidate generator, not as a correctness oracle.
- Results may vary depending on model version, prompts, and generation settings.