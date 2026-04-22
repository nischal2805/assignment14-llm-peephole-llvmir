module {
  func.func @f(%arg0: i32) -> i32 {
    %c992 = arith.constant 992 : i32
    %0 = arith.andi %arg0, %c992 : i32
    %c5 = arith.constant 5 : i32
    %1 = arith.shrui %0, %c5 : i32
    return %1 : i32
  }
}
