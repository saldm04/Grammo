; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@str_0 = constant [36 x i8] c"Demo numeri: primalita' e MCD (gcd)\00"
@str_1 = constant [3 x i8] c"%s\00"
@str_2 = local_unnamed_addr constant [2 x i8] c"\0A\00"
@str_3 = constant [44 x i8] c"Numero per primalita' (int >= 0, piccolo): \00"
@str_4 = constant [3 x i8] c"%d\00"
@str_5 = constant [20 x i8] c"Il numero e' primo.\00"
@str_6 = constant [24 x i8] c"Il numero NON e' primo.\00"
@str_7 = constant [10 x i8] c"A (int): \00"
@str_8 = constant [10 x i8] c"B (int): \00"
@str_9 = constant [10 x i8] c"gcd(A,B)=\00"

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
declare noundef i32 @scanf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree norecurse nosync nounwind memory(none)
define i1 @divisible(i32 %dv_n, i32 %dv_d) local_unnamed_addr #1 {
entry:
  %.7 = icmp slt i32 %dv_d, 1
  br i1 %.7, label %common.ret, label %if_merge

common.ret:                                       ; preds = %while_end, %entry
  %common.ret.op = phi i1 [ false, %entry ], [ %.22, %while_end ]
  ret i1 %common.ret.op

if_merge:                                         ; preds = %entry
  %spec.select = tail call i32 @llvm.abs.i32(i32 %dv_n, i1 false)
  br label %while_cond

while_cond:                                       ; preds = %while_cond, %if_merge
  %dv_t.1 = phi i32 [ %spec.select, %if_merge ], [ %.19, %while_cond ]
  %.17 = icmp sgt i32 %dv_t.1, 0
  %.19 = sub nsw i32 %dv_t.1, %dv_d
  br i1 %.17, label %while_cond, label %while_end

while_end:                                        ; preds = %while_cond
  %.22 = icmp eq i32 %dv_t.1, 0
  br label %common.ret
}

; Function Attrs: nofree norecurse nosync nounwind memory(none)
define noundef i1 @is_prime(i32 %pr_n) local_unnamed_addr #1 {
entry:
  %.5 = icmp slt i32 %pr_n, 2
  br i1 %.5, label %common.ret, label %while_cond.preheader

while_cond.preheader:                             ; preds = %entry
  %.11.not7 = icmp samesign ult i32 %pr_n, 4
  br i1 %.11.not7, label %common.ret, label %while_body

common.ret:                                       ; preds = %if_merge.1, %divisible.exit, %while_cond.preheader, %entry
  %common.ret.op = phi i1 [ false, %entry ], [ true, %while_cond.preheader ], [ true, %if_merge.1 ], [ false, %divisible.exit ]
  ret i1 %common.ret.op

while_body:                                       ; preds = %while_cond.preheader, %if_merge.1
  %pr_d.08 = phi i32 [ %.16, %if_merge.1 ], [ 2, %while_cond.preheader ]
  %.7.i = icmp slt i32 %pr_d.08, 1
  br i1 %.7.i, label %if_merge.1, label %while_cond.i

while_cond.i:                                     ; preds = %while_body, %while_cond.i
  %dv_t.1.i = phi i32 [ %.19.i, %while_cond.i ], [ %pr_n, %while_body ]
  %.17.i = icmp sgt i32 %dv_t.1.i, 0
  %.19.i = sub nsw i32 %dv_t.1.i, %pr_d.08
  br i1 %.17.i, label %while_cond.i, label %divisible.exit

divisible.exit:                                   ; preds = %while_cond.i
  %.22.i = icmp eq i32 %dv_t.1.i, 0
  br i1 %.22.i, label %common.ret, label %if_merge.1

if_merge.1:                                       ; preds = %while_body, %divisible.exit
  %.16 = add i32 %pr_d.08, 1
  %.10 = mul i32 %.16, %.16
  %.11.not = icmp sgt i32 %.10, %pr_n
  br i1 %.11.not, label %common.ret, label %while_body
}

