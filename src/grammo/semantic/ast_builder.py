from lark import Transformer, v_args
import ast as py_ast
from . import ast_nodes as ast

class ASTBuilder(Transformer):
    """Transform Lark parse tree into a custom AST.

    Methods match the grammar rules in the Lark file.
    """
    def _extract_pos(self, items):
        """Extracts the line and column from the given items."""
        if not isinstance(items, list):
            items = [items]
        for item in items:
            if hasattr(item, 'line') and getattr(item, 'line', 0) > 0:
                return item.line, item.column
            if isinstance(item, ast.Node) and item.line > 0:
                return item.line, item.column
        return 0, 0

    def start(self, items):
        """Returns the root of the AST."""
        return items[0]

    def program(self, items):
        line, col = self._extract_pos(items)
        return ast.Program(decls=items, line=line, column=col)

    def top_decl(self, items):
        return items[0]

    # Declarations
    def func_def(self, items):
        """Handles function definitions.

        Rule: FUNC return_type ARROW ID LPAR param_list? RPAR block
        """
        # items structure:
        # 1: return_type
        # 3: ID (function name)
        # 5: param_list (optional, if present)
        # last: block

        ret_type = items[1]
        func_name = str(items[3])

        # Check if param_list is present
        block_idx = len(items) - 1
        block = items[block_idx]

        params = []
        # FUNC RET ARROW ID LPAR PARAMS RPAR BLOCK = 8 items
        if len(items) > 7:
             # item 5 is param_list
             if isinstance(items[5], list):
                 params = items[5]

        return ast.FuncDef(name=func_name, return_type=ret_type, params=params, body=block, line=items[0].line, column=items[0].column)

    def return_type(self, items):
        # type | VOID_TYPE
        if isinstance(items[0], ast.Type):
            return items[0].name
        return str(items[0]) # "void"

    def type(self, items):
        # INT_TYPE | ...
        line, col = self._extract_pos(items)
        return ast.PrimitiveType(name=str(items[0]), line=line, column=col)

    def param_list(self, items):
        # param (COMMA param)*
        # Filter out commas
        return [item for item in items if isinstance(item, ast.Param)]

    def param(self, items):
        # type COLON ID
        # 0: type
        # 1: COLON
        # 2: ID
        line, col = self._extract_pos(items)
        return ast.Param(type_name=items[0].name, name=str(items[2]), line=line, column=col)

    def var_decl(self, items):
        """Handles variable declarations.

        Forms:
        1. VAR type COLON id_list SEMI
        2. VAR ID ASSIGN const_expr SEMI
        """
        # items[0] is VAR token

        if isinstance(items[1], ast.Type):
            # Case 1: var <type>: <id_list>;
            # 1: type, 2: COLON, 3: id_list, 4: SEMI
            line, col = self._extract_pos(items)
            return ast.VarDecl(type_name=items[1].name, names=items[3], line=line, column=col)
        else:
            # Case 2: var <name> = <const>;
            # 1: ID, 2: ASSIGN, 3: const_expr, 4: SEMI
            line, col = self._extract_pos(items)
            return ast.VarInit(name=str(items[1]), value=items[3], line=line, column=col)

    def id_list(self, items):
        # ID (COMMA ID)*
        return [str(item) for item in items if hasattr(item, 'type') and item.type == 'ID']

    def const_expr(self, items):
        # Returns a Literal
        # items[0] is one of INT_CONST, TRUE, etc.
        token = items[0]
        val = token.value
        t_type = token.type
        line, col = token.line, token.column
        
        if t_type == 'INT_CONST':
            return ast.Literal(value=int(val), type_name='int', line=line, column=col)
        elif t_type == 'REAL_CONST':
            return ast.Literal(value=float(val), type_name='real', line=line, column=col)
        elif t_type == 'STRING_CONST':
            return ast.Literal(value=py_ast.literal_eval(val), type_name='string', line=line, column=col)
        elif t_type == 'TRUE':
            return ast.Literal(value=True, type_name='bool', line=line, column=col)
        elif t_type == 'FALSE':
            return ast.Literal(value=False, type_name='bool', line=line, column=col)
        return ast.Literal(value=val, type_name='unknown', line=line, column=col)

    # Blocks & Stmts
    def block(self, items):
        # LBRACE stmt* RBRACE
        # Filter out braces
        stmts = [item for item in items if isinstance(item, ast.Stmt)]
        line, col = self._extract_pos(items)
        return ast.Block(stmts=stmts, line=line, column=col)

    def stmt(self, items):
        return items[0]

    def assign_stmt(self, items):
        # ID ASSIGN expr
        line, col = self._extract_pos(items)
        return ast.AssignStmt(name=str(items[0]), value=self._to_expr(items[2]), line=line, column=col)

    def proc_call(self, items):
        # ID LPAR arg_list? RPAR
        name = str(items[0])
        args = []
        if len(items) > 3: # ID LPAR args RPAR
             if isinstance(items[2], list):
                 args = items[2]
        line, col = self._extract_pos(items)
        return ast.ProcCallStmt(name=name, args=args, line=line, column=col)
        
    def arg_list(self, items):
         # expr (COMMA expr)*
         return [self._to_expr(item) for item in items if not (hasattr(item, 'type') and item.type == 'COMMA')]

    def return_stmt(self, items):
        # RETURN expr?
        # items[0] is RETURN
        val = None
        if len(items) > 1:
            val = self._to_expr(items[1])
        line, col = self._extract_pos(items)
        return ast.ReturnStmt(value=val, line=line, column=col)

    # I/O
    def output_stmt(self, items):
        # OUT io_args
        line, col = self._extract_pos(items)
        return ast.OutputStmt(is_newline=False, args=items[1], line=line, column=col)
        
    def outputln_stmt(self, items):
         # OUTLN io_args
         line, col = self._extract_pos(items)
         return ast.OutputStmt(is_newline=True, args=items[1], line=line, column=col)

    def input_stmt(self, items):
        # IN io_args
        line, col = self._extract_pos(items)
        return ast.InputStmt(args=items[1], line=line, column=col)

    def io_args(self, items):
        final_args = []
        idx = 0
        while idx < len(items):
            item = items[idx]
            is_hash = hasattr(item, "type") and item.type == "HASH"
            if is_hash and idx + 3 < len(items):
                t1 = items[idx + 1]
                mid = items[idx + 2]
                t3 = items[idx + 3]
                is_lpar = hasattr(t1, "type") and t1.type == "LPAR"
                is_rpar = hasattr(t3, "type") and t3.type == "RPAR"
                if is_lpar and is_rpar:
                    expr = self._to_expr(mid)
                    line, col = self._extract_pos([items[idx]])
                    final_args.append(ast.UnaryExpr(operator="#", operand=expr, line=line, column=col))
                    idx += 4
                    continue  # importante
            # fallback: singolo expr
            e = self._to_expr(item)
            if isinstance(e, ast.Expr):
                final_args.append(e)
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
        
        cond = items[2]
        then_blk = items[4]
        elifs = []
        else_blk = None
        
        for item in items[5:]:
             if isinstance(item, list): # elif_list returns list of ElifClause
                 elifs = item
             elif isinstance(item, ast.Block): # else_block returns Block
                 else_blk = item
        
        line, col = self._extract_pos(items)
        return ast.IfStmt(condition=cond, then_block=then_blk, elifs=elifs, else_block=else_blk, line=line, column=col)

    def elif_list(self, items):
        return items # Already a list of ElifClause

    def elif_clause(self, items):
        # ELIF LPAR expr RPAR block
        line, col = self._extract_pos(items)
        return ast.ElifClause(condition=items[2], block=items[4], line=line, column=col)

    def else_block(self, items):
        # ELSE block
        return items[1]

    def while_stmt(self, items):
        # WHILE LPAR expr RPAR block
        line, col = self._extract_pos(items)
        return ast.WhileStmt(condition=items[2], body=items[4], line=line, column=col)

    def for_stmt(self, items):
        """Handles for loops.

        Rule: FOR LPAR for_init? SEMI expr? SEMI for_update? RPAR block
        """
        init = None
        cond = None
        update = None
        body = None

        # 0: before 1st semi, 1: between semis, 2: after 2nd semi
        current_stage = 0

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

        line, col = self._extract_pos(items)
        return ast.ForStmt(init=init, condition=cond, update=update, body=body, line=line, column=col)

    def for_init(self, items):
        return items[0]
    def for_update(self, items):
        return items[0]

    # Expression wrappers
    def atomic_expr(self, items):
        return items[0]
    
    # Precedence levels - inlining
    def _to_expr(self, item):
        if hasattr(item, 'type'): # Token
             # Wrap in literal using logic from const_expr
             # Check type
             t_type = item.type
             val = item.value
             line, col = item.line, item.column
             if t_type == 'INT_CONST':
                 return ast.Literal(value=int(val), type_name='int', line=line, column=col)
             elif t_type == 'REAL_CONST':
                 return ast.Literal(value=float(val), type_name='real', line=line, column=col)
             elif t_type == 'STRING_CONST':
                 return ast.Literal(value=py_ast.literal_eval(val), type_name='string', line=line, column=col)
             elif t_type == 'TRUE':
                 return ast.Literal(value=True, type_name='bool', line=line, column=col)
             elif t_type == 'FALSE':
                 return ast.Literal(value=False, type_name='bool', line=line, column=col)
             
             return item 
        return item

    def _binary_op(self, items):
        # left op right
        # Ensure left/right are Expr
        left = self._to_expr(items[0])
        right = self._to_expr(items[2])
        line, col = self._extract_pos(items)
        return ast.BinaryExpr(left=left, operator=str(items[1]), right=right, line=line, column=col)

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
        line, col = self._extract_pos(items)
        return ast.UnaryExpr(operator=str(items[0]), operand=self._to_expr(items[1]), line=line, column=col)

    # Primary
    def primary(self, items):
        # Handle ( expr )
        if len(items) == 3 and getattr(items[0], 'type', None) == 'LPAR':
            return self._to_expr(items[1]) 
        return self._to_expr(items[0])

    def func_call(self, items):
        # ID LPAR arg_list? RPAR
        name = str(items[0])
        args = []
        if len(items) > 3:
             if isinstance(items[2], list):
                 args = items[2]
        line, col = self._extract_pos(items)
        return ast.FuncCallExpr(name=name, args=args, line=line, column=col)

    def var(self, items):
        line, col = self._extract_pos(items)
        return ast.VarRef(name=str(items[0]), line=line, column=col)
