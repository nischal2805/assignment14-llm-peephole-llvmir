define i64 @f(i64 %x) {
entry:
  %m = and i64 %x, 65535
  ret i64 %m
}
