; TITLE: Ambiguous: add redundant predicate to select
; EXPECTED: missed
; CATEGORY: ambiguous
; FAMILY: ambiguous_no_gain
; VARIANT: redundant_predicate_select
define i32 @f(i1 %c, i32 %x) {
entry:
  %a = select i1 %c, i32 %x, i32 %x
  ret i32 %a
}
