; TITLE: Compare xor to zero as inequality
; EXPECTED: already-optimized
define i32 @f(i32 %x, i32 %y) {
entry:
  %a = xor i32 %x, %y
  %cmp = icmp ne i32 %a, 0
  %r = zext i1 %cmp to i32
  ret i32 %r
}
