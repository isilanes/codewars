MAX_ROW = 7
MAX_COL = 7
I_TO_COL = "abcdefgh"
COL_TO_I = {letter: i for i, letter in enumerate(I_TO_COL)}


def ij_to_algebraic(ij):
    """
    Given position in (i, j) format, return algebraic equivalent.

    :param tuple ij: position in (int, int) format (i = column, j = row, both 0-7)
    :return str: algebraic notation, such as 'a3' or 'b5'
    """
    i, j = ij

    return f"{I_TO_COL[i]}{j}"


def algebraic_to_ij(algebraic):
    """
    Given position 'algebraic' in algebraic notation, return (i, j) tuple.

    :param str algebraic: string with algebraic notation.
    :return tuple: position in (int, int) format, (col, row) order.
    """
    pass


if __name__ == "__main__":
    print(COL_TO_I)
