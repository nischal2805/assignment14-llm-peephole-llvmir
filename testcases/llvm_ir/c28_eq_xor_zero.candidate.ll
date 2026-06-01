define i32 @f(i32 %x, i32 %y) {
entry:
  %cmp = icmp eq i32 %x, %y
  %r = zext i1 %cmp to i32
  ret i32 %r
}
