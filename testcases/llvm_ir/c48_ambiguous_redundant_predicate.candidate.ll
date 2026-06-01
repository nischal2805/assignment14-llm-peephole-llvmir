define i32 @f(i1 %c, i32 %x) {
entry:
  %a = and i1 %c, true
  %b = select i1 %a, i32 %x, i32 %x
  ret i32 %b
}
