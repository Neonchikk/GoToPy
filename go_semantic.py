from typing import Optional, Dict, List
from go_ast import *
from go_symbols import *
from go_diagnostics import Diagnostics


class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.functions: Dict[str, Optional[str]] = {}
        self.current_function_return: Optional[str] = None  #
        self.diagnostics = Diagnostics()
        self.loop_depth = 0

    def error(self, msg: str, node: AstNode):
        """Регистрация ошибки с сообщением и узлом."""
        self.diagnostics.report_error(msg, node)

    def analyze(self, node: AstNode) -> bool:
        """Главный метод анализа, который обрабатывает узлы программы."""
        if isinstance(node, ProgramNode):
            for stmt in node.childs:
                self.analyze(stmt)  # Рекурсивно анализируем все операторы программы

        elif isinstance(node, VarDeclNode):
            self.analyze_var_decl(node)  # Анализ объявления переменной

        elif isinstance(node, AssignNode):
            self.analyze_assign(node)  # Анализ присваивания

        elif isinstance(node, BinOpNode):
            return self.analyze_binop(node)  # Анализ бинарной операции

        elif isinstance(node, UnOpNode):
            return self.analyze_unop(node)  # Анализ унарной операции

        elif isinstance(node, IfNode):
            self.analyze_if(node)  # Анализ оператора if

        elif isinstance(node, ForNode):
            self.analyze_for(node)  # Анализ цикла for

        elif isinstance(node, BlockNode):
            self.analyze_block(node)  # Анализ блока кода

        elif isinstance(node, FuncDeclNode):
            self.analyze_func_decl(node)  # Анализ объявления функции

        elif isinstance(node, FuncCallNode):
            return self.analyze_func_call(node)  # Анализ вызова функции

        elif isinstance(node, ReturnNode):
            self.analyze_return(node)  # Анализ оператора return

        elif isinstance(node, PrintNode):
            self.analyze_print(node)  # Анализ оператора печати

        elif isinstance(node, IdentNode):
            return self.analyze_ident(node)  # Анализ идентификатора

        elif isinstance(node, (NumNode, BoolNode)):
            return self.get_type_from_value(node)  # Получение типа из значения

        return not self.diagnostics.has_errors()  # Проверка наличия ошибок

    def analyze_var_decl(self, node: VarDeclNode):
        """Анализ объявления переменной."""
        if self.current_scope.lookup(node.name.name, current_scope_only=True):
            self.error(f"Duplicate variable '{node.name.name}'", node)
            return

        symbol = Symbol(node.name.name, node.type, 'local', node)
        self.current_scope.add(symbol)

        if node.value:
            value_type = self.analyze(node.value)  # Анализ значения при инициализации
            if value_type and not self.check_type_compatibility(node.type, value_type):
                self.error(f"Cannot assign {value_type} to {node.type}", node)

    def analyze_assign(self, node: AssignNode):
        """Анализ присваивания значения переменной."""
        target_type = self.analyze(node.target)
        value_type = self.analyze(node.value)

        if not target_type:
            self.error(f"Undefined variable '{node.target.name}'", node.target)
            return

        if value_type and not self.check_type_compatibility(target_type, value_type):
            self.error(f"Cannot assign {value_type} to {target_type}", node)

    def analyze_binop(self, node: BinOpNode) -> Optional[str]:
        """Анализ бинарной операции."""
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)

        if not left_type or not right_type:
            return None

        # Для операторов сравнения возвращаем bool
        if node.op in {BinOp.EQ, BinOp.NE, BinOp.LT, BinOp.LE, BinOp.GT, BinOp.GE}:
            if not self.check_type_compatibility(left_type, right_type, node.op):
                self.error(f"Cannot compare {left_type} with {right_type}", node)
                return None
            return 'bool'
        elif node.op in {BinOp.AND, BinOp.OR}:
            if left_type != 'bool' or right_type != 'bool':
                self.error(f"Logical operators require boolean operands", node)
                return None
            return 'bool'

        # Для арифметических операций
        if left_type == 'float' or right_type == 'float':
            return 'float'
        return 'int'

    def analyze_func_decl(self, node: FuncDeclNode):
        """Анализ объявления функции."""
        if node.name.name in self.functions:
            self.error(f"Duplicate function '{node.name.name}'", node.name)
            return

        self.functions[node.name.name] = node.return_type
        self.current_function_return = node.return_type

        func_scope = self.current_scope.create_child()
        self.current_scope = func_scope

        for param in node.params:
            symbol = Symbol(param.name.name, param.type, 'param', param)
            self.current_scope.add(symbol)

        self.analyze(node.body)  # Анализ тела функции

        if node.return_type and not self.has_return_statement(node.body):
            self.error(f"Function '{node.name.name}' missing return", node)

        self.current_scope = self.current_scope.parent
        self.current_function_return = None

    def analyze_func_call(self, node: FuncCallNode) -> Optional[str]:
        """Анализ вызова функции."""
        if node.name.name not in self.functions:
            self.error(f"Undefined function '{node.name.name}'", node.name)
            return None
        return self.functions[node.name.name]

    def analyze_return(self, node: ReturnNode):
        """Анализ оператора return."""
        if not self.current_function_return:
            if node.value:
                self.error("Return with value in void function", node)

        if not node.value:
            self.error("Missing return value", node)

        return_type = self.analyze(node.value)  # Получение типа возвращаемого значения
        if return_type and not self.check_type_compatibility(self.current_function_return, return_type):
            self.error(f"Return type mismatch: expected {self.current_function_return}, got {return_type}", node)

    def check_type_compatibility(self, target: str, source: str, op: Optional[BinOp] = None) -> bool:
        """Проверка совместимости типов."""
        if target == source:
            return True

        if target == 'float' and source == 'int':
            return True

        if op and op in {BinOp.EQ, BinOp.NE, BinOp.LT, BinOp.LE, BinOp.GT, BinOp.GE}:
            return (target in {'int', 'float'} and source in {'int', 'float'})

        return False

    def get_type_from_value(self, node: ValueNode) -> Optional[str]:
        """Определение типа значения."""
        if isinstance(node, NumNode):
            return 'float' if isinstance(node.value, float) else 'int'
        elif isinstance(node, BoolNode):
            return 'bool'  # Булевый тип
        elif isinstance(node, IdentNode):
            symbol = self.current_scope.lookup(node.name)
            return symbol.type if symbol else None
        return None

    def has_return_statement(self, node: AstNode) -> bool:
        """Проверка наличия оператора return в узле."""
        if isinstance(node, ReturnNode):
            return True

        if isinstance(node, IfNode):
            has_then = self.has_return_statement(node.then_block)
            has_else = self.has_return_statement(node.else_block) if node.else_block else False
            return has_then and has_else

        if hasattr(node, 'childs'):
            for child in node.childs:
                if self.has_return_statement(child):
                    return True
        return False

    def analyze_ident(self, node: IdentNode) -> Optional[str]:
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            # Если у самого узла нет позиций, используем переданные
            line = node.lineno if hasattr(node, 'lineno') else '?'
            column = node.column if hasattr(node, 'column') else '?'
            self.error(f"Undefined variable '{node.name}'", node)
        return symbol.type if symbol else None

    def analyze_block(self, node: BlockNode):
        """Анализ блока кода."""
        new_scope = self.current_scope.create_child()
        self.current_scope = new_scope

        for stmt in node.childs:
            self.analyze(stmt)

        self.current_scope = self.current_scope.parent

    def analyze_if(self, node: IfNode):
        """Анализ условного оператора if."""
        cond_type = self.analyze(node.cond)
        if cond_type != 'bool':
            self.error("Condition must be boolean", node.cond)

        self.analyze(node.then_block)
        if node.else_block:
            self.analyze(node.else_block)

    def analyze_for(self, node: ForNode):
        """Анализ цикла for."""
        self.loop_depth += 1

        if node.init:
            self.analyze(node.init)
        if node.cond:
            cond_type = self.analyze(node.cond)
            if cond_type != 'bool':
                self.error("Loop condition must be boolean", node.cond)
        if node.step:
            self.analyze(node.step)

        self.analyze(node.body)
        self.loop_depth -= 1

    def analyze_print(self, node: PrintNode):
        """Анализ оператора печати."""
        for arg in node.childs:
            self.analyze(arg)

    def analyze_unop(self, node: UnOpNode) -> Optional[str]:
        """Анализ унарной операции."""
        arg_type = self.analyze(node.arg)
        if not arg_type:
            return None

        if node.op == UnOp.NOT:
            if arg_type != 'bool':
                self.error("NOT operator requires boolean operand", node)
                return None
            return 'bool'
        else:  # UnOp.NEG
            if arg_type not in ('int', 'float'):
                self.error("NEG operator requires numeric operand", node)
                return None
            return arg_type