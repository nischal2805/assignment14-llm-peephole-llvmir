; TITLE: De Morgan complement: ~(~x & 0xFF) to x | ~0xFF
; EXPECTED: missed
; CATEGORY: llm-candidate
; FAMILY: demorgan_complement
; VARIANT: mask255_i32
define i32 @f(i32 %x) {
entry:
  %nx = xor i32 %x, -1
  %a  = and i32 %nx, 255
  %r  = xor i32 %a, -1
  ret i32 %r
}