; Function Attrs: nofree norecurse nosync nounwind memory(none)
define i32 @gcd(i32 %gd_a, i32 %gd_b) local_unnamed_addr #1 {
entry:
  %gd_y.0 = tail call i32 @llvm.abs.i32(i32 %gd_b, i1 false)
  %.20 = icmp eq i32 %gd_a, 0
  br i1 %.20, label %common.ret, label %next_branch

common.ret:                                       ; preds = %while_body, %next_branch, %entry
  %common.ret.op = phi i32 [ %gd_y.0, %entry ], [ %spec.select, %next_branch ], [ %gd_x.2, %while_body ]
  ret i32 %common.ret.op

next_branch:                                      ; preds = %entry
  %spec.select = tail call i32 @llvm.abs.i32(i32 %gd_a, i1 false)
  %.22 = icmp eq i32 %gd_b, 0
  %.26.not16 = icmp eq i32 %spec.select, %gd_y.0
  %or.cond = or i1 %.22, %.26.not16
  br i1 %or.cond, label %common.ret, label %while_body

while_body:                                       ; preds = %next_branch, %while_body
  %gd_y.118 = phi i32 [ %gd_y.2, %while_body ], [ %gd_y.0, %next_branch ]
  %gd_x.117 = phi i32 [ %gd_x.2, %while_body ], [ %spec.select, %next_branch ]
  %.28 = icmp sgt i32 %gd_x.117, %gd_y.118
  %.29 = select i1 %.28, i32 %gd_y.118, i32 0
  %gd_x.2 = sub i32 %gd_x.117, %.29
  %.31 = select i1 %.28, i32 0, i32 %gd_x.117
  %gd_y.2 = sub i32 %gd_y.118, %.31
  %.26.not = icmp eq i32 %gd_x.2, %gd_y.2
  br i1 %.26.not, label %common.ret, label %while_body
}

; Function Attrs: nofree nounwind
define void @main() local_unnamed_addr #0 {
entry:
  %m_n = alloca i32, align 4
  store i32 0, ptr %m_n, align 4
  %m_a = alloca i32, align 4
  store i32 0, ptr %m_a, align 4
  %m_b = alloca i32, align 4
  store i32 0, ptr %m_b, align 4
  %.9 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_0)
  %putchar = tail call i32 @putchar(i32 10)
  %.15 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_3)
  %.17 = call i32 (ptr, ...) @scanf(ptr nonnull @str_4, ptr nonnull %m_n)
  %load_m_n = load i32, ptr %m_n, align 4
  %.5.i = icmp slt i32 %load_m_n, 2
  br i1 %.5.i, label %if_merge, label %while_cond.preheader.i

while_cond.preheader.i:                           ; preds = %entry
  %.11.not7.i = icmp samesign ult i32 %load_m_n, 4
  br i1 %.11.not7.i, label %if_merge, label %while_body.i

while_body.i:                                     ; preds = %while_cond.preheader.i, %if_merge.1.i
  %pr_d.08.i = phi i32 [ %.16.i, %if_merge.1.i ], [ 2, %while_cond.preheader.i ]
  %.7.i.i = icmp slt i32 %pr_d.08.i, 1
  br i1 %.7.i.i, label %if_merge.1.i, label %while_cond.i.i

while_cond.i.i:                                   ; preds = %while_body.i, %while_cond.i.i
  %dv_t.1.i.i = phi i32 [ %.19.i.i, %while_cond.i.i ], [ %load_m_n, %while_body.i ]
  %.17.i.i = icmp sgt i32 %dv_t.1.i.i, 0
  %.19.i.i = sub nsw i32 %dv_t.1.i.i, %pr_d.08.i
  br i1 %.17.i.i, label %while_cond.i.i, label %divisible.exit.i

