; TITLE: Unsigned compare canonicalization
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %cmp = icmp uge i32 %x, 1
  %r = zext i1 %cmp to i32
  ret i32 %r
}
