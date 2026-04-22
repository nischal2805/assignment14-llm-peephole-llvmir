; TITLE: Invalid rewrite sanity check
; EXPECTED: missed
; CATEGORY: hallucination
; FAMILY: hallucinated_boolean_arith
; VARIANT: xor_self_to_one_i32
define i32 @f(i32 %x) {
entry:
  %a = xor i32 %x, %x
  ret i32 %a
}
