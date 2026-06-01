define i32 @f(i32 %x) {
entry:
  %r = and i32 %x, 15
  ret i32 %r
}
