import re
import sys
from itertools import takewhile, dropwhile

from lark import Lark


def rulify_nums(rules):
    # Lark doesn't like rule names that are just integers, so prepend 'r' so
    # that, e.g., rule 0 becomes rule r0.
    return re.sub(r'(\d+)', r'r\1', rules)


def check(message, parser):
    try:
        parser.parse(message)
        return True
    except:
        return False


def main():
    rules = '\n'.join([line.strip() for line in takewhile(lambda l: l.strip(), sys.stdin)])
    messages = [line.strip() for line in dropwhile(lambda l: not l.strip(), sys.stdin)]

    grammar = rulify_nums(rules)
    parser = Lark(grammar, start='r0')
    print(len([m for m in messages if check(m, parser)]))

    
if __name__ == '__main__':
    main()
