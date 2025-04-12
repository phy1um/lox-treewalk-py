from token_type import *
from expr import *


class RuntimeException(Exception):
    def __init__(self, token, msg):
        super.__init__(msg)
        self.token = token


def _is_truthy(value):
    return value is not None and value is not False


class Interpreter(object):
    def __init__(self, ctx):
        self._ctx = ctx

    def visit_binary_expr(self, e):
        left = self.evaluate(e.left)
        right = self.evaluate(e.right)
        tt = e.operator.token_type
        if tt == MINUS:
            _assert_number_operand(left, right)
            return left - right
        elif tt == SLASH:
            _assert_number_operand(left, right)
            return left / right
        elif tt == STAR:
            _assert_number_operand(left, right)
            return left * right
        elif tt == PLUS:
            # assert numeric add if not both strings
            if type(left) != str or type(right) != str:
                _assert_number_operand(left, right)
            return left + right
        elif tt == GREATER:
            _assert_number_operand(left, right)
            return left > right
        elif tt == GREATER_EQUAL:
            _assert_number_operand(left, right)
            return left >= right
        elif tt == LESS:
            _assert_number_operand(left, right)
            return left < right
        elif tt == LESS_EQUAL:
            _assert_number_operand(left, right)
            return left <= right
        elif tt == BANG_EQUAL:
            return left != right
        elif tt == EQUAL_EQUAL:
            return left == right
        raise self.error(e.operator, "Unknown binary operator.")

    def visit_grouping_expr(self, e):
        return self.evaluate(e.expression)

    def visit_literal_expr(self, e):
        return e.value

    def visit_unary_expr(self, e):
        right = self.evaluate(e.right)
        if e.operator.token_type == MINUS:
            _assert_number_operand(e.operator, right)
            return -1 * right
        elif e.operator.token_type == BANG:
            return not _is_truthy(right)
        raise self.error(
            e.operator, f"Unknown unary operator: {e.operator.token_type}."
        )

    def visit_comma_expr(self, e):
        self.evaluate(e.left)
        return self.evaluate(e.right)

    def visit_ternary_expr(self, e):
        condition = self.evaluate(e.condition)
        if _is_truthy(condition):
            return self.evaluate(e.left)
        else:
            return self.evaluate(e.right)

    def error(msg):
        return RuntimeException(msg)

    def evaluate(self, expr):
        try:
            return expr.accept(self)
        except RuntimeException as e:
            self._ctx.runtime_error(e)


def _assert_number_operand(token, *operands):
    for operand in operands:
        if type(operand) != int and type(operand) != float:
            raise RuntimeException(token, "Operand must be a number.")
