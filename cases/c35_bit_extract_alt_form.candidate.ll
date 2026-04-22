define i32 @f(i32 %x) {
entry:
  %m = and i32 %x, 126976
  %b = lshr i32 %m, 12
  ret i32 %b
}
