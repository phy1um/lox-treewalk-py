from scanner import Scanner
from parser import Parser
from ast_printer import AstPrinter
from token_type import EOF


class Ctx(object):
    def __init__(self):
        import sys

        self._isError = False
        self._output = sys.stderr

    def _report(self, line, where, msg):
        print(f"[line {line}] Error{where}: {msg}", file=self._output)

    def error(self, line, msg):
        self._report(line, "", msg)
        self._isError = True

    def token_error(self, token, msg):
        if token.token_type == EOF:
            self._report(token.line, " at end", msg)
        else:
            self._report(token.line, f" at '{token.lexeme}'", msg)

    def has_error(self):
        return self._isError

    def clear_error(self):
        self._isError = False


def run(ctx, body):
    scanner = Scanner(ctx, body)
    tokens = scanner.all()
    parser = Parser(ctx, tokens)
    if ctx.has_error():
        return 1
    print(AstPrinter().print(parser.parse()))
    return 0


def repl():
    print("Running Lox REPL")
    ctx = Ctx()
    while True:
        line = input("> ")
        if len(line) == 0:
            break
        run(ctx, line)
        ctx.clear_error()
        print()


def usage():
    import sys

    print(
        """Usage: lox <script>
    """
    )
    sys.exit(1)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2:
        usage()
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            ctx = Ctx()
            run(ctx, f.read())
            if ctx.has_error():
                sys.exit(65)
    else:
        repl()
