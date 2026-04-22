# Experiment Summary

- Total cases: **48**
- Confirmed missed opportunities: **4**
- Invalid candidate rewrites: **0**
- Hallucinated candidate rewrites: **4**
- Already optimized by baseline: **31**
- Candidate profitability vs source (value-inst count, Alive-valid only): better **30**, neutral **12**, worse **2**

| Case | Expected | Category | Family | Alive2 | Cand inst count | Cand profitability | Baseline changed? | Candidate vs baseline | Classification |
|---|---|---|---|---|---|---|---|---|---|
| `c01_add_zero` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/1` | `better` | `True` | `False` | `baseline_optimizes` |
| `c02_xor_self` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/1` | `better` | `True` | `False` | `baseline_optimizes` |
| `c03_mul_one` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/1` | `better` | `True` | `False` | `baseline_optimizes` |
| `c04_select_const` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/1` | `better` | `True` | `False` | `baseline_optimizes` |
| `c05_or_zero` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/1` | `better` | `True` | `False` | `baseline_optimizes` |
| `c06_sdiv_self_nonzero` | `missed` | `llm-candidate` | `-` | `valid` | `0/2` | `better` | `True` | `False` | `not_missed` |
| `c07_udiv_self_nonzero` | `missed` | `llm-candidate` | `-` | `valid` | `0/2` | `better` | `True` | `False` | `not_missed` |
| `c08_invalid_candidate_example` | `missed` | `hallucination` | `hallucinated_boolean_arith` | `invalid` | `0/1` | `better` | `True` | `True` | `hallucinated_candidate` |
| `c09_and_or_partition` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/3` | `better` | `True` | `False` | `baseline_optimizes` |
| `c10_xor_cancel` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c11_add_sub_cancel` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c12_sub_add_cancel` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c13_shift_add_mul10` | `already-optimized` | `llm-candidate` | `-` | `valid` | `1/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c14_mul_sub_mul8` | `already-optimized` | `llm-candidate` | `-` | `valid` | `2/3` | `better` | `True` | `False` | `baseline_optimizes` |
| `c15_shift_mask_low24` | `already-optimized` | `llm-candidate` | `-` | `valid` | `1/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c16_zext_trunc_to_mask` | `already-optimized` | `llm-candidate` | `-` | `valid` | `1/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c17_udiv_pow2_to_lshr` | `already-optimized` | `llm-candidate` | `-` | `valid` | `1/1` | `neutral` | `True` | `False` | `baseline_optimizes` |
| `c18_urem_pow2_to_and` | `already-optimized` | `llm-candidate` | `-` | `valid` | `1/1` | `neutral` | `True` | `False` | `baseline_optimizes` |
| `c19_select_same_arms` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/1` | `better` | `True` | `False` | `baseline_optimizes` |
| `c20_select_const_to_zext` | `already-optimized` | `llm-candidate` | `-` | `valid` | `1/1` | `neutral` | `True` | `False` | `baseline_optimizes` |
| `c21_select_invert_bool` | `already-optimized` | `llm-candidate` | `-` | `valid` | `2/1` | `worse` | `True` | `True` | `baseline_optimizes` |
| `c22_absorb_or_and` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c23_absorb_and_or` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c24_double_negation` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c25_and_mask_merge` | `already-optimized` | `llm-candidate` | `-` | `valid` | `1/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c26_or_mask_merge` | `already-optimized` | `llm-candidate` | `-` | `valid` | `1/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c27_xor_const_merge` | `already-optimized` | `llm-candidate` | `-` | `valid` | `1/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c28_eq_xor_zero` | `already-optimized` | `llm-candidate` | `-` | `valid` | `2/3` | `better` | `True` | `False` | `baseline_optimizes` |
| `c29_ne_xor_zero` | `already-optimized` | `llm-candidate` | `-` | `valid` | `2/3` | `better` | `True` | `False` | `baseline_optimizes` |
| `c30_trunc_zext_roundtrip` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c31_trunc_sext_roundtrip` | `already-optimized` | `llm-candidate` | `-` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c32_cfg_phi_same_value` | `missed` | `llm-candidate` | `-` | `valid` | `0/3` | `better` | `True` | `False` | `not_missed` |
| `c33_cfg_redundant_branches` | `missed` | `llm-candidate` | `-` | `valid` | `0/0` | `neutral` | `True` | `False` | `not_missed` |
| `c34_phi_const_collapse` | `missed` | `llm-candidate` | `-` | `valid` | `0/1` | `better` | `True` | `False` | `not_missed` |
| `c35_bit_extract_alt_form` | `missed` | `llm-candidate` | `bit_extract_alt_form` | `valid` | `2/2` | `neutral` | `False` | `True` | `confirmed_missed` |
| `c36_icmp_uge_one_to_ne_zero` | `already-optimized` | `llm-candidate` | `-` | `valid` | `2/2` | `neutral` | `True` | `False` | `baseline_optimizes` |
| `c37_icmp_ule_zero_to_eq_zero` | `already-optimized` | `llm-candidate` | `-` | `valid` | `2/2` | `neutral` | `True` | `False` | `baseline_optimizes` |
| `c38_mul_add_mul3` | `already-optimized` | `llm-candidate` | `-` | `valid` | `1/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `c39_shift_add_mul7` | `missed` | `llm-candidate` | `-` | `valid` | `1/4` | `better` | `True` | `False` | `not_missed` |
| `c40_guarded_sdiv_self` | `missed` | `llm-candidate` | `-` | `valid` | `2/2` | `neutral` | `True` | `False` | `not_missed` |
| `c41_bit_extract_alt_form_shift5_i32` | `missed` | `llm-candidate` | `bit_extract_alt_form` | `valid` | `2/2` | `neutral` | `False` | `True` | `confirmed_missed` |
| `c42_bit_extract_alt_form_shift17_i64` | `missed` | `llm-candidate` | `bit_extract_alt_form` | `valid` | `2/2` | `neutral` | `False` | `True` | `confirmed_missed` |
| `c43_bit_extract_alt_form_shift9_i32` | `missed` | `llm-candidate` | `bit_extract_alt_form` | `valid` | `2/2` | `neutral` | `False` | `True` | `confirmed_missed` |
| `c44_hallucination_or_to_add` | `missed` | `hallucination` | `hallucinated_boolean_arith` | `invalid` | `1/1` | `neutral` | `False` | `True` | `hallucinated_candidate` |
| `c45_hallucination_and_to_mul` | `missed` | `hallucination` | `hallucinated_boolean_arith` | `invalid` | `1/1` | `neutral` | `False` | `True` | `hallucinated_candidate` |
| `c46_hallucination_xor_to_sub` | `missed` | `hallucination` | `hallucinated_boolean_arith` | `invalid` | `1/1` | `neutral` | `False` | `True` | `hallucinated_candidate` |
| `c47_ambiguous_reorder_add` | `missed` | `ambiguous` | `ambiguous_no_gain` | `valid` | `2/2` | `neutral` | `True` | `True` | `different_but_not_missed` |
| `c48_ambiguous_redundant_predicate` | `missed` | `ambiguous` | `ambiguous_no_gain` | `valid` | `2/1` | `worse` | `True` | `True` | `different_but_not_missed` |

