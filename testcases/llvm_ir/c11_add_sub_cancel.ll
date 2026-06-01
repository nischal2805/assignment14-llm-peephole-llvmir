; TITLE: Cancel add then subtract
; EXPECTED: already-optimized
define i32 @f(i32 %x, i32 %y) {
entry:
  %a = add i32 %x, %y
  %b = sub i32 %a, %y
  ret i32 %b
}
