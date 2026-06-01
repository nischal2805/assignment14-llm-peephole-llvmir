// TITLE: MLIR hallucination: or rewritten as add
// EXPECTED: missed
// CATEGORY: hallucination
// FAMILY: mlir_hallucinated_logic
// VARIANT: or_to_add_i32
module {
  func.func @f(%arg0: i32, %arg1: i32) -> i32 {
    %0 = arith.ori %arg0, %arg1 : i32
    return %0 : i32
  }
}
