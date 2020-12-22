import sys
import operator
from lark import Lark, Transformer, v_args


grammar = """
start: operation -> finish

operator: "+" -> plus
        | "*" -> mult

?operation: operation operator atom -> operation
         | atom

?atom: NUMBER -> number
     | "(" operation ")"

%import common.NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
"""


@v_args(inline=True)    
class Calculator(Transformer):

    def operation(self, a, op, b):
        return op(a, b)

    def number(self, value):
        return int(value)

    def finish(self, value):
        return value

    def plus(self, *args):
        return operator.add

    def mult(self, *args):
        return operator.mul



def main():
    parser = Lark(grammar, parser='lalr', transformer=Calculator())
    print(sum([parser.parse(line.strip()) for line in sys.stdin if line.strip()]))


if __name__ == '__main__':
    main()
