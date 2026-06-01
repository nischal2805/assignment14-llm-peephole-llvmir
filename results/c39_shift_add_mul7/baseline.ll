; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c39_shift_add_mul7.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c39_shift_add_mul7.ll"

define i32 @f(i32 %x) {
entry:
  %d = mul i32 %x, 7
  ret i32 %d
}
