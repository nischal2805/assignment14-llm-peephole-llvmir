; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c27_xor_const_merge.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c27_xor_const_merge.ll"

define i32 @f(i32 %x) {
entry:
  %b = xor i32 %x, 102
  ret i32 %b
}
