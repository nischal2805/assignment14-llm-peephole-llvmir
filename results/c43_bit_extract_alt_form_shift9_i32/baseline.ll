; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c43_bit_extract_alt_form_shift9_i32.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c43_bit_extract_alt_form_shift9_i32.ll"

define i32 @f(i32 %x) {
entry:
  %a = lshr i32 %x, 9
  %b = and i32 %a, 63
  ret i32 %b
}
