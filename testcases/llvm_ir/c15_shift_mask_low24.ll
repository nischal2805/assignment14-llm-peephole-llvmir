; TITLE: Recover low 24 bits via shifts
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = shl i32 %x, 8
  %b = lshr i32 %a, 8
  ret i32 %b
}
