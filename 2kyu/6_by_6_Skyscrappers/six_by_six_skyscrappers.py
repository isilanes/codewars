# https://www.codewars.com/kata/5679d5a3f2272011d700000d

from itertools import permutations


def seen_from_left(combo):
    seen = 0
    max_h = 0
    for h in combo:
        if h == 6:
            seen += 1
            break

        if h > max_h:
            seen += 1
            max_h = h

    return seen


def seen_from_right(combo):
    return seen_from_left(reversed(combo))


def seen_from_sides(combo):
    return seen_from_left(combo), seen_from_right(combo)


def solve_puzzle(clues):
    return Puzzle(clues).solve()


def main():
    clues = (
        3, 2, 2, 3, 2, 1,
        1, 2, 3, 3, 2, 2,
        5, 1, 2, 2, 4, 3,
        3, 2, 1, 2, 2, 4
    )

    print(solve_puzzle(clues))


class Puzzle:

    def __init__(self, clues):
        self.all_combos = list(permutations(range(1, 7)))
        self.clues = clues
        self._row_clues = None
        self._seen_from_sides = None

    @property
    def row_clues(self):
        if self._row_clues is None:
            self._row_clues = [
                (self.clues[23], self.clues[6]),
                (self.clues[22], self.clues[7]),
                (self.clues[21], self.clues[8]),
                (self.clues[20], self.clues[9]),
                (self.clues[19], self.clues[10]),
                (self.clues[18], self.clues[11]),
            ]

        return self._row_clues

    @property
    def seen_from_sides(self):
        if self._seen_from_sides is None:
            self._seen_from_sides = []
            for i, combo in enumerate(self.all_combos):
                seen = seen_from_sides(combo)
                self._seen_from_sides.append(seen)

        return self._seen_from_sides

    def fits_in_row(self, i_row, i_combo):
        left_clue, right_clue = self.row_clues[i_row]
        left_seen, right_seen = self.seen_from_sides[i_combo]

        if left_clue != 0 and left_clue != left_seen:
            return False

        if right_clue != 0 and right_clue != right_seen:
            return False

        return True

    def solve(self):
        n_row = 0
        while n_row < 5:
            for i, combo in enumerate(self.all_combos):
                if self.fits_in_row(n_row, i):
                    print(combo)
                    n_row += 1
                    break


if __name__ == "__main__":
    main()
