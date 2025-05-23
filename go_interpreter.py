from typing import Dict, Any, Optional
from go_ast import *

class InterpreterError(Exception):
    pass

class Environment:
    def __init__(self, parent=None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent

    def get(self, name: str) -> Any:
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise InterpreterError(f"Undefined variable: {name}")

    def set(self, name: str, value: Any):
        self.variables[name] = value

class Interpreter:
    def __init__(self):
        self.environment = Environment()
        self.return_value = None
        self.should_return = False

    def interpret(self, node: AstNode) -> Any:
        if isinstance(node, ProgramNode):
            return self.visit_program(node)
        elif isinstance(node, BlockNode):
            return self.visit_block(node)
        elif isinstance(node, VarDeclNode):
            return self.visit_var_decl(node)
        elif isinstance(node, AssignNode):
            return self.visit_assign(node)
        elif isinstance(node, IfNode):
            return self.visit_if(node)
        elif isinstance(node, ForNode):
            return self.visit_for(node)
        elif isinstance(node, WhileNode):
            return self.visit_while(node)
        elif isinstance(node, PrintNode):
            return self.visit_print(node)
        elif isinstance(node, BinOpNode):
            return self.visit_bin_op(node)
        elif isinstance(node, UnOpNode):
            return self.visit_un_op(node)
        elif isinstance(node, NumNode):
            return node.value
        elif isinstance(node, BoolNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, IdentNode):
            return self.environment.get(node.name)
        elif isinstance(node, FuncDeclNode):
            return self.visit_func_decl(node)
        elif isinstance(node, FuncCallNode):
            return self.visit_func_call(node)
        elif isinstance(node, ReturnNode):
            return self.visit_return(node)
        else:
            raise InterpreterError(f"Unknown node type: {type(node)}")

    def visit_program(self, node: ProgramNode) -> Any:
        result = None
        for statement in node.statements:
            result = self.interpret(statement)
        return result

    def visit_block(self, node: BlockNode) -> Any:
        result = None
        for statement in node.statements:
            result = self.interpret(statement)
            if self.should_return:
                return self.return_value
        return result

    def visit_var_decl(self, node: VarDeclNode) -> Any:
        value = self.interpret(node.value) if node.value else None
        self.environment.set(node.name.name, value)
        return value

    def visit_assign(self, node: AssignNode) -> Any:
        value = self.interpret(node.value)
        self.environment.set(node.target.name, value)
        return value

    def visit_if(self, node: IfNode) -> Any:
        condition = self.interpret(node.cond)
        if condition:
            return self.interpret(node.then_block)
        elif node.else_block:
            return self.interpret(node.else_block)
        return None

    def visit_for(self, node: ForNode) -> Any:
        if node.init:
            self.interpret(node.init)
        
        while True:
            if node.cond:
                condition = self.interpret(node.cond)
                if not condition:
                    break
            
            self.interpret(node.body)
            
            if node.step:
                self.interpret(node.step)

    def visit_while(self, node: WhileNode) -> Any:
        while self.interpret(node.cond):
            result = self.interpret(node.body)
            if self.should_return:
                return self.return_value
        return None

    def visit_print(self, node: PrintNode) -> Any:
        values = []
        for arg in node.args:
            value = self.interpret(arg)
            if isinstance(value, bool):
                values.append(str(value).lower())
            else:
                values.append(str(value))
        print(*values)
        return None

    def visit_bin_op(self, node: BinOpNode) -> Any:
        left = self.interpret(node.left)
        right = self.interpret(node.right)
        
        if node.op == BinOp.ADD:
            if isinstance(left, str) or isinstance(right, str):
                if isinstance(left, str):
                    left = left.replace('\\n', '\n')
                if isinstance(right, str):
                    right = right.replace('\\n', '\n')
                result = str(left) + str(right)
                return result
            result = left + right
            return result
        elif node.op == BinOp.SUB:
            if isinstance(left, str) or isinstance(right, str):
                raise InterpreterError("Cannot subtract strings")
            return left - right
        elif node.op == BinOp.MUL:
            if isinstance(left, str) or isinstance(right, str):
                raise InterpreterError("Cannot multiply strings")
            return left * right
        elif node.op == BinOp.DIV:
            if isinstance(left, str) or isinstance(right, str):
                raise InterpreterError("Cannot divide strings")
            if right == 0:
                raise InterpreterError("Division by zero")
            return left / right
        elif node.op == BinOp.MOD:
            if isinstance(left, str) or isinstance(right, str):
                raise InterpreterError("Cannot use modulo with strings")
            if right == 0:
                raise InterpreterError("Modulo by zero")
            return left % right
        elif node.op == BinOp.EQ:
            return left == right
        elif node.op == BinOp.NE:
            return left != right
        elif node.op == BinOp.LT:
            if isinstance(left, str) and isinstance(right, str):
                return left < right
            if isinstance(left, str) or isinstance(right, str):
                raise InterpreterError("Cannot compare strings with numbers")
            return left < right
        elif node.op == BinOp.LE:
            if isinstance(left, str) and isinstance(right, str):
                return left <= right
            if isinstance(left, str) or isinstance(right, str):
                raise InterpreterError("Cannot compare strings with numbers")
            return left <= right
        elif node.op == BinOp.GT:
            if isinstance(left, str) and isinstance(right, str):
                return left > right
            if isinstance(left, str) or isinstance(right, str):
                raise InterpreterError("Cannot compare strings with numbers")
            return left > right
        elif node.op == BinOp.GE:
            if isinstance(left, str) and isinstance(right, str):
                return left >= right
            if isinstance(left, str) or isinstance(right, str):
                raise InterpreterError("Cannot compare strings with numbers")
            return left >= right
        elif node.op == BinOp.AND:
            if isinstance(left, str) or isinstance(right, str):
                raise InterpreterError("Cannot use logical operators with strings")
            return left and right
        elif node.op == BinOp.OR:
            if isinstance(left, str) or isinstance(right, str):
                raise InterpreterError("Cannot use logical operators with strings")
            return left or right
        else:
            raise InterpreterError(f"Unknown binary operator: {node.op}")

    def visit_un_op(self, node: UnOpNode) -> Any:
        value = self.interpret(node.arg)
        
        if node.op == UnOp.NEG:
            return -value
        elif node.op == UnOp.NOT:
            return not value
        else:
            raise InterpreterError(f"Unknown unary operator: {node.op}")

    def visit_func_decl(self, node: FuncDeclNode) -> Any:
        self.environment.set(node.name.name, node)
        return None

    def visit_func_call(self, node: FuncCallNode) -> Any:
        func = self.environment.get(node.name.name)
        if not isinstance(func, FuncDeclNode):
            raise InterpreterError(f"{node.name.name} is not a function")
        func_env = Environment(self.environment)
        args = [self.interpret(arg) for arg in node.args]
        for param, arg in zip(func.params, args):
            func_env.set(param.name.name, arg)
        old_env = self.environment
        old_should_return = self.should_return
        old_return_value = self.return_value
        self.environment = func_env
        self.should_return = False
        self.return_value = None
        try:
            result = self.interpret(func.body)
            if self.should_return:
                result = self.return_value
            return result
        finally:
            self.environment = old_env
            self.should_return = old_should_return
            self.return_value = old_return_value

    def visit_return(self, node: ReturnNode) -> Any:
        if node.value:
            self.return_value = self.interpret(node.value)
        else:
            self.return_value = None
        self.should_return = True
        return self.return_value 