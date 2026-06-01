// TITLE: MLIR fold muli by one
// EXPECTED: already-optimized
// CATEGORY: llm-candidate
// FAMILY: mlir_baseline_identities
// VARIANT: muli_one_rhs_i32
module {
  func.func @f(%arg0: i32) -> i32 {
    %c1 = arith.constant 1 : i32
    %0 = arith.muli %arg0, %c1 : i32
    return %0 : i32
  }
}
