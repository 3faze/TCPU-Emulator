class Register:
    def __init__(self, name, type):
        self.name = name
        self.value = 0.0
        self.type = type

    def __str__(self):
        return(self.value)

    def read_val(self):
        return self.value
    def write_val(self, value):
        self.value = value

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class LexicalToken:
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.value = token_value

def next_token(src):
    # Current char also keeps track of the length of the current token
    current_char = 0

    # We use this to automatically handle the case where n >= len(src) everywhere
    def get_char(n):
        if n >= len(src):
            return "\0"
        else:
            return src[n]

    # Tells us if a character can be part of an identifier
    def is_ident_character(c, first):
        #print(c, src[current_char], type(c))
        if first:
            return c.isalpha() or c == "_"
        else:
            # Identifiers can have numbers in them, just not as the first character
            return c.isalnum() or c == "_"

    if get_char(current_char) == "\0":
        return "EOF", current_char

    if get_char(current_char) == "(":
        current_char += 1
        return "LPAREN", current_char

    if get_char(current_char) == ")":
        current_char += 1
        return "RPAREN", current_char

    if get_char(current_char) == ",":
        current_char += 1
        return "COMMA", current_char

    if get_char(current_char) == "#":
        while get_char(current_char) != "\n" and get_char(current_char) != "\0":
            current_char += 1
        return "COMMENT", current_char

    if get_char(current_char) == "+":
        current_char += 1
        if get_char(current_char) == "=":
            current_char += 1
            return "ADD_EQ", current_char
        return "ADD", current_char

    if get_char(current_char) == "-":
        current_char += 1
        if get_char(current_char) == "=":
            current_char += 1
            return "SUB_EQ", current_char
        return "SUB", current_char

    if get_char(current_char) == "*":
        current_char += 1
        if get_char(current_char) == "=":
            current_char += 1
            return "MUL_EQ", current_char
        return "MUL", current_char

    if get_char(current_char) == "/":
        current_char += 1
        if get_char(current_char) == "=":
            current_char += 1
            return "DIV_EQ", current_char
        return "DIV", current_char

    if get_char(current_char) == ";":
        current_char += 1
        return "SEMI", current_char

    if get_char(current_char) == "\n":
        current_char += 1
        return "NL", current_char

    if get_char(current_char) == '"':
        current_char += 1
        while get_char(current_char) != '"':
            current_char += 1

        return "STRING", current_char

    if get_char(current_char) == "<":
        current_char += 1
        if get_char(current_char) == "<":
            current_char += 1
            if get_char(current_char) == "=":
                current_char += 1
                return "LSHIFT_EQ", current_char
            return "LSHIFT", current_char
        if get_char(current_char) == "=":
            current_char += 1
            return "LT_EQ", current_char
        return "LT", current_char

    if get_char(current_char) == ">":
        current_char += 1
        if get_char(current_char) == ">":
            current_char += 1
            if get_char(current_char) == "=":
                current_char += 1
                return "RSHIFT_EQ", current_char
            return "RSHIFT", current_char
        if get_char(current_char) == "=":
            current_char += 1
            return "GT_EQ", current_char
        return "GT", current_char

    if get_char(current_char).isspace():
        while get_char(current_char).isspace():
            current_char += 1
        return "WHITESPACE", current_char

    if get_char(current_char).isdigit():
        while get_char(current_char).isdigit():
            current_char += 1
        return "NUMBER", current_char

    if is_ident_character(get_char(current_char), True):
        while is_ident_character(get_char(current_char), False):
            current_char += 1

        return "IDENT", current_char

def tokenize(src):
    to_skip = ["COMMENT", "WHITESPACE"]
    current_loc = 0

    # A convenient loop to skip tokens we don't want to parse
    while True:
        token_ty, token_len = next_token(src)
        token_start = current_loc
        #val = src[token_start:token_start+token_len]
        current_loc += token_len

        val = src[:token_len]
        src = src[token_len:]

        if token_ty not in to_skip:
            yield token_ty, token_start, token_len, val


class AddNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.type = "AddNode"

class InstructionParser:
    def __init__(self):
        self.src = None
        self.curr_token = None
        self.last_add = None

    def parse(self, src):
        nodes = []
        self.src = src
        for token in src:
            #print(token)
            if token[0] == "IDENT":
                if token[3] == "add":
                    self.last_add = AddNode()
                else:
                    if self.last_add != None:
                        if self.last_add.left == None:
                            self.last_add.left = token[3]
                        elif self.last_add.left != None:
                            if self.last_add.right == None:
                                self.last_add.right = token[3]
                                #print(self.last_add.left, self.last_add.right)
                                nodes.append(self.last_add)
                                self.last_add = None
            if token[0] == "NL":
                if self.last_add != None:
                    self.last_add = None
            if token[0] == "EOF":
                return nodes

