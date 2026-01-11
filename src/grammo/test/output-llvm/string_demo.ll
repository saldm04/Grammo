; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-pc-windows-msvc"

@str_0 = constant [1 x i8] zeroinitializer
@str_1 = constant [14 x i8] c"Demo stringhe\00"
@str_2 = constant [3 x i8] c"%s\00"
@str_3 = local_unnamed_addr constant [2 x i8] c"\0A\00"
@str_4 = constant [7 x i8] c"Nome: \00"
@str_5 = constant [6 x i8] c"%255s\00"
@str_6 = constant [24 x i8] c"Larghezza linea (int): \00"
@str_7 = constant [3 x i8] c"%d\00"
@str_8 = local_unnamed_addr constant [2 x i8] c"-\00"
@str_9 = local_unnamed_addr constant [2 x i8] c"[\00"
@str_10 = local_unnamed_addr constant [2 x i8] c"]\00"
@str_11 = local_unnamed_addr constant [6 x i8] c"Ciao \00"
@str_12 = local_unnamed_addr constant [2 x i8] c"!\00"
@str_13 = constant [7 x i8] c"Echo: \00"

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: nofree nounwind
declare noundef i32 @scanf(ptr nocapture noundef readonly, ...) local_unnamed_addr #0

; Function Attrs: mustprogress nofree nounwind willreturn memory(argmem: read)
declare i64 @strlen(ptr nocapture) local_unnamed_addr #1

; Function Attrs: mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite)
declare noalias noundef ptr @malloc(i64 noundef) local_unnamed_addr #2

; Function Attrs: mustprogress nofree nounwind willreturn memory(argmem: readwrite)
declare ptr @strcpy(ptr noalias returned writeonly, ptr noalias nocapture readonly) local_unnamed_addr #3

; Function Attrs: mustprogress nofree nounwind willreturn memory(argmem: readwrite)
declare ptr @strcat(ptr noalias returned, ptr noalias nocapture readonly) local_unnamed_addr #3

; Function Attrs: nofree nounwind
define noundef ptr @repeat(ptr nocapture readonly %rp_s, i32 %rp_n) local_unnamed_addr #0 {
entry:
  %.122 = icmp sgt i32 %rp_n, 0
  br i1 %.122, label %for_body, label %for_end

for_body:                                         ; preds = %entry, %for_body
  %rp_i.04 = phi i32 [ %.22, %for_body ], [ 0, %entry ]
  %rp_out.03 = phi ptr [ %.18, %for_body ], [ @str_0, %entry ]
  %.14 = tail call i64 @strlen(ptr noundef nonnull dereferenceable(1) %rp_out.03)
  %.15 = tail call i64 @strlen(ptr noundef nonnull dereferenceable(1) %rp_s)
  %.16 = add i64 %.14, 1
  %.17 = add i64 %.16, %.15
  %.18 = tail call ptr @malloc(i64 %.17)
  %.19 = tail call ptr @strcpy(ptr noundef nonnull dereferenceable(1) %.18, ptr noundef nonnull dereferenceable(1) %rp_out.03)
  %.20 = tail call ptr @strcat(ptr noundef nonnull dereferenceable(1) %.18, ptr noundef nonnull dereferenceable(1) %rp_s)
  %.22 = add nuw nsw i32 %rp_i.04, 1
  %.12 = icmp slt i32 %.22, %rp_n
  br i1 %.12, label %for_body, label %for_end

for_end:                                          ; preds = %for_body, %entry
  %rp_out.0.lcssa = phi ptr [ @str_0, %entry ], [ %.18, %for_body ]
  ret ptr %rp_out.0.lcssa
}

