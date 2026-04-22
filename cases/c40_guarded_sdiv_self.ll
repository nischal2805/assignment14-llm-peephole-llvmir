; TITLE: Guarded self division to branchless form
; EXPECTED: missed
define i32 @f(i32 %x) {
entry:
  %iszero = icmp eq i32 %x, 0
  br i1 %iszero, label %zero, label %nonzero

zero:
  ret i32 0

nonzero:
  %q = sdiv i32 %x, %x
  ret i32 %q
}
