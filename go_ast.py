from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
from enum import Enum


class AstNode(ABC):
    """Абстрактный базовый класс для всех узлов AST"""

    @property
    @abstractmethod
    def childs(self) -> Tuple['AstNode', ...]:
        """Возвращает дочерние узлы"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление узла"""
        pass

    @property
    def tree(self) -> List[str]:
        """Формирует дерево в виде списка строк (для вывода)"""
        res = [str(self)]
        for i, child in enumerate(self.childs):
            ch0, ch = '├', '│'
            if i == len(self.childs) - 1:
                ch0, ch = '└', ' '
            for j, line in enumerate(child.tree):
                res.append((ch0 if j == 0 else ch) + ' ' + line)
        return res


class ValueNode(AstNode, ABC):
    """Базовый класс для всех узлов-значений (числа, строки, выражения)"""
    pass


class NumNode(ValueNode):
    """Узел для числовых литералов (42, 3.14)"""

    def __init__(self, value: float):
        self.value = value

    @property
    def childs(self) -> Tuple[()]:
        return ()

    def __str__(self) -> str:
        return str(self.value)


class IdentNode(ValueNode):
    """Узел для идентификаторов (переменные, имена функций)"""

    def __init__(self, name: str):
        self.name = name

    @property
    def childs(self) -> Tuple[()]:
        return ()

    def __str__(self) -> str:
        return self.name


class BoolNode(ValueNode):
    """Узел для булевых значений (true/false)"""

    def __init__(self, value: bool):
        self.value = value

    @property
    def childs(self) -> Tuple[()]:
        return ()

    def __str__(self) -> str:
        return 'true' if self.value else 'false'


class BinOp(Enum):
    """Бинарные операции"""
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'
    EQ = '=='
    NE = '!='
    LT = '<'
    LE = '<='
    GT = '>'
    GE = '>='
    AND = '&&'
    OR = '||'


class BinOpNode(ValueNode):
    """Узел для бинарных операций (a + b, x && y)"""

    def __init__(self, op: BinOp, left: ValueNode, right: ValueNode):
        self.op = op
        self.left = left
        self.right = right

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.left, self.right

    def __str__(self) -> str:
        return str(self.op.value)


class UnOp(Enum):
    """Унарные операции"""
    NEG = '-'
    NOT = '!'


class UnOpNode(ValueNode):
    """Узел для унарных операций (-x, !flag)"""

    def __init__(self, op: UnOp, arg: ValueNode):
        self.op = op
        self.arg = arg

    @property
    def childs(self) -> Tuple[ValueNode]:
        return (self.arg,)

    def __str__(self) -> str:
        return str(self.op.value)


class BlockNode(AstNode):
    """Узел для блоков кода { ... }"""

    def __init__(self, statements: List[AstNode]):
        self.statements = statements

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return tuple(self.statements)

    def __str__(self) -> str:
        return 'block'


class VarDeclNode(AstNode):
    """Узел для объявления переменных (var x: int = 10)"""

    def __init__(self, name: IdentNode, type_: str, value: Optional[ValueNode] = None):
        self.name = name
        self.type = type_
        self.value = value

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        if self.value is not None:
            return (self.name, self.value)
        return (self.name,)

    def __str__(self) -> str:
        return f'var {self.type}'


class AssignNode(AstNode):
    """Узел для присваивания (x = 10)"""

    def __init__(self, target: IdentNode, value: ValueNode):
        self.target = target
        self.value = value

    @property
    def childs(self) -> Tuple[IdentNode, ValueNode]:
        return self.target, self.value

    def __str__(self) -> str:
        return '='


class PrintNode(AstNode):
    """Узел для вывода (print("Hello"))"""

    def __init__(self, args: List[ValueNode]):
        self.args = args

    @property
    def childs(self) -> Tuple[ValueNode, ...]:
        return tuple(self.args)

    def __str__(self) -> str:
        return 'print'


class IfNode(AstNode):
    """Узел для условия (if x > 0 { ... } else { ... })"""

    def __init__(self, cond: ValueNode, then_block: AstNode, else_block: Optional[AstNode] = None):
        self.cond = cond
        self.then_block = then_block
        self.else_block = else_block

    @property
    def childs(self) -> Tuple[ValueNode, AstNode, Optional[AstNode]]:
        return (self.cond, self.then_block, self.else_block) if self.else_block else (self.cond, self.then_block)

    def __str__(self) -> str:
        return 'if'


class ForNode(AstNode):
    """Узел для цикла for (for i := 0; i < 10; i++ { ... })"""

    def __init__(self, init: Optional[AstNode], cond: Optional[ValueNode],
                 step: Optional[AstNode], body: AstNode):
        self.init = init
        self.cond = cond
        self.step = step
        self.body = body

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return tuple(child for child in (self.init, self.cond, self.step, self.body) if child is not None)

    def __str__(self) -> str:
        return 'for'


class ProgramNode(AstNode):
    """Корневой узел программы (список всех выражений)"""

    def __init__(self, statements: List[AstNode]):
        self.statements = statements

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return tuple(self.statements)

    def __str__(self) -> str:
        return 'program'


class ParamNode(AstNode):
    """Узел для параметров функции (n: int)"""

    def __init__(self, name: IdentNode, type_: str):
        self.name = name
        self.type = type_

    @property
    def childs(self) -> Tuple[IdentNode]:
        return (self.name,)

    def __str__(self) -> str:
        return f'param: {self.type}'


class FuncDeclNode(AstNode):
    """Узел для объявления функции (func foo(): int { ... })"""

    def __init__(self, name: IdentNode, params: List[ParamNode], return_type: Optional[str], body: AstNode):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return (self.name, *self.params, self.body)

    def __str__(self) -> str:
        return f'func -> {self.return_type}' if self.return_type else 'func'


class FuncCallNode(ValueNode):
    """Узел для вызова функции (factorial(5))"""

    def __init__(self, name: IdentNode, args: List[ValueNode]):
        self.name = name
        self.args = args

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return (self.name, *self.args)

    def __str__(self) -> str:
        return 'call'


class ReturnNode(AstNode):
    """Узел для return (return 42)"""

    def __init__(self, value: Optional[ValueNode]):
        self.value = value

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return (self.value,) if self.value else ()

    def __str__(self) -> str:
        return 'return'


class Symbol:
    """Информация о символе (переменная/функция)"""

    def __init__(self, name: str, type_: str, scope: str, node: AstNode):
        self.name = name
        self.type = type_
        self.scope = scope  # 'global', 'function', 'block'
        self.node = node  # Ссылка на AST-узел


class SymbolTable:
    """Таблица символов с поддержкой вложенных областей видимости"""

    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.children = []

    def add(self, symbol: Symbol) -> bool:
        """Добавляет символ в текущую область видимости"""
        if symbol.name in self.symbols:
            return False  # Дублирование
        self.symbols[symbol.name] = symbol
        return True

    def lookup(self, name: str, current_scope_only=False) -> Optional[Symbol]:
        """Поиск символа (рекурсивно по родителям)"""
        symbol = self.symbols.get(name)
        if symbol is not None:
            return symbol
        if current_scope_only or self.parent is None:
            return None
        return self.parent.lookup(name)

    def create_child(self) -> 'SymbolTable':
        """Создает дочернюю область видимости"""
        child = SymbolTable(self)
        self.children.append(child)
        return child
