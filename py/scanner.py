from token_type import *
from token import Token

KEYWORDS = {
    "and": AND,
    "class": CLASS,
    "else": ELSE,
    "false": FALSE,
    "for": FOR,
    "fun": FUN,
    "if": IF,
    "nil": NIL,
    "or": OR,
    "print": PRINT,
    "return": RETURN,
    "super": SUPER,
    "this": THIS,
    "true": TRUE,
    "var": VAR,
    "while": WHILE,
}


def _is_identifier_char_first(c):
    return c.isalpha() or c == "_"


def _is_identifier_char(c):
    return c.isalpha() or c.isdigit() or c == "_"


class Scanner(object):
    def __init__(self, ctx, source):
        self._x = ctx
        self._src = source
        self._start = 0
        self._current = 0
        self._line = 1

    def done(self):
        return self._current >= len(self._src)

    def next(self):
        self._start = self._current
        c = self._advance()
        if c == "(":
            return self._token(LEFT_PAREN, None)
        elif c == ")":
            return self._token(RIGHT_PAREN, None)
        elif c == "{":
            return self._token(LEFT_BRACE, None)
        elif c == "}":
            return self._token(RIGHT_BRACE, None)
        elif c == ",":
            return self._token(COMMA, None)
        elif c == ".":
            return self._token(DOT, None)
        elif c == "+":
            return self._token(PLUS, None)
        elif c == ";":
            return self._token(SEMICOLON, None)
        elif c == "*":
            return self._token(STAR, None)
        elif c == "!":
            if self._match("="):
                return self._token(BANG_EQUAL, None)
            else:
                return self._token(BANG, None)
        elif c == "=":
            if self._match("="):
                return self._token(EQUAL_EQUAL, None)
            else:
                return self._token(EQUAL, None)
        elif c == ">":
            if self._match("="):
                return self._token(GREATER_EQUAL, None)
            else:
                return self._token(GREATER, None)
        elif c == "<":
            if self._match("="):
                return self._token(LESS_EQUAL, None)
            else:
                return self._token(LESS, None)
        elif c == "/":
            # comment
            if self._match("/"):
                while self._peek() != "\n" and not self.done():
                    self._advance()
                if self.done():
                    return None
                return self.next()
            else:
                return self._token(SLASH, None)
        elif c == " " or c == "\r" or c == "\t":
            return
        elif c == "\n":
            self._line += 1
            return
        elif c == '"':
            return self._string()
        elif c.isdigit():
            return self._number()
        elif _is_identifier_char_first(c):
            return self._identifier()

        self._x.error(self._line, f'Unexpected character "{c}".')

    def all(self):
        out = []
        while not self.done():
            nxt = self.next()
            if nxt is not None:
                out.append(nxt)
        return out

    def _token(self, token_type, literal):
        text = self._src[self._start : self._current]
        return Token(token_type, text, literal, self._line)

    def _advance(self):
        out = self._src[self._current]
        self._current += 1
        return out

    def _match(self, c):
        if self.done():
            return False
        elif self._src[self._current] != c:
            return False
        self._current += 1
        return True

    def _peek(self):
        if self.done():
            return "\0"
        return self._src[self._current]

    def _string(self):
        while self._peek() != '"' and not self.done():
            if self._peek() == "\n":
                self._line += 1
            self._advance()
        if self.done():
            self._x.error(self._line, "Unterminated string.")
            return
        self._advance()
        value = self._src[self._start + 1 : self._current - 1]
        return self._token(STRING, value)

    def _number(self):
        while self._peek().isdigit():
            self._advance()
        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()
        return self._token(NUMBER, float(self._src[self._start : self._current]))

    def _identifier(self):
        while _is_identifier_char(self._peek()):
            self._advance()

        text = self._src[self._start : self._current]
        if text in KEYWORDS:
            return self._token(KEYWORDS[text], None)
        else:
            return self._token(IDENTIFIER, None)

    def _peek_next(self):
        if self._current + 1 >= len(self._src):
            return "\0"
        return self._src[self._current + 1]
