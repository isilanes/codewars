# https://www.codewars.com/kata/5679d5a3f2272011d700000d

from typing import Union
from itertools import permutations


def seen_from_left(combo):
    seen = 0
    max_h = 0
    for h in combo:
        if h == 7:
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
        self.solution_rows = [None for _ in range(6)]
        self.solution_cols = [None for _ in range(6)]
        self.skipped = [0 for _ in range(12)]
        self.valids_for_row = [None for _ in range(6)]
        self.valids_for_col = [None for _ in range(6)]

        self._row_clues = None
        self._col_clues = None
        self._seen_from_sides = None
        self._combos_for_row = None
        self._combos_for_col = None
        self._sorted_rows = None
        self._sorted_cols = None

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
    def sorted_rows(self) -> list:
        if self._sorted_rows is None:
            dsu = [(len(self.combos_for_row[i]), i) for i in range(6)]
            self._sorted_rows = [i for _, i in sorted(dsu)]

        return self._sorted_rows

    @property
    def sorted_cols(self) -> list:
        if self._sorted_cols is None:
            dsu = [(len(self.combos_for_col[i]), i) for i in range(6)]
            self._sorted_cols = [i for _, i in sorted(dsu)]

        return self._sorted_cols

    @property
    def solution(self) -> tuple:
        return tuple([row for row in self.solution_rows])

    def fits_in_row(self, i_row, combo) -> bool:
        left_clue, right_clue = self.row_clues[i_row]
        left_seen, right_seen = self.seen_from_sides[combo]

        if left_clue != 0 and left_clue != left_seen:
            return False

        if right_clue != 0 and right_clue != right_seen:
            return False

        return True

    def fits_in_col(self, j_col, combo) -> bool:
        top_clue, bottom_clue = self.col_clues[j_col]

        top_seen, bottom_seen = self.seen_from_sides[combo]

        if top_clue != 0 and top_clue != top_seen:
            return False

        if bottom_clue != 0 and bottom_clue != bottom_seen:
            return False

        return True

    def solve(self):
        i_placement = 0
        while i_placement < 12:
            combo = self.place_combo(i_placement)
            if combo is None:
                self.skipped[i_placement] = 0
                self.skipped[i_placement-1] += 1
                i_placement -= 1
                continue

            i_placement += 1

        return self.solution

    def place_combo(self, i_placement: int) -> Union[list, None]:
        if i_placement == 0:
            return self.place_first_combo()

        elif i_placement == 1:
            return self.place_second_combo()

        elif i_placement == 2:
            return self.place_third_combo()

        elif i_placement == 3:
            return self.place_fourth_combo()

        elif i_placement == 4:
            return self.place_fifth_combo()

        elif i_placement == 5:
            return self.place_sixth_combo()

        elif i_placement == 6:
            return self.place_seventh_combo()

        elif i_placement == 7:
            return self.place_eighth_combo()

        elif i_placement == 8:
            return self.place_ninth_combo()

        elif i_placement == 9:
            return self.place_tenth_combo()

        elif i_placement == 10:
            return self.place_eleventh_combo()

        elif i_placement == 11:
            return self.check_twelfth_combo()

    def place_first_combo(self) -> Union[list, None]:
        i_row = self.sorted_rows[0]

        if self.skipped[0] == 0:
            self.valids_for_row[i_row] = self.combos_for_row[i_row]

        # This should always work, unless there is no solution:
        proposed_combo = self.valids_for_row[i_row][self.skipped[0]]
        self.solution_rows[i_row] = proposed_combo

        return proposed_combo

    def place_second_combo(self) -> Union[list, None]:
        i_col = self.sorted_cols[0]

        i_row = self.sorted_rows[0]
        v0 = self.solution_rows[i_row][i_col]
        if self.skipped[1] == 0:
            self.valids_for_col[i_col] = [c for c in self.combos_for_col[i_col] if c[i_row] == v0]

        try:
            proposed_combo = self.valids_for_col[i_col][self.skipped[1]]
            self.solution_cols[i_col] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_third_combo(self) -> Union[list, None]:
        i_row = self.sorted_rows[1]

        i0 = self.sorted_cols[0]
        v0 = self.solution_cols[i0][i_row]
        if self.skipped[2] == 0:
            self.valids_for_row[i_row] = [c for c in self.combos_for_row[i_row] if c[i0] == v0]

        try:
            proposed_combo = self.valids_for_row[i_row][self.skipped[2]]
            self.solution_rows[i_row] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_fourth_combo(self) -> Union[list, None]:
        i_col = self.sorted_cols[1]

        i0 = self.sorted_rows[0]
        i1 = self.sorted_rows[1]
        v0 = self.solution_rows[i0][i_col]
        v1 = self.solution_rows[i1][i_col]
        if self.skipped[3] == 0:
            self.valids_for_col[i_col] = [c for c in self.combos_for_col[i_col] if c[i0] == v0 and c[i1] == v1]

        try:
            proposed_combo = self.valids_for_col[i_col][self.skipped[3]]
            self.solution_cols[i_col] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_fifth_combo(self) -> Union[list, None]:
        i_row = self.sorted_rows[2]

        i0 = self.sorted_cols[0]
        i1 = self.sorted_cols[1]
        v0 = self.solution_cols[i0][i_row]
        v1 = self.solution_cols[i1][i_row]
        if self.skipped[4] == 0:
            self.valids_for_row[i_row] = [c for c in self.combos_for_row[i_row] if c[i0] == v0 and c[i1] == v1]

        try:
            proposed_combo = self.valids_for_row[i_row][self.skipped[4]]
            self.solution_rows[i_row] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_sixth_combo(self) -> Union[list, None]:
        i_col = self.sorted_cols[2]

        i0 = self.sorted_rows[0]
        i1 = self.sorted_rows[1]
        i2 = self.sorted_rows[2]
        v0 = self.solution_rows[i0][i_col]
        v1 = self.solution_rows[i1][i_col]
        v2 = self.solution_rows[i2][i_col]
        if self.skipped[5] == 0:
            self.valids_for_col[i_col] = [c for c in self.combos_for_col[i_col] if c[i0] == v0 and c[i1] == v1 and c[i2] == v2]  # NOQA

        try:
            proposed_combo = self.valids_for_col[i_col][self.skipped[5]]
            self.solution_cols[i_col] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_seventh_combo(self) -> Union[list, None]:
        i_row = self.sorted_rows[3]

        i0 = self.sorted_cols[0]
        i1 = self.sorted_cols[1]
        i2 = self.sorted_cols[2]
        v0 = self.solution_cols[i0][i_row]
        v1 = self.solution_cols[i1][i_row]
        v2 = self.solution_cols[i2][i_row]

        if self.skipped[6] == 0:
            self.valids_for_row[i_row] = [c for c in self.combos_for_row[i_row] if c[i0] == v0 and c[i1] == v1 and c[i2] == v2]

        try:
            proposed_combo = self.valids_for_row[i_row][self.skipped[6]]
            self.solution_rows[i_row] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_eighth_combo(self) -> Union[list, None]:
        i_col = self.sorted_cols[3]

        i0 = self.sorted_rows[0]
        i1 = self.sorted_rows[1]
        i2 = self.sorted_rows[2]
        i3 = self.sorted_rows[3]
        v0 = self.solution_rows[i0][i_col]
        v1 = self.solution_rows[i1][i_col]
        v2 = self.solution_rows[i2][i_col]
        v3 = self.solution_rows[i3][i_col]

        if self.skipped[7] == 0:
            self.valids_for_col[i_col] = [c for c in self.combos_for_col[i_col] if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3]  # NOQA

        try:
            proposed_combo = self.valids_for_col[i_col][self.skipped[7]]
            self.solution_cols[i_col] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_ninth_combo(self) -> Union[list, None]:
        i_row = self.sorted_rows[4]

        i0 = self.sorted_cols[0]
        i1 = self.sorted_cols[1]
        i2 = self.sorted_cols[2]
        i3 = self.sorted_cols[3]
        v0 = self.solution_cols[i0][i_row]
        v1 = self.solution_cols[i1][i_row]
        v2 = self.solution_cols[i2][i_row]
        v3 = self.solution_cols[i3][i_row]

        if self.skipped[8] == 0:
            self.valids_for_row[i_row] = [c for c in self.combos_for_row[i_row] if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3]

        try:
            proposed_combo = self.valids_for_row[i_row][self.skipped[8]]
            self.solution_rows[i_row] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_tenth_combo(self) -> Union[list, None]:
        i_col = self.sorted_cols[4]

        i0 = self.sorted_rows[0]
        i1 = self.sorted_rows[1]
        i2 = self.sorted_rows[2]
        i3 = self.sorted_rows[3]
        i4 = self.sorted_rows[4]
        v0 = self.solution_rows[i0][i_col]
        v1 = self.solution_rows[i1][i_col]
        v2 = self.solution_rows[i2][i_col]
        v3 = self.solution_rows[i3][i_col]
        v4 = self.solution_rows[i4][i_col]

        if self.skipped[9] == 0:
            self.valids_for_col[i_col] = [c for c in self.combos_for_col[i_col] if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3 and c[i4] == v4]  # NOQA

        try:
            proposed_combo = self.valids_for_col[i_col][self.skipped[9]]
            self.solution_cols[i_col] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_eleventh_combo(self) -> Union[list, None]:
        i_row = self.sorted_rows[5]

        i0 = self.sorted_cols[0]
        i1 = self.sorted_cols[1]
        i2 = self.sorted_cols[2]
        i3 = self.sorted_cols[3]
        i4 = self.sorted_cols[4]
        v0 = self.solution_cols[i0][i_row]
        v1 = self.solution_cols[i1][i_row]
        v2 = self.solution_cols[i2][i_row]
        v3 = self.solution_cols[i3][i_row]
        v4 = self.solution_cols[i4][i_row]

        if self.skipped[10] == 0:
            self.valids_for_row[i_row] = [c for c in self.combos_for_row[i_row] if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3 and c[i4] == v4]  # NOQA

        try:
            proposed_combo = self.valids_for_row[i_row][self.skipped[10]]
            self.solution_rows[i_row] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def check_twelfth_combo(self) -> Union[list, None]:
        i_col = self.sorted_cols[5]
        i0 = self.sorted_rows[0]
        i1 = self.sorted_rows[1]
        i2 = self.sorted_rows[2]
        i3 = self.sorted_rows[3]
        i4 = self.sorted_rows[4]
        i5 = self.sorted_rows[5]

        combo_must_be = [None for _ in range(6)]
        combo_must_be[i0] = self.solution_rows[i0][i_col]
        combo_must_be[i1] = self.solution_rows[i1][i_col]
        combo_must_be[i2] = self.solution_rows[i2][i_col]
        combo_must_be[i3] = self.solution_rows[i3][i_col]
        combo_must_be[i4] = self.solution_rows[i4][i_col]
        combo_must_be[i5] = self.solution_rows[i5][i_col]
        combo_must_be = tuple(combo_must_be)

        if combo_must_be in self.combos_for_col[i_col]:
            return combo_must_be

        return None
