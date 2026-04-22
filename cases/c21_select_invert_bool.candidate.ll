define i32 @f(i1 %c) {
entry:
  %z = zext i1 %c to i32
  %r = xor i32 %z, 1
  ret i32 %r
}
