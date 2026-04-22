; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c42_bit_extract_alt_form_shift17_i64.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c42_bit_extract_alt_form_shift17_i64.ll"

define i64 @f(i64 %x) {
entry:
  %a = lshr i64 %x, 17
  %b = and i64 %a, 1023
  ret i64 %b
}
