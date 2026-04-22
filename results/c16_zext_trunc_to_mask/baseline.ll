; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c16_zext_trunc_to_mask.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c16_zext_trunc_to_mask.ll"

define i64 @f(i64 %x) {
entry:
  %z = and i64 %x, 65535
  ret i64 %z
}
