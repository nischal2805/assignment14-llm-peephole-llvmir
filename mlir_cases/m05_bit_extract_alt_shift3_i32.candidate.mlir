module {
  func.func @f(%arg0: i32) -> i32 {
    %c56 = arith.constant 56 : i32
    %0 = arith.andi %arg0, %c56 : i32
    %c3 = arith.constant 3 : i32
    %1 = arith.shrui %0, %c3 : i32
    return %1 : i32
  }
}
