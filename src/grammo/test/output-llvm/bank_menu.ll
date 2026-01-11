; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@G_START_BAL = local_unnamed_addr global double 1.000000e+03
@str_0 = constant [15 x i8] c"Mini Bank Demo\00"
@G_TITLE = local_unnamed_addr global ptr @str_0
@str_1 = local_unnamed_addr constant [2 x i8] c"\0A\00"
@str_2 = constant [3 x i8] c"%s\00"
@str_3 = constant [17 x i8] c"1 = Mostra saldo\00"
@str_4 = constant [13 x i8] c"2 = Deposita\00"
@str_5 = constant [12 x i8] c"3 = Preleva\00"
@str_6 = constant [9 x i8] c"0 = Esci\00"
@str_7 = constant [19 x i8] c"Importo non valido\00"
@str_8 = constant [20 x i8] c"Fondi insufficienti\00"
@str_9 = constant [9 x i8] c"Scelta: \00"
@str_10 = constant [3 x i8] c"%d\00"
@str_11 = constant [7 x i8] c"Saldo=\00"
@str_12 = constant [5 x i8] c"%.6f\00"
@str_13 = constant [19 x i8] c"Importo deposito: \00"
@str_14 = constant [4 x i8] c"%lf\00"
@str_15 = constant [13 x i8] c"Nuovo saldo=\00"
@str_16 = constant [19 x i8] c"Importo prelievo: \00"
@str_17 = constant [18 x i8] c"Scelta non valida\00"
@str_18 = constant [13 x i8] c"Arrivederci.\00"

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
declare noundef i32 @scanf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
define void @show_menu() local_unnamed_addr #0 {
entry:
  %putchar = tail call i32 @putchar(i32 10)
  %load_G_TITLE = load ptr, ptr @G_TITLE, align 8
  %.6 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr %load_G_TITLE)
  %putchar1 = tail call i32 @putchar(i32 10)
  %.12 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_3)
  %putchar2 = tail call i32 @putchar(i32 10)
  %.18 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_4)
  %putchar3 = tail call i32 @putchar(i32 10)
  %.24 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_5)
  %putchar4 = tail call i32 @putchar(i32 10)
  %.30 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_6)
  %putchar5 = tail call i32 @putchar(i32 10)
  ret void
}

; Function Attrs: mustprogress nofree norecurse nosync nounwind willreturn memory(none)
define double @deposit(double %dp_bal, double %dp_amt) local_unnamed_addr #1 {
entry:
  %.6 = fadd double %dp_bal, %dp_amt
  ret double %.6
}

; Function Attrs: nofree nounwind
define double @withdraw(double %wd_bal, double %wd_amt) local_unnamed_addr #0 {
entry:
  %.6 = fcmp ugt double %wd_amt, 0.000000e+00
  br i1 %.6, label %next_branch, label %if_then

common.ret:                                       ; preds = %elif_0_next, %elif_0_then, %if_then
  %common.ret.op = phi double [ %wd_bal, %if_then ], [ %wd_bal, %elif_0_then ], [ %.23, %elif_0_next ]
  ret double %common.ret.op

if_then:                                          ; preds = %entry
  %.9 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_7)
  %putchar1 = tail call i32 @putchar(i32 10)
  br label %common.ret

next_branch:                                      ; preds = %entry
  %.14 = fcmp ogt double %wd_amt, %wd_bal
  br i1 %.14, label %elif_0_then, label %elif_0_next

elif_0_then:                                      ; preds = %next_branch
  %.18 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_8)
  %putchar = tail call i32 @putchar(i32 10)
  br label %common.ret

elif_0_next:                                      ; preds = %next_branch
  %.23 = fsub double %wd_bal, %wd_amt
  br label %common.ret
}

