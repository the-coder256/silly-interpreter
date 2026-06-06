import tokeniser

class Output:
    def __init__(self, value):
        self.value = value
class New:
    def __init__(self, name):
        self.name = name
class Put:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
class Variable:
    def __init__(self, name):
        self.name = name
class Input:
    def __init__(self, name):
        self.name = name
class BinOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
class IfCondition:
    def __init__(self, condition, statements:list):
        self.condition = condition
        self.statements = statements

class Parser:
    def __init__(self):
        self.tokens:list = []
        self.tree  :list = []
        self.index = 0
    
    def peek(self, amount = 1):
        try:
            return self.tokens[self.index + amount]
        except:
            return tokeniser.T_TokensEnd("TOKENS_END")
    
    def consume(self):
        return self.tokens[self.index]
    
    def advance(self):
        self.index += 1
        return self.tokens[self.index - 1]
    
    def parse_expr(self):
        t_start = type(self.consume())
        start = self.advance().value
        if t_start == tokeniser.T_Instruction:
            if start == "VARIABLE":
                name = self.advance().value
                return Variable(name)
            elif start == "ADD":
                left = self.parse_expr()
                right = self.parse_expr()
                return BinOp("+", left, right)
            elif start == "SUBTRACT":
                left = self.parse_expr()
                right = self.parse_expr()
                return BinOp("-", left, right)
            elif start == "MULTIPLY":
                left = self.parse_expr()
                right = self.parse_expr()
                return BinOp("*", left, right)
            elif start == "DIVIDE":
                left = self.parse_expr()
                right = self.parse_expr()
                return BinOp("/", left, right)
        else:
            return start
    
    def parse_output(self):
        expr = self.parse_expr()
        return Output(expr)
    
    def parse_new(self):
        name = self.advance().value
        return New(name)

    def parse_put(self):
        name = self.advance().value
        expr = self.parse_expr()
        return Put(name, expr)
    
    def parse_input(self):
        name = self.advance().value
        return Input(name)
    
    def parse_if(self):
        condition = self.parse_expr()
        statements = []
        while self.consume().value != "END":
            stmt = self.parse_stmt()
            if not stmt:
                print("ERROR: Expected `END`")
                print("  HELP: Use `END` to close an if condition")
                exit(1)
            statements.append(stmt)
        self.advance()
        return IfCondition(condition, statements)
    
    def parse_stmt(self):
        beginning = self.advance()
        if type(beginning) == tokeniser.T_Instruction:
            if beginning.value == "OUTPUT":
                return self.parse_output()
            elif beginning.value == "NEW":
                return self.parse_new()
            elif beginning.value == "PUT":
                return self.parse_put()
            elif beginning.value == "INPUT":
                return self.parse_input()
            elif beginning.value == "IF":
                return self.parse_if()
    
    def at_end(self):
        return type(self.consume()) == tokeniser.T_TokensEnd
    
    def parse(self, __tokens):
        self.tokens = __tokens
        while not self.at_end():
            node = self.parse_stmt()
            self.tree.append(node)
        return self.tree