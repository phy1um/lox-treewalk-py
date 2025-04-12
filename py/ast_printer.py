class AstPrinter(object):
    def visit_binary_expr(self, e):
        return self._parenthesize(e.operator.lexeme, e.left, e.right)

    def visit_grouping_expr(self, e):
        return self._parenthesize("group", e.expression)

    def visit_literal_expr(self, e):
        if e.value == None:
            return "nil"
        return str(e.value)

    def visit_unary_expr(self, e):
        return self._parenthesize(e.operator.lexeme, e.right)

    def visit_comma_expr(self, e):
        return self._parenthesize(",", e.left, e.right)

    def _parenthesize(self, name, *exprs):
        out = ["(", name]
        for expr in exprs:
            out.append(" ")
            out.append(expr.accept(self))
        out.append(")")
        return "".join(out)

    def print(self, expr):
        return expr.accept(self)


if __name__ == "__main__":
    from main import Ctx
    from expr import *
    from token_type import *

    test_expression = BinaryExpr(
        UnaryExpr(Token(MINUS, "-", None, 1), LiteralExpr(123)),
        Token(STAR, "*", None, 1),
        GroupingExpr(LiteralExpr(45.67)),
    )
    print(AstPrinter().print(test_expression))
