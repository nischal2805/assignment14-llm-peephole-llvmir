define i64 @f(i64 %x) {
entry:
  %m = and i64 %x, 134086656
  %b = lshr i64 %m, 17
  ret i64 %b
}
