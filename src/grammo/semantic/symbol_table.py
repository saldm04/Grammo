from dataclasses import dataclass
from typing import Dict, Optional, List

@dataclass
class Symbol:
    """Base class for all symbols in the symbol table.

    Attributes:
        name: The name of the symbol.
        type_name: The type of the symbol (e.g., "int", "void", "func").
    """
    name: str
    type_name: str

@dataclass
class VarSymbol(Symbol):
    """Represents a variable symbol."""
    pass

@dataclass
class FuncSymbol(Symbol):
    """Represents a function symbol.

    Attributes:
        param_types: A list of parameter type names.
        return_type: The return type of the function.
    """
    param_types: List[str]
    return_type: str

class SymbolTable:
    """Manages symbols and scopes for semantic analysis.

    Supports nested scopes (global -> local -> block).
    """

    def __init__(self):
        """Initializes the symbol table with a global scope."""
        # scopes[0] is Global
        self.scopes: List[Dict[str, Symbol]] = [{}]

    def enter_scope(self):
        """Enters a new nested scope."""
        self.scopes.append({})

    def exit_scope(self):
        """Exits the current scope.

        Does nothing if attempting to exit the global scope.
        """
        if len(self.scopes) > 1:
            self.scopes.pop()

    def insert(self, symbol: Symbol) -> bool:
        """Inserts a symbol into the current scope.

        Args:
            symbol: The symbol to insert.

        Returns:
            bool: True if insertion was successful, False if a collision occurred in the current scope.
        """
        current = self.scopes[-1]
        if symbol.name in current:
            # Check for allowed shadowing?
            # User said "One level of scope".
            # We treat collision as error.
            return False
        current[symbol.name] = symbol
        return True

    def lookup(self, name: str) -> Optional[Symbol]:
        """Looks up a symbol by name, searching from the innermost to the outermost scope.

        Args:
            name: The name of the symbol to look up.

        Returns:
            Optional[Symbol]: The found symbol, or None if not found.
        """
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def __repr__(self):
        return f"SymbolTable(depth={len(self.scopes)})"
