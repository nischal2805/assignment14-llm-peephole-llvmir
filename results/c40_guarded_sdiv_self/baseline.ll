; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c40_guarded_sdiv_self.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c40_guarded_sdiv_self.ll"

define i32 @f(i32 %x) {
entry:
  %iszero = icmp eq i32 %x, 0
  %. = select i1 %iszero, i32 0, i32 1
  ret i32 %.
}
