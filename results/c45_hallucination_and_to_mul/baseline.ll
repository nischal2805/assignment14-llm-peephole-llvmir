; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c45_hallucination_and_to_mul.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c45_hallucination_and_to_mul.ll"

define i32 @f(i32 %x) {
entry:
  %a = and i32 %x, 1
  ret i32 %a
}
