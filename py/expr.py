from dataclasses import dataclass
from lox_token import Token


class Expr(object):
    pass


@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, v):
        return v.visit_binary_expr(self)


@dataclass
class GroupingExpr(Expr):
    expression: Expr

    def accept(self, v):
        return v.visit_grouping_expr(self)


@dataclass
class LiteralExpr(Expr):
    value: object

    def accept(self, v):
        return v.visit_literal_expr(self)


@dataclass
class UnaryExpr(Expr):
    operator: Token
    right: Expr

    def accept(self, v):
        return v.visit_unary_expr(self)


@dataclass
class CommaExpr(Expr):
    left: Expr
    right: Expr

    def accept(self, v):
        return v.visit_comma_expr(self)


@dataclass
class TernaryExpr(Expr):
    condition: Expr
    left: Expr
    right: Expr

    def accept(self, v):
        return v.visit_ternary_expr(self)
