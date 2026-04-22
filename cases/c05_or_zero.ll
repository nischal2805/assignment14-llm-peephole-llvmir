; TITLE: Remove or with zero
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = or i32 %x, 0
  ret i32 %a
}
