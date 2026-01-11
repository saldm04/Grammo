; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@str_0 = constant [19 x i8] c"Interessi composti\00"
@G_TITLE = local_unnamed_addr global ptr @str_0
@str_1 = constant [3 x i8] c"%s\00"
@str_2 = local_unnamed_addr constant [2 x i8] c"\0A\00"
@str_3 = constant [27 x i8] c"Capitale iniziale (real): \00"
@str_4 = constant [4 x i8] c"%lf\00"
@str_5 = constant [23 x i8] c"Tasso annuo % (real): \00"
@str_6 = constant [18 x i8] c"Anni (int >= 0): \00"
@str_7 = constant [3 x i8] c"%d\00"
@str_8 = constant [30 x i8] c"Errore: anni deve essere >= 0\00"
@str_9 = constant [29 x i8] c"Tasso nullo: saldo costante.\00"
@str_10 = constant [6 x i8] c"Anno \00"
@str_11 = constant [8 x i8] c" saldo=\00"
@str_12 = constant [5 x i8] c"%.6f\00"
@str_13 = constant [14 x i8] c"Saldo finale=\00"

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
declare noundef i32 @scanf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: mustprogress nofree norecurse nosync nounwind willreturn memory(none)
define double @apply_interest(double %ai_balance, double %ai_rate_percent) local_unnamed_addr #1 {
entry:
  %.6 = fdiv double %ai_rate_percent, 1.000000e+02
  %.7 = fadd double %.6, 1.000000e+00
  %.8 = fmul double %ai_balance, %.7
  ret double %.8
}

; Function Attrs: nofree nounwind
define void @main() local_unnamed_addr #0 {
entry:
  %m_principal = alloca double, align 8
  store double 0.000000e+00, ptr %m_principal, align 8
  %m_rate = alloca double, align 8
  store double 0.000000e+00, ptr %m_rate, align 8
  %m_years = alloca i32, align 4
  store i32 0, ptr %m_years, align 4
  %load_G_TITLE = load ptr, ptr @G_TITLE, align 8
  %.8 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr %load_G_TITLE)
  %putchar = tail call i32 @putchar(i32 10)
  %.14 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_3)
  %.16 = call i32 (ptr, ...) @scanf(ptr nonnull @str_4, ptr nonnull %m_principal)
  %.19 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_5)
  %.21 = call i32 (ptr, ...) @scanf(ptr nonnull @str_4, ptr nonnull %m_rate)
  %.24 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_6)
  %.26 = call i32 (ptr, ...) @scanf(ptr nonnull @str_7, ptr nonnull %m_years)
  %load_m_years = load i32, ptr %m_years, align 4
  %.27 = icmp slt i32 %load_m_years, 0
  br i1 %.27, label %if_then, label %next_branch

common.ret:                                       ; preds = %for_end, %if_then
  %putchar4 = call i32 @putchar(i32 10)
  ret void

if_then:                                          ; preds = %entry
  %.30 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_8)
  br label %common.ret

next_branch:                                      ; preds = %entry
  %load_m_principal = load double, ptr %m_principal, align 8
  %load_m_rate = load double, ptr %m_rate, align 8
  %.36 = fcmp oeq double %load_m_rate, 0.000000e+00
  br i1 %.36, label %if_then.1, label %if_merge

if_then.1:                                        ; preds = %next_branch
  %.39 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_9)
  %putchar3 = call i32 @putchar(i32 10)
  %load_m_years.17.pre = load i32, ptr %m_years, align 4
  br label %if_merge

if_merge:                                         ; preds = %if_then.1, %next_branch
  %load_m_years.17 = phi i32 [ %load_m_years.17.pre, %if_then.1 ], [ %load_m_years, %next_branch ]
  %.47.not8 = icmp slt i32 %load_m_years.17, 1
  br i1 %.47.not8, label %for_end, label %for_body

for_body:                                         ; preds = %if_merge, %for_body
  %m_y.010 = phi i32 [ %.64, %for_body ], [ 1, %if_merge ]
  %m_balance.09 = phi double [ %.8.i, %for_body ], [ %load_m_principal, %if_merge ]
  %load_m_rate.1 = load double, ptr %m_rate, align 8
  %.6.i = fdiv double %load_m_rate.1, 1.000000e+02
  %.7.i = fadd double %.6.i, 1.000000e+00
  %.8.i = fmul double %m_balance.09, %.7.i
  %.53 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_10)
  %.55 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_7, i32 %m_y.010)
  %.58 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_11)
  %.60 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_12, double %.8.i)
  %putchar5 = call i32 @putchar(i32 10)
  %.64 = add i32 %m_y.010, 1
  %load_m_years.1 = load i32, ptr %m_years, align 4
  %.47.not = icmp sgt i32 %.64, %load_m_years.1
  br i1 %.47.not, label %for_end, label %for_body

for_end:                                          ; preds = %for_body, %if_merge
  %m_balance.0.lcssa = phi double [ %load_m_principal, %if_merge ], [ %.8.i, %for_body ]
  %.69 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_13)
  %.71 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_12, double %m_balance.0.lcssa)
  br label %common.ret
}

; Function Attrs: nofree nounwind
declare noundef i32 @putchar(i32 noundef) local_unnamed_addr #0

attributes #0 = { nofree nounwind }
attributes #1 = { mustprogress nofree norecurse nosync nounwind willreturn memory(none) }
