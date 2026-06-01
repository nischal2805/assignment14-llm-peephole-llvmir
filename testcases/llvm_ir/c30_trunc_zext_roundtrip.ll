; TITLE: Trunc of zext roundtrip
; EXPECTED: already-optimized
define i8 @f(i8 %x) {
entry:
  %z = zext i8 %x to i32
  %t = trunc i32 %z to i8
  ret i8 %t
}
