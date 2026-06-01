; TITLE: Select inverted bool to xor form
; EXPECTED: already-optimized
define i32 @f(i1 %c) {
entry:
  %s = select i1 %c, i32 0, i32 1
  ret i32 %s
}
