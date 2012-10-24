class _Filter(object):
    """The Base class of different filters. Implement these methods
    """
    def __str__(self):
        return self.value

    def __repr__(self):
        return "<{1}>".format(self.__class__, self)

    def compile_Q(self, ntype):
        pass

class TextFilter(_Filter):
    def __init__(self, rvalue):
        self.value = rvalue
        self.Q = self.compile_Q(rvalue)

    def compile_Q(self, value):
        pass

class REFilter(TextFilter):
    def compile_Q(self, value):
        pass

class DirectiveFilter(_Filter):
    def __init__(self, rvalue, directive, dvalue):
        self.value = rvalue
        self.directive = directive
        self.dvalue = dvalue
        self.Q = self.compile_Q(directive, dvalue)

    def compile_Q(self, directive, dvalue):
        pass

