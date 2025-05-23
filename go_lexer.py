import ply.lex as lex

tokens = (
    'NUMBER',
    'IDENT',
    'STRING',
    'BOOL',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'EQ',
    'NE',
    'LT',
    'LE',
    'GT',
    'GE',
    'ASSIGN',
    'DECLARE',
    'AND',
    'OR',
    'NOT',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMI',
    'COMMA',
    'COLON',
    'VAR',
    'PRINT',
    'IF',
    'ELSE',
    'FOR',
    'WHILE',
    'TYPE',
    'FUNC',
    'RETURN'
)

reserved = {
    'var': 'VAR',
    'true': 'BOOL',
    'false': 'BOOL',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'int': 'TYPE',
    'float': 'TYPE',
    'bool': 'TYPE',
    'string': 'TYPE',
    'func': 'FUNC',
    'return': 'RETURN'
}

# Регулярные выражения для простых токенов
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_ASSIGN = r'='
t_DECLARE = r':='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_COMMA = r','
t_COLON = r':'

# Игнорируем пробелы и табы
t_ignore = ' \t'

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    t.type = 'STRING'
    return t

def t_COMMENT(t):
    r'//.*|\/\*(.|\n)*?\*\/'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()