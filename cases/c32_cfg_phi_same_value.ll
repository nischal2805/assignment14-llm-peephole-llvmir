; TITLE: Collapse phi fed by same value
; EXPECTED: missed
define i32 @f(i1 %c, i32 %x) {
entry:
  br i1 %c, label %then, label %else

then:
  %t = add i32 %x, 0
  br label %merge

else:
  %e = add i32 %x, 0
  br label %merge

merge:
  %p = phi i32 [ %t, %then ], [ %e, %else ]
  ret i32 %p
}
