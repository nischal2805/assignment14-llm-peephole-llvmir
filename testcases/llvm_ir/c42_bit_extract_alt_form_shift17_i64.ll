; TITLE: Extract 10-bit field in i64 via mask then shift
; EXPECTED: missed
; CATEGORY: llm-candidate
; FAMILY: bit_extract_alt_form
; VARIANT: shift17_mask1023_i64
define i64 @f(i64 %x) {
entry:
  %a = lshr i64 %x, 17
  %b = and i64 %a, 1023
  ret i64 %b
}
