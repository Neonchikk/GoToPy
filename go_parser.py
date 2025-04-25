import ply.yacc as yacc
from go_lexer import tokens, lexer
from go_ast import *

# Правила для программы и списка statements
def p_program(p):
    '''program : statement_list'''
    p[0] = ProgramNode(p[1])

def p_statement_list(p):
    '''statement_list : statement
                     | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : expression_statement
                | block_statement
                | var_declaration
                | if_statement
                | for_statement
                | print_statement
                | func_declaration
                | return_statement'''
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression SEMI
                           | SEMI'''
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = None

def p_block_statement(p):
    '''block_statement : LBRACE statement_list RBRACE'''
    p[0] = BlockNode(p[2])

def p_var_declaration(p):
    '''var_declaration : VAR IDENT COLON type SEMI
                      | VAR IDENT COLON type ASSIGN expression SEMI'''
    if len(p) == 6:
        p[0] = VarDeclNode(
            IdentNode(p[2], lineno=p.lineno(2), column=p.lexpos(2)),  # Закрыли IdentNode
            p[4],
            lineno=p.lineno(1),
            column=p.lexpos(1)
        )
    else:
        p[0] = VarDeclNode(
            IdentNode(p[2], lineno=p.lineno(2), column=p.lexpos(2)),  # Добавили column
            p[4],
            p[6],
            lineno=p.lineno(1),
            column=p.lexpos(1)
        )

def p_type(p):
    '''type : TYPE'''
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement
                   | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = IfNode(p[3], p[5])
    else:
        p[0] = IfNode(p[3], p[5], p[7])

def p_for_statement(p):
    '''for_statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement
                    | FOR LPAREN var_declaration expression_statement expression RPAREN statement
                    | FOR LPAREN expression_statement expression_statement RPAREN statement
                    | FOR LPAREN var_declaration expression_statement RPAREN statement
                    | FOR LPAREN RPAREN statement
                    | FOR statement'''
    if len(p) == 8:
        p[0] = ForNode(p[3], p[4], p[5], p[7])
    elif len(p) == 7:
        if isinstance(p[3], VarDeclNode):
            p[0] = ForNode(p[3], p[4], None, p[6])
        else:
            p[0] = ForNode(p[3], p[4], p[5], p[6])
    elif len(p) == 5:
        p[0] = ForNode(None, None, None, p[4])
    elif len(p) == 3:
        p[0] = ForNode(None, None, None, p[2])
    else:
        p[0] = ForNode(None, None, None, BlockNode([]))

def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression_list RPAREN SEMI'''
    p[0] = PrintNode(p[3])

def p_expression_list(p):
    '''expression_list : expression
                      | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expression(p):
    '''expression : assignment_expression
                 | logical_or_expression'''
    p[0] = p[1]

def p_assignment_expression(p):
    '''assignment_expression : IDENT ASSIGN expression
                            | IDENT DECLARE expression'''
    p[0] = AssignNode(
        IdentNode(p[1], lineno=p.lineno(1), column=p.lexpos(1)),
        p[3],
        lineno=p.lineno(2),  # Позиция оператора (= или :=)
        column=p.lexpos(2)
    )

def p_logical_or_expression(p):
    '''logical_or_expression : logical_and_expression
                            | logical_or_expression OR logical_and_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinOpNode(BinOp.OR, p[1], p[3])

def p_logical_and_expression(p):
    '''logical_and_expression : equality_expression
                             | logical_and_expression AND equality_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinOpNode(BinOp.AND, p[1], p[3])

def p_equality_expression(p):
    '''equality_expression : relational_expression
                          | equality_expression EQ relational_expression
                          | equality_expression NE relational_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinOpNode(BinOp(p[2]), p[1], p[3])

def p_relational_expression(p):
    '''relational_expression : additive_expression
                            | relational_expression LT additive_expression
                            | relational_expression LE additive_expression
                            | relational_expression GT additive_expression
                            | relational_expression GE additive_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinOpNode(BinOp(p[2]), p[1], p[3])

def p_additive_expression(p):
    '''additive_expression : multiplicative_expression
                          | additive_expression PLUS multiplicative_expression
                          | additive_expression MINUS multiplicative_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinOpNode(BinOp(p[2]), p[1], p[3])

def p_multiplicative_expression(p):
    '''multiplicative_expression : unary_expression
                                | multiplicative_expression TIMES unary_expression
                                | multiplicative_expression DIVIDE unary_expression
                                | multiplicative_expression MOD unary_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = BinOpNode(BinOp(p[2]), p[1], p[3])

def p_unary_expression(p):
    '''unary_expression : primary_expression
                       | MINUS unary_expression
                       | NOT unary_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = UnOpNode(UnOp(p[1]), p[2])

def p_primary_expression(p):
    '''primary_expression : IDENT
                         | NUMBER
                         | BOOL
                         | STRING
                         | LPAREN expression RPAREN
                         | IDENT LPAREN args RPAREN'''
    if len(p) == 2:
        if isinstance(p[1], (int, float)):
            p[0] = NumNode(p[1], lineno=p.lineno(1), column=p.lexpos(1))
        elif p[1] in ('true', 'false'):
            p[0] = BoolNode(p[1] == 'true', lineno=p.lineno(1), column=p.lexpos(1))
        elif isinstance(p[1], str):
            p[0] = IdentNode(p[1], lineno=p.lineno(1), column=p.lexpos(1))
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = FuncCallNode(
            IdentNode(p[1], lineno=p.lineno(1), column=p.lexpos(1)),
            p[3],
            lineno=p.lineno(1),
            column=p.lexpos(1)
        )

def p_args(p):
    '''args : expression
            | args COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_func_declaration(p):
    '''func_declaration : FUNC IDENT LPAREN params RPAREN COLON type block_statement
                       | FUNC IDENT LPAREN RPAREN COLON type block_statement
                       | FUNC IDENT LPAREN params RPAREN block_statement
                       | FUNC IDENT LPAREN RPAREN block_statement'''
    if len(p) == 9:
        p[0] = FuncDeclNode(
            IdentNode(p[2], lineno=p.lineno(2), column=p.lexpos(2)),
            p[4],
            p[7],
            p[8],
            lineno=p.lineno(1),
            column=p.lexpos(1)
        )
    elif len(p) == 8:
        p[0] = FuncDeclNode(
            IdentNode(p[2], lineno=p.lineno(2), column=p.lexpos(2)),
            [],
            p[6],
            p[7],
            lineno=p.lineno(1),
            column=p.lexpos(1)
        )
    elif len(p) == 7:
        p[0] = FuncDeclNode(
            IdentNode(p[2], lineno=p.lineno(2), column=p.lexpos(2)),
            p[4],
            None,
            p[6],
            lineno=p.lineno(1),
            column=p.lexpos(1)
        )
    else:
        p[0] = FuncDeclNode(
            IdentNode(p[2], lineno=p.lineno(2), column=p.lexpos(2)),
            [],
            None,
            p[5],
            lineno=p.lineno(1),
            column=p.lexpos(1)
        )

def p_params(p):
    '''params : param
             | params COMMA param'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_param(p):
    '''param : IDENT COLON type'''
    p[0] = ParamNode(IdentNode(p[1]), p[3])

def p_return_statement(p):
    '''return_statement : RETURN expression SEMI
                       | RETURN SEMI'''
    if len(p) == 4:
        p[0] = ReturnNode(p[2])
    else:
        p[0] = ReturnNode(None)

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ({p.value}) at line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def build_tree(code: str) -> AstNode:
    return parser.parse(code, lexer=lexer)