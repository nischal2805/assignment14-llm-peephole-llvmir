; TITLE: Merge chained xor constants
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = xor i32 %x, 85
  %b = xor i32 %a, 51
  ret i32 %b
}
