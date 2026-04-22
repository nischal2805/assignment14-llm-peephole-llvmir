# Experiment Summary

- Total cases: **40**
- Confirmed missed opportunities: **1**
- Invalid candidate rewrites: **1**
- Already optimized by baseline: **31**

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
| `c09_and_or_partition` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c10_xor_cancel` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c11_add_sub_cancel` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c12_sub_add_cancel` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c13_shift_add_mul10` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c14_mul_sub_mul8` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c15_shift_mask_low24` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c16_zext_trunc_to_mask` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c17_udiv_pow2_to_lshr` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c18_urem_pow2_to_and` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c19_select_same_arms` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c20_select_const_to_zext` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c21_select_invert_bool` | `already-optimized` | `valid` | `True` | `True` | `baseline_optimizes` |
| `c22_absorb_or_and` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c23_absorb_and_or` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c24_double_negation` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c25_and_mask_merge` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c26_or_mask_merge` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c27_xor_const_merge` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c28_eq_xor_zero` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c29_ne_xor_zero` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c30_trunc_zext_roundtrip` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c31_trunc_sext_roundtrip` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c32_cfg_phi_same_value` | `missed` | `valid` | `True` | `False` | `not_missed` |
| `c33_cfg_redundant_branches` | `missed` | `valid` | `True` | `False` | `not_missed` |
| `c34_phi_const_collapse` | `missed` | `valid` | `True` | `False` | `not_missed` |
| `c35_bit_extract_alt_form` | `missed` | `valid` | `False` | `True` | `confirmed_missed` |
| `c36_icmp_uge_one_to_ne_zero` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c37_icmp_ule_zero_to_eq_zero` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c38_mul_add_mul3` | `already-optimized` | `valid` | `True` | `False` | `baseline_optimizes` |
| `c39_shift_add_mul7` | `missed` | `valid` | `True` | `False` | `not_missed` |
| `c40_guarded_sdiv_self` | `missed` | `valid` | `True` | `False` | `not_missed` |

## Notes

- **c01_add_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c02_xor_self**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c03_mul_one**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c04_select_const**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c05_or_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c06_sdiv_self_nonzero**: Candidate does not provide a distinct simplification over baseline output.
- **c07_udiv_self_nonzero**: Candidate does not provide a distinct simplification over baseline output.
- **c08_invalid_candidate_example**: Candidate rewrite is unsound per Alive2.
- **c09_and_or_partition**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c10_xor_cancel**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c11_add_sub_cancel**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c12_sub_add_cancel**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c13_shift_add_mul10**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c14_mul_sub_mul8**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c15_shift_mask_low24**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c16_zext_trunc_to_mask**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c17_udiv_pow2_to_lshr**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c18_urem_pow2_to_and**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c19_select_same_arms**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c20_select_const_to_zext**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c21_select_invert_bool**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c22_absorb_or_and**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c23_absorb_and_or**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c24_double_negation**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c25_and_mask_merge**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c26_or_mask_merge**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c27_xor_const_merge**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c28_eq_xor_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c29_ne_xor_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c30_trunc_zext_roundtrip**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c31_trunc_sext_roundtrip**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c32_cfg_phi_same_value**: Candidate does not provide a distinct simplification over baseline output.
- **c33_cfg_redundant_branches**: Candidate does not provide a distinct simplification over baseline output.
- **c34_phi_const_collapse**: Candidate does not provide a distinct simplification over baseline output.
- **c35_bit_extract_alt_form**: Candidate is Alive2-valid and differs from baseline; baseline did not apply equivalent simplification.
- **c36_icmp_uge_one_to_ne_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c37_icmp_ule_zero_to_eq_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c38_mul_add_mul3**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform.
- **c39_shift_add_mul7**: Candidate does not provide a distinct simplification over baseline output.
- **c40_guarded_sdiv_self**: Candidate does not provide a distinct simplification over baseline output.

Each case has detailed outputs under `results/<case>/`.