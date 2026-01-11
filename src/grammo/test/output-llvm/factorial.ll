; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@str_0 = constant [14 x i8] c"Inserisci n: \00"
@str_1 = constant [3 x i8] c"%s\00"
@str_2 = constant [3 x i8] c"%d\00"
@str_3 = constant [9 x i8] c"fact(n)=\00"
@str_4 = local_unnamed_addr constant [2 x i8] c"\0A\00"

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
declare noundef i32 @scanf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree norecurse nosync nounwind memory(none)
define i32 @fact(i32 %n) local_unnamed_addr #1 {
entry:
  %.6 = icmp slt i32 %n, 0
  br i1 %.6, label %common.ret, label %for_cond.preheader

for_cond.preheader:                               ; preds = %entry
  %.11.not5 = icmp eq i32 %n, 0
  br i1 %.11.not5, label %common.ret, label %for_body.preheader

for_body.preheader:                               ; preds = %for_cond.preheader
  %min.iters.check = icmp ult i32 %n, 20
  br i1 %min.iters.check, label %for_body.preheader9, label %vector.scevcheck

vector.scevcheck:                                 ; preds = %for_body.preheader
  %0 = zext nneg i32 %n to i64
  %1 = add nsw i64 %0, -1
  %2 = trunc nsw i64 %1 to i32
  %3 = icmp ugt i32 %2, 2147483645
  %4 = icmp ugt i64 %1, 4294967295
  %5 = or i1 %3, %4
  br i1 %5, label %for_body.preheader9, label %vector.ph

vector.ph:                                        ; preds = %vector.scevcheck
  %n.vec = and i32 %n, 2147483640
  %6 = or disjoint i32 %n.vec, 1
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i32 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %vec.phi = phi <4 x i32> [ splat (i32 1), %vector.ph ], [ %7, %vector.body ]
  %vec.phi8 = phi <4 x i32> [ splat (i32 1), %vector.ph ], [ %8, %vector.body ]
  %vec.ind = phi <4 x i32> [ <i32 1, i32 2, i32 3, i32 4>, %vector.ph ], [ %vec.ind.next, %vector.body ]
  %step.add = add <4 x i32> %vec.ind, splat (i32 4)
  %7 = mul <4 x i32> %vec.phi, %vec.ind
  %8 = mul <4 x i32> %vec.phi8, %step.add
  %index.next = add nuw i32 %index, 8
  %vec.ind.next = add <4 x i32> %vec.ind, splat (i32 8)
  %9 = icmp eq i32 %index.next, %n.vec
  br i1 %9, label %middle.block, label %vector.body, !llvm.loop !0

middle.block:                                     ; preds = %vector.body
  %bin.rdx = mul <4 x i32> %8, %7
  %10 = tail call i32 @llvm.vector.reduce.mul.v4i32(<4 x i32> %bin.rdx)
  %cmp.n = icmp eq i32 %n, %n.vec
  br i1 %cmp.n, label %common.ret, label %for_body.preheader9

for_body.preheader9:                              ; preds = %vector.scevcheck, %for_body.preheader, %middle.block
  %r.07.ph = phi i32 [ 1, %for_body.preheader ], [ 1, %vector.scevcheck ], [ %10, %middle.block ]
  %i.06.ph = phi i32 [ 1, %for_body.preheader ], [ 1, %vector.scevcheck ], [ %6, %middle.block ]
  br label %for_body

common.ret:                                       ; preds = %for_body, %middle.block, %for_cond.preheader, %entry
  %common.ret.op = phi i32 [ 0, %entry ], [ 1, %for_cond.preheader ], [ %10, %middle.block ], [ %.13, %for_body ]
  ret i32 %common.ret.op

for_body:                                         ; preds = %for_body.preheader9, %for_body
  %r.07 = phi i32 [ %.13, %for_body ], [ %r.07.ph, %for_body.preheader9 ]
  %i.06 = phi i32 [ %.15, %for_body ], [ %i.06.ph, %for_body.preheader9 ]
  %.13 = mul i32 %r.07, %i.06
  %.15 = add i32 %i.06, 1
  %.11.not = icmp sgt i32 %.15, %n
  br i1 %.11.not, label %common.ret, label %for_body, !llvm.loop !3
}

; Function Attrs: nofree nounwind
define void @main() local_unnamed_addr #0 {
entry:
  %n = alloca i32, align 4
  store i32 0, ptr %n, align 4
  %.6 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_0)
  %.8 = call i32 (ptr, ...) @scanf(ptr nonnull @str_2, ptr nonnull %n)
  %load_n = load i32, ptr %n, align 4
  %.6.i = icmp slt i32 %load_n, 0
  br i1 %.6.i, label %fact.exit, label %for_cond.preheader.i

