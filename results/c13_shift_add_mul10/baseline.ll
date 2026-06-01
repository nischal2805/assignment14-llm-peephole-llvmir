; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c13_shift_add_mul10.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c13_shift_add_mul10.ll"

define i32 @f(i32 %x) {
entry:
  %a = and i32 %x, -2
  ret i32 %a
}
