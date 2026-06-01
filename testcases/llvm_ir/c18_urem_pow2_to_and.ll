; TITLE: Unsigned remainder by power of two
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %r = urem i32 %x, 16
  ret i32 %r
}
