from llvmlite import ir, binding
from ..semantic import ast_nodes as ast

class CodeGenerator:
    """Generates LLVM IR from the Grammo AST.

    Attributes:
        module: The LLVM module being generated.
        builder: The LLVM IR builder.
        func_symtab: A symbol table for function-local variables.
        current_func: The current LLVM function being compiled.
    """

    def __init__(self):
        """Initializes the code generator."""
        self.module = ir.Module(name="grammo_module")
        self.module.triple = binding.get_default_triple()
        self.builder = None
        self.func_symtab = {}  # Maps variable names to ir.Value (allocas)
        self.current_func = None
        
        # Standard library declarations
        self.printf = None
        self.scanf = None
        self._declare_stdlib()

        # String constants management
        self.string_counter = 0
        self.string_literals = {} # Map content -> GlobalVariable

        # Type Mappings
        self.type_map = {
            'int': ir.IntType(32),
            'real': ir.DoubleType(),
            'bool': ir.IntType(1), # 0 or 1
            'string': ir.IntType(8).as_pointer(), # char*
            'void': ir.VoidType()
        }

    def _declare_stdlib(self):
        """Declares standard library functions (printf, scanf, etc.) in the module."""
        # void printf(i8*, ...)
        void_ptr_type = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [void_ptr_type], var_arg=True)
        self.printf = ir.Function(self.module, printf_ty, name="printf")
        
        # int scanf(i8*, ...)
        scanf_ty = ir.FunctionType(ir.IntType(32), [void_ptr_type], var_arg=True)
        self.scanf = ir.Function(self.module, scanf_ty, name="scanf")
        
        # String utils
        # i64 strlen(i8*)
        strlen_ty = ir.FunctionType(ir.IntType(64), [void_ptr_type])
        self.strlen = ir.Function(self.module, strlen_ty, name="strlen")
        
        # i8* malloc(i64)
        malloc_ty = ir.FunctionType(void_ptr_type, [ir.IntType(64)])
        self.malloc = ir.Function(self.module, malloc_ty, name="malloc")
        
        # i8* strcpy(i8*, i8*)
        strcpy_ty = ir.FunctionType(void_ptr_type, [void_ptr_type, void_ptr_type])
        self.strcpy = ir.Function(self.module, strcpy_ty, name="strcpy")
        
        # i8* strcat(i8*, i8*)
        strcat_ty = ir.FunctionType(void_ptr_type, [void_ptr_type, void_ptr_type])
        self.strcat = ir.Function(self.module, strcat_ty, name="strcat")

    def _get_llvm_type(self, type_name):
        """Maps Grammo types to LLVM types."""
        return self.type_map.get(type_name, ir.VoidType())

    def visit(self, node):
        """Dispatches the visit method for the given node."""
        return getattr(self, f"visit_{node.__class__.__name__}")(node)

    # ==========================
    # Program & Functions
    # ==========================

    def visit_Program(self, node: ast.Program):
        """Generates code for the program declarations."""
        for decl in node.decls:
            self.visit(decl)
        return self.module

    def visit_VarDecl(self, node: ast.VarDecl):
        """Generates code for a variable declaration."""
        # Global variable declaration (if strictly global context)
        # OR local if inside function.
        llvm_type = self._get_llvm_type(node.type_name)
        
        # Determine initializer
        if node.type_name == 'real':
            init_const = ir.Constant(llvm_type, 0.0)
        elif node.type_name == 'string':
            init_const = ir.Constant(llvm_type, None)
        else:
            init_const = ir.Constant(llvm_type, 0)

        if self.builder is None:
            # Global variables
            for name in node.names:
                gvar = ir.GlobalVariable(self.module, llvm_type, name=name)
                gvar.initializer = init_const
        else:
            # Local variables
            for name in node.names:
                alloca = self.builder.alloca(llvm_type, name=name)
                self.func_symtab[name] = alloca
                self.builder.store(init_const, alloca)

    def visit_VarInit(self, node: ast.VarInit):
        """Generates code for a variable initialization."""
        # var <name> = <const>;
        val = self.visit(node.value) # Should be a constant literal
        
        if self.builder is None:
             gvar = ir.GlobalVariable(self.module, val.type, name=node.name)
             gvar.initializer = val
        else:
            # Local constant? Treat as var.
            alloca = self.builder.alloca(val.type, name=node.name)
            self.builder.store(val, alloca)
            self.func_symtab[node.name] = alloca

    def visit_FuncDef(self, node: ast.FuncDef):
        """Generates code for a function definition."""
        ret_type = self._get_llvm_type(node.return_type)
        param_types = [self._get_llvm_type(p.type_name) for p in node.params]
        func_ty = ir.FunctionType(ret_type, param_types)
        func = ir.Function(self.module, func_ty, name=node.name)
        
        # Setup entry block
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        self.current_func = func
        self.func_symtab = {} # Reset local symbol table
        
        # Arg processing
        for i, arg in enumerate(func.args):
            arg.name = node.params[i].name
            # Allocate space for arg to be mutable
            alloca = self.builder.alloca(arg.type, name=arg.name)
            self.builder.store(arg, alloca)
            self.func_symtab[arg.name] = alloca

        # Process function body (Block)
        self.visit(node.body)
        
        # Add implicit return void if missing
        if not self.builder.block.is_terminated:
            if node.return_type == 'void':
                self.builder.ret_void()
            else:
                self.builder.unreachable()
            
        self.builder = None
        self.current_func = None

    # ==========================
    # Statements
    # ==========================

    def visit_Block(self, node: ast.Block):
        for stmt in node.stmts:
            self.visit(stmt)
            if self.builder.block.is_terminated:
                break # Unreachable code after this

    def visit_AssignStmt(self, node: ast.AssignStmt):
        val = self.visit(node.value)
        ptr = self._lookup_var(node.name)
        
        # Handle implicit casting (int -> real)
        if ptr.type.pointee == ir.DoubleType() and val.type == ir.IntType(32):
            val = self.builder.sitofp(val, ir.DoubleType())
            
        self.builder.store(val, ptr)

    def visit_ReturnStmt(self, node: ast.ReturnStmt):
        if node.value:
            val = self.visit(node.value)
             # Handle implicit casting (int -> real) for return
            if self.current_func.function_type.return_type == ir.DoubleType() and val.type == ir.IntType(32):
                val = self.builder.sitofp(val, ir.DoubleType())
            self.builder.ret(val)
        else:
            self.builder.ret_void()

    def visit_IfStmt(self, node: ast.IfStmt):
        # 1. Evaluate Condition
        cond = self.visit(node.condition)
        start_block = self.builder.block

        # 2. Create Blocks (but not Merge yet)
        then_block = self.current_func.append_basic_block(name="if_then")
        
        next_block = None
        if node.else_block or node.elifs:
            next_block = self.current_func.append_basic_block(name="next_branch")

        jumps_to_merge = []

        # 3. Populate Then Block
        self.builder.position_at_start(then_block)
        self.visit(node.then_block)
        if not self.builder.block.is_terminated:
            jumps_to_merge.append(self.builder.block)

        # 4. Populate Next Block (Elifs / Else)
        elif_branches_to_patch = [] # List of (block, cond, true_dest) to jump to merge on false

        if next_block:
            curr_bb = next_block
            
            # Elifs
            for i, elif_clause in enumerate(node.elifs):
                self.builder.position_at_start(curr_bb)
                elif_cond = self.visit(elif_clause.condition)
                
                elif_then_bb = self.current_func.append_basic_block(name=f"elif_{i}_then")
                
                has_next = (i < len(node.elifs) - 1) or (node.else_block is not None)
                
                if has_next:
                    elif_next_bb = self.current_func.append_basic_block(name=f"elif_{i}_next")
                    self.builder.cbranch(elif_cond, elif_then_bb, elif_next_bb)
                    curr_bb = elif_next_bb
                else:
                    # Last elif, no else -> false jumps to merge
                    elif_branches_to_patch.append((self.builder.block, elif_cond, elif_then_bb))
                
                # Elif Body
                self.builder.position_at_start(elif_then_bb)
                self.visit(elif_clause.block)
                if not self.builder.block.is_terminated:
                    jumps_to_merge.append(self.builder.block)

            # Else
            if node.else_block:
                self.builder.position_at_start(curr_bb)
                self.visit(node.else_block)
                if not self.builder.block.is_terminated:
                    jumps_to_merge.append(self.builder.block)
        
        # 5. Create Merge Block (LAST)
        merge_block = self.current_func.append_basic_block(name="if_merge")
        
        # 6. Apply Patches
        
        # Patch Start Block
        self.builder.position_at_end(start_block)
        if next_block:
            self.builder.cbranch(cond, then_block, next_block)
        else:
            self.builder.cbranch(cond, then_block, merge_block)
            
        # Patch Elif False Branches
        for blk, e_cond, true_dest in elif_branches_to_patch:
            self.builder.position_at_end(blk)
            self.builder.cbranch(e_cond, true_dest, merge_block)
            
        # Patch Jumps to Merge
        for blk in jumps_to_merge:
            self.builder.position_at_end(blk)
            self.builder.branch(merge_block)

        # 7. Continue
        self.builder.position_at_start(merge_block)

    def visit_WhileStmt(self, node: ast.WhileStmt):
        cond_block = self.current_func.append_basic_block(name="while_cond")
        body_block = self.current_func.append_basic_block(name="while_body")
        end_block = self.current_func.append_basic_block(name="while_end")
        
        self.builder.branch(cond_block)
        
        # Condition
        self.builder.position_at_start(cond_block)
        cond = self.visit(node.condition)
        self.builder.cbranch(cond, body_block, end_block)
        
        # Body
        self.builder.position_at_start(body_block)
        self.visit(node.body)
        if not self.builder.block.is_terminated:
            self.builder.branch(cond_block)
            
        self.builder.position_at_start(end_block)

    def visit_ForStmt(self, node: ast.ForStmt):
        if node.init:
            self.visit(node.init)
            
        cond_block = self.current_func.append_basic_block(name="for_cond")
        body_block = self.current_func.append_basic_block(name="for_body")
        end_block = self.current_func.append_basic_block(name="for_end")
        
        self.builder.branch(cond_block)
        
        # Condition
        self.builder.position_at_start(cond_block)
        if node.condition:
            cond = self.visit(node.condition)
            self.builder.cbranch(cond, body_block, end_block)
        else:
            self.builder.branch(body_block) # Infinite loop if no cond
            
        # Body
        self.builder.position_at_start(body_block)
        self.visit(node.body)
        
        # Update
        if node.update:
            self.visit(node.update)
            
        if not self.builder.block.is_terminated:
            self.builder.branch(cond_block)
            
        self.builder.position_at_start(end_block)

    def visit_OutputStmt(self, node: ast.OutputStmt):
        for arg in node.args:
            val = self.visit(arg)
            self._print_val(val)
        
        if node.is_newline:
            self._print_str("\n")

    def visit_InputStmt(self, node: ast.InputStmt):
        for arg in node.args:
            # Unwrap UnaryExpr (e.g. #n)
            while isinstance(arg, ast.UnaryExpr) and arg.operator == '#':
                arg = arg.operand

            if isinstance(arg, ast.Literal):
                val = self.visit(arg)
                self._print_val(val)
            elif isinstance(arg, ast.VarRef):
                ptr = self._lookup_var(arg.name)
                val_type = ptr.type.pointee
                
                fmt = ""
                if val_type == ir.IntType(32):
                    fmt = "%d"
                elif val_type == ir.DoubleType():
                    fmt = "%lf" # scanf needs %lf for double
                elif val_type == ir.IntType(8).as_pointer():
                    
                    # Fix: Allocate buffer (malloc) for scanf to write into
                    # We allocate 256 bytes
                    size_const = ir.Constant(ir.IntType(64), 256)
                    buf = self.builder.call(self.malloc, [size_const])
                    
                    fmt = "%255s" 
                    fmt_ptr = self._get_global_string_ptr(fmt)
                    self.builder.call(self.scanf, [fmt_ptr, buf])
                    
                    # Store the pointer to the buffer in the variable
                    self.builder.store(buf, ptr)
                    
                    continue # Skip the default logic at bottom
                
                if fmt:
                    fmt_ptr = self._get_global_string_ptr(fmt)
                    self.builder.call(self.scanf, [fmt_ptr, ptr])

    def visit_ProcCallStmt(self, node: ast.ProcCallStmt):
        func = self.module.globals.get(node.name)
        args_vals = [self.visit(a) for a in node.args]
        self.builder.call(func, args_vals)

    # ==========================
    # Expressions
    # ==========================

    def visit_Literal(self, node: ast.Literal):
        if node.type_name == 'int':
            return ir.Constant(ir.IntType(32), int(node.value))
        elif node.type_name == 'real':
            return ir.Constant(ir.DoubleType(), float(node.value))
        elif node.type_name == 'bool':
            return ir.Constant(ir.IntType(1), 1 if node.value else 0)
        elif node.type_name == 'string':
            return self._get_global_string_ptr(node.value)
        return ir.Constant(ir.IntType(32), 0)

    def visit_VarRef(self, node: ast.VarRef):
        ptr = self._lookup_var(node.name)
        return self.builder.load(ptr, name=f"load_{node.name}")

    def visit_BinaryExpr(self, node: ast.BinaryExpr):
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)
        
        # Type balancing
        types = [lhs.type, rhs.type]
        if ir.DoubleType() in types:
            if lhs.type == ir.IntType(32): lhs = self.builder.sitofp(lhs, ir.DoubleType())
            if rhs.type == ir.IntType(32): rhs = self.builder.sitofp(rhs, ir.DoubleType())
            is_float = True
        else:
            is_float = False
            
        op = node.operator
        if is_float:
            if op == '+': return self.builder.fadd(lhs, rhs)
            if op == '-': return self.builder.fsub(lhs, rhs)
            if op == '*': return self.builder.fmul(lhs, rhs)
            if op == '/': return self.builder.fdiv(lhs, rhs)
            # Compare
            if op == '==': return self.builder.fcmp_ordered('==', lhs, rhs)
            if op == '<>': return self.builder.fcmp_ordered('!=', lhs, rhs)
            if op == '<':  return self.builder.fcmp_ordered('<', lhs, rhs)
            if op == '<=': return self.builder.fcmp_ordered('<=', lhs, rhs)
            if op == '>':  return self.builder.fcmp_ordered('>', lhs, rhs)
            if op == '>=': return self.builder.fcmp_ordered('>=', lhs, rhs)
        else:
            # Strings?
            # Check for pointers (i8*) using loose string check
            # We check if they are pointers.
            is_lhs_ptr = '*' in str(lhs.type) or isinstance(lhs.type, ir.PointerType) # Paranoid
            is_rhs_ptr = '*' in str(rhs.type) or isinstance(rhs.type, ir.PointerType)
            
            if is_lhs_ptr and is_rhs_ptr:
                 if op == '+':
                     # String concatenation
                     # new_str = malloc(strlen(lhs) + strlen(rhs) + 1)
                     len1 = self.builder.call(self.strlen, [lhs])
                     len2 = self.builder.call(self.strlen, [rhs])
                     total_len = self.builder.add(len1, len2)
                     total_len = self.builder.add(total_len, ir.Constant(ir.IntType(64), 1))
                     
                     new_str = self.builder.call(self.malloc, [total_len])
                     self.builder.call(self.strcpy, [new_str, lhs])
                     self.builder.call(self.strcat, [new_str, rhs])
                     return new_str

            if op == '+': return self.builder.add(lhs, rhs)
            if op == '-': return self.builder.sub(lhs, rhs)
            if op == '*': return self.builder.mul(lhs, rhs)
            if op == '/': return self.builder.sdiv(lhs, rhs)
            # Compare
            if op == '==': return self.builder.icmp_signed('==', lhs, rhs)
            if op == '<>': return self.builder.icmp_signed('!=', lhs, rhs)
            if op == '<':  return self.builder.icmp_signed('<', lhs, rhs)
            if op == '<=': return self.builder.icmp_signed('<=', lhs, rhs)
            if op == '>':  return self.builder.icmp_signed('>', lhs, rhs)
            if op == '>=': return self.builder.icmp_signed('>=', lhs, rhs)
            
        # Bool ops
        if op == '&&': return self.builder.and_(lhs, rhs)
        if op == '||': return self.builder.or_(lhs, rhs)
        
    def visit_UnaryExpr(self, node: ast.UnaryExpr):
        operand = self.visit(node.operand)
        if node.operator == '-':
            if isinstance(operand.type, ir.FloatType) or isinstance(operand.type, ir.DoubleType):
                return self.builder.fneg(operand)
            return self.builder.neg(operand)
        elif node.operator == '!':
            return self.builder.not_(operand)
        elif node.operator == '#':
            return operand

    def visit_FuncCallExpr(self, node: ast.FuncCallExpr):
        func = self.module.globals.get(node.name)
        args_vals = []
        for i, arg in enumerate(node.args):
            val = self.visit(arg)
            # Check implicit cast against function signature
            if i < len(func.args):
                 expected_type = func.args[i].type
                 if expected_type == ir.DoubleType() and val.type == ir.IntType(32):
                     val = self.builder.sitofp(val, ir.DoubleType())
            args_vals.append(val)
            
        return self.builder.call(func, args_vals)

    # ==========================
    # Helpers
    # ==========================

    def _lookup_var(self, name):
        if name in self.func_symtab:
            return self.func_symtab[name]
        return self.module.globals.get(name)

    def _get_global_string_ptr(self, s):
        # Dedup strings using a map
        if s in self.string_literals:
            gvar = self.string_literals[s]
            if self.builder:
                return self.builder.bitcast(gvar, ir.IntType(8).as_pointer())
            return gvar.bitcast(ir.IntType(8).as_pointer())

        # Escape string
        # Simply byte array
        b = bytearray(s.encode("utf8"))
        b.append(0)
        c = ir.Constant(ir.ArrayType(ir.IntType(8), len(b)), b)
        
        name = f"str_{self.string_counter}"
        self.string_counter += 1
        
        gvar = ir.GlobalVariable(self.module, c.type, name=name)
        gvar.global_constant = True
        gvar.initializer = c
        
        self.string_literals[s] = gvar
        
        if self.builder:
            return self.builder.bitcast(gvar, ir.IntType(8).as_pointer())
        return gvar.bitcast(ir.IntType(8).as_pointer())

    def _print_val(self, val):
        if val.type == ir.IntType(32):
            fmt = "%d"
            fmt_ptr = self._get_global_string_ptr(fmt)
            self.builder.call(self.printf, [fmt_ptr, val])
        elif val.type == ir.DoubleType():
            fmt = "%.6f"
            fmt_ptr = self._get_global_string_ptr(fmt)
            self.builder.call(self.printf, [fmt_ptr, val])
        elif val.type == ir.IntType(1):
             # Bool -> print 0 or 1? Or true/false?
             # Let's print true/false
             pass 
             fmt = "%d" 
             fmt_ptr = self._get_global_string_ptr(fmt)
             # Zero extend for printf
             val_zext = self.builder.zext(val, ir.IntType(32))
             self.builder.call(self.printf, [fmt_ptr, val_zext])
        elif isinstance(val.type, ir.PointerType):
            fmt = "%s"
            fmt_ptr = self._get_global_string_ptr(fmt)
            self.builder.call(self.printf, [fmt_ptr, val])

    def _print_str(self, s):
        ptr = self._get_global_string_ptr(s)
        fmt = "%s"
        fmt_ptr = self._get_global_string_ptr(fmt)
        self.builder.call(self.printf, [fmt_ptr, ptr])
