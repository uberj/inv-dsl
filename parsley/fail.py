from parsley import wrapGrammar
from ometa.grammar import OMeta
from ometa.runtime import OMetaBase
g = """
        expr = 'simple' -> self.bar()
    """

class Foo(
    OMeta.makeGrammar(g, name="Foo").createParserClass(OMetaBase, globals())):
    def bar(self):
        print "bar!"

class Bar(Foo):
    pass

def make_local_grammar():
    return wrapGrammar(Bar)

if __name__ == '__main__':
    g = make_local_grammar()
    g('simple').expr()
