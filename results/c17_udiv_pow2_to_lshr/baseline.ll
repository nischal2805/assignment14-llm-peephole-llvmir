; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c17_udiv_pow2_to_lshr.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c17_udiv_pow2_to_lshr.ll"

define i32 @f(i32 %x) {
entry:
  %q1 = lshr i32 %x, 4
  ret i32 %q1
}
