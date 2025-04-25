from go_ast import *


class SemanticError:
    def __init__(self, message: str, node: AstNode, severity: str = "error"):
        self.message = message
        self.severity = severity
        self.line = getattr(node, 'lineno', '?')
        self.column = getattr(node, 'column', '?')

        if self.line == '?' and hasattr(node, 'childs') and node.childs:
            first_child = node.childs[0]
            self.line = getattr(first_child, 'lineno', '?')
            self.column = getattr(first_child, 'column', '?')

    def __str__(self):
        return f"{self.severity.upper()} (line {self.line}, col {self.column}): {self.message}"

class Diagnostics:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def report_error(self, message: str, node: AstNode):
        self.errors.append(SemanticError(message, node, "error"))

    def report_warning(self, message: str, node: AstNode):
        self.warnings.append(SemanticError(message, node, "warning"))

    def print_errors(self):
        for err in self.errors + self.warnings:
            print(str(err))

    def has_errors(self) -> bool:
        return any(e.severity == "error" for e in self.errors)