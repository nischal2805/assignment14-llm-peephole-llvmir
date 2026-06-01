; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c41_bit_extract_alt_form_shift5_i32.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c41_bit_extract_alt_form_shift5_i32.ll"

define i32 @f(i32 %x) {
entry:
  %a = lshr i32 %x, 5
  %b = and i32 %a, 127
  ret i32 %b
}
