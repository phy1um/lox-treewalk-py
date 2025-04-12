from token_type import TOKEN_TYPE_NAMES


class Token(object):
    def __init__(self, token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{TOKEN_TYPE_NAMES[self.token_type]} {self.lexeme} {self.literal}"
