; TITLE: Remove add by zero
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = add i32 %x, 0
  ret i32 %a
}
