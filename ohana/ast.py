class Node(object):
    pass

class ExprAST(Node):
    pass

class BinOpExprAST(ExprAST):
    def __init__(self, op, left, right):
        self.left = left
        self.right = right
        self.op = op

class NumberExprAST(ExprAST):
    def __init__(self, value):
        self.value = value

class VariableExprAST(ExprAST):
    def __init__(self, name):
        self.name = name

class CallExprAST(ExprAST):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

class PrototypeAST(ExprAST):
    def __init__(self, name, arg_names):
        self.name = name
        self.arg_names = arg_names

class FunctionAST(ExprAST):
    def __init__(self, proto, body):
        self.proto = proto
        self.body = body

    _anonymous_function_counter = 0

    @classmethod
    def create_anonymous(rep, expr):
        rep._anonymous_function_counter += 1
        return rep(
                PrototypeAST('_anon{0}'.format(rep._anonymous_function_counter),
                    []),
                expr)

    def is_anonymous(self):
        return self.proto.name.startswith('_anon')
