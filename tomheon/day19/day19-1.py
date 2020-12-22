import sys
from itertools import takewhile, dropwhile


def make_atom_checker(rule_text):
    atom = rule_text.strip('"')

    def _check_atom(message):
        nonlocal atom
        if message.startswith(atom):
            return True, message[len(atom):]
        else:
            return False, message

    return _check_atom


def make_concat_checker(checkers, rule_text):
    sub_rules = [int(r) for r in rule_text.split()]

    def _check_concat(message):
        remaining = message
        nonlocal sub_rules
        for r in sub_rules:
            matched, remaining = checkers[r](remaining)
            if not matched:
                return False, message
        return True, remaining

    return _check_concat


def make_optional_checker(checkers, rule_text):
    sub_checkers = [make_concat_checker(checkers, r) for r in rule_text.split('|')]

    def _check_optional(message):
        nonlocal sub_checkers
        for c in sub_checkers:
            matched, remaining = c(message)
            if matched:
                return True, remaining
        return False, message

    return _check_optional


def is_atom_rule(rule_text):
    return rule_text.startswith('"')


def is_concat_rule(rule_text):
    return all([x not in rule_text for x in ['"', '|']])


def is_optional_rule(rule_text):
    return '|' in rule_text


def make_rules_checker(rules):
    checkers = dict()
    for rule in rules:
        rule_no, rule_text = rule.split(":")
        rule_no = int(rule_no)
        rule_text = rule_text.strip()
        checker = None
        if is_atom_rule(rule_text):
            checker = make_atom_checker(rule_text)
        elif is_concat_rule(rule_text):
            checker = make_concat_checker(checkers, rule_text)
        elif is_optional_rule(rule_text):
            checker = make_optional_checker(checkers, rule_text)
        else:
            raise Error(f"Couldn't create checker for {rule_no} {rule_text}")
        checkers[rule_no] = checker

    def _rules_checker(message):
        nonlocal checkers
        matched, remaining = checkers[0](message)
        return matched and not remaining
        
    return _rules_checker


def main():
    rules = [line.strip() for line in takewhile(lambda l: l.strip(), sys.stdin)]
    checker = make_rules_checker(rules)
    messages = [line.strip() for line in dropwhile(lambda l: not l.strip(), sys.stdin)]
    print(len([m for m in messages if checker(m)]))


if __name__ == '__main__':
    main()
