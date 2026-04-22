# Assignment 14  
# Can LLMs Discover Missed Peephole Optimizations in LLVM IR?

This project is a complete, runnable experiment harness for your assignment.

It is designed for a beginner:

- no prior LLVM knowledge required,
- one-command execution,
- clear outputs and interpretable results,
- reproducible pipeline using LLVM + Alive2, plus MLIR bounded/rule-based checking.

---

## 1) What this project does

For each LLVM IR test case, the pipeline checks:

1. **LLM candidate validity** using `alive-tv`  
   (is the proposed rewrite actually correct?)

2. **LLVM baseline behavior** using:
   - `opt -passes=instcombine,simplifycfg`

3. **Candidate vs baseline comparison** using:
   - `llvm-diff`

4. **Profitability proxy** using value-producing instruction counts
   (source vs candidate vs baseline)

5. **Generalization analysis** by grouping related variants into families

For each MLIR test case, a companion runner checks:

1. **Bounded equivalence validation** using an internal interpreter over sampled inputs
2. **Rule-based baseline simulation** for common canonicalizations
3. **Candidate vs baseline comparison** and the same classification buckets

Then it classifies each case as:

- `baseline_optimizes` (LLVM already does it)
- `confirmed_missed` (candidate valid and baseline missed it)
- `invalid_candidate` (LLM rewrite is unsound)
- `hallucinated_candidate` (intentionally bogus rewrite rejected by the validator)
- other review classes

---

## 2) Folder structure

```text
assignment14-llm-peephole-llvmir/
├── README.md
├── cases/
│   ├── *.ll                     # source IR
│   ├── *.candidate.ll           # candidate rewrite IR
│   └── README.md
├── mlir_cases/
│   ├── *.mlir                   # source MLIR patterns
│   ├── *.candidate.mlir         # candidate MLIR rewrites
│   └── README.md
├── scripts/
│   ├── check_env.sh             # tool/version sanity check
│   ├── run_experiments.py       # core runner
│   ├── run_mlir_experiments.py  # MLIR bounded/rule-based runner
│   └── run_all.sh               # one-command entrypoint
├── results/
│   ├── summary.md
│   ├── summary.json
│   └── <case-name>/
│       ├── alive-tv.txt
│       ├── baseline.ll
│       ├── baseline.diff.txt
│       ├── baseline.stderr.txt
│       └── candidate_vs_baseline.diff.txt
└── results_mlir/
    ├── summary.md
    ├── summary.json
    └── <case-name>/
        ├── validator.txt
        ├── baseline.mlir
        ├── baseline.diff.txt
        └── candidate_vs_baseline.diff.txt
```

> `results/` is for LLVM IR experiments; `results_mlir/` is for MLIR experiments.

---

## 3) Prerequisites

This repository is already configured to use:

- Debug LLVM build: `/home/boss/llvm/llvm-build-debug/bin`
- Alive2: `/usr/local/bin/alive-tv`
- Python 3

If your paths differ, pass overrides using environment variables:

- `LLVM_BIN=/path/to/llvm/bin`
- `ALIVE_TV=/path/to/alive-tv`

---

## 4) Quick start

From this directory:

```bash
cd /home/boss/llvm/assignment14-llm-peephole-llvmir
./scripts/run_all.sh
```

After it finishes:

- LLVM human-readable: `results/summary.md`
- LLVM machine-readable: `results/summary.json`
- MLIR human-readable: `results_mlir/summary.md`
- MLIR machine-readable: `results_mlir/summary.json`

---

## 5) Current experiment results

Run the pipeline to regenerate current numbers:

```bash
./scripts/run_all.sh
```

Then inspect:

- `results/summary.json` for machine-readable metrics
- `results/summary.md` for tables and notes (including family and profitability sections)
- `results_mlir/summary.json` for MLIR machine-readable metrics
- `results_mlir/summary.md` for MLIR tables and notes

---

## 6) How to add your own test case

Add two files in `cases/`:

1. `my_case.ll`  
2. `my_case.candidate.ll`

`my_case.ll` should include metadata at top:

```llvm
; TITLE: My optimization idea
; EXPECTED: missed
; CATEGORY: llm-candidate
; FAMILY: my_pattern_family
; VARIANT: v1
define i32 @f(i32 %x) {
entry:
  ; source version
  ret i32 %x
}
```

`CATEGORY`, `FAMILY`, and `VARIANT` are optional but recommended for
hallucination/ambiguity tracking and generalization analysis.

Candidate file should contain same function signature:

```llvm
define i32 @f(i32 %x) {
entry:
  ; candidate rewrite
  ret i32 %x
}
```

Then rerun:

```bash
./scripts/run_all.sh
```

To add an MLIR case, create:

1. `mlir_cases/my_case.mlir`
2. `mlir_cases/my_case.candidate.mlir`

With MLIR metadata at top:

```mlir
// TITLE: My MLIR optimization idea
// EXPECTED: missed
// CATEGORY: llm-candidate
// FAMILY: my_mlir_family
// VARIANT: v1
module {
  func.func @f(%arg0: i32) -> i32 {
    return %arg0 : i32
  }
}
```

---

## 7) Understanding the generated files

For each case, inspect:

- `alive-tv.txt`  
  Shows whether candidate is semantically correct.

- `baseline.ll`  
  LLVM output after baseline optimization passes.

- `baseline.diff.txt`  
  Difference between source and baseline.

- `candidate_vs_baseline.diff.txt`  
  Difference between candidate and baseline.

For MLIR cases, inspect:

- `results_mlir/<case>/validator.txt`  
  Bounded-check verdict and baseline-rule notes.

- `results_mlir/<case>/baseline.mlir` and `baseline.diff.txt`  
  Simulated baseline output and source-vs-baseline diff.

- `results_mlir/<case>/candidate_vs_baseline.diff.txt`  
  Candidate-vs-baseline diff.

And at the aggregate level:

- `results/summary.md`  
  Includes per-case classification, candidate profitability buckets,
  family-level generalization conclusions, and quality bucket counts.

If candidate is valid **and** baseline did not apply equivalent simplification, that is your strongest “missed optimization” evidence.

---

## 8) Suggested report structure (for your submission)

Use this format:

1. **Goal**  
   Evaluate whether LLM-proposed LLVM IR peepholes reveal optimizer gaps.

2. **Method**  
   Candidate generation → Alive2 validation → Baseline pass comparison.

3. **Toolchain**  
   Debug LLVM, Alive2, scripts in this project.

4. **Case design**  
   Explain case categories: already-optimized, potential-missed, invalid sanity.

5. **Results table**  
   Use `results/summary.md`.

6. **Discussion**  
   Why many candidates were already optimized; value of formal validation.

7. **Future work**  
   Expand case generation, target other passes (`reassociate`, `gvn`, etc.), integrate automated LLM prompt loop.

---

## 9) Common issues

- **`alive-tv` not found**  
  Set `ALIVE_TV=/full/path/to/alive-tv`.

- **LLVM tools not found**  
  Set `LLVM_BIN=/full/path/to/llvm/bin`.

- **Alive2 says candidate invalid**  
  Keep it! Invalid cases are useful to show why formal checking matters.

---

## 10) Key takeaway

You now have a full assignment-grade experimental framework:

- reproducible,
- explainable,
- beginner-friendly,
- and ready for extension until you find strong missed-optimization examples.
