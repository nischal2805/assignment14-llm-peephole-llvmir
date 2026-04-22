; TITLE: Clear least-significant bit via shifts
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = lshr i32 %x, 1
  %b = shl i32 %a, 1
  ret i32 %b
}
