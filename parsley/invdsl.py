import parsley
from ometa.runtime import ParseError


class ICompiler(object):
    ParseError = ParseError
    g = None  # Memozie

    def __init__(self, fname, DEBUG=False):
        self.fname = fname
        self.DEBUG = DEBUG

    def __call__(self, *args, **kwargs):
        grammar_text = open(self.fname).read()
        g = parsley.makeGrammar(
            grammar_text, self.bindings
        )
        return g(*args, **kwargs)

    def print_grammar(self):
        print '-------------------'
        print self.grammar_text
        print '-------------------'


class DebugCompiler(ICompiler):
    def __init__(self, fname, **kwargs):
        self.bindings = {
            'directive': self.directive,
            'regexpr': self.regexpr,
            'text': self.text,
            'compile': self.arith_compile,
            'AND_op': lambda a, b: '({a} AND {b})'.format(a=a, b=b),
            'OR_op': lambda a, b: '({a} OR {b})'.format(a=a, b=b),
            'NOT_op': lambda a: '(NOT {0})'.format(a)
        }
        super(DebugCompiler, self).__init__(fname, **kwargs)

    def directive(self, d, v):
        print 'matched DRCT ' + str((d, v))
        return d, v

    def regexpr(self, r):
        print 'matched RE ' + r
        return r

    def text(self, t):
        print 'matched TEXT ' + t
        return t

    def arith_compile(self, initial, values):
        print initial, values
        ret = initial
        for op, value in values:
            ret = op(ret, value)
        return ret
    def OR(self):
        return



if __name__ == '__main__':
    import sys
    invdsl = DebugCompiler('invdsl.parsley')
    print invdsl(sys.argv[1]).expr()