; Function Attrs: mustprogress nofree nounwind willreturn
define noundef ptr @surround(ptr nocapture readonly %sd_core, ptr nocapture readonly %sd_left, ptr nocapture readonly %sd_right) local_unnamed_addr #4 {
entry:
  %.8 = tail call i64 @strlen(ptr noundef nonnull dereferenceable(1) %sd_left)
  %.9 = tail call i64 @strlen(ptr noundef nonnull dereferenceable(1) %sd_core)
  %.10 = add i64 %.8, 1
  %.11 = add i64 %.10, %.9
  %.12 = tail call ptr @malloc(i64 %.11)
  %.13 = tail call ptr @strcpy(ptr noundef nonnull dereferenceable(1) %.12, ptr noundef nonnull dereferenceable(1) %sd_left)
  %.14 = tail call ptr @strcat(ptr noundef nonnull dereferenceable(1) %.12, ptr noundef nonnull dereferenceable(1) %sd_core)
  %.15 = tail call i64 @strlen(ptr noundef nonnull dereferenceable(1) %.12)
  %.16 = tail call i64 @strlen(ptr noundef nonnull dereferenceable(1) %sd_right)
  %.17 = add i64 %.15, 1
  %.18 = add i64 %.17, %.16
  %.19 = tail call ptr @malloc(i64 %.18)
  %.20 = tail call ptr @strcpy(ptr noundef nonnull dereferenceable(1) %.19, ptr noundef nonnull dereferenceable(1) %.12)
  %.21 = tail call ptr @strcat(ptr noundef nonnull dereferenceable(1) %.19, ptr noundef nonnull dereferenceable(1) %sd_right)
  ret ptr %.19
}

; Function Attrs: nofree nounwind
define void @main() local_unnamed_addr #0 {
entry:
  %m_width = alloca i32, align 4
  store i32 0, ptr %m_width, align 4
  %.9 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_1)
  %putchar = tail call i32 @putchar(i32 10)
  %.15 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_4)
  %.16 = tail call dereferenceable_or_null(256) ptr @malloc(i64 256)
  %.18 = tail call i32 (ptr, ...) @scanf(ptr nonnull @str_5, ptr %.16)
  %.22 = tail call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_6)
  %.24 = call i32 (ptr, ...) @scanf(ptr nonnull @str_7, ptr nonnull %m_width)
  %load_m_width = load i32, ptr %m_width, align 4
  %.122.i = icmp sgt i32 %load_m_width, 0
  br i1 %.122.i, label %for_body.i, label %repeat.exit

for_body.i:                                       ; preds = %entry, %for_body.i
  %rp_i.04.i = phi i32 [ %.22.i, %for_body.i ], [ 0, %entry ]
  %rp_out.03.i = phi ptr [ %.18.i, %for_body.i ], [ @str_0, %entry ]
  %.14.i = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %rp_out.03.i)
  %.17.i = add i64 %.14.i, 2
  %.18.i = call ptr @malloc(i64 %.17.i)
  %.19.i = call ptr @strcpy(ptr noundef nonnull dereferenceable(1) %.18.i, ptr noundef nonnull dereferenceable(1) %rp_out.03.i)
  %strlen27 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %.18.i)
  %endptr28 = getelementptr inbounds i8, ptr %.18.i, i64 %strlen27
  store i16 45, ptr %endptr28, align 1
  %.22.i = add nuw nsw i32 %rp_i.04.i, 1
  %.12.i = icmp slt i32 %.22.i, %load_m_width
  br i1 %.12.i, label %for_body.i, label %repeat.exit

