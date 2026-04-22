; TITLE: Eliminate redundant select arms
; EXPECTED: already-optimized
define i32 @f(i1 %c, i32 %x) {
entry:
  %s = select i1 %c, i32 %x, i32 %x
  ret i32 %s
}
