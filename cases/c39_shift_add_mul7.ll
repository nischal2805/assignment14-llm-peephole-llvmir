; TITLE: Combine shifts and add to 7x
; EXPECTED: missed
define i32 @f(i32 %x) {
entry:
  %a = shl i32 %x, 2
  %b = shl i32 %x, 1
  %c = add i32 %a, %b
  %d = add i32 %c, %x
  ret i32 %d
}
