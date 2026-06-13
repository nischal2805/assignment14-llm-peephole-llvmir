define i32 @f(i32 %x) {
entry:
  %r = or i32 %x, -241
  ret i32 %r
}
