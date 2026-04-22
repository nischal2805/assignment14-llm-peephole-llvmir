; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c14_mul_sub_mul8.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c14_mul_sub_mul8.ll"

define i32 @f(i32 %x, i32 %y) {
entry:
  %a1 = xor i32 %x, %y
  %c = and i32 %a1, 1
  ret i32 %c
}
