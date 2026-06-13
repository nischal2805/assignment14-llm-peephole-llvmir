; Hallucination: LLM confuses x*x with x<<x (only equal when x is a power of 2)
; Counterexample: x=2 -> mul gives 4, shl gives 8
define i32 @f(i32 %x) {
entry:
  %r = shl i32 %x, %x
  ret i32 %r
}
