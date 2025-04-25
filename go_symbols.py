from go_ast import *
class Symbol:
    def __init__(self, name: str, type_: str, scope: str, node: AstNode):
        self.name = name
        self.type = type_
        self.scope = scope
        self.node = node

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def lookup(self, name: str, current_scope_only=False) -> Optional[Symbol]:
        symbol = self.symbols.get(name)
        if symbol:
            return symbol
        if self.parent and not current_scope_only:
            return self.parent.lookup(name)
        return None

    def create_child(self) -> 'SymbolTable':
        child_scope = SymbolTable()
        child_scope.parent = self
        return child_scope

    def add(self, symbol: Symbol):
        if symbol.name in self.symbols and self.symbols[symbol.name].scope == symbol.scope:
            raise ValueError(f"Shadowing detected for '{symbol.name}'")
        self.symbols[symbol.name] = symbol