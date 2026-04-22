; TITLE: Trunc of sext roundtrip
; EXPECTED: already-optimized
define i8 @f(i8 %x) {
entry:
  %s = sext i8 %x to i32
  %t = trunc i32 %s to i8
  ret i8 %t
}
