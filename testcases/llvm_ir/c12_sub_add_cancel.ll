; TITLE: Cancel subtract then add
; EXPECTED: already-optimized
define i32 @f(i32 %x, i32 %y) {
entry:
  %a = sub i32 %x, %y
  %b = add i32 %a, %y
  ret i32 %b
}
