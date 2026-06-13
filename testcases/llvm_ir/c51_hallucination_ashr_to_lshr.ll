; TITLE: Hallucination: arithmetic shift right rewritten as logical shift right
; EXPECTED: missed
; CATEGORY: hallucination
; FAMILY: hallucinated_shift_semantics
; VARIANT: ashr_to_lshr_i32
define i32 @f(i32 %x) {
entry:
  %r = ashr i32 %x, 1
  ret i32 %r
}
