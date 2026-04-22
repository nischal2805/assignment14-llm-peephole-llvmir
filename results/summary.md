# Experiment Summary

- Total cases: **8**
- Confirmed missed opportunities: **0**
- Invalid candidate rewrites: **1**
- Already optimized by baseline: **5**

| Case | Expected | Alive2 | Baseline changed? | Candidate vs baseline | Classification |
|---|---|---|---|---|---|
| `c01_add_zero` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c02_xor_self` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c03_mul_one` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c04_select_const` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c05_or_zero` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c06_sdiv_self_nonzero` | `missed` | `valid` | `True` | `False` | `not_missed` |
| `c07_udiv_self_nonzero` | `missed` | `valid` | `True` | `False` | `not_missed` |
| `c08_invalid_candidate_example` | `missed` | `invalid` | `True` | `True` | `invalid_candidate` |

## Notes

- **c01_add_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c02_xor_self**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c03_mul_one**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c04_select_const**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c05_or_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c06_sdiv_self_nonzero**: Candidate does not provide a distinct simplification over baseline output.
- **c07_udiv_self_nonzero**: Candidate does not provide a distinct simplification over baseline output.
- **c08_invalid_candidate_example**: Candidate rewrite is unsound per Alive2.

Each case has detailed outputs under `results/<case>/`.