from ply import lex

reserved = {
    "func": "FUNC",
    "seq": "SEQ",
    "comp": "COMP",
    "for": "FOR",
    "in": "IN",
    "when": "WHEN",
    "if": "IF",
    "lambda": "LAMBDA",
    "try": "TRY",
    "catch": "CATCH",
    "throw": "THROW",
}

tokens = list(reserved.values()) + [
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "EQ",
    "NE",
    "LE",
    "GE",
    "LT",
    "GT",
    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "BANG",
    "HASH_T",
    "HASH_F",
    "NUMBER",
    "NAME",
    "STRING",
]

t_ignore = " \t"

t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_EQ = r"=="
t_NE = r"!="
t_LE = r"<="
t_GE = r">="
t_LT = r"<"
t_GT = r">"
t_PLUS = r"\+"
t_MINUS = r"\-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"/"
t_BANG = r"\!"


def t_HASH_T(t):
    r"\#t"
    return t


def t_HASH_F(t):
    r"\#f"
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_NAME(t):
    r"[A-Za-z_][\w_]*"
    t.type = reserved.get(t.value, "NAME")
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_comment(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")


def t_STRING(t):
    r'".*?"'
    t.value = t.value[1:-1]
    return t


def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)


def reset_lineno():
    lexer.lineno = 1


lexer = lex.lex()
