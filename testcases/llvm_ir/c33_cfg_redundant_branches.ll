; TITLE: Remove redundant branch diamonds
; EXPECTED: missed
define i32 @f(i1 %c, i32 %x) {
entry:
  br i1 %c, label %left, label %right

left:
  br label %exit

right:
  br label %exit

exit:
  ret i32 %x
}
