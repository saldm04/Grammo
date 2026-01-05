from dataclasses import dataclass, field
from typing import List, Optional, Union, Any

# ==========================================
# Abstract Base Class
# ==========================================

@dataclass(kw_only=True)
class Node:
    """Base class for all AST nodes.

    Attributes:
        line: The line number where the node starts.
        column: The column number where the node starts.
    """
    line: int = 0
    column: int = 0

# ==========================================
# Type Nodes
# ==========================================

@dataclass(kw_only=True)
class Type(Node):
    """Represents a type in the AST.

    Attributes:
        name: The name of the type.
    """
    name: str

@dataclass(kw_only=True)
class PrimitiveType(Type):
    """Represents a primitive type (e.g., int, bool)."""
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
    """Represents a literal value.

    Attributes:
        value: The value of the literal.
        type_name: The type of the literal ('int', 'real', 'string', 'bool').
    """
    value: Any
    type_name: str  # 'int', 'real', 'string', 'bool'

@dataclass(kw_only=True)
class VarRef(Expr):
    """Represents a variable reference.

    Attributes:
        name: The name of the referenced variable.
    """
    name: str

@dataclass(kw_only=True)
class BinaryExpr(Expr):
    """Represents a binary expression.

    Attributes:
        left: The left operand.
        operator: The operator symbol.
        right: The right operand.
    """
    left: Expr
    operator: str
    right: Expr

@dataclass(kw_only=True)
class UnaryExpr(Expr):
    """Represents a unary expression.

    Attributes:
        operator: The operator symbol.
        operand: The operand expression.
    """
    operator: str
    operand: Expr

@dataclass(kw_only=True)
class FuncCallExpr(Expr):
    """Function call used as an expression (returns a value).

    Attributes:
        name: The name of the function being called.
        args: A list of argument expressions.
    """
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
    """Represents an assignment statement.

    Attributes:
        name: The name of the variable being assigned to.
        value: The expression evaluating to the value to assign.
    """
    name: str
    value: Expr

@dataclass(kw_only=True)
class ProcCallStmt(Stmt):
    """Procedure call used as a statement (void return).

    Attributes:
        name: The name of the procedure being called.
        args: A list of argument expressions.
    """
    name: str
    args: List[Expr] = field(default_factory=list)

@dataclass(kw_only=True)
class ReturnStmt(Stmt):
    """Represents a return statement.

    Attributes:
        value: The return value expression, or None if void.
    """
    value: Optional[Expr] = None

@dataclass(kw_only=True)
class Block(Stmt):
    """Represents a block of statements.

    Attributes:
        stmts: A list of statements in the block.
    """
    stmts: List[Stmt] = field(default_factory=list)

@dataclass(kw_only=True)
class IfStmt(Stmt):
    """Represents an if statement.

    Attributes:
        condition: The if condition.
        then_block: The block to execute if the condition is true.
        elifs: A list of elif clauses.
        else_block: The block to execute if no condition is true (optional).
    """
    condition: Expr
    then_block: Block
    # Elifs are handled as nested Ifs or list of (cond, block) pairs?
    # To match grammar structure (elif_list):
    elifs: List['ElifClause'] = field(default_factory=list)
    else_block: Optional[Block] = None

@dataclass(kw_only=True)
class ElifClause(Node):
    """Represents an elif clause in an if statement.

    Attributes:
        condition: The elif condition.
        block: The block to execute if the condition is true.
    """
    condition: Expr
    block: Block

@dataclass(kw_only=True)
class WhileStmt(Stmt):
    """Represents a while statement.

    Attributes:
        condition: The loop condition.
        body: The block to execute while the condition is true.
    """
    condition: Expr
    body: Block

@dataclass(kw_only=True)
class ForStmt(Stmt):
    """Represents a for statement.

    Attributes:
        init: The initialization statement.
        condition: The loop condition.
        update: The update statement.
        body: The loop body block.
    """
    init: Optional[AssignStmt]
    condition: Optional[Expr]
    update: Optional[AssignStmt]
    body: Block

@dataclass(kw_only=True)
class OutputStmt(Stmt):
    """Represents an output statement (print).

    Attributes:
        is_newline: Whether to print a newline at the end.
        args: A list of expressions to print.
    """
    is_newline: bool
    args: List[Expr] = field(default_factory=list)

@dataclass(kw_only=True)
class InputStmt(Stmt):
    """Represents an input statement.

    Attributes:
        args: A list of arguments for input.
    """
    args: List[Expr] = field(default_factory=list)

# ==========================================
# Declarations
# ==========================================

@dataclass(kw_only=True)
class Declaration(Stmt):
    pass

@dataclass(kw_only=True)
class VarDecl(Declaration):
    """Represents a variable declaration: var <type>: <id_list>;

    Attributes:
        type_name: The type of the variables.
        names: A list of variable names.
    """
    type_name: str
    names: List[str]

@dataclass(kw_only=True)
class VarInit(Declaration):
    """Represents a variable initialization: var <name> = <const>;

    Attributes:
        name: The name of the variable.
        value: The initial value (must be a literal/const).
    """
    name: str
    value: Literal # Grammar restricts this to Const

@dataclass(kw_only=True)
class Param(Node):
    """Represents a function parameter.

    Attributes:
        name: The name of the parameter.
        type_name: The type of the parameter.
    """
    name: str
    type_name: str

@dataclass(kw_only=True)
class FuncDef(Declaration):
    """Represents a function definition.

    Attributes:
        name: The name of the function.
        return_type: The return type of the function ('void' or specific type).
        params: A list of parameters.
        body: The function body block.
    """
    name: str
    return_type: str # 'void' or specific type
    params: List[Param]
    body: Block

@dataclass(kw_only=True)
class Program(Node):
    """Represents a complete program.

    Attributes:
        decls: A list of top-level declarations (vars, functions).
    """
    decls: List[Declaration]
