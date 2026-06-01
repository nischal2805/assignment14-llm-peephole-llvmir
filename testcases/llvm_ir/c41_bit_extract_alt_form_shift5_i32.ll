; TITLE: Extract 7-bit field via mask then shift
; EXPECTED: missed
; CATEGORY: llm-candidate
; FAMILY: bit_extract_alt_form
; VARIANT: shift5_mask127_i32
define i32 @f(i32 %x) {
entry:
  %a = lshr i32 %x, 5
  %b = and i32 %a, 127
  ret i32 %b
}
