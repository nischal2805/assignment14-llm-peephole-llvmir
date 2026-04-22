; TITLE: Invalid rewrite sanity check
; EXPECTED: missed
define i32 @f(i32 %x) {
entry:
  %a = xor i32 %x, %x
  ret i32 %a
}