## Family Generalization (>=2 variants)

| Family | Variants | Alive-valid | Invalid/Hallucinated | Confirmed missed | Profitable | Unprofitable | Conclusion |
|---|---|---|---|---|---|---|---|
| `ambiguous_no_gain` | `2` | `2` | `0` | `0` | `0` | `1` | `valid_but_no_missed_evidence` |
| `bit_extract_alt_form` | `4` | `4` | `0` | `4` | `0` | `0` | `generalizes` |
| `hallucinated_boolean_arith` | `4` | `0` | `4` | `0` | `0` | `0` | `hallucinated_family` |

## Candidate Quality Buckets

| Bucket | Count |
|---|---|
| `ambiguous_valid` | `2` |
| `hallucinated` | `4` |
| `valid_neutral` | `11` |
| `valid_profitable` | `30` |
| `valid_unprofitable` | `1` |

## Notes

- **c01_add_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 1 (better).
- **c02_xor_self**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 1 (better).
- **c03_mul_one**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 1 (better).
- **c04_select_const**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 1 (better).
- **c05_or_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 1 (better).
- **c06_sdiv_self_nonzero**: Candidate does not provide a distinct simplification over baseline output. Candidate value-inst count is 0 vs source 2 (better).
- **c07_udiv_self_nonzero**: Candidate does not provide a distinct simplification over baseline output. Candidate value-inst count is 0 vs source 2 (better).
- **c08_invalid_candidate_example**: Intentional hallucination candidate was rejected by Alive2. Candidate value-inst count is 0 vs source 1 (better).
- **c09_and_or_partition**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 3 (better).
- **c10_xor_cancel**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **c11_add_sub_cancel**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **c12_sub_add_cancel**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **c13_shift_add_mul10**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 1 vs source 2 (better).
- **c14_mul_sub_mul8**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 2 vs source 3 (better).
- **c15_shift_mask_low24**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 1 vs source 2 (better).
- **c16_zext_trunc_to_mask**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 1 vs source 2 (better).
- **c17_udiv_pow2_to_lshr**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 1 vs source 1 (neutral).
- **c18_urem_pow2_to_and**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 1 vs source 1 (neutral).
- **c19_select_same_arms**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 1 (better).
- **c20_select_const_to_zext**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 1 vs source 1 (neutral).
- **c21_select_invert_bool**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 2 vs source 1 (worse).
- **c22_absorb_or_and**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **c23_absorb_and_or**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **c24_double_negation**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **c25_and_mask_merge**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 1 vs source 2 (better).
- **c26_or_mask_merge**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 1 vs source 2 (better).
- **c27_xor_const_merge**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 1 vs source 2 (better).
- **c28_eq_xor_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 2 vs source 3 (better).
- **c29_ne_xor_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 2 vs source 3 (better).
- **c30_trunc_zext_roundtrip**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **c31_trunc_sext_roundtrip**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **c32_cfg_phi_same_value**: Candidate does not provide a distinct simplification over baseline output. Candidate value-inst count is 0 vs source 3 (better).
- **c33_cfg_redundant_branches**: Candidate does not provide a distinct simplification over baseline output. Candidate value-inst count is 0 vs source 0 (neutral).
- **c34_phi_const_collapse**: Candidate does not provide a distinct simplification over baseline output. Candidate value-inst count is 0 vs source 1 (better).
- **c35_bit_extract_alt_form**: Candidate is Alive2-valid and differs from baseline; baseline did not apply equivalent simplification. Candidate value-inst count is 2 vs source 2 (neutral).
- **c36_icmp_uge_one_to_ne_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 2 vs source 2 (neutral).
- **c37_icmp_ule_zero_to_eq_zero**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 2 vs source 2 (neutral).
- **c38_mul_add_mul3**: Baseline InstCombine/SimplifyCFG already performs an equivalent transform. Candidate value-inst count is 1 vs source 2 (better).
- **c39_shift_add_mul7**: Candidate does not provide a distinct simplification over baseline output. Candidate value-inst count is 1 vs source 4 (better).
- **c40_guarded_sdiv_self**: Candidate does not provide a distinct simplification over baseline output. Candidate value-inst count is 2 vs source 2 (neutral).
- **c41_bit_extract_alt_form_shift5_i32**: Candidate is Alive2-valid and differs from baseline; baseline did not apply equivalent simplification. Candidate value-inst count is 2 vs source 2 (neutral).
- **c42_bit_extract_alt_form_shift17_i64**: Candidate is Alive2-valid and differs from baseline; baseline did not apply equivalent simplification. Candidate value-inst count is 2 vs source 2 (neutral).
- **c43_bit_extract_alt_form_shift9_i32**: Candidate is Alive2-valid and differs from baseline; baseline did not apply equivalent simplification. Candidate value-inst count is 2 vs source 2 (neutral).
- **c44_hallucination_or_to_add**: Intentional hallucination candidate was rejected by Alive2. Candidate value-inst count is 1 vs source 1 (neutral).
- **c45_hallucination_and_to_mul**: Intentional hallucination candidate was rejected by Alive2. Candidate value-inst count is 1 vs source 1 (neutral).
- **c46_hallucination_xor_to_sub**: Intentional hallucination candidate was rejected by Alive2. Candidate value-inst count is 1 vs source 1 (neutral).
- **c47_ambiguous_reorder_add**: Candidate differs, but baseline also changed IR; investigate semantic relation. Candidate value-inst count is 2 vs source 2 (neutral).
- **c48_ambiguous_redundant_predicate**: Candidate differs, but baseline also changed IR; investigate semantic relation. Candidate value-inst count is 2 vs source 1 (worse).

Each case has detailed outputs under `results/<case>/`.