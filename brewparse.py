"""Brew AST parser.

A function call has the form ``[name arg1 arg2 ...]`` where each ``arg`` is a full ``expr``
(same nonterminal as everywhere else): literals, variables, nested calls, ``if``, ``seq``, etc.
"""
from element import Element
from brewlex import *
from intbase import InterpreterBase
from ply import yacc


def collapse_items(p, group_index, singleton_index):
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[group_index]
        p[0].append(p[singleton_index])


def p_program(p):
    "program : funcdefs"
    p[0] = Element(InterpreterBase.PROGRAM_NODE, functions=p[1])


def p_funcdefs(p):
    """funcdefs : funcdefs funcdef
    | funcdef"""
    collapse_items(p, 1, 2)


def p_funcdef(p):
    """funcdef : LBRACKET FUNC NAME LBRACKET params RBRACKET expr RBRACKET
    | LBRACKET FUNC NAME LBRACKET RBRACKET expr RBRACKET"""
    if len(p) == 9:
        p[0] = Element(InterpreterBase.FUNC_NODE, name=p[3], args=p[5], body=p[7])
    else:
        p[0] = Element(InterpreterBase.FUNC_NODE, name=p[3], args=[], body=p[6])


def p_params(p):
    """params : params NAME
    | NAME"""
    if len(p) == 2:
        p[0] = [Element(InterpreterBase.ARG_NODE, name=p[1])]
    else:
        p[0] = p[1]
        p[0].append(Element(InterpreterBase.ARG_NODE, name=p[2]))


def p_expr_if(p):
    "expr : LBRACKET IF expr expr expr RBRACKET"
    p[0] = Element(
        InterpreterBase.IF_NODE,
        cond=p[3],
        then_expr=p[4],
        else_expr=p[5],
    )


def p_expr_not(p):
    "expr : LBRACKET BANG expr RBRACKET"
    p[0] = Element(InterpreterBase.NOT_NODE, op1=p[3])


def p_expr_try(p):
    "expr : LBRACKET TRY expr catch_clauses RBRACKET"
    p[0] = Element(InterpreterBase.TRY_NODE, body=p[3], catchers=p[4])


def p_catch_clauses(p):
    """catch_clauses : catch_clauses catch_clause
    | catch_clause"""
    collapse_items(p, 1, 2)


def p_catch_clause(p):
    "catch_clause : LBRACKET CATCH STRING expr RBRACKET"
    p[0] = Element(InterpreterBase.CATCH_NODE, tag=p[3], body=p[4])


def p_expr_throw(p):
    "expr : LBRACKET THROW expr RBRACKET"
    p[0] = Element(InterpreterBase.THROW_NODE, val=p[3])


def p_expr_bool_t(p):
    "expr : HASH_T"
    p[0] = Element(InterpreterBase.BOOL_NODE, val=True)


def p_expr_bool_f(p):
    "expr : HASH_F"
    p[0] = Element(InterpreterBase.BOOL_NODE, val=False)


def p_expr_cmp(p):
    """expr : LBRACKET EQ expr expr RBRACKET
    | LBRACKET NE expr expr RBRACKET
    | LBRACKET LT expr expr RBRACKET
    | LBRACKET LE expr expr RBRACKET
    | LBRACKET GT expr expr RBRACKET
    | LBRACKET GE expr expr RBRACKET"""
    p[0] = Element(
        InterpreterBase.FCALL_NODE,
        fn=Element(InterpreterBase.QUALIFIED_NAME_NODE, name=p[2]),
        args=[p[3], p[4]],
    )


def p_expr_binop(p):
    """expr : LBRACKET PLUS expr expr RBRACKET
    | LBRACKET MINUS expr expr RBRACKET
    | LBRACKET MULTIPLY expr expr RBRACKET
    | LBRACKET DIVIDE expr expr RBRACKET"""
    p[0] = Element(
        InterpreterBase.FCALL_NODE,
        fn=Element(InterpreterBase.QUALIFIED_NAME_NODE, name=p[2]),
        args=[p[3], p[4]],
    )


