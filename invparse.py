import pdb
from invlex import InvLexer
import ply.yacc as yacc

class BOP(object):
    def __init__(self, value, l_child, r_child):
        self.value = value
        self.l_child = l_child
        self.r_child = r_child

    def __str__(self):
        return self.value

    def __repr__(self):
        return "<BOP {0}>".format(self.value)

class UOP(object):
    def __init__(self, value, child):
        self.value = value
        self.child = child

    def __str__(self):
        return self.value

    def __repr__(self):
        return "<UOP {0}>".format(self.value)


precedence = (
    ('left', 'AND'),
    ('left', 'IMPAND'),
    ('left', 'PAREN'),
    ('right', 'NOT'),
    )

def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]

def p_expression_expr_term(p):
    'expression : expression term %prec IMPAND'
    p[0] = BOP('AND', p[1], p[2])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_expression_uminus(p):
    'expression : NOT expression'
    p[0] = UOP('NOT', p[2])


def p_expression_binop(p):
    '''expression : expression OR expression
                  | expression NOT expression
                  | expression AND expression
                  | LPAREN expression RPAREN expression %prec PAREN
                  | expression LPAREN expression RPAREN %prec PAREN'''
    if p[2] == 'NOT':
        p3_invert = UOP('NOT', p[3])
        p[0] = BOP('AND', p[1], p3_invert)
    elif p[2] == 'AND' or p[2] == 'OR':
        p[0] = BOP(p[2], p[1], p[3])
    elif p[1] == '(':  # Matched 'LPAREN expression RPAREN expression'
        p[0] = BOP('AND', p[2], p[4])
    elif p[2] == '(':
        p[0] = BOP('AND', p[1], p[3])



def p_expression_group(p):
    'expression : LPAREN expression RPAREN %prec PAREN'
    p[0] = p[2]

def p_term_DIRECTIVE(p):
    'term : DIRECTIVE'
    p[0] = p[1]

def p_term_TEXT(p):
    'term : TEXT'
    p[0] = p[1]

def p_term_RE(p):
    'term : RE'
    p[0] = p[1]

def p_error(p):
    if not p:
        print "Syntax error at end of line"
    else:
        print "Syntax error at '{0}'".format(p.value)

def build_parser():
    lexer = InvLexer()
    lexer.build_lexer()
    tokens = lexer.tokens
    p = yacc.yacc()
    def parse(s):
        return yacc.parse(s, lexer=lexer.lexer)
    return parse

if __name__ == "__main__":
    lexer = InvLexer()
    lexer.build_lexer()
    tokens = lexer.tokens
    p = yacc.yacc()

    """
    s = "a b"
    print
    print '-' * 10
    s = "a OR -b AND c"
    print s
    yacc.parse(s, lexer=lexer.lexer)
    print
    print '-' * 10
    print s
    s = "(a OR b) AND c"
    p.parse(s)
    print
    print '-' * 10

    s = "-(a OR b) AND c"
    print s
    p.parse(s)
    print
    print '-' * 10

    s = "type=:a vlan=:b"
    print s
    p.parse(s)
    print
    print '-' * 10

    s = "/a"
    print s
    p.parse(s)
    print
    print '-'*10

    s = "(a) (b)"
    print s
    p.parse(s)
    print
    print '-'*10

    s = "a (b)"
    print s
    p.parse(s)
    print
    print '-'*10

    s = "(a) b"
    print s
    p.parse(s)
    print
    print '-'*10

    s = "(((a)) (b))"
    print s
    p.parse(s)
    print
    print '-'*10

    s = "(a b c)"
    print s
    p.parse(s)
    print
    print '-'*10

    s = "a b d OR c f g"
    print s
    p.parse(s)
    print
    print '-'*10

    s = "(a (b c))"
    print s
    p.parse(s)
    print
    print '-'*10

    s = "a -(c OR b)"
    print s
    p.parse(s)
    print
    print '-'*10

    s = "a AND"
    print s
    p.parse(s)
    print
    print '-'*10
    """
