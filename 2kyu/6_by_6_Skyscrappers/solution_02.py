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


def solve_puzzle(clues, rotate=None):
    return Puzzle(clues).solve(rotate)


class Puzzle:

    def __init__(self, clues):
        self.clues = clues

        self.all_combos = list(permutations(range(1, 7)))
        self.solution_indices = [None for _ in range(6)]

        self._row_clues = None
        self._col_clues = None
        self._seen_from_sides = None
        self._combos_for_row = None
        self._combos_for_col = None
        self._placement_to_row = None

    def clean(self):
        self.solution_indices = [None for _ in range(6)]
        self._row_clues = None
        self._col_clues = None
        self._seen_from_sides = None
        self._combos_for_row = None
        self._combos_for_col = None
        self._placement_to_row = None

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

    @property
    def combos_for_col(self):
        if self._combos_for_col is None:
            self._combos_for_col = []
            for i_col in range(6):
                valid_combos = [c for c in self.all_combos if self.fits_in_col(i_col, c)]
                self._combos_for_col.append(valid_combos)

        return self._combos_for_col

    @property
    def placement_to_row(self):
        """Which actual row corresponds to i-th placement."""

        if self._placement_to_row is None:
            dsu = [(len(self.combos_for_row[i]), i) for i in range(6)]
            self._placement_to_row = [i for _, i in sorted(dsu)]

        return self._placement_to_row

    @property
    def solution(self):
        return tuple([self.combos_for_row[i][j] for i, j in enumerate(self.solution_indices)])

    @property
    def n_combinations_rows(self):
        p = 1
        for c in self.combos_for_row:
            p *= len(c)

        return p

    @property
    def n_combinations_cols(self):
        p = 1
        for c in self.combos_for_col:
            p *= len(c)

        return p

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

    def fits_with_previous(self, i_placement, combo):
        row_indices = self.placement_to_row[:i_placement + 1]
        for i_col in range(6):
            numbers = []
            for i_row in row_indices[:-1]:
                combos_for_that_row = self.combos_for_row[i_row]
                combo_for_that_row = combos_for_that_row[self.solution_indices[i_row]]
                number_on_that_row = combo_for_that_row[i_col]
                numbers.append(number_on_that_row)
            numbers.append(combo[i_col])
            numbers = tuple(numbers)

            possibles = []
            for possible_combo in self.combos_for_col[i_col]:
                possible = tuple([possible_combo[i] for i in row_indices])
                possibles.append(possible)

            if numbers not in possibles:
                return False

        return True

    def solve(self):
        i_placement = 0
        while i_placement < 11:
            combo = self.place_combo(i_placement)
            print(combo)

        return self.solution

    def place_combo(self, i_placement):
        if i_placement == 0:
            return self.place_first_combo()

        return None

    def place_first_combo(self):
        valid = self.combos_for_row[0]