define i32 @f(i1 %c) {
entry:
  %z = zext i1 %c to i32
  ret i32 %z
}
