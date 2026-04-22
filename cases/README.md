# Case Pack Overview

This directory contains assignment test cases.

Each case has two files:

- `<name>.ll`: source (unoptimized / baseline input)
- `<name>.candidate.ll`: candidate rewrite proposed by the “LLM”

Metadata is embedded at the top of each source file:

- `; TITLE: ...`
- `; EXPECTED: ...` where values are:
  - `already-optimized` (baseline LLVM should usually handle it)
  - `missed` (candidate may expose a missed peephole)
- `; CATEGORY: ...` (optional) where common values are:
  - `llm-candidate` (default)
  - `hallucination` (intentionally wrong rewrite)
  - `ambiguous` (semantics-preserving but unclear/no gain)
- `; FAMILY: ...` (optional) to group related variants for generalization checks
- `; VARIANT: ...` (optional) variant name inside a family

The experiment runner validates candidates with Alive2 and compares
candidate output against LLVM baseline output, adds a simple profitability
metric, and aggregates per-family generalization results.
