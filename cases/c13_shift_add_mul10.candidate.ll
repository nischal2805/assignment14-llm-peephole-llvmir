define i32 @f(i32 %x) {
entry:
  %m = and i32 %x, -2
  ret i32 %m
}
