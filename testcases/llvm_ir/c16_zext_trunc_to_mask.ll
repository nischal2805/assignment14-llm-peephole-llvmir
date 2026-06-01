; TITLE: Convert zext trunc to mask
; EXPECTED: already-optimized
define i64 @f(i64 %x) {
entry:
  %t = trunc i64 %x to i16
  %z = zext i16 %t to i64
  ret i64 %z
}
