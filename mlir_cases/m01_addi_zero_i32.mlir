// TITLE: MLIR fold addi by zero
// EXPECTED: already-optimized
// CATEGORY: llm-candidate
// FAMILY: mlir_baseline_identities
// VARIANT: addi_zero_rhs_i32
module {
  func.func @f(%arg0: i32) -> i32 {
    %c0 = arith.constant 0 : i32
    %0 = arith.addi %arg0, %c0 : i32
    return %0 : i32
  }
}
