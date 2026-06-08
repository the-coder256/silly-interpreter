import parser

class Evaluator:
    def __init__(self):
        self.tree = []
        self.node = None
        self.variables = {}
        self.definitions = {}
    
    def is_base_type(self, value):
        return type(value) in [str, int, float]
    
    def get_type(self, value):    # based on SILLY types
        actual = type(value)
        if actual == int:
            return "INTEGER"
        elif actual == float:
            return "FLOAT"
        elif actual == str:
            return "STRING"
        else:
            return "STRING"
    
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
        elif t_type == parser.Integer:
            if not self.is_base_type(node.expr):
                expr = self.evaluate_tree(node.expr)
            else:
                expr = node.expr
            try:
                return int(expr)
            except:
                print("ERROR: Cannot convert " + str(self.get_type(expr)) + " to INTEGER")
                print("  HELP: Check type of operand")
                exit(1)
        elif t_type == parser.Float:
            if not self.is_base_type(node.expr):
                expr = self.evaluate_tree(node.expr)
            else:
                expr = node.expr
            try:
                return int(expr)
            except:
                print("ERROR: Cannot convert " + str(self.get_type(expr)) + " to FLOAT")
                print("  HELP: Check type of operand")
                exit(1)
        elif t_type == parser.String:
            if not self.is_base_type(node.expr):
                expr = self.evaluate_tree(node.expr)
            else:
                expr = node.expr
            try:
                return int(expr)
            except:
                print("ERROR: Cannot convert " + str(self.get_type(expr)) + " to STRING")
                print("  HELP: Check type of operand")
                exit(1)
        elif t_type == parser.Define:
            self.definitions.update({str(node.name): node})
        elif t_type == parser.Call:
            definition:parser.Define = self.definitions.get(str(node.name))
            # initialise the variables
            for index in range(len(definition.parameters)):
                param = definition.parameters[index]
                try:
                    if not self.is_base_type(node.arguments[index]):
                        arg = self.evaluate_tree(node.arguments[index])
                    else:
                        arg = node.arguments[index]
                except:
                    print("ERROR: No argument for parameter " + str(param))
                    print("  HELP: Check arguments passed into " + str(definition.name))
                    exit(1)
                self.variables.update({str(param): arg})
            # run the code in the definition
            for stmt in definition.statements:
                if not self.is_base_type(stmt):
                    if type(stmt) == parser.Return:
                        # evaluate return value BEFORE deleting variables
                        if not self.is_base_type(stmt.value):
                            ret_val = self.evaluate_tree(stmt.value)
                        else:
                            ret_val = stmt.value
                        # remove parameter variables
                        for param in definition.parameters:
                            self.variables.pop(str(param))
                        # actually return
                        return ret_val
                    else:
                        self.evaluate_tree(stmt)
            # remove parameter variables
            for param in definition.parameters:
                self.variables.pop(str(param))

    def evaluate(self, __tree):
        self.tree = __tree
        for __node in self.tree:
            self.node = __node
            self.evaluate_tree(self.node)