# https://www.codewars.com/kata/546d15cebed2e10334000ed9


def solve_runes(runes):
    cant_be = []
    i_operator = None
    i_equal = None
    for i, c in enumerate(runes):
        if (i_operator is None) and (c in ["+", "*"] or (c == "-" and i > 0)):
            i_operator = i

        elif c == "=":
            i_equal = i

        elif c in "0123456789":
            cant_be.append(c)

    first = runes[:i_operator]
    second = runes[i_operator+1:i_equal]
    operator = runes[i_operator]
    result = runes[i_equal+1:]

    # Zero is special:
    if "0" not in cant_be:
        for num in [first, second, result]:
            if num[0] == "?" and len(num) > 1:
                cant_be.append("0")
                break

    can_be = [i for i in "0123456789" if i not in cant_be]

    for r in can_be:
        v_first = int(first.replace("?", r))
        v_second = int(second.replace("?", r))
        v_result = int(result.replace("?", r))

        if operator == "+" and v_first + v_second == v_result:
            return int(r)

        if operator == "*" and v_first * v_second == v_result:
            return int(r)

        if operator == "-" and v_first - v_second == v_result:
            return int(r)

    return -1


if __name__ == "__main__":
    print(solve_runes("1+1=?"))
    print(solve_runes("123*45?=5?088"))
    print(solve_runes("-5?*-1=5?"))
