# Assignment 14  
# Can LLMs Discover Missed Peephole Optimizations in LLVM IR?

This project is a complete, runnable experiment harness for your assignment.

It is designed for a beginner:

- no prior LLVM knowledge required,
- one-command execution,
- clear outputs and interpretable results,
- reproducible pipeline using LLVM + Alive2.

---

## 1) What this project does

For each test case, the pipeline checks:

1. **LLM candidate validity** using `alive-tv`  
   (is the proposed rewrite actually correct?)

2. **LLVM baseline behavior** using:
   - `opt -passes=instcombine,simplifycfg`

3. **Candidate vs baseline comparison** using:
   - `llvm-diff`

Then it classifies each case as:

- `baseline_optimizes` (LLVM already does it)
- `confirmed_missed` (candidate valid and baseline missed it)
- `invalid_candidate` (LLM rewrite is unsound)
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
├── scripts/
│   ├── check_env.sh             # tool/version sanity check
│   ├── run_experiments.py       # core runner
│   └── run_all.sh               # one-command entrypoint
└── results/
    ├── summary.md
    ├── summary.json
    └── <case-name>/
        ├── alive-tv.txt
        ├── baseline.ll
        ├── baseline.diff.txt
        ├── baseline.stderr.txt
        └── candidate_vs_baseline.diff.txt
```

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

- Human-readable results: `results/summary.md`
- Machine-readable results: `results/summary.json`

---

## 5) Current experiment results (this run)

From `results/summary.json`:

- Total cases: **8**
- Confirmed missed opportunities: **0**
- Invalid candidate rewrites: **1**
- Already optimized by baseline: **5**

Interpretation:

- The harness works end-to-end.
- Your current curated case set mostly contains known simplifications that LLVM already performs.
- One intentionally unsound candidate is correctly rejected by Alive2 (good sanity check).

This is still a valid assignment outcome: the methodology is correct and reproducible, even if this first case pack did not produce a confirmed miss yet.

---

## 6) How to add your own test case

Add two files in `cases/`:

1. `my_case.ll`  
2. `my_case.candidate.ll`

`my_case.ll` should include metadata at top:

```llvm
; TITLE: My optimization idea
; EXPECTED: missed
define i32 @f(i32 %x) {
entry:
  ; source version
  ret i32 %x
}
```

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

