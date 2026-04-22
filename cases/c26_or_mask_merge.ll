; TITLE: Merge nested or constants
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = or i32 %x, 16
  %b = or i32 %a, 2
  ret i32 %b
}
