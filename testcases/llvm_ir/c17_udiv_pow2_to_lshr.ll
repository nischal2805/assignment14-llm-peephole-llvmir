; TITLE: Unsigned divide by power of two
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %q = udiv i32 %x, 16
  ret i32 %q
}
