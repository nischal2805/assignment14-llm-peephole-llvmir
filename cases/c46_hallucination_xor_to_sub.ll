; TITLE: Hallucination: XOR with one rewritten as SUB one
; EXPECTED: missed
; CATEGORY: hallucination
; FAMILY: hallucinated_boolean_arith
; VARIANT: xor_to_sub_i32
define i32 @f(i32 %x) {
entry:
  %a = xor i32 %x, 1
  ret i32 %a
}
