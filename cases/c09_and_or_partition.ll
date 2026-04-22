; TITLE: Bit partition and recombine
; EXPECTED: already-optimized
define i32 @f(i32 %x) {
entry:
  %a = and i32 %x, 252645135
  %b = and i32 %x, -252645136
  %c = or i32 %a, %b
  ret i32 %c
}
