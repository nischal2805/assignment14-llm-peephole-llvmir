define i32 @f(i32 %x) {
entry:
  %iszero = icmp eq i32 %x, 0
  %r = select i1 %iszero, i32 0, i32 1
  ret i32 %r
}
