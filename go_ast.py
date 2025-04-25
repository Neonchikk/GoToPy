from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
from enum import Enum


class AstNode(ABC):
    def __init__(self, lineno=None, column=None):
        self.lineno = lineno
        self.column = column

    @property
    @abstractmethod
    def childs(self) -> Tuple['AstNode', ...]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def tree(self) -> List[str]:
        res = [str(self)]
        for i, child in enumerate(self.childs):
            ch0, ch = '├', '│'
            if i == len(self.childs) - 1:
                ch0, ch = '└', ' '
            for j, line in enumerate(child.tree):
                res.append((ch0 if j == 0 else ch) + ' ' + line)
        return res


class ValueNode(AstNode, ABC):
    pass


class NumNode(ValueNode):
    def __init__(self, value: float, lineno=None, column=None):
        super().__init__(lineno, column)
        self.value = value

    @property
    def childs(self) -> Tuple[()]:
        return ()

    def __str__(self) -> str:
        return str(self.value)


class IdentNode(ValueNode):
    def __init__(self, name: str, lineno=None, column=None):
        super().__init__(lineno, column)
        self.name = name

    @property
    def childs(self) -> Tuple[()]:
        return ()

    def __str__(self) -> str:
        return self.name


class BoolNode(ValueNode):
    def __init__(self, value: bool, lineno=None, column=None):
        super().__init__(lineno, column)
        self.value = value

    @property
    def childs(self) -> Tuple[()]:
        return ()

    def __str__(self) -> str:
        return 'true' if self.value else 'false'


class BinOp(Enum):
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
    def __init__(self, op: BinOp, left: ValueNode, right: ValueNode, lineno=None, column=None):
        super().__init__(lineno, column)
        self.op = op
        self.left = left
        self.right = right

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.left, self.right

    def __str__(self) -> str:
        return str(self.op.value)


class UnOp(Enum):
    NEG = '-'
    NOT = '!'


class UnOpNode(ValueNode):
    def __init__(self, op: UnOp, arg: ValueNode, lineno=None, column=None):
        super().__init__(lineno, column)
        self.op = op
        self.arg = arg

    @property
    def childs(self) -> Tuple[ValueNode]:
        return (self.arg,)

    def __str__(self) -> str:
        return str(self.op.value)


class BlockNode(AstNode):
    def __init__(self, statements: List[AstNode], lineno=None, column=None):
        super().__init__(lineno, column)
        self.statements = statements

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return tuple(self.statements)

    def __str__(self) -> str:
        return 'block'


class VarDeclNode(AstNode):
    def __init__(self, name: IdentNode, type_: str, value: Optional[ValueNode] = None, lineno=None, column=None):
        super().__init__(lineno, column)
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
    def __init__(self, target: IdentNode, value: ValueNode, lineno=None, column=None):
        super().__init__(lineno, column)
        self.target = target
        self.value = value

    @property
    def childs(self) -> Tuple[IdentNode, ValueNode]:
        return self.target, self.value

    def __str__(self) -> str:
        return '='


class PrintNode(AstNode):
    def __init__(self, args: List[ValueNode], lineno=None, column=None):
        super().__init__(lineno, column)
        self.args = args

    @property
    def childs(self) -> Tuple[ValueNode, ...]:
        return tuple(self.args)

    def __str__(self) -> str:
        return 'print'


class IfNode(AstNode):
    def __init__(self, cond: ValueNode, then_block: AstNode, else_block: Optional[AstNode] = None, lineno=None,
                 column=None):
        super().__init__(lineno, column)
        self.cond = cond
        self.then_block = then_block
        self.else_block = else_block

    @property
    def childs(self) -> Tuple[ValueNode, AstNode, Optional[AstNode]]:
        return (self.cond, self.then_block, self.else_block) if self.else_block else (self.cond, self.then_block)

    def __str__(self) -> str:
        return 'if'


class ForNode(AstNode):
    def __init__(self, init: Optional[AstNode], cond: Optional[ValueNode],
                 step: Optional[AstNode], body: AstNode, lineno=None, column=None):
        super().__init__(lineno, column)
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
    def __init__(self, statements: List[AstNode], lineno=None, column=None):
        super().__init__(lineno, column)
        self.statements = statements

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return tuple(self.statements)

    def __str__(self) -> str:
        return 'program'


class ParamNode(AstNode):
    def __init__(self, name: IdentNode, type_: str, lineno=None, column=None):
        super().__init__(lineno, column)
        self.name = name
        self.type = type_

    @property
    def childs(self) -> Tuple[IdentNode]:
        return (self.name,)

    def __str__(self) -> str:
        return f'param: {self.type}'


class FuncDeclNode(AstNode):
    def __init__(self, name: IdentNode, params: List[ParamNode], return_type: Optional[str], body: AstNode, lineno=None,
                 column=None):
        super().__init__(lineno, column)
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
    def __init__(self, name: IdentNode, args: List[ValueNode], lineno=None, column=None):
        super().__init__(lineno, column)
        self.name = name
        self.args = args

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return (self.name, *self.args)

    def __str__(self) -> str:
        return 'call'


class ReturnNode(AstNode):
    def __init__(self, value: Optional[ValueNode], lineno=None, column=None):
        super().__init__(lineno, column)
        self.value = value

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return (self.value,) if self.value else ()

    def __str__(self) -> str:
        return 'return'