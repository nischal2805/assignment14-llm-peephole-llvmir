; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c20_select_const_to_zext.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c20_select_const_to_zext.ll"

define i32 @f(i1 %c) {
entry:
  %s = zext i1 %c to i32
  ret i32 %s
}
