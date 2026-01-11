; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@str_0 = constant [14 x i8] c"Inserisci n: \00"
@str_1 = constant [3 x i8] c"%s\00"
@str_2 = constant [3 x i8] c"%d\00"
@str_3 = constant [8 x i8] c"fib(n)=\00"
@str_4 = local_unnamed_addr constant [2 x i8] c"\0A\00"

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
declare noundef i32 @scanf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree norecurse nosync nounwind memory(none)
define i32 @fib(i32 %n) local_unnamed_addr #1 {
entry:
  %.8 = icmp slt i32 %n, 1
  br i1 %.8, label %common.ret, label %next_branch

common.ret:                                       ; preds = %while_body, %next_branch, %entry
  %common.ret.op = phi i32 [ 0, %entry ], [ 1, %next_branch ], [ %.19, %while_body ]
  ret i32 %common.ret.op

next_branch:                                      ; preds = %entry
  %.17.not6 = icmp eq i32 %n, 1
  br i1 %.17.not6, label %common.ret, label %while_body

while_body:                                       ; preds = %next_branch, %while_body
  %i.09 = phi i32 [ %.23, %while_body ], [ 2, %next_branch ]
  %b.08 = phi i32 [ %.19, %while_body ], [ 1, %next_branch ]
  %a.07 = phi i32 [ %b.08, %while_body ], [ 0, %next_branch ]
  %.19 = add i32 %b.08, %a.07
  %.23 = add i32 %i.09, 1
  %.17.not = icmp sgt i32 %.23, %n
  br i1 %.17.not, label %common.ret, label %while_body
}

; Function Attrs: nofree nounwind
define void @main() local_unnamed_addr #0 {
entry:
  %n = alloca i32, align 4
  store i32 0, ptr %n, align 4
  %.6 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_0)
  %.8 = call i32 (ptr, ...) @scanf(ptr nonnull @str_2, ptr nonnull %n)
  %load_n = load i32, ptr %n, align 4
  %.8.i = icmp slt i32 %load_n, 1
  br i1 %.8.i, label %fib.exit, label %next_branch.i

next_branch.i:                                    ; preds = %entry
  %.17.not6.i = icmp eq i32 %load_n, 1
  br i1 %.17.not6.i, label %fib.exit, label %while_body.i

while_body.i:                                     ; preds = %next_branch.i, %while_body.i
  %i.09.i = phi i32 [ %.23.i, %while_body.i ], [ 2, %next_branch.i ]
  %b.08.i = phi i32 [ %.19.i, %while_body.i ], [ 1, %next_branch.i ]
  %a.07.i = phi i32 [ %b.08.i, %while_body.i ], [ 0, %next_branch.i ]
  %.19.i = add i32 %a.07.i, %b.08.i
  %.23.i = add i32 %i.09.i, 1
  %.17.not.i = icmp sgt i32 %.23.i, %load_n
  br i1 %.17.not.i, label %fib.exit, label %while_body.i

fib.exit:                                         ; preds = %while_body.i, %entry, %next_branch.i
  %common.ret.op.i = phi i32 [ 0, %entry ], [ 1, %next_branch.i ], [ %.19.i, %while_body.i ]
  %.13 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_1, ptr nonnull @str_3)
  %.15 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, i32 %common.ret.op.i)
  %putchar = call i32 @putchar(i32 10)
  ret void
}

; Function Attrs: nofree nounwind
declare noundef i32 @putchar(i32 noundef) local_unnamed_addr #0

attributes #0 = { nofree nounwind }
attributes #1 = { nofree norecurse nosync nounwind memory(none) }