def p_expr_seq(p):
    "expr : LBRACKET SEQ LBRACKET vardefs RBRACKET exprs RBRACKET"
    p[0] = Element(InterpreterBase.SEQ_NODE, vars=p[4], exprs=p[6])


def p_expr_seq_novars(p):
    "expr : LBRACKET SEQ LBRACKET RBRACKET exprs RBRACKET"
    p[0] = Element(InterpreterBase.SEQ_NODE, vars=[], exprs=p[5])


def p_expr_comp(p):
    "expr : LBRACKET COMP expr comp_clauses RBRACKET"
    generators = []
    guards = []
    for kind, node in p[4]:
        if kind == "for":
            generators.append(node)
        else:
            guards.append(node)
    p[0] = Element(
        InterpreterBase.COMP_NODE,
        fn=p[3],
        generators=generators,
        guards=guards,
    )


def p_comp_clauses(p):
    """comp_clauses : comp_clauses comp_clause
    | comp_clause"""
    collapse_items(p, 1, 2)


def p_comp_clause_for(p):
    "comp_clause : LBRACKET FOR NAME IN expr RBRACKET"
    p[0] = (
        "for",
        Element(InterpreterBase.VAR_DEF_NODE, name=p[3], val=p[5]),
    )


def p_comp_clause_when(p):
    "comp_clause : LBRACKET WHEN expr RBRACKET"
    p[0] = ("when", p[3])


def p_vardefs(p):
    """vardefs : vardefs vardef
    | vardef"""
    collapse_items(p, 1, 2)


def p_vardef(p):
    "vardef : LBRACKET NAME expr RBRACKET"
    p[0] = Element(InterpreterBase.VAR_DEF_NODE, name=p[2], val=p[3])


def p_empty(p):
    "empty :"
    pass


def p_expr_lambda(p):
    "expr : LBRACKET LAMBDA LBRACKET lambda_params RBRACKET expr RBRACKET"
    p[0] = Element(InterpreterBase.LAMBDA_NODE, formals=p[4], body=p[6])


def p_lambda_params_empty(p):
    "lambda_params : empty"
    p[0] = []


def p_lambda_params(p):
    "lambda_params : params"
    p[0] = p[1]


def p_expr_list_empty(p):
    "expr : LBRACE RBRACE"
    p[0] = Element(InterpreterBase.LIST_NODE, elements=[])


def p_list_exprs(p):
    """list_exprs : list_exprs expr
    | expr"""
    collapse_items(p, 1, 2)


def p_expr_list(p):
    "expr : LBRACE list_exprs RBRACE"
    p[0] = Element(InterpreterBase.LIST_NODE, elements=p[2])


def p_expr_call(p):
    "expr : LBRACKET expr call_args RBRACKET"
    p[0] = Element(InterpreterBase.FCALL_NODE, fn=p[2], args=p[3])


def p_call_args_empty(p):
    "call_args : empty"
    p[0] = []


def p_call_args_exprs(p):
    "call_args : exprs"
    p[0] = p[1]


def p_exprs(p):
    """exprs : exprs expr
    | expr"""
    collapse_items(p, 1, 2)


def p_expr_number(p):
    "expr : NUMBER"
    p[0] = Element(InterpreterBase.INT_NODE, val=p[1])


def p_expr_string(p):
    "expr : STRING"
    p[0] = Element(InterpreterBase.STRING_NODE, val=p[1])


def p_expr_var(p):
    "expr : NAME"
    p[0] = Element(InterpreterBase.QUALIFIED_NAME_NODE, name=p[1])


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")


def parse_program(program, plot=False):
    reset_lineno()
    ast = yacc.parse(program, lexer=lexer)
    if ast is None:
        raise SyntaxError("Syntax error")
    if plot:
        from plot import plot_ast
        plot_ast(ast)
    return ast


yacc.yacc()
