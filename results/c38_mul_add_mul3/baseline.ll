; ModuleID = '/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c38_mul_add_mul3.ll'
source_filename = "/home/boss/llvm/assignment14-llm-peephole-llvmir/cases/c38_mul_add_mul3.ll"

define i32 @f(i32 %x) {
entry:
  %b = mul i32 %x, 3
  ret i32 %b
}
