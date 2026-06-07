import parser

class Evaluator:
    def __init__(self):
        self.tree = []
        self.node = None
        self.variables = {}
    
    def is_base_type(self, value):
        return type(value) in [str, int, float]
    
    def evaluate_tree(self, node):
        t_type = type(node)
        if t_type == parser.Output:
            if not self.is_base_type(node.value):
                value = self.evaluate_tree(node.value)
            else:
                value = node.value
            print(value)
        elif t_type == parser.New:
            if node.name in self.variables.keys():
                print("ERROR: " + str(node.name) + " already exists")
                print("  HELP: Remove `NEW " + str(node.name) + "`")
                exit(1)
            self.variables.update({str(node.name): ""})
        elif t_type == parser.Put:
            if node.name not in self.variables.keys():
                print("ERROR: " + str(node.name) + " does not exist")
                print("  HELP: Create it with `NEW " + str(node.name) + "`")
                exit(1)
            if not self.is_base_type(node.expr):
                expr = self.evaluate_tree(node.expr)
            else:
                expr = node.expr
            self.variables.update({str(node.name): expr})
        elif t_type == parser.Variable:
            if node.name not in self.variables.keys():
                print("ERROR: " + str(node.name) + " does not exist")
                print("  HELP: Create it with `NEW " + str(node.name) + "`")
                exit(1)
            return self.variables.get(str(node.name))
        elif t_type == parser.Input:
            if node.name not in self.variables.keys():
                print("ERROR: " + str(node.name) + " does not exist")
                print("  HELP: Create it with `NEW " + str(node.name) + "`")
                exit(1)
            self.variables.update({str(node.name): input()})
        elif t_type == parser.BinOp:
            if not self.is_base_type(node.left):
                left = self.evaluate_tree(node.left)
            else:
                left = node.left
            if not self.is_base_type(node.right):
                right = self.evaluate_tree(node.right)
            else:
                right = node.right
            if node.op == "+":
                return left + right
            elif node.op == "-":
                return left - right
            elif node.op == "*":
                return left * right
            elif node.op == "/":
                return left / right    # does not do integer division
            elif node.op == "=":
                return int(left == right)
            elif node.op == ">":
                return int(left > right)
            elif node.op == "<":
                return int(left < right)
            elif node.op == "&&":
                return int(left and right)
            elif node.op == "||":
                return int(left or right)
        elif t_type == parser.IfCondition:
            if not self.is_base_type(node.condition):
                condition = self.evaluate_tree(node.condition)
            else:
                condition = node.condition
            if condition:
                for stmt in node.statements:
                    if not self.is_base_type(stmt):
                        self.evaluate_tree(stmt)
            else:
                for else_stmt in node.else_statements:
                    if not self.is_base_type(else_stmt):
                        self.evaluate_tree(else_stmt)
        elif t_type == parser.While:
            while True:
                if not self.is_base_type(node.condition):
                    condition = self.evaluate_tree(node.condition)
                else:
                    condition = node.condition
                if condition:
                    for stmt in node.statements:
                        if not self.is_base_type(stmt):
                            self.evaluate_tree(stmt)
                else:
                    break
        elif t_type == parser.UnOp:
            if not self.is_base_type(node.expr):
                expr = self.evaluate_tree()
            else:
                expr = node.expr
            if node.op == "!":
                return int(not expr)

    def evaluate(self, __tree):
        self.tree = __tree
        for __node in self.tree:
            self.node = __node
            self.evaluate_tree(self.node)