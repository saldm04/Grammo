from dataclasses import dataclass, field
from typing import List, Optional, Union, Any

# ==========================================
# Abstract Base Class
# ==========================================

@dataclass(kw_only=True)
class Node:
    """Base class for all AST nodes."""
    line: int = 0
    column: int = 0

# ==========================================
# Type Nodes
# ==========================================

@dataclass(kw_only=True)
class Type(Node):
    name: str

@dataclass(kw_only=True)
class PrimitiveType(Type):
    pass

# We can instantiate these for easy use in comparisons, 
# or use them as factories from the parser.
# e.g. INT_TYPE = PrimitiveType("int")

# ==========================================
# Expressions
# ==========================================

@dataclass(kw_only=True)
class Expr(Node):
    """Base class for expressions."""
    pass

@dataclass(kw_only=True)
class Literal(Expr):
    value: Any
    type_name: str  # 'int', 'real', 'string', 'bool'

@dataclass(kw_only=True)
class VarRef(Expr):
    name: str

@dataclass(kw_only=True)
class BinaryExpr(Expr):
    left: Expr
    operator: str
    right: Expr

@dataclass(kw_only=True)
class UnaryExpr(Expr):
    operator: str
    operand: Expr

@dataclass(kw_only=True)
class FuncCallExpr(Expr):
    """Function call used as an expression (returns a value)."""
    name: str
    args: List[Expr] = field(default_factory=list)

# ==========================================
# Statements
# ==========================================

@dataclass(kw_only=True)
class Stmt(Node):
    """Base class for statements."""
    pass

@dataclass(kw_only=True)
class AssignStmt(Stmt):
    name: str
    value: Expr

@dataclass(kw_only=True)
class ProcCallStmt(Stmt):
    """Procedure call used as a statement (void return)."""
    name: str
    args: List[Expr] = field(default_factory=list)

@dataclass(kw_only=True)
class ReturnStmt(Stmt):
    value: Optional[Expr] = None

@dataclass(kw_only=True)
class Block(Stmt):
    stmts: List[Stmt] = field(default_factory=list)

@dataclass(kw_only=True)
class IfStmt(Stmt):
    condition: Expr
    then_block: Block
    # Elifs are handled as nested Ifs or list of (cond, block) pairs?
    # To match grammar structure (elif_list):
    elifs: List['ElifClause'] = field(default_factory=list) 
    else_block: Optional[Block] = None

@dataclass(kw_only=True)
class ElifClause(Node):
    condition: Expr
    block: Block

@dataclass(kw_only=True)
class WhileStmt(Stmt):
    condition: Expr
    body: Block

@dataclass(kw_only=True)
class ForStmt(Stmt):
    init: Optional[AssignStmt]
    condition: Optional[Expr]
    update: Optional[AssignStmt]
    body: Block

@dataclass(kw_only=True)
class IOArg(Node):
    """Argument for IO statements which can be an expression or specific formatting."""
    pass

@dataclass(kw_only=True)
class ExprArg(IOArg):
    expr: Expr

@dataclass(kw_only=True)
class OutputStmt(Stmt):
    is_newline: bool
    args: List[IOArg] = field(default_factory=list)

@dataclass(kw_only=True)
class InputStmt(Stmt):
    args: List[IOArg] = field(default_factory=list)

# ==========================================
# Declarations
# ==========================================

@dataclass(kw_only=True)
class Declaration(Stmt):
    pass

@dataclass(kw_only=True)
class VarDecl(Declaration):
    """
    Represents: var <type>: <id_list>;
    """
    type_name: str
    names: List[str]

@dataclass(kw_only=True)
class VarInit(Declaration):
    """
    Represents: var <name> = <const>;
    """
    name: str
    value: Literal # Grammar restricts this to Const

@dataclass(kw_only=True)
class Param(Node):
    name: str
    type_name: str

@dataclass(kw_only=True)
class FuncDef(Declaration):
    name: str
    return_type: str # 'void' or specific type
    params: List[Param]
    body: Block

@dataclass(kw_only=True)
class Program(Node):
    decls: List[Declaration]
