; TITLE: Extract bitfield via mask then shift
; EXPECTED: missed
define i32 @f(i32 %x) {
entry:
  %a = lshr i32 %x, 12
  %b = and i32 %a, 31
  ret i32 %b
}
