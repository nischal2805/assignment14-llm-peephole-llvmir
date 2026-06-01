; TITLE: Parity xor reassociation
; EXPECTED: already-optimized
define i32 @f(i32 %x, i32 %y) {
entry:
  %a = and i32 %x, 1
  %b = and i32 %y, 1
  %c = xor i32 %a, %b
  ret i32 %c
}
