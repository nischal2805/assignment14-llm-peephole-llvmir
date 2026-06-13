define i32 @f(i32 %x) {
entry:
  %r = or i32 %x, -256
  ret i32 %r
}
