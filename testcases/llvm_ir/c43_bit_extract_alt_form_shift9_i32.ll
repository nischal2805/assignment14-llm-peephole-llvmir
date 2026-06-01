; TITLE: Extract 6-bit field via mask then shift
; EXPECTED: missed
; CATEGORY: llm-candidate
; FAMILY: bit_extract_alt_form
; VARIANT: shift9_mask63_i32
define i32 @f(i32 %x) {
entry:
  %a = lshr i32 %x, 9
  %b = and i32 %a, 63
  ret i32 %b
}
