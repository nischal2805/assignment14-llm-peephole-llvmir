define i32 @f(i32 %x, i32 %y) {
entry:
  %d = xor i32 %x, %y
  %e = and i32 %d, 1
  ret i32 %e
}
