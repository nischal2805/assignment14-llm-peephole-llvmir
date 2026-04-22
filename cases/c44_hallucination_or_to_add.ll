; TITLE: Hallucination: OR rewritten as ADD
; EXPECTED: missed
; CATEGORY: hallucination
; FAMILY: hallucinated_boolean_arith
; VARIANT: or_to_add_i32
define i32 @f(i32 %x, i32 %y) {
entry:
  %a = or i32 %x, %y
  ret i32 %a
}
