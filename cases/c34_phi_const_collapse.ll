; TITLE: Fold phi of equal constants
; EXPECTED: missed
define i32 @f(i1 %c) {
entry:
  br i1 %c, label %then, label %else

then:
  br label %merge

else:
  br label %merge

merge:
  %p = phi i32 [ 42, %then ], [ 42, %else ]
  ret i32 %p
}
