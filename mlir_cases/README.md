# MLIR Case Pack Overview

This directory contains MLIR optimization test cases.

Each case has two files:

- `<name>.mlir`: source pattern (baseline input)
- `<name>.candidate.mlir`: candidate rewrite proposed by the LLM

Metadata is embedded at the top of each source file:

- `// TITLE: ...`
- `// EXPECTED: ...` where values are:
  - `already-optimized`
  - `missed`
- `// CATEGORY: ...` (`llm-candidate`, `hallucination`, or `ambiguous`)
- `// FAMILY: ...` for generalization grouping
- `// VARIANT: ...` for variant labels

The MLIR experiment runner performs bounded equivalence checking and a
small rule-based baseline simulation to classify each case.
