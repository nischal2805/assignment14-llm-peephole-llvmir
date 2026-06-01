# Assignment 14 — Can LLMs Discover Missed Peephole Optimizations in LLVM IR?

This repository implements a controlled study of LLM-generated peephole rewrites for LLVM IR and MLIR. It provides a curated dataset, correctness validation, baseline comparison against LLVM’s local passes, and quantitative summaries.

**Required documents:** `DESIGN`, `IMPLEMENTATION`, `EVALUATION`.

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

Per-case analyses and diffs are in `results/summary.md` and `results_mlir/summary.md`. These include the classification for every testcase.

## Results site (GitHub Pages)

The repository includes a static HTML report at `docs/index.html`. Enable GitHub Pages to publish it (Settings → Pages → Source: `main` / `/docs`).

## Method summary

1. **Dataset**: source/candidate pairs in `testcases/llvm_ir` and `testcases/mlir`.
2. **Correctness**:
   - LLVM IR: Alive2 (`alive-tv`)
   - MLIR: bounded equivalence over sampled inputs
3. **Baseline comparison**:
   - LLVM IR: `opt -passes=instcombine,simplifycfg` + `llvm-diff`
   - MLIR: rule-based canonicalization simulation
4. **Classification**: confirmed missed, baseline optimizes, invalid/hallucinated, and profitability proxy.

## Prerequisites

- LLVM tools: `opt`, `llvm-diff`, `llvm-as`, `llvm-dis`, `llc`
- Alive2: `alive-tv`
- Python 3

Default paths (override via environment variables):

- `LLVM_BIN=/home/boss/llvm/llvm-build-debug/bin`
- `ALIVE_TV=/usr/local/bin/alive-tv`

## Repository layout

```text
assignment14-llm-peephole-llvmir/
├── README.md
├── DESIGN
├── IMPLEMENTATION
├── EVALUATION
├── docs/
│   └── index.html
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
