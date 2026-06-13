; Hallucination: LLM claims ashr == lshr, ignoring sign extension
; Counterexample: x=-1 -> ashr gives -1, lshr gives 2147483647
define i32 @f(i32 %x) {
entry:
  %r = lshr i32 %x, 1
  ret i32 %r
}