repeat.exit:                                      ; preds = %for_body.i, %entry
  %rp_out.0.lcssa.i = phi ptr [ @str_0, %entry ], [ %.18.i, %for_body.i ]
  %.9.i = call i64 @strlen(ptr noundef nonnull readonly dereferenceable(1) %.16)
  %.11.i = add i64 %.9.i, 2
  %.12.i5 = call ptr @malloc(i64 %.11.i)
  store i16 91, ptr %.12.i5, align 1
  %.14.i6 = call ptr @strcat(ptr noundef nonnull dereferenceable(1) %.12.i5, ptr noundef nonnull readonly dereferenceable(1) %.16)
  %.15.i7 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %.12.i5)
  %.18.i10 = add i64 %.15.i7, 2
  %.19.i11 = call noundef ptr @malloc(i64 %.18.i10)
  %.20.i12 = call ptr @strcpy(ptr noundef nonnull dereferenceable(1) %.19.i11, ptr noundef nonnull dereferenceable(1) %.12.i5)
  %strlen29 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %.19.i11)
  %endptr30 = getelementptr inbounds i8, ptr %.19.i11, i64 %strlen29
  store i16 93, ptr %endptr30, align 1
  %.34 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %.19.i11)
  %.36 = add i64 %.34, 6
  %.37 = call ptr @malloc(i64 %.36)
  call void @llvm.memcpy.p0.p0.i64(ptr noundef nonnull align 1 dereferenceable(6) %.37, ptr noundef nonnull align 1 dereferenceable(6) @str_11, i64 6, i1 false)
  %.39 = call ptr @strcat(ptr noundef nonnull dereferenceable(1) %.37, ptr noundef nonnull dereferenceable(1) %.19.i11)
  %.41 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %.37)
  %.44 = add i64 %.41, 2
  %.45 = call ptr @malloc(i64 %.44)
  %.46 = call ptr @strcpy(ptr noundef nonnull dereferenceable(1) %.45, ptr noundef nonnull dereferenceable(1) %.37)
  %strlen = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %.45)
  %endptr = getelementptr inbounds i8, ptr %.45, i64 %strlen
  store i16 33, ptr %endptr, align 1
  %.50 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull %rp_out.0.lcssa.i)
  %putchar1 = call i32 @putchar(i32 10)
  %.55 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr %.45)
  %putchar2 = call i32 @putchar(i32 10)
  %.61 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull @str_13)
  %.15.i17 = call i64 @strlen(ptr noundef nonnull readonly dereferenceable(1) %.16)
  %invariant.op = add i64 %.15.i17, 1
  %.18.i20 = call ptr @malloc(i64 %invariant.op)
  store i8 0, ptr %.18.i20, align 1
  %.20.i22 = call ptr @strcat(ptr noundef nonnull dereferenceable(1) %.18.i20, ptr noundef nonnull readonly dereferenceable(1) %.16)
  %.14.i16.1 = call i64 @strlen(ptr noundef nonnull dereferenceable(1) %.18.i20)
  %.17.i19.reass.1 = add i64 %.14.i16.1, %invariant.op
  %.18.i20.1 = call ptr @malloc(i64 %.17.i19.reass.1)
  %.19.i21.1 = call ptr @strcpy(ptr noundef nonnull dereferenceable(1) %.18.i20.1, ptr noundef nonnull dereferenceable(1) %.18.i20)
  %.20.i22.1 = call ptr @strcat(ptr noundef nonnull dereferenceable(1) %.18.i20.1, ptr noundef nonnull readonly dereferenceable(1) %.16)
  %.64 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr %.18.i20.1)
  %putchar3 = call i32 @putchar(i32 10)
  %.69 = call i32 (ptr, ...) @printf(ptr nonnull dereferenceable(1) @str_2, ptr nonnull %rp_out.0.lcssa.i)
  %putchar4 = call i32 @putchar(i32 10)
  ret void
}

; Function Attrs: nofree nounwind
declare noundef i32 @putchar(i32 noundef) local_unnamed_addr #0

; Function Attrs: nocallback nofree nounwind willreturn memory(argmem: readwrite)
declare void @llvm.memcpy.p0.p0.i64(ptr noalias nocapture writeonly, ptr noalias nocapture readonly, i64, i1 immarg) #5

attributes #0 = { nofree nounwind }
attributes #1 = { mustprogress nofree nounwind willreturn memory(argmem: read) }
attributes #2 = { mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) memory(inaccessiblemem: readwrite) "alloc-family"="malloc" }
attributes #3 = { mustprogress nofree nounwind willreturn memory(argmem: readwrite) }
attributes #4 = { mustprogress nofree nounwind willreturn }
attributes #5 = { nocallback nofree nounwind willreturn memory(argmem: readwrite) }
