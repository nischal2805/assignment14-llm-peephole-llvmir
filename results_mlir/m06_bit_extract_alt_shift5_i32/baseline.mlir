// TITLE: MLIR bit extract via shift then mask variant
// EXPECTED: missed
// CATEGORY: llm-candidate
// FAMILY: mlir_bit_extract_alt_form
// VARIANT: shift5_mask31_i32
module {
  func.func @f(%arg0: i32) -> i32 {
    %c5 = arith.constant 5 : i32
    %0 = arith.shrui %arg0, %c5 : i32
    %c31 = arith.constant 31 : i32
    %1 = arith.andi %0, %c31 : i32
    return %1 : i32
  }
}
