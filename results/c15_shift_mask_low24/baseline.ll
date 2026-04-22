; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c15_shift_mask_low24.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c15_shift_mask_low24.ll"

define i32 @f(i32 %x) {
entry:
  %a = and i32 %x, 16777215
  ret i32 %a
}
