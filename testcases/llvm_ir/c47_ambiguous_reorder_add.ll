; TITLE: Ambiguous: reorder add operands
; EXPECTED: missed
; CATEGORY: ambiguous
; FAMILY: ambiguous_no_gain
; VARIANT: reorder_add_operands
define i32 @f(i32 %x, i32 %y) {
entry:
  %a = add i32 %x, %y
  %b = sub i32 %a, %y
  ret i32 %b
}
