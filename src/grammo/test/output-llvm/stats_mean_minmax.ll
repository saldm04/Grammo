; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@str_0 = constant [27 x i8] c"Statistiche: media/min/max\00"
@str_1 = constant [3 x i8] c"%s\00"
@str_2 = local_unnamed_addr constant [2 x i8] c"\0A\00"
@str_3 = constant [26 x i8] c"Quanti valori (int > 0)? \00"
@str_4 = constant [3 x i8] c"%d\00"
@str_5 = constant [26 x i8] c"Errore: n deve essere > 0\00"
@str_6 = constant [18 x i8] c"Valore 1 (real): \00"
@str_7 = constant [4 x i8] c"%lf\00"
@str_8 = constant [16 x i8] c"Valore (real): \00"
@str_9 = constant [7 x i8] c"Somma=\00"
@str_10 = constant [5 x i8] c"%.6f\00"
@str_11 = constant [7 x i8] c"Media=\00"
@str_12 = constant [5 x i8] c"Min=\00"
@str_13 = constant [7 x i8] c"  Max=\00"

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
declare noundef i32 @scanf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
define void @main() local_unnamed_addr #0 {
entry:
  %m_n = alloca i32, align 4
  store i32 0, ptr %m_n, align 4
  %m_x = alloca double, align 8
  store double 0.000000e+00, ptr %m_x, align 8
  %.11 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_0)
  %putchar = tail call i32 @putchar(i32 10)
  %.17 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_3)
  %.19 = call i32 (ptr, ...) @scanf(ptr nonnull @str_4, ptr nonnull %m_n)
  %load_m_n = load i32, ptr %m_n, align 4
  %.20 = icmp slt i32 %load_m_n, 1
  br i1 %.20, label %if_then, label %next_branch

common.ret:                                       ; preds = %for_end, %if_then
  %putchar4 = call i32 @putchar(i32 10)
  ret void

if_then:                                          ; preds = %entry
  %.23 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_5)
  br label %common.ret

next_branch:                                      ; preds = %entry
  %.30 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_6)
  %.32 = call i32 (ptr, ...) @scanf(ptr nonnull @str_7, ptr nonnull %m_x)
  %load_m_x = load double, ptr %m_x, align 8
  %load_m_n.16 = load i32, ptr %m_n, align 4
  %.38.not7 = icmp slt i32 %load_m_n.16, 2
  br i1 %.38.not7, label %for_end, label %for_body

for_body:                                         ; preds = %next_branch, %for_body
  %m_maxv.011 = phi double [ %m_maxv.1, %for_body ], [ %load_m_x, %next_branch ]
  %m_minv.010 = phi double [ %m_minv.1, %for_body ], [ %load_m_x, %next_branch ]
  %m_sum.09 = phi double [ %.45, %for_body ], [ %load_m_x, %next_branch ]
  %m_i.08 = phi i32 [ %.55, %for_body ], [ 2, %next_branch ]
  %.42 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_8)
  %.44 = call i32 (ptr, ...) @scanf(ptr nonnull @str_7, ptr nonnull %m_x)
  %load_m_x.3 = load double, ptr %m_x, align 8
  %.45 = fadd double %m_sum.09, %load_m_x.3
  %.47 = fcmp olt double %load_m_x.3, %m_minv.010
  %m_minv.1 = select i1 %.47, double %load_m_x.3, double %m_minv.010
  %.51 = fcmp ogt double %load_m_x.3, %m_maxv.011
  %m_maxv.1 = select i1 %.51, double %load_m_x.3, double %m_maxv.011
  %.55 = add i32 %m_i.08, 1
  %load_m_n.1 = load i32, ptr %m_n, align 4
  %.38.not = icmp sgt i32 %.55, %load_m_n.1
  br i1 %.38.not, label %for_end, label %for_body

for_end:                                          ; preds = %for_body, %next_branch
  %m_sum.0.lcssa = phi double [ %load_m_x, %next_branch ], [ %.45, %for_body ]
  %m_minv.0.lcssa = phi double [ %load_m_x, %next_branch ], [ %m_minv.1, %for_body ]
  %m_maxv.0.lcssa = phi double [ %load_m_x, %next_branch ], [ %m_maxv.1, %for_body ]
  %load_m_n.1.lcssa = phi i32 [ %load_m_n.16, %next_branch ], [ %load_m_n.1, %for_body ]
  %.58 = sitofp i32 %load_m_n.1.lcssa to double
  %.60 = fdiv double %m_sum.0.lcssa, %.58
  %.64 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_9)
  %.66 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_10, double %m_sum.0.lcssa)
  %putchar2 = call i32 @putchar(i32 10)
  %.72 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_11)
  %.74 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_10, double %.60)
  %putchar3 = call i32 @putchar(i32 10)
  %.80 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_12)
  %.82 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_10, double %m_minv.0.lcssa)
  %.85 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_13)
  %.87 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_10, double %m_maxv.0.lcssa)
  br label %common.ret
}

; Function Attrs: nofree nounwind
declare noundef i32 @putchar(i32 noundef) local_unnamed_addr #0

attributes #0 = { nofree nounwind }
