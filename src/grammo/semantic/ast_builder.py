from lark import Transformer, v_args
from . import ast_nodes as ast

class ASTBuilder(Transformer):
    def start(self, items):
        return items[0]

    def program(self, items):
        return ast.Program(decls=items)

    def top_decl(self, items):
        # items has 1 element: func_def or var_decl
        return items[0]

    # Declarations
    def func_def(self, items):
        # FUNC return_type ARROW ID LPAR param_list? RPAR block
        # items: [return_type, ID, param_list (optional), block]
        # Lark strips terminals like FUNC, ARROW, LPAR, RPAR by default in tree unless kept?
        # No, Transformer usually gets reduced items of the rule.
        # Rule: FUNC return_type ARROW ID LPAR param_list? RPAR block
        
        # We need to filter out tokens if they are kept or handle indices carefully.
        # But wait, in standard Lark (not keep_all_tokens), terminals are discarded if not named or if they are literals?
        # Actually usually terminals defined as strings in the grammar (like "func") appear as Token objects if not filtered?
        # Let's assume standard behavior: items matches the structure of the rule without ignored stuff.
        # ID is a terminal.
        
        # return_type is items[0]
        # ID is items[1]
        # param_list? : if present, items[2] is param_list, items[3] is block
        # if absent, items[2] is block?
        
        # Actually, let's look at the rule:
        # func_def: FUNC return_type ARROW ID LPAR param_list? RPAR block
        
        # The tokens FUNC, ARROW, LPAR, RPAR are unlikely to be in `items` if they are anonymous literals 
        # UNLESS ! is used or similar. But here they are named terminals in the token section 
        # e.g. FUNC: "func".
        # If they are named terminals, they DO appear in `items`.
        
        # Let's inspect items carefully.
        # 0: FUNC (Token)
        # 1: return_type (Result of return_type rule)
        # 2: ARROW (Token)
        # 3: ID (Token)
        # 4: LPAR (Token)
        # ... param_list? 
        # ... RPAR (Token)
        # ... block
        
        # Helper to filter tokens that are purely syntactic sugar?
        # Or just index by position.
        
        ret_type = items[1]
        func_name = str(items[3])
        
        # Check if param_list is present
        # We can scan for Block.
        block_idx = len(items) - 1
        block = items[block_idx]
        
        # params are between LPAR (4) and RPAR.
        # if param_list is present, it will be at index 5.
        # If no params, index 5 is RPAR?
        
        params = []
        if len(items) > 7: # FUNC RET ARROW ID LPAR PARAMS RPAR BLOCK = 8 items
             # item 5 is param_list
             if isinstance(items[5], list):
                 params = items[5]
        
        return ast.FuncDef(name=func_name, return_type=ret_type, params=params, body=block)

    def return_type(self, items):
        # type | VOID_TYPE
        if isinstance(items[0], ast.Type):
            return items[0].name
        return str(items[0]) # "void"

    def type(self, items):
        # INT_TYPE | ...
        return ast.PrimitiveType(name=str(items[0]))

    def param_list(self, items):
        # param (COMMA param)*
        # Filter out commas
        return [item for item in items if isinstance(item, ast.Param)]

    def param(self, items):
        # type COLON ID
        # 0: type
        # 1: COLON
        # 2: ID
        return ast.Param(type_name=items[0].name, name=str(items[2]))

    def var_decl(self, items):
        # Two forms:
        # 1. VAR type COLON id_list SEMI
        # 2. VAR ID ASSIGN const_expr SEMI
        
        # items[0] is VAR token
        
        if isinstance(items[1], ast.Type): 
            # Case 1
            # 1: type
            # 2: COLON
            # 3: id_list (list of strings)
            # 4: SEMI
            return ast.VarDecl(type_name=items[1].name, names=items[3])
        else:
            # Case 2
            # 1: ID
            # 2: ASSIGN
            # 3: const_expr (Literal)
            # 4: SEMI
            return ast.VarInit(name=str(items[1]), value=items[3])

    def id_list(self, items):
        # ID (COMMA ID)*
        return [str(item) for item in items if hasattr(item, 'type') and item.type == 'ID']

    def const_expr(self, items):
        # Returns a Literal
        # items[0] is one of INT_CONST, TRUE, etc.
        token = items[0]
        val = token.value
        t_type = token.type
        
        if t_type == 'INT_CONST':
            return ast.Literal(value=int(val), type_name='int')
        elif t_type == 'REAL_CONST':
            return ast.Literal(value=float(val), type_name='real')
        elif t_type == 'STRING_CONST':
            return ast.Literal(value=val[1:-1], type_name='string') # strip quotes
        elif t_type == 'TRUE':
            return ast.Literal(value=True, type_name='bool')
        elif t_type == 'FALSE':
            return ast.Literal(value=False, type_name='bool')
        return ast.Literal(value=val, type_name='unknown')

    # Blocks & Stmts
    def block(self, items):
        # LBRACE stmt* RBRACE
        # Filter out braces
        stmts = [item for item in items if isinstance(item, ast.Stmt)]
        return ast.Block(stmts=stmts)

    def stmt(self, items):
        # Just returns the child
        return items[0]

    def assign_stmt(self, items):
        # ID ASSIGN expr
        return ast.AssignStmt(name=str(items[0]), value=self._to_expr(items[2]))

    def proc_call(self, items):
        # ID LPAR arg_list? RPAR
        name = str(items[0])
        args = []
        if len(items) > 3: # ID LPAR args RPAR
             if isinstance(items[2], list):
                 args = items[2]
        return ast.ProcCallStmt(name=name, args=args)
        
    def arg_list(self, items):
         # expr (COMMA expr)*
         # items is list of exprs AND commas (if kept)
         # If not kept, list of exprs.
         # _to_expr ensures we wrap tokens.
         return [self._to_expr(item) for item in items if not (hasattr(item, 'type') and item.type == 'COMMA')]

    def return_stmt(self, items):
        # RETURN expr?
        # items[0] is RETURN
        val = None
        if len(items) > 1:
            val = self._to_expr(items[1])
        return ast.ReturnStmt(value=val)

    # I/O
    def output_stmt(self, items):
        # OUT io_args
        return ast.OutputStmt(is_newline=False, args=items[1])
        
    def outputln_stmt(self, items):
         # OUTLN io_args
         return ast.OutputStmt(is_newline=True, args=items[1])

    def input_stmt(self, items):
        # IN io_args
        return ast.InputStmt(args=items[1])

    def io_args(self, items):
        # (expr | HASH LPAR expr RPAR)*
        # This one is tricky because structure is flat sequence.
        # Lark might give us mixed tokens/nodes.
        # HASH LPAR expr RPAR -> we want to capture that specific structure if possible?
        # But here `items` is just a list of children.
        # If we see HASH, then LPAR, then expr, then RPAR.
        # However, `expr` is a node.
        
        # Actually, simpler:
        # HASH LPAR expr RPAR -> Could be handled by a sub-rule? No, it's inline.
        # Wait, the rule is `io_args: (expr | HASH LPAR expr RPAR)*`
        # Lark will give us a list of ALL children.
        # e.g. [Expr, HASH, LPAR, Expr, RPAR, Expr]
        
        args = []
        i = 0
        while i < len(items):
            item = items[i]
            if getattr(item, 'type', None) == 'HASH':
                # Skip HASH, LPAR(next), Expr(next+1), RPAR(next+2)
                # The expr we want is at i+2
                if i + 2 < len(items):
                    expr_node = items[i+2]
                    # We treat this specially? The prompt said:
                    # "#(Expr) per interpolare un’espressione nei flussi di I/O."
                    # In InputStmt, #(Expr) must be an ID (target variable).
                    # I will wrap this in a special arg type?
                    # Or just treat it as an expression but context matters?
                    # Let's support an IOArg wrapper in AST.
                    # Wait, defined `ExprArg`. Maybe `InterpolatedArg`?
                    # Let's abuse `ExprArg` or add `InterpolatedArg`.
                    # I'll modify AST node usage slightly or just store as ExprArg.
                    # Actually, for output it's just expr. For input it's variable.
                    # But the syntax `#( )` distinguishes it.
                    # I'll assume valid syntax and just collect exprs, but I lose the `#` distinction if I don't wrap it.
                    # Let's assume standard exprs are just values/prompts, hash exprs are ... something else?
                    # Actually for Output, `<< "Sum: " #(a+b)` -> print string, then print value of a+b.
                    # It seems `#(...)` is just an explicit separation or formatting?
                    # Re-reading: "Scelte semantiche: ... In input (InputStmt): gli argomenti HASH LPAR Expr RPAR dovranno essere identificatori ... eventuali Expr 'nude' saranno normalmente stringhe di prompt".
                    # So `#(...)` is semantically significant (Target vs Prompt).
                    # I need to distinguish them in AST.
                    # I'll use a wrapper class locally or modify AST.
                    pass
                args.append(item) # Placeholder logic, will fix in loop
            i += 1
            
        # Refined loop:
        final_args = []
        idx = 0
        while idx < len(items):
            item = items[idx]
            if hasattr(item, 'type') and item.type == 'HASH':
                 # Sequence is HASH, LPAR, Expr, RPAR
                 expr = self._to_expr(items[idx+2])
                 final_args.append(ast.UnaryExpr(operator='#', operand=expr))
                 idx += 4
            else:
                 # Try to convert to expr
                 e = self._to_expr(item)
                 if isinstance(e, ast.Expr):
                     final_args.append(e)
                 # else skip terminals like tokens of other types (if any)
                 idx += 1
        return final_args

    # Control Flow
    def if_stmt(self, items):
        # IF LPAR expr RPAR block elif_list? else_block?
        # items structure: 
        # 0: IF
        # 1: LPAR
        # 2: expr
        # 3: RPAR
        # 4: block
        # 5: elif_list (optional)
        # 6: else_block (optional)
        
        # We need to find the parts.
        cond = items[2]
        then_blk = items[4]
        elifs = []
        else_blk = None
        
        for item in items[5:]:
             if isinstance(item, list): # elif_list returns list of ElifClause
                 elifs = item
             elif isinstance(item, ast.Block): # else_block returns Block
                 else_blk = item
        
        return ast.IfStmt(condition=cond, then_block=then_blk, elifs=elifs, else_block=else_blk)

    def elif_list(self, items):
        return items # Already a list of ElifClause

    def elif_clause(self, items):
        # ELIF LPAR expr RPAR block
        return ast.ElifClause(condition=items[2], block=items[4])

    def else_block(self, items):
        # ELSE block
        return items[1]

    def while_stmt(self, items):
        # WHILE LPAR expr RPAR block
        return ast.WhileStmt(condition=items[2], body=items[4])

    def for_stmt(self, items):
        # FOR LPAR for_init? SEMI expr? SEMI for_update? RPAR block
        # Indices are fixedish but optional items might be None or missing tokens?
        # Layout: FOR(0) LPAR(1) INIT?(2) SEMI(3) EXPR?(4) SEMI(5) UPDATE?(6) RPAR(7) BODY(8)
        # But optional rules in Lark (`name?`) might be present or None in the list, OR omitted from list.
        # Lark standard parser usually includes `None` if `maybe_placeholders=True`.
        # Code checked `maybe_placeholders=False` in `check_grammo.py`.
        # So missing items are missing from the list.
        
        # We have terminals: FOR, LPAR, SEMI, SEMI, RPAR.
        # Let's count SEMIs to find positions.
        
        # Easier strategy: filter children by type?
        # init is AssignStmt
        # expr is Expr
        # update is AssignStmt
        # block is Block
        
        # Be careful: Init and Update are BOTH AssignStmt.
        # We need position relative to SEMIs.
        
        init = None
        cond = None
        update = None
        body = None
        
        # Scan items
        current_stage = 0 # 0: before 1st semi, 1: between semis, 2: after 2nd semi
        
        for item in items:
            if hasattr(item, 'type') and item.type == 'SEMI':
                current_stage += 1
                continue
            
            if isinstance(item, ast.AssignStmt):
                if current_stage == 0:
                    init = item
                elif current_stage == 2:
                    update = item
            elif isinstance(item, ast.Expr):
                if current_stage == 1:
                    cond = item
            elif isinstance(item, ast.Block):
                body = item
        
        return ast.ForStmt(init=init, condition=cond, update=update, body=body)

    def for_init(self, items):
        return items[0]
    def for_update(self, items):
        return items[0]

    # Expression wrappers
    def atomic_expr(self, items):
        return items[0]
    
    # Precedence levels
    # Since ?expr: or_expr, etc., Transformer might skip the wrapper if it has one child.
    # If it has 3 children (left op right), we handle it.
    
    def _to_expr(self, item):
        if hasattr(item, 'type'): # Token
             # Wrap in literal using logic from const_expr
             # Check type
             t_type = item.type
             val = item.value
             if t_type == 'INT_CONST':
                 return ast.Literal(value=int(val), type_name='int')
             elif t_type == 'REAL_CONST':
                 return ast.Literal(value=float(val), type_name='real')
             elif t_type == 'STRING_CONST':
                 return ast.Literal(value=val[1:-1], type_name='string')
             elif t_type == 'TRUE':
                 return ast.Literal(value=True, type_name='bool')
             elif t_type == 'FALSE':
                 return ast.Literal(value=False, type_name='bool')
             
             # Fallback for operators or others if misused?
             # Only literals land here if unhandled.
             return item 
        return item

    def _binary_op(self, items):
        # left op right
        # Ensure left/right are Expr
        left = self._to_expr(items[0])
        right = self._to_expr(items[2])
        return ast.BinaryExpr(left=left, operator=str(items[1]), right=right)

    def or_expr(self, items):
        if len(items) == 1: return self._to_expr(items[0])
        return self._binary_op(items)
    def and_expr(self, items):
        if len(items) == 1: return self._to_expr(items[0])
        return self._binary_op(items)
    def equality_expr(self, items):
        if len(items) == 1: return self._to_expr(items[0])
        return self._binary_op(items)
    def rel_expr(self, items):
        if len(items) == 1: return self._to_expr(items[0])
        return self._binary_op(items)
    def add_expr(self, items):
        if len(items) == 1: return self._to_expr(items[0])
        return self._binary_op(items)
    def mul_expr(self, items):
        if len(items) == 1: return self._to_expr(items[0])
        return self._binary_op(items)

    def unary_expr(self, items):
        if len(items) == 1: return self._to_expr(items[0])
        # OP expr
        return ast.UnaryExpr(operator=str(items[0]), operand=self._to_expr(items[1]))

    # Primary
    def primary(self, items):
        # Handle ( expr )
        if len(items) == 3 and getattr(items[0], 'type', None) == 'LPAR':
            return self._to_expr(items[1]) 
        # Fallback for literals if they land here?
        # But ?primary implies literals are inlined. 
        # If a literal comes here, it is 1 item.
        return self._to_expr(items[0])

    def func_call(self, items):
        # ID LPAR arg_list? RPAR
        name = str(items[0])
        args = []
        if len(items) > 3:
             if isinstance(items[2], list):
                 args = items[2]
        return ast.FuncCallExpr(name=name, args=args)

    def var(self, items):
        return ast.VarRef(name=str(items[0]))
