; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@str_0 = constant [27 x i8] c"Errore: divisione per zero\00"
@str_1 = constant [3 x i8] c"%s\00"
@str_2 = local_unnamed_addr constant [2 x i8] c"\0A\00"
@str_3 = constant [22 x i8] c"Calcolatrice semplice\00"
@str_4 = constant [19 x i8] c"1=+  2=-  3=*  4=/\00"
@str_5 = constant [13 x i8] c"Operazione: \00"
@str_6 = constant [3 x i8] c"%d\00"
@str_7 = constant [4 x i8] c"A: \00"
@str_8 = constant [4 x i8] c"%lf\00"
@str_9 = constant [4 x i8] c"B: \00"
@str_10 = constant [11 x i8] c"Risultato=\00"
@str_11 = constant [5 x i8] c"%.6f\00"
@str_12 = constant [46 x i8] c"Vuoi fare un'altra operazione? (1=si, 0=no): \00"

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
declare noundef i32 @scanf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
define double @calc(double %a, double %b, i32 %op) local_unnamed_addr #0 {
entry:
  switch i32 %op, label %elif_1_next [
    i32 1, label %if_then
    i32 2, label %elif_0_then
    i32 3, label %elif_1_then
  ]

common.ret:                                       ; preds = %next_branch.1, %if_then.1, %elif_1_then, %elif_0_then, %if_then
  %common.ret.op = phi double [ %.9, %if_then ], [ %.13, %elif_0_then ], [ %.17, %elif_1_then ], [ 0.000000e+00, %if_then.1 ], [ %.27, %next_branch.1 ]
  ret double %common.ret.op

if_then:                                          ; preds = %entry
  %.9 = fadd double %a, %b
  br label %common.ret

elif_0_then:                                      ; preds = %entry
  %.13 = fsub double %a, %b
  br label %common.ret

elif_1_then:                                      ; preds = %entry
  %.17 = fmul double %a, %b
  br label %common.ret

elif_1_next:                                      ; preds = %entry
  %.19 = fcmp oeq double %b, 0.000000e+00
  br i1 %.19, label %if_then.1, label %next_branch.1

if_then.1:                                        ; preds = %elif_1_next
  %.22 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_0)
  %putchar = tail call i32 @putchar(i32 10)
  br label %common.ret

next_branch.1:                                    ; preds = %elif_1_next
  %.27 = fdiv double %a, %b
  br label %common.ret
}

; Function Attrs: nofree nounwind
define void @main() local_unnamed_addr #0 {
entry:
  %a = alloca double, align 8
  store double 0.000000e+00, ptr %a, align 8
  %b = alloca double, align 8
  store double 0.000000e+00, ptr %b, align 8
  %op = alloca i32, align 4
  store i32 0, ptr %op, align 4
  %cont = alloca i32, align 4
  %.9 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_3)
  %putchar = tail call i32 @putchar(i32 10)
  %.15 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_4)
  %putchar1 = tail call i32 @putchar(i32 10)
  store i32 1, ptr %cont, align 4
  br label %while_body

while_body:                                       ; preds = %entry, %calc.exit
  %.25 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_5)
  %.27 = call i32 (ptr, ...) @scanf(ptr nonnull @str_6, ptr nonnull %op)
  %.30 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_7)
  %.32 = call i32 (ptr, ...) @scanf(ptr nonnull @str_8, ptr nonnull %a)
  %.35 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_9)
  %.37 = call i32 (ptr, ...) @scanf(ptr nonnull @str_8, ptr nonnull %b)
  %load_a = load double, ptr %a, align 8
  %load_b = load double, ptr %b, align 8
  %load_op = load i32, ptr %op, align 4
  switch i32 %load_op, label %elif_1_next.i [
    i32 1, label %if_then.i
    i32 2, label %elif_0_then.i
    i32 3, label %elif_1_then.i
  ]

if_then.i:                                        ; preds = %while_body
  %.9.i = fadd double %load_a, %load_b
  br label %calc.exit

elif_0_then.i:                                    ; preds = %while_body
  %.13.i = fsub double %load_a, %load_b
  br label %calc.exit

elif_1_then.i:                                    ; preds = %while_body
  %.17.i = fmul double %load_a, %load_b
  br label %calc.exit

elif_1_next.i:                                    ; preds = %while_body
  %.19.i = fcmp oeq double %load_b, 0.000000e+00
  br i1 %.19.i, label %if_then.1.i, label %next_branch.1.i

if_then.1.i:                                      ; preds = %elif_1_next.i
  %.22.i = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_0)
  %putchar.i = call i32 @putchar(i32 10)
  br label %calc.exit

next_branch.1.i:                                  ; preds = %elif_1_next.i
  %.27.i = fdiv double %load_a, %load_b
  br label %calc.exit

calc.exit:                                        ; preds = %if_then.i, %elif_0_then.i, %elif_1_then.i, %if_then.1.i, %next_branch.1.i
  %common.ret.op.i = phi double [ %.9.i, %if_then.i ], [ %.13.i, %elif_0_then.i ], [ %.17.i, %elif_1_then.i ], [ 0.000000e+00, %if_then.1.i ], [ %.27.i, %next_branch.1.i ]
  %.42 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_10)
  %.44 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_11, double %common.ret.op.i)
  %putchar2 = call i32 @putchar(i32 10)
  %.50 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_12)
  %.52 = call i32 (ptr, ...) @scanf(ptr nonnull @str_6, ptr nonnull %cont)
  %load_cont.pr = load i32, ptr %cont, align 4
  %.21 = icmp eq i32 %load_cont.pr, 1
  br i1 %.21, label %while_body, label %while_end

while_end:                                        ; preds = %calc.exit
  ret void
}

; Function Attrs: nofree nounwind
declare noundef i32 @putchar(i32 noundef) local_unnamed_addr #0

attributes #0 = { nofree nounwind }
