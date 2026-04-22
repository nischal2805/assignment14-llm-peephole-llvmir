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

The experiment runner validates candidates with Alive2 and compares
candidate output against LLVM baseline output.
