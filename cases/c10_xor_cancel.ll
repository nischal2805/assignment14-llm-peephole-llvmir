; TITLE: Cancel repeated xor operand
; EXPECTED: already-optimized
define i32 @f(i32 %x, i32 %y) {
entry:
  %a = xor i32 %x, %y
  %b = xor i32 %a, %y
  ret i32 %b
}
