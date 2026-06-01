; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c46_hallucination_xor_to_sub.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c46_hallucination_xor_to_sub.ll"

define i32 @f(i32 %x) {
entry:
  %a = xor i32 %x, 1
  ret i32 %a
}
