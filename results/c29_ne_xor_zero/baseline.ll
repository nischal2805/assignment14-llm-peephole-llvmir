; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c29_ne_xor_zero.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c29_ne_xor_zero.ll"

define i32 @f(i32 %x, i32 %y) {
entry:
  %cmp = icmp ne i32 %x, %y
  %r = zext i1 %cmp to i32
  ret i32 %r
}
