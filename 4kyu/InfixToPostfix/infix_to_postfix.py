# https://www.codewars.com/kata/52e864d1ffb6ac25db00017f/train/python


def has_greater_precedence(operator_a, operator_b):
    """Returns True if operator_a has greater precedence than operator_b. False otherwise."""

    if operator_a == "^":
        return operator_b != "^"

    if operator_a in "*/":
        return operator_b in "+-"

    return False


def have_equal_precedence(operator_a, operator_b):
    """Returns True if both operators have equal precedence. False otherwise."""

    if operator_a in "+-":
        return operator_b in "+-"

    if operator_a in "*/":
        return operator_b in "*/"

    return operator_a == operator_b  # for remaining case "^"


def is_left_associative(operator):
    """Return True if operator is left-associative. False otherwise."""

    return operator in "+-*/"


def to_postfix(infix):
    """
    We use Dijkstra's shunting-yard algorithm:
    https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    """
    output_queue = []
    operator_stack = []
    for token in infix:
        if token in "0123456789":  # i.e. an operand, as they are single digits
            output_queue.append(token)

        elif token == "(":
            operator_stack.append(token)

        elif token == ")":
            while operator_stack[-1] != "(":
                operator = operator_stack.pop()
                output_queue.append(operator)

            operator_stack.pop()  # discard the "(" that surely is now on top of stack (guaranteed paired parentheses)

        else:  # then it is an operator (we could also check for token in "+-*/^")
            if not operator_stack:  # no operator in stack yet
                operator_stack.append(token)
                continue

            while operator_stack:
                top = operator_stack[-1]
                if top == "(":
                    break

                if has_greater_precedence(top, token) or (have_equal_precedence(top, token) and is_left_associative(token)):
                    output_queue.append(operator_stack.pop())
                else:
                    break

            operator_stack.append(token)

    # Having consumed all tokens in input:
    output_queue.extend(reversed(operator_stack))

    return "".join(output_queue)


def main():
    infixes = [
        "2+7*5",
        "3*3/(7+1)",
        "5+(6-2)*9+3^(7-1)",
        "(5-4-1)+9/5/2-7/1/7",
    ]
    postfixes = [
        "275*+",
        "33*71+/",
        "562-9*+371-^+",
        "54-1-95/2/+71/7/-",
    ]
    for infix, postfix in zip(infixes, postfixes):
        print(f"{infix} -> {postfix}")
        assert to_postfix(infix) == postfix, to_postfix(infix)


if __name__ == "__main__":
    main()
