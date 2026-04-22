; TITLE: Remove multiply by one
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = mul i32 %x, 1
  ret i32 %a
}
