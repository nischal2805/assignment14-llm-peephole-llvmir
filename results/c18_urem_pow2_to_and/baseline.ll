; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c18_urem_pow2_to_and.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/testcases/llvm_ir/c18_urem_pow2_to_and.ll"

define i32 @f(i32 %x) {
entry:
  %r = and i32 %x, 15
  ret i32 %r
}
