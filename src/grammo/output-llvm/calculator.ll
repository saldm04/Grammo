; ModuleID = '<string>'
source_filename = "<string>"
target triple = "unknown-unknown-unknown"

@str_-4632012517719779295 = constant [27 x i8] c"Errore: divisione per zero\00"
@str_-120980284675553327 = constant [3 x i8] c"%s\00"
@str_-6041228084570676652 = constant [2 x i8] c"\0A\00"
@str_5874105106702485220 = constant [22 x i8] c"Calcolatrice semplice\00"
@str_-679336470922510512 = constant [19 x i8] c"1=+  2=-  3=*  4=/\00"
@str_-6591615611739641353 = constant [13 x i8] c"Operazione: \00"
@str_-2616813324064646988 = constant [3 x i8] c"%d\00"
@str_2935478610624354 = constant [4 x i8] c"A: \00"
@str_6923136249815258289 = constant [4 x i8] c"%lf\00"
@str_362257735689411047 = constant [4 x i8] c"B: \00"
@str_4060537070354532679 = constant [11 x i8] c"Risultato=\00"
@str_7325109128805684496 = constant [5 x i8] c"%.6f\00"

declare i32 @printf(ptr, ...)

declare i32 @scanf(ptr, ...)

declare i64 @strlen(ptr)

declare ptr @malloc(i64)

declare ptr @strcpy(ptr, ptr)

declare ptr @strcat(ptr, ptr)

define double @calc(double %a, double %b, i32 %op) {
entry:
  %a.1 = alloca double, align 8
  store double %a, ptr %a.1, align 8
  %b.1 = alloca double, align 8
  store double %b, ptr %b.1, align 8
  %op.1 = alloca i32, align 4
  store i32 %op, ptr %op.1, align 4
  %load_op = load i32, ptr %op.1, align 4
  %.8 = icmp eq i32 %load_op, 1
  br i1 %.8, label %if_then, label %next_branch

if_then:                                          ; preds = %entry
  %load_a = load double, ptr %a.1, align 8
  %load_b = load double, ptr %b.1, align 8
  %.9 = fadd double %load_a, %load_b
  ret double %.9

next_branch:                                      ; preds = %entry
  %load_op.1 = load i32, ptr %op.1, align 4
  %.11 = icmp eq i32 %load_op.1, 2
  br i1 %.11, label %elif_0_then, label %elif_0_next

elif_0_then:                                      ; preds = %next_branch
  %load_a.1 = load double, ptr %a.1, align 8
  %load_b.1 = load double, ptr %b.1, align 8
  %.13 = fsub double %load_a.1, %load_b.1
  ret double %.13

elif_0_next:                                      ; preds = %next_branch
  %load_op.2 = load i32, ptr %op.1, align 4
  %.15 = icmp eq i32 %load_op.2, 3
  br i1 %.15, label %elif_1_then, label %elif_1_next

elif_1_then:                                      ; preds = %elif_0_next
  %load_a.2 = load double, ptr %a.1, align 8
  %load_b.2 = load double, ptr %b.1, align 8
  %.17 = fmul double %load_a.2, %load_b.2
  ret double %.17

elif_1_next:                                      ; preds = %elif_0_next
  %load_b.3 = load double, ptr %b.1, align 8
  %.19 = fcmp oeq double %load_b.3, 0.000000e+00
  br i1 %.19, label %if_then.1, label %next_branch.1

if_then.1:                                        ; preds = %elif_1_next
  %.20 = bitcast ptr @str_-4632012517719779295 to ptr
  %.21 = bitcast ptr @str_-120980284675553327 to ptr
  %.22 = call i32 (ptr, ...) @printf(ptr %.21, ptr %.20)
  %.23 = bitcast ptr @str_-6041228084570676652 to ptr
  %.24 = bitcast ptr @str_-120980284675553327 to ptr
  %.25 = call i32 (ptr, ...) @printf(ptr %.24, ptr %.23)
  ret double 0.000000e+00

next_branch.1:                                    ; preds = %elif_1_next
  %load_a.3 = load double, ptr %a.1, align 8
  %load_b.4 = load double, ptr %b.1, align 8
  %.27 = fdiv double %load_a.3, %load_b.4
  ret double %.27

if_merge:                                         ; No predecessors!
  br label %if_merge.1

if_merge.1:                                       ; preds = %if_merge
  unreachable
}

