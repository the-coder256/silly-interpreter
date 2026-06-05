instructions = [
    "OUTPUT",
    "NEW",
    "PUT",
    "VARIABLE",
    "INPUT"
]

class T_Int:
    def __init__(self, value):
        self.value = int(value)
class T_Float:
    def __init__(self, value):
        self.value = float(value)
class T_String:
    def __init__(self, value):
        self.value = value[1:]
class T_Name:
    def __init__(self, value):
        self.value = value
class T_Instruction:
    def __init__(self, value):
        self.value = value
class T_TokensEnd:
    def __init__(self, value):
        self.value = value

class Tokeniser:
    def __init__(self):
        self.content = ""
        self.tokens = []
        self.current_token = ""
    
    def append_token(self, extra = None):
        if self.current_token:
            self.tokens.append(self.create_token(self.current_token))
            self.current_token = ""
        if extra:
            self.tokens.append(self.create_token(extra))
    
    def create_token(self, value):
        t_type = None
        if value in instructions:
            t_type = T_Instruction
        elif value[0] == "'":
            t_type = T_String
        else:
            try:
                x = float(value)
                if x == int(x):
                    t_type = T_Int
                else:
                    t_type = T_Float
            except:
                t_type = T_Name
        return t_type(value)
    
    def get_value(self, char):
        return self.current_token + char
    
    def tokenise(self, __content):
        self.content = __content
        inComment = 0
        inString = 0
        stringChar = ""
        for char in self.content:
            if char == "\n":
                self.append_token()
                inComment = 0
            elif inComment:
                continue
            elif (char == " " or char == "\t") and not inString:
                self.append_token()
            elif inString and char == stringChar:
                inString = 0
            elif char in ["'", '"']:
                self.current_token += "'"
                inString = 1
                stringChar = char
            elif inString:
                self.current_token += char
            elif char == "#":
                inComment = 1
            else:
                self.current_token += char
        self.append_token()   # append anything left in current_token
        self.tokens.append(T_TokensEnd("TOKENS_END"))
        return self.tokens