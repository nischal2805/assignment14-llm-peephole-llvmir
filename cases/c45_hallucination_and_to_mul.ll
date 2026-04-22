; TITLE: Hallucination: bit mask rewritten as multiply
; EXPECTED: missed
; CATEGORY: hallucination
; FAMILY: hallucinated_boolean_arith
; VARIANT: and_to_mul_i32
define i32 @f(i32 %x) {
entry:
  %a = and i32 %x, 1
  ret i32 %a
}
