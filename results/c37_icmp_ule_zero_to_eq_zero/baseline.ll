; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c37_icmp_ule_zero_to_eq_zero.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c37_icmp_ule_zero_to_eq_zero.ll"

define i32 @f(i32 %x) {
entry:
  %cmp = icmp eq i32 %x, 0
  %r = zext i1 %cmp to i32
  ret i32 %r
}
