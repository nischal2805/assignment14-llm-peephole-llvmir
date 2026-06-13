; TITLE: Hallucination: x*x rewritten as x<<x
; EXPECTED: missed
; CATEGORY: hallucination
; FAMILY: hallucinated_shift_semantics
; VARIANT: square_to_selfshift_i32
define i32 @f(i32 %x) {
entry:
  %r = mul i32 %x, %x
  ret i32 %r
}
