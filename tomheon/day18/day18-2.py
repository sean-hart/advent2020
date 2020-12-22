import sys
import operator
from lark import Lark, Transformer, v_args


grammar = """
start: product -> finish

?product: product "*" product -> mult
       | sum

?sum: sum "+" sum -> plus
   | atom

?atom: NUMBER -> number
     | "(" product ")"

%import common.NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
"""


@v_args(inline=True)    
class Calculator(Transformer):

    def number(self, value):
        return int(value)

    def finish(self, value):
        return value

    def plus(self, a, b):
        return a + b

    def mult(self, a, b):
        return a * b


def main():
    parser = Lark(grammar, parser='lalr', transformer=Calculator())
    print(sum([parser.parse(line.strip()) for line in sys.stdin if line.strip()]))


if __name__ == '__main__':
    main()
