; TITLE: Combine 2x plus x
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = mul i32 %x, 2
  %b = add i32 %a, %x
  ret i32 %b
}
