; TITLE: Fold select on constant condition
; EXPECTED: already-optimized
define i32 @f(i32 %x, i32 %y) {
entry:
  %a = select i1 true, i32 %x, i32 %y
  ret i32 %a
}