define void @main() {
entry:
  %a = alloca double, align 8
  store double 0.000000e+00, ptr %a, align 8
  %b = alloca double, align 8
  store double 0.000000e+00, ptr %b, align 8
  %res = alloca double, align 8
  store double 0.000000e+00, ptr %res, align 8
  %op = alloca i32, align 4
  store i32 0, ptr %op, align 4
  %.6 = bitcast ptr @str_5874105106702485220 to ptr
  %.7 = bitcast ptr @str_-120980284675553327 to ptr
  %.8 = call i32 (ptr, ...) @printf(ptr %.7, ptr %.6)
  %.9 = bitcast ptr @str_-6041228084570676652 to ptr
  %.10 = bitcast ptr @str_-120980284675553327 to ptr
  %.11 = call i32 (ptr, ...) @printf(ptr %.10, ptr %.9)
  %.12 = bitcast ptr @str_-679336470922510512 to ptr
  %.13 = bitcast ptr @str_-120980284675553327 to ptr
  %.14 = call i32 (ptr, ...) @printf(ptr %.13, ptr %.12)
  %.15 = bitcast ptr @str_-6041228084570676652 to ptr
  %.16 = bitcast ptr @str_-120980284675553327 to ptr
  %.17 = call i32 (ptr, ...) @printf(ptr %.16, ptr %.15)
  %.18 = bitcast ptr @str_-6591615611739641353 to ptr
  %.19 = bitcast ptr @str_-120980284675553327 to ptr
  %.20 = call i32 (ptr, ...) @printf(ptr %.19, ptr %.18)
  %.21 = bitcast ptr @str_-2616813324064646988 to ptr
  %.22 = call i32 (ptr, ...) @scanf(ptr %.21, ptr %op)
  %.23 = bitcast ptr @str_2935478610624354 to ptr
  %.24 = bitcast ptr @str_-120980284675553327 to ptr
  %.25 = call i32 (ptr, ...) @printf(ptr %.24, ptr %.23)
  %.26 = bitcast ptr @str_6923136249815258289 to ptr
  %.27 = call i32 (ptr, ...) @scanf(ptr %.26, ptr %a)
  %.28 = bitcast ptr @str_362257735689411047 to ptr
  %.29 = bitcast ptr @str_-120980284675553327 to ptr
  %.30 = call i32 (ptr, ...) @printf(ptr %.29, ptr %.28)
  %.31 = bitcast ptr @str_6923136249815258289 to ptr
  %.32 = call i32 (ptr, ...) @scanf(ptr %.31, ptr %b)
  %load_a = load double, ptr %a, align 8
  %load_b = load double, ptr %b, align 8
  %load_op = load i32, ptr %op, align 4
  %.33 = call double @calc(double %load_a, double %load_b, i32 %load_op)
  store double %.33, ptr %res, align 8
  %.35 = bitcast ptr @str_4060537070354532679 to ptr
  %.36 = bitcast ptr @str_-120980284675553327 to ptr
  %.37 = call i32 (ptr, ...) @printf(ptr %.36, ptr %.35)
  %load_res = load double, ptr %res, align 8
  %.38 = bitcast ptr @str_7325109128805684496 to ptr
  %.39 = call i32 (ptr, ...) @printf(ptr %.38, double %load_res)
  %.40 = bitcast ptr @str_-6041228084570676652 to ptr
  %.41 = bitcast ptr @str_-120980284675553327 to ptr
  %.42 = call i32 (ptr, ...) @printf(ptr %.41, ptr %.40)
  ret void
}
