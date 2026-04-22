; TITLE: Absorption law x & (x | y)
; EXPECTED: already-optimized
define i32 @f(i32 %x, i32 %y) {
entry:
  %a = or i32 %x, %y
  %b = and i32 %x, %a
  ret i32 %b
}
