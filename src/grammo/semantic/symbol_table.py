from dataclasses import dataclass
from typing import Dict, Optional, List

@dataclass
class Symbol:
    name: str
    type_name: str # e.g. "int", "void", "func"

@dataclass
class VarSymbol(Symbol):
    pass

@dataclass
class FuncSymbol(Symbol):
    param_types: List[str]
    return_type: str

class SymbolTable:
    def __init__(self):
        # scopes[0] is Global
        self.scopes: List[Dict[str, Symbol]] = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def insert(self, symbol: Symbol) -> bool:
        """
        Inserts a symbol into the current scope.
        Returns False if collision in CURRENT scope.
        """
        current = self.scopes[-1]
        if symbol.name in current:
            # Check for allowed shadowing?
            # User said "One level of scope" -> "dichiarazioni multiple dello stesso identificatore".
            # We treat collision as error.
            return False
        current[symbol.name] = symbol
        return True

    def lookup(self, name: str) -> Optional[Symbol]:
        """Looks up a symbol, searching from logical inner to outer."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def __repr__(self):
        return f"SymbolTable(depth={len(self.scopes)})"
