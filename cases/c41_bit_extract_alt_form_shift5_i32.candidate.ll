define i32 @f(i32 %x) {
entry:
  %m = and i32 %x, 4064
  %b = lshr i32 %m, 5
  ret i32 %b
}
