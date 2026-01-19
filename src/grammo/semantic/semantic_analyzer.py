import sys
from . import ast_nodes as ast
from .symbol_table import SymbolTable, VarSymbol, FuncSymbol, Symbol

class SemanticError(Exception):
    """Exception raised for semantic analysis errors."""
    pass

class SemanticAnalyzer:
    """Performs semantic analysis on the AST.

    Checks for:
    - Undeclared variables/functions.
    - Type mismatches.
    - Control flow issues (e.g. missing returns).
    - Scope rules.
    """

    def __init__(self):
        """Initializes the semantic analyzer with an empty symbol table."""
        self.symbol_table = SymbolTable()
        self.current_func_ret_type = None
        self.errors = []

    def error(self, msg: str, node: ast.Node = None):
        """Raises a SemanticError with the given message and node location."""
        full_msg = f"Semantic Error: {msg}"
        if node and hasattr(node, 'line') and node.line != 0:
             full_msg += f" (near line {node.line})"
        raise SemanticError(full_msg)

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit method for {node.__class__.__name__}")

    # ==========================
    # Top Level Helper
    # ==========================

    def analyze(self, program_node: ast.Program):
        """Runs the semantic analysis on the program.

        Args:
            program_node (ast.Program): The root AST node.
        """
        # Pass 1: Register all global functions and variables
        for decl in program_node.decls:
            if isinstance(decl, ast.FuncDef):
                self._register_func_signature(decl)
            elif isinstance(decl, (ast.VarDecl, ast.VarInit)):
                self.visit(decl) # Validates and adds to symbol table
        
        # Check for Main
        main_sym = self.symbol_table.lookup("main")
        if not isinstance(main_sym, FuncSymbol):
            self.error("Missing 'main' function.")
        if main_sym.return_type != 'void':
             self.error(f"'main' function must return void, got {main_sym.return_type}")
        if len(main_sym.param_types) > 0:
             self.error("'main' function must take no parameters.")

        # Pass 2: Analyze Function Bodies
        for decl in program_node.decls:
            if isinstance(decl, ast.FuncDef):
                self._analyze_func_body(decl)

    def _register_func_signature(self, node: ast.FuncDef):
        if self.symbol_table.lookup(node.name):
            self.error(f"Function/Identifier '{node.name}' already declared.", node)
        
        param_types = [p.type_name for p in node.params]
        sym = FuncSymbol(name=node.name, type_name="func", param_types=param_types, return_type=node.return_type)
        self.symbol_table.insert(sym)

    def _analyze_func_body(self, node: ast.FuncDef):
        self.symbol_table.enter_scope()

        for param in node.params:
            if self.symbol_table.lookup(param.name):
                self.error(f"Parameter '{param.name}' collides with existing symbol.", node)
            
            p_sym = VarSymbol(name=param.name, type_name=param.type_name)
            self.symbol_table.insert(p_sym)

        self.current_func_ret_type = node.return_type
        self.visit(node.body)
        self.current_func_ret_type = None
        
        if node.return_type != 'void':
            if not self._check_all_paths_return(node.body):
                self.error(f"Function '{node.name}' (type {node.return_type}) does not return a value in all code paths.", node)

        self.symbol_table.exit_scope()

    def _check_all_paths_return(self, node: ast.Node) -> bool:
        """Recursively checks if the statement/block guarantees a return."""
        if isinstance(node, ast.ReturnStmt):
            return True
        
        if isinstance(node, ast.Block):
            for stmt in node.stmts:
                if self._check_all_paths_return(stmt):
                    return True
            return False
        
        if isinstance(node, ast.IfStmt):
            if not node.else_block:
                return False
            
            if not self._check_all_paths_return(node.then_block):
                return False
            
            if not self._check_all_paths_return(node.else_block):
                return False
            
            for elif_clause in node.elifs:
                if not self._check_all_paths_return(elif_clause.block):
                   return False
                   
            return True
            
        return False

    # ==========================
    # Declarations
    # ==========================
    
    def visit_VarDecl(self, node: ast.VarDecl):
        for name in node.names:
            if self.symbol_table.lookup(name):
                self.error(f"Variable '{name}' already declared.", node)
            sym = VarSymbol(name=name, type_name=node.type_name)
            self.symbol_table.insert(sym)

    def visit_VarInit(self, node: ast.VarInit):
        if self.symbol_table.lookup(node.name):
            self.error(f"Variable '{node.name}' already declared.", node)
            
        val_node = node.value
        type_name = val_node.type_name
        sym = VarSymbol(name=node.name, type_name=type_name)
        self.symbol_table.insert(sym)

    def visit_FuncDef(self, node: ast.FuncDef):
        pass

    # ==========================
    # Statements
    # ==========================

    def visit_Block(self, node: ast.Block):
        for stmt in node.stmts:
            self.visit(stmt)

    def visit_AssignStmt(self, node: ast.AssignStmt):
        sym = self.symbol_table.lookup(node.name)
        if not sym:
            self.error(f"Variable '{node.name}' not declared.", node)
        if not isinstance(sym, VarSymbol):
            self.error(f"Cannot assign to '{node.name}' (not a variable).", node)
        
        rhs_type = self.visit(node.value)
        
        if not self._check_compatibility(sym.type_name, rhs_type):
            self.error(f"Type mismatch in assignment to '{node.name}': expected {sym.type_name}, got {rhs_type}", node)

    def visit_ProcCallStmt(self, node: ast.ProcCallStmt):
        sym = self.symbol_table.lookup(node.name)
        if not sym:
            self.error(f"Procedure '{node.name}' not declared.", node)
        if not isinstance(sym, FuncSymbol):
             self.error(f"'{node.name}' is not a procedure/function.", node)
        
        if sym.return_type != 'void':
             self.error(f"Function '{node.name}' returns {sym.return_type}, but called as statement (ignored return value).", node)
        
        self._check_args(sym, node.args, node)

    def visit_ReturnStmt(self, node: ast.ReturnStmt):
        expected = self.current_func_ret_type
        if not expected:
            self.error("Return statement outside function.", node)
        
        if expected == 'void':
            if node.value is not None:
                self.error("Void function cannot return a value.", node)
        else:
            if node.value is None:
                self.error(f"non-void function must return value of type {expected}.", node)
            
            got_type = self.visit(node.value)
            if not self._check_compatibility(expected, got_type):
                self.error(f"Return type mismatch: expected {expected}, got {got_type}", node)

    def visit_IfStmt(self, node: ast.IfStmt):
        cond_type = self.visit(node.condition)
        if cond_type != 'bool':
             self.error(f"If condition must be bool, got {cond_type}", node)
        
        self.visit(node.then_block)
        for elif_clause in node.elifs:
            self.visit(elif_clause)
        if node.else_block:
            self.visit(node.else_block)

    def visit_ElifClause(self, node: ast.ElifClause):
        cond_type = self.visit(node.condition)
        if cond_type != 'bool':
             self.error(f"Elif condition must be bool, got {cond_type}", node)
        self.visit(node.block)

    def visit_WhileStmt(self, node: ast.WhileStmt):
        cond_type = self.visit(node.condition)
        if cond_type != 'bool':
            self.error(f"While condition must be bool, got {cond_type}", node)
        self.visit(node.body)

    def visit_ForStmt(self, node: ast.ForStmt):
        if node.init: self.visit(node.init)
        if node.condition:
            cond_type = self.visit(node.condition)
            if cond_type != 'bool':
                self.error(f"For condition must be bool, got {cond_type}", node)
        
        if node.update: self.visit(node.update)
        self.visit(node.body)

    def visit_OutputStmt(self, node: ast.OutputStmt):
        for arg in node.args:
            if isinstance(arg, ast.UnaryExpr) and arg.operator == '#':
                 self.visit(arg.operand)
            elif isinstance(arg, ast.Expr):
                 self.visit(arg)
            else:
                 pass

    def visit_InputStmt(self, node: ast.InputStmt):
        for arg in node.args:
            if isinstance(arg, ast.UnaryExpr) and arg.operator == '#':
                target = arg.operand
                if not isinstance(target, ast.VarRef):
                     self.error("Input target #(...) must be a variable identifier.", node)
                
                sym = self.symbol_table.lookup(target.name)
                if not sym:
                    self.error(f"Input variable '{target.name}' not declared.", node)
                if not isinstance(sym, VarSymbol):
                    self.error(f"Input target '{target.name}' is not a variable.", node)
                
            elif isinstance(arg, ast.Expr):
                t = self.visit(arg)
                if t != 'string':
                     self.error(f"Input prompt must be string, got {t}", node)

    # ==========================
    # Expressions
    # ==========================

    def visit_Literal(self, node: ast.Literal):
        return node.type_name

    def visit_VarRef(self, node: ast.VarRef):
        sym = self.symbol_table.lookup(node.name)
        if not sym:
            self.error(f"Variable '{node.name}' not declared.", node)
        if not isinstance(sym, VarSymbol):
             self.error(f"'{node.name}' is not a variable.", node)
        return sym.type_name

    def visit_BinaryExpr(self, node: ast.BinaryExpr):
        l_type = self.visit(node.left)
        r_type = self.visit(node.right)
        op = node.operator

        if op in ['+', '-', '*', '/']:
            if l_type == 'int' and r_type == 'int': return 'int'
            if l_type == 'real' and r_type == 'real': return 'real'
            if (l_type == 'int' and r_type == 'real') or (l_type == 'real' and r_type == 'int'):
                 return 'real'
            if op == '+' and l_type == 'string' and r_type == 'string':
                 return 'string'
            
            self.error(f"Invalid types for operator '{op}': {l_type}, {r_type}", node)
        
        if op in ['&&', '||']:
            if l_type == 'bool' and r_type == 'bool': return 'bool'
            self.error(f"Invalid types for logic '{op}': {l_type}, {r_type}", node)
            
        if op in ['==', '<>', '<', '<=', '>', '>=']:
            if op in ['==', '<>']:
                if self._check_compatibility(l_type, r_type) or self._check_compatibility(r_type, l_type):
                    return 'bool'
            if l_type in ['int', 'real'] and r_type in ['int', 'real']:
                 return 'bool'
            self.error(f"Invalid types for comparison '{op}': {l_type}, {r_type}", node)
            
        return 'unknown'

    def visit_UnaryExpr(self, node: ast.UnaryExpr):
        op = node.operator
        t = self.visit(node.operand)
        
        if op == '!':
            if t == 'bool': return 'bool'
        elif op == '-':
            if t in ['int', 'real']: return t
        
        self.error(f"Invalid type for unary '{op}': {t}", node)

    def visit_FuncCallExpr(self, node: ast.FuncCallExpr):
        sym = self.symbol_table.lookup(node.name)
        if not sym:
            self.error(f"Function '{node.name}' not declared.", node)
        if not isinstance(sym, FuncSymbol):
             self.error(f"'{node.name}' is not a function.", node)
        
        if sym.return_type == 'void':
            self.error(f"Void function '{node.name}' cannot be used as expression.", node)
            
        self._check_args(sym, node.args, node)
        return sym.return_type

    # ==========================
    # Helpers
    # ==========================

    def _check_compatibility(self, target: str, source: str) -> bool:
        if target == source: return True
        if target == 'real' and source == 'int': return True
        return False

    def _check_args(self, func_sym: FuncSymbol, args: list, node):
        if len(args) != len(func_sym.param_types):
            self.error(f"Function '{func_sym.name}' expects {len(func_sym.param_types)} args, got {len(args)}", node)
        
        for i, arg in enumerate(args):
            expected = func_sym.param_types[i]
            got = self.visit(arg)
            if not self._check_compatibility(expected, got):
                self.error(f"Argument {i+1} mismatch: expected {expected}, got {got}", node)