; Function Attrs: nofree nounwind
define void @main() local_unnamed_addr #0 {
entry:
  %m_amount = alloca double, align 8
  store double 0.000000e+00, ptr %m_amount, align 8
  %m_choice = alloca i32, align 4
  store i32 0, ptr %m_choice, align 4
  %load_G_START_BAL = load double, ptr @G_START_BAL, align 8
  br label %while_body

while_body:                                       ; preds = %if_merge, %entry
  %m_balance.06 = phi double [ %load_G_START_BAL, %entry ], [ %m_balance.1, %if_merge ]
  call void @show_menu()
  %.13 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_9)
  %.15 = call i32 (ptr, ...) @scanf(ptr nonnull @str_10, ptr nonnull %m_choice)
  %load_m_choice = load i32, ptr %m_choice, align 4
  switch i32 %load_m_choice, label %elif_2_next [
    i32 1, label %if_then
    i32 2, label %elif_0_then
    i32 3, label %elif_1_then
    i32 0, label %while_end
  ]

while_end:                                        ; preds = %while_body
  %.77 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_18)
  %putchar = call i32 @putchar(i32 10)
  ret void

if_then:                                          ; preds = %while_body
  %.19 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_11)
  %.21 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_12, double %m_balance.06)
  br label %if_merge

elif_0_then:                                      ; preds = %while_body
  %.29 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_13)
  %.31 = call i32 (ptr, ...) @scanf(ptr nonnull @str_14, ptr nonnull %m_amount)
  %load_m_amount = load double, ptr %m_amount, align 8
  %.6.i = fadd double %m_balance.06, %load_m_amount
  %.36 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_15)
  %.38 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_12, double %.6.i)
  br label %if_merge

elif_1_then:                                      ; preds = %while_body
  %.46 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_16)
  %.48 = call i32 (ptr, ...) @scanf(ptr nonnull @str_14, ptr nonnull %m_amount)
  %load_m_amount.1 = load double, ptr %m_amount, align 8
  %.6.i5 = fcmp ugt double %load_m_amount.1, 0.000000e+00
  br i1 %.6.i5, label %next_branch.i, label %if_then.i

if_then.i:                                        ; preds = %elif_1_then
  %.9.i = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_7)
  %putchar1.i = call i32 @putchar(i32 10)
  br label %withdraw.exit

next_branch.i:                                    ; preds = %elif_1_then
  %.14.i = fcmp ogt double %load_m_amount.1, %m_balance.06
  br i1 %.14.i, label %elif_0_then.i, label %elif_0_next.i

elif_0_then.i:                                    ; preds = %next_branch.i
  %.18.i = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_8)
  %putchar.i = call i32 @putchar(i32 10)
  br label %withdraw.exit

elif_0_next.i:                                    ; preds = %next_branch.i
  %.23.i = fsub double %m_balance.06, %load_m_amount.1
  br label %withdraw.exit

withdraw.exit:                                    ; preds = %if_then.i, %elif_0_then.i, %elif_0_next.i
  %common.ret.op.i = phi double [ %m_balance.06, %if_then.i ], [ %m_balance.06, %elif_0_then.i ], [ %.23.i, %elif_0_next.i ]
  %.53 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_15)
  %.55 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_12, double %common.ret.op.i)
  br label %if_merge

elif_2_next:                                      ; preds = %while_body
  %.64 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_17)
  br label %if_merge

if_merge:                                         ; preds = %elif_2_next, %withdraw.exit, %elif_0_then, %if_then
  %m_balance.1 = phi double [ %m_balance.06, %if_then ], [ %.6.i, %elif_0_then ], [ %common.ret.op.i, %withdraw.exit ], [ %m_balance.06, %elif_2_next ]
  %putchar1 = call i32 @putchar(i32 10)
  br label %while_body
}

; Function Attrs: nofree nounwind
declare noundef i32 @putchar(i32 noundef) local_unnamed_addr #0

attributes #0 = { nofree nounwind }
attributes #1 = { mustprogress nofree norecurse nosync nounwind willreturn memory(none) }
