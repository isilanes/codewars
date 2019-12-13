# https://www.codewars.com/kata/shortest-knight-path/python

MAX_ROW = 7
MAX_COL = 7
MAX_STEPS = 2  # try these many steps at most (avoid infinite loops due to, say,  bugs)
I_TO_COL = "abcdefgh"
COL_TO_I = {letter: i for i, letter in enumerate(I_TO_COL)}


def ij_to_algebraic(ij):
    """
    Given position in (i, j) format, return algebraic equivalent.

    :param tuple ij: position in (int, int) format (i = column, j = row, both 0-7)
    :return str: algebraic notation, such as 'a3' or 'b5'
    """
    i, j = ij

    return f"{I_TO_COL[i]}{j+1}"


def algebraic_to_ij(algebraic):
    """
    Given position 'algebraic' in algebraic notation, return (i, j) tuple.

    :param str algebraic: string with algebraic notation.
    :return tuple: position in (int, int) format, (col, row) order.
    """
    letter, j = list(algebraic)

    return COL_TO_I[letter], int(j)-1


def destinations_from(pos):
    """
    Given a position (in (i, j) format), return all possible destinations (in same format).

    :param tuple pos: origin position in (i, j) format.
    :return list: valid destination positions in (i, j) format.
    """
    i, j = pos

    if i > 0:
        if j > 1:
            yield i-1, j-2
        if j < 6:
            yield i-1, j+2
        if i > 1:
            if j > 0:
                yield i-2, j-1
            if j < 7:
                yield i-2, j+1

    if i < 7:
        if j > 1:
            yield i+1, j-2
        if j < 6:
            yield i+1, j+2
        if i < 6:
            if j > 0:
                yield i+2, j-1
            if j < 7:
                yield i+2, j+1


def knight(initial, final):
    """
    Given initial position 'initial' and destination position 'final', both in algebraic notation, return minimum number
    of steps to reach final from initial.

    :param str initial: initial position in algebraic format.
    :param str final: final position in algebraic format.
    :return int: minimum amount of steps from initial to final.
    """
    sources = [algebraic_to_ij(initial)]

    for i_step in range(MAX_STEPS):  # just in case, avoid while True
        destinations = set()
        for source in sources:
            for destination in destinations_from(source):
                if ij_to_algebraic(destination) == final:
                    return i_step + 1
                if destination not in sources:
                    destinations.add(destination)  # remember this is a set()

        sources = destinations

    raise ValueError(f"Couldn't reach destination in {MAX_STEPS} steps")  # we should never reach here. Signal if we do.


def main():
    print(knight("a1", "d4"))


if __name__ == "__main__":
    main()
