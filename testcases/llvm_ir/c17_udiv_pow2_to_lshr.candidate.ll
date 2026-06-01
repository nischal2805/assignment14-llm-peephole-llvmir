define i32 @f(i32 %x) {
entry:
  %q = lshr i32 %x, 4
  ret i32 %q
}
