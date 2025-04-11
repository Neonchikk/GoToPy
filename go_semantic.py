from typing import Optional, Dict, List
from go_ast import *


class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.functions: Dict[str, Optional[str]] = {}  # {name: return_type}
        self.current_function_return: Optional[str] = None
        self.errors: List[str] = []
        self.loop_depth = 0  # Для проверки break/continue

    def error(self, msg: str, node: AstNode):
        line = getattr(node, 'lineno', '?')
        self.errors.append(f"msg}")

    def analyze(self, node: AstNode) -> bool:
        """Основной метод анализа. Возвращает True если нет ошибок"""
        if isinstance(node, ProgramNode):
            for stmt in node.childs:
                self.analyze(stmt)

        elif isinstance(node, VarDeclNode):
            self.analyze_var_decl(node)

        elif isinstance(node, AssignNode):
            self.analyze_assign(node)

        elif isinstance(node, BinOpNode):
            return self.analyze_binop(node)

        elif isinstance(node, UnOpNode):
            return self.analyze_unop(node)

        elif isinstance(node, IfNode):
            self.analyze_if(node)

        elif isinstance(node, ForNode):
            self.analyze_for(node)

        elif isinstance(node, BlockNode):
            self.analyze_block(node)

        elif isinstance(node, FuncDeclNode):
            self.analyze_func_decl(node)

        elif isinstance(node, FuncCallNode):
            return self.analyze_func_call(node)

        elif isinstance(node, ReturnNode):
            self.analyze_return(node)

        elif isinstance(node, PrintNode):
            self.analyze_print(node)

        elif isinstance(node, IdentNode):
            return self.analyze_ident(node)

        elif isinstance(node, (NumNode, BoolNode)):
            return self.get_type_from_value(node)

        return len(self.errors) == 0

    # ========== Основные методы анализа ==========

    def analyze_var_decl(self, node: VarDeclNode):
        """Проверка объявления переменной"""
        if self.current_scope.lookup(node.name.name, current_scope_only=True):
            self.error(f"Duplicate variable '{node.name.name}'", node)
            return

        symbol = Symbol(node.name.name, node.type, 'local', node)
        self.current_scope.add(symbol)

        if node.value:
            value_type = self.analyze(node.value)
            if value_type and not self.check_type_compatibility(node.type, value_type):
                self.error(f"Cannot assign {value_type} to {node.type}", node)

    def analyze_assign(self, node: AssignNode):
        """Проверка присваивания"""
        target_type = self.analyze(node.target)
        value_type = self.analyze(node.value)

        if not target_type:
            self.error(f"Undefined variable '{node.target.name}'", node.target)
            return

        if value_type and not self.check_type_compatibility(target_type, value_type):
            self.error(f"Cannot assign {value_type} to {target_type}", node)

    def analyze_binop(self, node: BinOpNode) -> Optional[str]:
        """Проверка бинарных операций и определение типа результата"""
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)

        if not left_type or not right_type:
            return None

        # Проверка совместимости типов
        if not self.check_type_compatibility(left_type, right_type, node.op):
            self.error(f"Operation {node.op} between {left_type} and {right_type}", node)
            return None

        # Определение типа результата
        if node.op in {BinOp.AND, BinOp.OR}:
            return 'bool'
        elif node.op in {BinOp.EQ, BinOp.NE, BinOp.LT, BinOp.LE, BinOp.GT, BinOp.GE}:
            return 'bool'
        else:
            return left_type  # Для арифметических операций тип = тип операндов

    def analyze_func_decl(self, node: FuncDeclNode):
        """Проверка объявления функции"""
        if node.name.name in self.functions:
            self.error(f"Duplicate function '{node.name.name}'", node.name)
            return

        self.functions[node.name.name] = node.return_type
        self.current_function_return = node.return_type

        # Новая область видимости для функции
        func_scope = self.current_scope.create_child()
        self.current_scope = func_scope

        # Добавляем параметры в область видимости
        for param in node.params:
            symbol = Symbol(param.name.name, param.type, 'param', param)
            self.current_scope.add(symbol)

        # Анализируем тело функции
        self.analyze(node.body)

        # Проверка возврата в функциях с возвращаемым значением
        if node.return_type and not self.has_return_statement(node.body):
            self.error(f"Function '{node.name.name}' missing return", node)

        self.current_scope = self.current_scope.parent
        self.current_function_return = None

    def analyze_func_call(self, node: FuncCallNode) -> Optional[str]:
        """Проверка вызова функции и определение типа результата"""
        if node.name.name not in self.functions:
            self.error(f"Undefined function '{node.name.name}'", node.name)
            return None

        # TODO: Проверка количества и типов аргументов
        return self.functions[node.name.name]

    def analyze_return(self, node: ReturnNode):
        """Проверка return"""
        if not self.current_function_return:
            if node.value:
                self.error("Return with value in void function", node)
            return

        if not node.value:
            self.error("Missing return value", node)
            return

        return_type = self.analyze(node.value)
        if return_type and not self.check_type_compatibility(self.current_function_return, return_type):
            self.error(f"Return type mismatch: expected {self.current_function_return}, got {return_type}", node)

    # ========== Вспомогательные методы ==========

    def check_type_compatibility(self, target: str, source: str, op: Optional[BinOp] = None) -> bool:
        """Проверка совместимости типов с учетом операций"""
        if target == source:
            return True

        # Разрешаем неявное приведение int -> float
        if target == 'float' and source == 'int':
            return True

        # Для операций сравнения разрешаем разные числовые типы
        if op and op in {BinOp.EQ, BinOp.NE, BinOp.LT, BinOp.LE, BinOp.GT, BinOp.GE}:
            return (target in {'int', 'float'} and source in {'int', 'float'})

        return False

    def get_type_from_value(self, node: ValueNode) -> Optional[str]:
        """Определение типа значения"""
        if isinstance(node, NumNode):
            return 'float' if isinstance(node.value, float) else 'int'
        elif isinstance(node, BoolNode):
            return 'bool'
        elif isinstance(node, IdentNode):
            symbol = self.current_scope.lookup(node.name)
            return symbol.type if symbol else None
        return None

    def has_return_statement(self, node: AstNode) -> bool:
        """Проверяет содержит ли узел return (рекурсивно)"""
        if isinstance(node, ReturnNode):
            return True

        if hasattr(node, 'childs'):
            for child in node.childs:
                if self.has_return_statement(child):
                    return True

        return False

    def analyze_ident(self, node: IdentNode) -> Optional[str]:
        """Проверка использования идентификатора"""
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            self.error(f"Undefined variable '{node.name}'", node)
            return None
        return symbol.type

    def analyze_block(self, node: BlockNode):
        """Анализ блока кода с новой областью видимости"""
        new_scope = self.current_scope.create_child()
        self.current_scope = new_scope

        for stmt in node.childs:
            self.analyze(stmt)

        self.current_scope = self.current_scope.parent

    def analyze_if(self, node: IfNode):
        """Проверка условного оператора"""
        cond_type = self.analyze(node.cond)
        if cond_type != 'bool':
            self.error("Condition must be boolean", node.cond)

        self.analyze(node.then_block)
        if node.else_block:
            self.analyze(node.else_block)

    def analyze_for(self, node: ForNode):
        """Проверка цикла for"""
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
        """Проверка аргументов print"""
        for arg in node.childs:
            self.analyze(arg)  # Все типы допустимы для вывода