for_cond.preheader.i:                             ; preds = %entry
  %.11.not5.i = icmp eq i32 %load_n, 0
  br i1 %.11.not5.i, label %fact.exit, label %for_body.i.preheader

for_body.i.preheader:                             ; preds = %for_cond.preheader.i
  %min.iters.check = icmp ult i32 %load_n, 20
  br i1 %min.iters.check, label %for_body.i.preheader2, label %vector.scevcheck

vector.scevcheck:                                 ; preds = %for_body.i.preheader
  %0 = zext nneg i32 %load_n to i64
  %1 = add nsw i64 %0, -1
  %2 = trunc nsw i64 %1 to i32
  %3 = icmp ugt i32 %2, 2147483645
  %4 = icmp ugt i64 %1, 4294967295
  %5 = or i1 %3, %4
  br i1 %5, label %for_body.i.preheader2, label %vector.ph

vector.ph:                                        ; preds = %vector.scevcheck
  %n.vec = and i32 %load_n, 2147483640
  %6 = or disjoint i32 %n.vec, 1
  br label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.ph
  %index = phi i32 [ 0, %vector.ph ], [ %index.next, %vector.body ]
  %vec.phi = phi <4 x i32> [ splat (i32 1), %vector.ph ], [ %7, %vector.body ]
  %vec.phi1 = phi <4 x i32> [ splat (i32 1), %vector.ph ], [ %8, %vector.body ]
  %vec.ind = phi <4 x i32> [ <i32 1, i32 2, i32 3, i32 4>, %vector.ph ], [ %vec.ind.next, %vector.body ]
  %step.add = add <4 x i32> %vec.ind, splat (i32 4)
  %7 = mul <4 x i32> %vec.ind, %vec.phi
  %8 = mul <4 x i32> %step.add, %vec.phi1
  %index.next = add nuw i32 %index, 8
  %vec.ind.next = add <4 x i32> %vec.ind, splat (i32 8)
  %9 = icmp eq i32 %index.next, %n.vec
  br i1 %9, label %middle.block, label %vector.body, !llvm.loop !4

middle.block:                                     ; preds = %vector.body
  %bin.rdx = mul <4 x i32> %8, %7
  %10 = call i32 @llvm.vector.reduce.mul.v4i32(<4 x i32> %bin.rdx)
  %cmp.n = icmp eq i32 %load_n, %n.vec
  br i1 %cmp.n, label %fact.exit, label %for_body.i.preheader2

for_body.i.preheader2:                            ; preds = %vector.scevcheck, %for_body.i.preheader, %middle.block
  %r.07.i.ph = phi i32 [ 1, %for_body.i.preheader ], [ 1, %vector.scevcheck ], [ %10, %middle.block ]
  %i.06.i.ph = phi i32 [ 1, %for_body.i.preheader ], [ 1, %vector.scevcheck ], [ %6, %middle.block ]
  br label %for_body.i

for_body.i:                                       ; preds = %for_body.i.preheader2, %for_body.i
  %r.07.i = phi i32 [ %.13.i, %for_body.i ], [ %r.07.i.ph, %for_body.i.preheader2 ]
  %i.06.i = phi i32 [ %.15.i, %for_body.i ], [ %i.06.i.ph, %for_body.i.preheader2 ]
  %.13.i = mul i32 %i.06.i, %r.07.i
  %.15.i = add i32 %i.06.i, 1
  %.11.not.i = icmp sgt i32 %.15.i, %load_n
  br i1 %.11.not.i, label %fact.exit, label %for_body.i, !llvm.loop !5

fact.exit:                                        ; preds = %for_body.i, %middle.block, %entry, %for_cond.preheader.i
  %common.ret.op.i = phi i32 [ 0, %entry ], [ 1, %for_cond.preheader.i ], [ %10, %middle.block ], [ %.13.i, %for_body.i ]
  %.13 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_3)
  %.15 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, i32 %common.ret.op.i)
  %putchar = call i32 @putchar(i32 10)
  ret void
}

; Function Attrs: nofree nounwind
declare noundef i32 @putchar(i32 noundef) local_unnamed_addr #0

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare i32 @llvm.vector.reduce.mul.v4i32(<4 x i32>) #2

attributes #0 = { nofree nounwind }
attributes #1 = { nofree norecurse nosync nounwind memory(none) }
attributes #2 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }

!0 = distinct !{!0, !1, !2}
!1 = !{!"llvm.loop.isvectorized", i32 1}
!2 = !{!"llvm.loop.unroll.runtime.disable"}
!3 = distinct !{!3, !1}
!4 = distinct !{!4, !1, !2}
!5 = distinct !{!5, !1}
