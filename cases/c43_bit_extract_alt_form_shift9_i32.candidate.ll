define i32 @f(i32 %x) {
entry:
  %m = and i32 %x, 32256
  %b = lshr i32 %m, 9
  ret i32 %b
}
