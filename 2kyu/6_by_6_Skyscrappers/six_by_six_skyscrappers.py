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
        self.solution_indices = [None for _ in range(6)]
        self.solution = None

        self._row_clues = None
        self._col_clues = None
        self._seen_from_sides = None
        self._combos_for_row = None

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
    def col_clues(self):
        if self._col_clues is None:
            self._col_clues = [
                (self.clues[0], self.clues[17]),
                (self.clues[1], self.clues[16]),
                (self.clues[2], self.clues[15]),
                (self.clues[3], self.clues[14]),
                (self.clues[4], self.clues[13]),
                (self.clues[5], self.clues[12]),
            ]

        return self._col_clues

    @property
    def seen_from_sides(self):
        if self._seen_from_sides is None:
            self._seen_from_sides = {}
            for i, combo in enumerate(self.all_combos):
                self._seen_from_sides[combo] = seen_from_sides(combo)

        return self._seen_from_sides

    @property
    def combos_for_row(self):
        if self._combos_for_row is None:
            self._combos_for_row = []
            for i_row in range(6):
                valid_combos = [c for c in self.all_combos if self.fits_in_row(i_row, c)]
                self._combos_for_row.append(valid_combos)

        return self._combos_for_row

    def fits_in_row(self, i_row, combo):
        left_clue, right_clue = self.row_clues[i_row]
        left_seen, right_seen = self.seen_from_sides[combo]

        if left_clue != 0 and left_clue != left_seen:
            return False

        if right_clue != 0 and right_clue != right_seen:
            return False

        return True

    def fits_in_col(self, j_col, combo):
        top_clue, bottom_clue = self.col_clues[j_col]
        top_seen, bottom_seen = self.seen_from_sides[combo]

        if top_clue != 0 and top_clue != top_seen:
            return False

        if bottom_clue != 0 and bottom_clue != bottom_seen:
            return False

        return True

    def fits_with_previous(self, i_row, combo):
        for i_col, number in enumerate(combo):
            previous_numbers = [self.combos_for_row[i][j][i_col] for i, j in enumerate(self.solution_indices[:i_row])]
            if number in previous_numbers:
                return False

        return True

    def deduce_last_combo(self):
        for i_col in range(6):
            previous_numbers = [self.combos_for_row[i][j][i_col] for i, j in enumerate(self.solution_indices[:5])]
            yield 21 - sum(previous_numbers)  # since sum(range(1, 7)) = 21

    def columns_fit(self, combo):
        for i_col in range(6):
            column = [self.combos_for_row[i][j][i_col] for i, j in enumerate(self.solution_indices[:5])]
            column = tuple(column + [combo[i_col]])
            if not self.fits_in_col(i_col, column):
                return False

        return True

    def solve(self):
        n_row = 0
        while n_row < 6:

            # Last row is special:
            if n_row == 5:
                last_combo = tuple(self.deduce_last_combo())
                self.columns_fit(last_combo)
                if not self.fits_in_row(5, last_combo) or not self.columns_fit(last_combo):
                    self.solution_indices[5] = None
                    n_row -= 1
                    continue

                self.solution = [self.combos_for_row[i][j] for i, j in enumerate(self.solution_indices[:5])]
                self.solution.append(last_combo)
                break

            i_start = 0
            if self.solution_indices[n_row] is not None:
                i_start = self.solution_indices[n_row] + 1

            match_found = False
            for i in range(i_start, len(self.combos_for_row[n_row])):
                current_combo = self.combos_for_row[n_row][i]

                if not self.fits_in_row(n_row, current_combo):
                    continue

                if not self.fits_with_previous(n_row, current_combo):
                    continue

                self.solution_indices[n_row] = i
                match_found = True
                break

            if match_found:  # go to next row
                n_row += 1
            else:  # discard this line and go back one row
                self.solution_indices[n_row] = None
                n_row -= 1

        return tuple(self.solution)


if __name__ == "__main__":
    main()
