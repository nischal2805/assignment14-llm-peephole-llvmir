; TITLE: Divide a nonzero value by itself
; EXPECTED: missed
define i32 @f(i32 %x) {
entry:
  %nz = or i32 %x, 1
  %q = sdiv i32 %nz, %nz
  ret i32 %q
}
