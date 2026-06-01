; TITLE: Select bool to integer cast
; EXPECTED: already-optimized
define i32 @f(i1 %c) {
entry:
  %s = select i1 %c, i32 1, i32 0
  ret i32 %s
}
