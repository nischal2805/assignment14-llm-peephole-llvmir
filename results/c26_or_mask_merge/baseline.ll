; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c26_or_mask_merge.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c26_or_mask_merge.ll"

define i32 @f(i32 %x) {
entry:
  %b = or i32 %x, 18
  ret i32 %b
}
