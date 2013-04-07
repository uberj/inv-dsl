from parsley import wrapGrammar

from ometa.grammar import OMeta
from ometa.runtime import OMetaBase


fname = 'invdsl.parsley'
name = 'InvDSL'
g = open(fname).read()
B = OMeta.makeGrammar(g, name=name).createParserClass(OMetaBase, globals())


class ICompiler(B):
    def directive(self, d, v):
        raise NotImplemented()

    def regexpr(self, r):
        raise NotImplemented()

    def text(self, t):
        raise NotImplemented()

    def compile(self, initial, values):
        raise NotImplemented()

    def OR_op(self, a, b):
        raise NotImplemented()

    def AND_op(self, a, b):
        raise NotImplemented()

    def NOT_op(self, a):
        raise NotImplemented()


class DebugCompiler(ICompiler):
    def directive(self, d, v):
        print 'matched DRCT ' + str((d, v))
        return d, v

    def regexpr(self, r):
        print 'matched RE ' + r
        return r

    def text(self, t):
        print 'matched TEXT ' + t
        return t

    def compile(self, initial, values):
        print initial, values
        ret = initial
        for op, value in values:
            ret = op(ret, value)
        return ret

    def OR_op(self, a, b):
        return '({0} {1} {2})'.format(a, 'OR', b)

    def AND_op(self, a, b):
        return '({0} {1} {2})'.format(a, 'AND', b)

    def NOT_op(self, a):
        return '({0} {1})'.format('NOT', a)


def make_compiler():
    return wrapGrammar(DebugCompiler)


if __name__ == '__main__':
    import sys
    invdsl = make_compiler()
    print invdsl(sys.argv[1]).expr()
