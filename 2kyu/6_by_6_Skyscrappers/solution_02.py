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


class Puzzle:

    def __init__(self, clues):
        self.clues = clues

        self.all_combos = list(permutations(range(1, 7)))
        self.solution_combos = [None for _ in range(11)]
        self.skipped = [0 for _ in range(11)]

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
        return tuple([self.solution_combos[i] for i in range(0, 11, 2)])

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
            do_break = self.place_combo(i_placement)
            if do_break:
                break
            if self.solution_combos[i_placement] is None:
                self.skipped[i_placement] = 0
                self.skipped[i_placement-1] += 1
                i_placement -= 1
                continue

            i_placement += 1

        return self.solution

    def place_combo(self, i_placement):
        if i_placement == 0:
            self.place_first_combo()

        elif i_placement == 1:
            self.place_second_combo()

        elif i_placement == 2:
            self.place_third_combo()

        elif i_placement == 3:
            self.place_fourth_combo()

        elif i_placement == 4:
            self.place_fifth_combo()

        elif i_placement == 5:
            self.place_sixth_combo()

        elif i_placement == 6:
            self.place_seventh_combo()

        elif i_placement == 7:
            self.place_eighth_combo()

        elif i_placement == 8:
            self.place_ninth_combo()

        elif i_placement == 9:
            self.place_tenth_combo()

        elif i_placement == 10:
            self.place_eleventh_combo()

        else:
            return True

    def place_first_combo(self):
        valids = self.combos_for_row[0]
        if len(valids) > self.skipped[0]:  # although this would mean there is no solution
            self.solution_combos[0] = valids[self.skipped[0]]

    def place_second_combo(self):
        v0 = self.solution_combos[0][0]
        valids = [c for c in self.combos_for_col[0] if c[0] == v0]
        try:
            self.solution_combos[1] = valids[self.skipped[1]]
        except IndexError:
            self.solution_combos[1] = None

    def place_third_combo(self):
        v0 = self.solution_combos[1][1]
        valids = [c for c in self.combos_for_row[1] if c[0] == v0]
        try:
            self.solution_combos[2] = valids[self.skipped[2]]
        except IndexError:
            self.solution_combos[2] = None

    def place_fourth_combo(self):
        v0 = self.solution_combos[0][1]
        v1 = self.solution_combos[2][1]
        valids = [c for c in self.combos_for_col[1] if c[0] == v0 and c[1] == v1]
        try:
            self.solution_combos[3] = valids[self.skipped[3]]
        except IndexError:
            self.solution_combos[3] = None

    def place_fifth_combo(self):
        v0 = self.solution_combos[1][2]
        v1 = self.solution_combos[3][2]
        valids = [c for c in self.combos_for_row[2] if c[0] == v0 and c[1] == v1]
        try:
            self.solution_combos[4] = valids[self.skipped[4]]
        except IndexError:
            self.solution_combos[4] = None

    def place_sixth_combo(self):
        v0 = self.solution_combos[0][2]
        v1 = self.solution_combos[2][2]
        v2 = self.solution_combos[4][2]
        valids = [c for c in self.combos_for_col[2] if c[0] == v0 and c[1] == v1 and c[2] == v2]
        try:
            self.solution_combos[5] = valids[self.skipped[5]]
        except IndexError:
            self.solution_combos[5] = None

    def place_seventh_combo(self):
        v0 = self.solution_combos[1][3]
        v1 = self.solution_combos[3][3]
        v2 = self.solution_combos[5][3]
        valids = [c for c in self.combos_for_row[3] if c[0] == v0 and c[1] == v1 and c[2] == v2]
        try:
            self.solution_combos[6] = valids[self.skipped[6]]
        except IndexError:
            self.solution_combos[6] = None

    def place_eighth_combo(self):
        v0 = self.solution_combos[0][3]
        v1 = self.solution_combos[2][3]
        v2 = self.solution_combos[4][3]
        v3 = self.solution_combos[6][3]
        valids = [c for c in self.combos_for_col[3] if c[0] == v0 and c[1] == v1 and c[2] == v2 and c[3] == v3]
        try:
            self.solution_combos[7] = valids[self.skipped[7]]
        except IndexError:
            self.solution_combos[7] = None

    def place_ninth_combo(self):
        v0 = self.solution_combos[1][4]
        v1 = self.solution_combos[3][4]
        v2 = self.solution_combos[5][4]
        v3 = self.solution_combos[7][4]
        valids = [c for c in self.combos_for_row[4] if c[0] == v0 and c[1] == v1 and c[2] == v2 and c[3] == v3]
        try:
            self.solution_combos[8] = valids[self.skipped[8]]
        except IndexError:
            self.solution_combos[8] = None

    def place_tenth_combo(self):
        v0 = self.solution_combos[0][4]
        v1 = self.solution_combos[2][4]
        v2 = self.solution_combos[4][4]
        v3 = self.solution_combos[6][4]
        v4 = self.solution_combos[8][4]
        valids = [c for c in self.combos_for_col[4] if c[0] == v0 and c[1] == v1 and c[2] == v2 and c[3] == v3 and c[4] == v4]
        try:
            self.solution_combos[9] = valids[self.skipped[9]]
        except IndexError:
            self.solution_combos[9] = None

    def place_eleventh_combo(self):
        v0 = self.solution_combos[1][5]
        v1 = self.solution_combos[3][5]
        v2 = self.solution_combos[5][5]
        v3 = self.solution_combos[7][5]
        v4 = self.solution_combos[9][5]
        valids = [c for c in self.combos_for_row[5] if c[0] == v0 and c[1] == v1 and c[2] == v2 and c[3] == v3 and c[4] == v4]
        try:
            self.solution_combos[10] = valids[self.skipped[10]]
        except IndexError:
            self.solution_combos[10] = None
