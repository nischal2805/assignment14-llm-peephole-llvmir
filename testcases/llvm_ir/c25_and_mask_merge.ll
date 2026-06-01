; TITLE: Merge nested and masks
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = and i32 %x, 255
  %b = and i32 %a, 15
  ret i32 %b
}
