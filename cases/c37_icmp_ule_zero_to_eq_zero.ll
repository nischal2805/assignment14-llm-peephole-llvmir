; TITLE: Unsigned compare to zero canonicalization
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %cmp = icmp ule i32 %x, 0
  %r = zext i1 %cmp to i32
  ret i32 %r
}
