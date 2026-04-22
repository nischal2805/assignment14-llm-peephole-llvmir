; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c21_select_invert_bool.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c21_select_invert_bool.ll"

define i32 @f(i1 %c) {
entry:
  %not.c = xor i1 %c, true
  %s = zext i1 %not.c to i32
  ret i32 %s
}