divisible.exit.i:                                 ; preds = %while_cond.i.i
  %.22.i.i = icmp eq i32 %dv_t.1.i.i, 0
  br i1 %.22.i.i, label %if_merge, label %if_merge.1.i

if_merge.1.i:                                     ; preds = %divisible.exit.i, %while_body.i
  %.16.i = add i32 %pr_d.08.i, 1
  %.10.i = mul i32 %.16.i, %.16.i
  %.11.not.i = icmp sgt i32 %.10.i, %load_m_n
  br i1 %.11.not.i, label %if_merge, label %while_body.i

if_merge:                                         ; preds = %divisible.exit.i, %if_merge.1.i, %entry, %while_cond.preheader.i
  %str_6.sink = phi ptr [ @str_5, %while_cond.preheader.i ], [ @str_6, %entry ], [ @str_5, %if_merge.1.i ], [ @str_6, %divisible.exit.i ]
  %.28 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull %str_6.sink)
  %putchar1 = call i32 @putchar(i32 10)
  %.37 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_7)
  %.39 = call i32 (ptr, ...) @scanf(ptr nonnull @str_4, ptr nonnull %m_a)
  %.42 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_8)
  %.44 = call i32 (ptr, ...) @scanf(ptr nonnull @str_4, ptr nonnull %m_b)
  %load_m_a = load i32, ptr %m_a, align 4
  %load_m_b = load i32, ptr %m_b, align 4
  %gd_y.0.i = call i32 @llvm.abs.i32(i32 %load_m_b, i1 false)
  %.20.i = icmp eq i32 %load_m_a, 0
  br i1 %.20.i, label %gcd.exit, label %next_branch.i

next_branch.i:                                    ; preds = %if_merge
  %spec.select.i = call i32 @llvm.abs.i32(i32 %load_m_a, i1 false)
  %.22.i = icmp eq i32 %load_m_b, 0
  %.26.not16.i = icmp eq i32 %spec.select.i, %gd_y.0.i
  %or.cond.i = or i1 %.22.i, %.26.not16.i
  br i1 %or.cond.i, label %gcd.exit, label %while_body.i4

while_body.i4:                                    ; preds = %next_branch.i, %while_body.i4
  %gd_y.118.i = phi i32 [ %gd_y.2.i, %while_body.i4 ], [ %gd_y.0.i, %next_branch.i ]
  %gd_x.117.i = phi i32 [ %gd_x.2.i, %while_body.i4 ], [ %spec.select.i, %next_branch.i ]
  %.28.i = icmp sgt i32 %gd_x.117.i, %gd_y.118.i
  %.29.i = select i1 %.28.i, i32 %gd_y.118.i, i32 0
  %gd_x.2.i = sub i32 %gd_x.117.i, %.29.i
  %.31.i = select i1 %.28.i, i32 0, i32 %gd_x.117.i
  %gd_y.2.i = sub i32 %gd_y.118.i, %.31.i
  %.26.not.i = icmp eq i32 %gd_x.2.i, %gd_y.2.i
  br i1 %.26.not.i, label %gcd.exit, label %while_body.i4

gcd.exit:                                         ; preds = %while_body.i4, %if_merge, %next_branch.i
  %common.ret.op.i5 = phi i32 [ %gd_y.0.i, %if_merge ], [ %spec.select.i, %next_branch.i ], [ %gd_x.2.i, %while_body.i4 ]
  %.49 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_9)
  %.51 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_4, i32 %common.ret.op.i5)
  %putchar3 = call i32 @putchar(i32 10)
  ret void
}

; Function Attrs: nofree nounwind
declare noundef i32 @putchar(i32 noundef) local_unnamed_addr #0

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.abs.i32(i32, i1 immarg) #2

attributes #0 = { nofree nounwind }
attributes #1 = { nofree norecurse nosync nounwind memory(none) }
attributes #2 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
