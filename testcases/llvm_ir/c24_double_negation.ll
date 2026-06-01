; TITLE: Eliminate double arithmetic negation
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = sub i32 0, %x
  %b = sub i32 0, %a
  ret i32 %b
}
