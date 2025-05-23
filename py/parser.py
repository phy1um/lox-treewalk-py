from token_type import *
from expr import *


class ParseError(Exception):
    pass


class Parser(object):
    def __init__(self, ctx, tokens):
        self._tokens = tokens
        self._current = 0
        self._ctx = ctx

    def parse(self):
        try:
            return self.comma()
        except ParseError:
            return None

    def comma(self):
        expr = self.ternary()
        while self.match(COMMA):
            expr = CommaExpr(expr, self.ternary())
        return expr

    def ternary(self):
        condition = self.expression()
        if self.match(QUESTION):
            left = self.expression()
            if self.match(COLON):
                right = self.expression()
                return TernaryExpr(condition, left, right)
            raise self.error(
                self.peek().token_type, "Missing ':' from '?:' expression."
            )
        return condition

    def expression(self):
        return self.equality()

    def equality(self):
        if self.match(BANG_EQUAL, EQUAL_EQUAL):
            err = self.error(
                self.previous(), "Missing left hand side of binary operator."
            )
            self.comparison()
            raise err
        expr = self.comparison()
        while self.match(BANG_EQUAL, EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def comparison(self):
        if self.match(GREATER, GREATER_EQUAL, LESS, LESS_EQUAL):
            err = self.error(
                self.previous(), "Missing left hand side of binary operator."
            )
            self.term()
            raise err
        expr = self.term()
        while self.match(GREATER, GREATER_EQUAL, LESS, LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def term(self):
        if self.match(PLUS):
            err = self.error(
                self.previous(), "Missing left hand side of binary operator."
            )
            self.factor()
            raise err
        expr = self.factor()
        while self.match(MINUS, PLUS):
            operator = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def factor(self):
        if self.match(SLASH, STAR):
            err = self.error(
                self.previous(), "Missing left hand side of binary operator."
            )
            self.unary()
            raise err
        expr = self.unary()
        while self.match(SLASH, STAR):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def unary(self):
        if self.match(BANG, MINUS):
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)
        return self.primary()

    def primary(self):
        if self.match(FALSE):
            return LiteralExpr(False)
        elif self.match(TRUE):
            return LiteralExpr(True)
        elif self.match(NIL):
            return LiteralExpr(None)
        elif self.match(NUMBER, STRING):
            return LiteralExpr(self.previous().literal)
        elif self.match(LEFT_PAREN):
            expr = self.expression()
            self.consume(RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)
        raise self.error(self.previous(), "Expect expression.")

    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check_any(self, *token_types):
        if self.done():
            return False
        for token_type in token_types:
            if self.peek().token_type == token_type:
                return True
        return False

    def check(self, token_type):
        return self.check_any(token_type)

    def advance(self):
        if not self.done():
            self._current += 1
        return self.previous()

    def previous(self):
        return self._tokens[self._current - 1]

    def peek(self):
        return self._tokens[self._current]

    def consume(self, token_type, error_message):
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), error_message)

    def done(self):
        return self._current >= len(self._tokens)

    def error(self, token, msg):
        self._ctx.token_error(token, msg)
        return ParseError()

    def synchronize(self):
        self.advance()
        while not self.done():
            if self.previous().token_type == SEMICOLON:
                return
            tt = self.peek().token_type
            if (
                tt == CLASS
                or tt == FOR
                or tt == FUN
                or tt == IF
                or tt == PRINT
                or tt == RETURN
                or tt == VAR
                or tt == WHILE
            ):
                return
        self.advance()
