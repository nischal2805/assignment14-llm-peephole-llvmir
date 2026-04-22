; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c44_hallucination_or_to_add.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c44_hallucination_or_to_add.ll"

define i32 @f(i32 %x, i32 %y) {
entry:
  %a = or i32 %x, %y
  ret i32 %a
}
