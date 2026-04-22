; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c35_bit_extract_alt_form.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c35_bit_extract_alt_form.ll"

define i32 @f(i32 %x) {
entry:
  %a = lshr i32 %x, 12
  %b = and i32 %a, 31
  ret i32 %b
}
