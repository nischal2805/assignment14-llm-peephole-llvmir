# MLIR Experiment Summary

- Validation mode: **bounded equivalence + rule-based baseline simulation**
- Total cases: **8**
- Confirmed missed opportunities: **2**
- Invalid candidate rewrites: **0**
- Hallucinated candidate rewrites: **2**
- Already optimized by baseline: **4**
- Candidate profitability vs source (value-inst count, validator-valid only): better **4**, neutral **2**, worse **0**

| Case | Expected | Category | Family | Validator | Cand inst count | Cand profitability | Baseline changed? | Candidate vs baseline | Classification |
|---|---|---|---|---|---|---|---|---|---|
| `m01_addi_zero_i32` | `already-optimized` | `llm-candidate` | `mlir_baseline_identities` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `m02_muli_one_i32` | `already-optimized` | `llm-candidate` | `mlir_baseline_identities` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `m03_ori_zero_i32` | `already-optimized` | `llm-candidate` | `mlir_baseline_identities` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `m04_andi_allones_i32` | `already-optimized` | `llm-candidate` | `mlir_baseline_identities` | `valid` | `0/2` | `better` | `True` | `False` | `baseline_optimizes` |
| `m05_bit_extract_alt_shift3_i32` | `missed` | `llm-candidate` | `mlir_bit_extract_alt_form` | `valid` | `4/4` | `neutral` | `False` | `True` | `confirmed_missed` |
| `m06_bit_extract_alt_shift5_i32` | `missed` | `llm-candidate` | `mlir_bit_extract_alt_form` | `valid` | `4/4` | `neutral` | `False` | `True` | `confirmed_missed` |
| `m07_hallucination_or_to_add_i32` | `missed` | `hallucination` | `mlir_hallucinated_logic` | `invalid` | `1/1` | `neutral` | `False` | `True` | `hallucinated_candidate` |
| `m08_hallucination_and_to_mul_i32` | `missed` | `hallucination` | `mlir_hallucinated_logic` | `invalid` | `2/2` | `neutral` | `False` | `True` | `hallucinated_candidate` |

## Family Generalization (>=2 variants)

| Family | Variants | Valid | Invalid/Hallucinated | Confirmed missed | Profitable | Unprofitable | Conclusion |
|---|---|---|---|---|---|---|---|
| `mlir_baseline_identities` | `4` | `4` | `0` | `0` | `4` | `0` | `valid_but_no_missed_evidence` |
| `mlir_bit_extract_alt_form` | `2` | `2` | `0` | `2` | `0` | `0` | `generalizes` |
| `mlir_hallucinated_logic` | `2` | `0` | `2` | `0` | `0` | `0` | `hallucinated_family` |

## Candidate Quality Buckets

| Bucket | Count |
|---|---|
| `hallucinated` | `2` |
| `valid_neutral` | `2` |
| `valid_profitable` | `4` |

## Notes

- **m01_addi_zero_i32**: Simulated MLIR baseline already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **m02_muli_one_i32**: Simulated MLIR baseline already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **m03_ori_zero_i32**: Simulated MLIR baseline already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **m04_andi_allones_i32**: Simulated MLIR baseline already performs an equivalent transform. Candidate value-inst count is 0 vs source 2 (better).
- **m05_bit_extract_alt_shift3_i32**: Candidate passed bounded equivalence and differs from simulated baseline. Candidate value-inst count is 4 vs source 4 (neutral).
- **m06_bit_extract_alt_shift5_i32**: Candidate passed bounded equivalence and differs from simulated baseline. Candidate value-inst count is 4 vs source 4 (neutral).
- **m07_hallucination_or_to_add_i32**: Intentional hallucination candidate failed bounded equivalence. Candidate value-inst count is 1 vs source 1 (neutral).
- **m08_hallucination_and_to_mul_i32**: Intentional hallucination candidate failed bounded equivalence. Candidate value-inst count is 2 vs source 2 (neutral).

Each MLIR case has detailed outputs under `results_mlir/<case>/`.