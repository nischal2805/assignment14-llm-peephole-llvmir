define i32 @f(i32 %x) {
entry:
  %cmp = icmp ne i32 %x, 0
  %r = zext i1 %cmp to i32
  ret i32 %r
}
