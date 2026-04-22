; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c25_and_mask_merge.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c25_and_mask_merge.ll"

define i32 @f(i32 %x) {
entry:
  %b = and i32 %x, 15
  ret i32 %b
}
