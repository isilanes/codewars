# https://www.codewars.com/kata/5679d5a3f2272011d700000d

from typing import Union
from itertools import permutations


N_ELEMENTS = 7


def seen_from_left(combo):
    seen = 0
    max_h = 0
    for h in combo:
        if h == N_ELEMENTS:
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

        self.all_combos = list(permutations(range(1, N_ELEMENTS+1)))

        self.skipped_for_position = [0 for _ in range(2 * N_ELEMENTS)]
        self.valids_for_position = [None for _ in range(2 * N_ELEMENTS)]
        self.combo_for_position = [None for _ in range(2 * N_ELEMENTS)]
        self.position_to_row_or_col = [None for _ in range(2 * N_ELEMENTS)]

        self._row_clues = None
        self._col_clues = None
        self._seen_from_sides = None
        self._combos_for_row = None
        self._combos_for_col = None

    @property
    def row_clues(self):
        if self._row_clues is None:
            self._row_clues = [(self.clues[4*N_ELEMENTS - 1 - i], self.clues[N_ELEMENTS + i]) for i in range(N_ELEMENTS)]

        return self._row_clues

    @property
    def col_clues(self):
        if self._col_clues is None:
            self._col_clues = [(self.clues[i], self.clues[3*N_ELEMENTS - 1 - i]) for i in range(N_ELEMENTS)]

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
            for i_row in range(N_ELEMENTS):
                valid_combos = [c for c in self.all_combos if self.fits_in_row(i_row, c)]
                self._combos_for_row.append(valid_combos)

        return self._combos_for_row

    @property
    def combos_for_col(self):
        if self._combos_for_col is None:
            self._combos_for_col = []
            for i_col in range(N_ELEMENTS):
                valid_combos = [c for c in self.all_combos if self.fits_in_col(i_col, c)]
                self._combos_for_col.append(valid_combos)

        return self._combos_for_col

    @property
    def solution(self) -> tuple:
        s = [None for _ in range(N_ELEMENTS)]
        for p in range(0, 2 * N_ELEMENTS, 2):
            i_row = self.position_to_row_or_col[p]
            if i_row is not None:
                s[i_row] = self.combo_for_position[p]

        return tuple(s)

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
        while i_placement < 4:
            combo = self.place_nth_combo(i_placement)
            if combo is None:
                self.skipped_for_position[i_placement] = 0
                self.valids_for_position[i_placement] = None
                self.position_to_row_or_col[i_placement] = None
                self.skipped_for_position[i_placement - 1] += 1
                i_placement -= 1
                continue

            i_placement += 1

        return self.solution

    def calc_valids_for_first_row(self) -> bool:
        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_row):
            n_valids = len(combos)
            if min_n_valids is None or n_valids < min_n_valids:
                min_index, min_valids, min_n_valids = i, combos, n_valids

        self.valids_for_position[0] = self.combos_for_row[min_index]
        self.position_to_row_or_col[0] = min_index

        return True

    def calc_valids_for_first_col(self) -> bool:
        i0 = self.position_to_row_or_col[0]

        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_col):
            v0 = self.combo_for_position[0][i]
            valids = [c for c in combos if c[i0] == v0]
            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids = i, valids, n_valids

        self.valids_for_position[1] = min_valids
        self.position_to_row_or_col[1] = min_index

        return True

    def calc_valids_for_second_row(self) -> bool:
        i0 = self.position_to_row_or_col[1]

        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_row):
            if i == self.position_to_row_or_col[0]:  # avoid re-placing previous row
                continue
            v0 = self.combo_for_position[1][i]
            valids = [c for c in combos if c[i0] == v0]
            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids = i, valids, n_valids

        self.valids_for_position[2] = min_valids
        self.position_to_row_or_col[2] = min_index

        return True

    def calc_valids_for_second_col(self) -> bool:
        i0, i1 = self.position_to_row_or_col[:3:2]  # 0, 2 (rows)

        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_col):
            if i == self.position_to_row_or_col[1]:
                continue
            v0, v1 = [c[i] for c in self.combo_for_position[:3:2]]  # 1, 3 (cols)
            valids = [c for c in combos if c[i0] == v0 and c[i1] == v1]
            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids = i, valids, n_valids

        self.valids_for_position[3] = min_valids
        self.position_to_row_or_col[3] = min_index

        return True

    def calc_valids_for_third_row(self) -> bool:
        i0, i1 = self.position_to_row_or_col[1:4:2]  # 1, 3 (cols)

        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_row):
            if i in self.position_to_row_or_col[:3:2]:  # 0 and 2  (rows)
                continue
            v0, v1 = [c[i] for c in self.combo_for_position[1:4:2]]  # 1, 3 (cols)
            valids = [c for c in combos if c[i0] == v0 and c[i1] == v1]
            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids = i, valids, n_valids

        self.valids_for_position[4] = min_valids
        self.position_to_row_or_col[4] = min_index

        return True

    def calc_valids_for_third_col(self) -> bool:
        i0, i1, i2 = self.position_to_row_or_col[:5:2]  # indices for rows 0, 2, 4

        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_col):
            if i in self.position_to_row_or_col[1:4:2]:  # indices for cols 1 and 3
                continue
            v0, v1, v2 = [c[i] for c in self.combo_for_position[:5:2]]
            valids = [c for c in combos if c[i0] == v0 and c[i1] == v1 and c[i2] == v2]
            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids = i, valids, n_valids

        self.valids_for_position[5] = min_valids
        self.position_to_row_or_col[5] = min_index

        return True

    def calc_valids_for_fourth_row(self) -> bool:
        i0, i1, i2 = self.position_to_row_or_col[1:6:2]  # 1, 3, 5 (cols)

        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_row):
            if i in self.position_to_row_or_col[:5:2]:  # 0, 2, 4 (rows)
                continue
            v0, v1, v2 = [c[i] for c in self.combo_for_position[1:6:2]]
            valids = [c for c in combos if c[i0] == v0 and c[i1] == v1 and c[i2] == v2]
            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids = i, valids, n_valids

        self.valids_for_position[6] = min_valids
        self.position_to_row_or_col[6] = min_index

        return True

    def calc_valids_for_fourth_col(self) -> bool:
        i0, i1, i2, i3 = self.position_to_row_or_col[:7:2]  # 0, 2, 4, 6 (rows)

        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_col):
            if i in self.position_to_row_or_col[1:6:2]:  # 1, 3, 5 (cols)
                continue
            v0, v1, v2, v3 = [c[i] for c in self.combo_for_position[:7:2]]
            valids = [c for c in combos if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3]
            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids = i, valids, n_valids

        self.valids_for_position[7] = min_valids
        self.position_to_row_or_col[7] = min_index

        return True

    def calc_valids_for_fifth_row(self) -> bool:
        i0, i1, i2, i3 = self.position_to_row_or_col[1:8:2]  # 1, 3, 5, 7 (cols)

        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_row):
            if i in self.position_to_row_or_col[:7:2]:  # 0, 2, 4, 6 (rows)
                continue
            v0, v1, v2, v3 = [c[i] for c in self.combo_for_position[1:8:2]]
            valids = [c for c in combos if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3]
            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids = i, valids, n_valids

        self.valids_for_position[8] = min_valids
        self.position_to_row_or_col[8] = min_index

        return True

    def calc_valids_for_fifth_col(self) -> bool:
        i0, i1, i2, i3, i4 = self.position_to_row_or_col[0:9:2]  # 0, 2, 4, 8, 10 (rows)

        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_col):
            if i in self.position_to_row_or_col[1:8:2]:  # 1, 3, 5, 5 (cols)
                continue
            v0, v1, v2, v3, v4 = [c[i] for c in self.combo_for_position[:9:2]]
            valids = [c for c in combos if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3 and c[i4] == v4]
            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids = i, valids, n_valids

        self.valids_for_position[9] = min_valids
        self.position_to_row_or_col[9] = min_index

        return True

    def calc_valids_for_sixth_row(self) -> bool:
        i0, i1, i2, i3, i4 = self.position_to_row_or_col[1:10:2]  # 1, 3, 5, 7, 9 (cols)

        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_row):
            if i in self.position_to_row_or_col[:9:2]:  # 0, 2, 4, 6, 8 (rows)
                continue
            v0, v1, v2, v3, v4 = [c[i] for c in self.combo_for_position[1:10:2]]
            valids = [c for c in combos if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3 and c[i4] == v4]
            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids = i, valids, n_valids

        self.valids_for_position[10] = min_valids
        self.position_to_row_or_col[10] = min_index

        return True

    def check_sixth_col(self) -> bool:
        already_placed_cols = self.position_to_row_or_col[1:10:2]
        missing_col = 15 - sum(already_placed_cols)  # 15 = 0 + 1 + 2 + 3 + 4 + 5

        combo_must_be = [None for _ in range(N_ELEMENTS)]
        for i, ix in enumerate(self.position_to_row_or_col[:11:2]):  # 0, 2, 4, 6, 8, 10 (all rows)
            combo_must_be[ix] = self.combo_for_position[2*i][missing_col]

        combo_must_be = tuple(combo_must_be)

        if combo_must_be in self.combos_for_col[missing_col]:
            return True

    def set_combo(self, i) -> Union[list, None]:
        try:
            proposed_combo = self.valids_for_position[i][self.skipped_for_position[i]]
            self.combo_for_position[i] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_nth_combo(self, n: int) -> Union[list, None]:
        if self.position_to_row_or_col[n] is None:
            calcs = (
                self.calc_valids_for_first_row,
                self.calc_valids_for_first_col,
                self.calc_valids_for_second_row,
                self.calc_valids_for_second_col,
                self.calc_valids_for_third_row,
                self.calc_valids_for_third_col,
                self.calc_valids_for_fourth_row,
                self.calc_valids_for_fourth_col,
                self.calc_valids_for_fifth_row,
                self.calc_valids_for_fifth_col,
                self.calc_valids_for_sixth_row,
                self.check_sixth_col,
            )
            success = calcs[n]()
            if not success:
                return None

            if n == 2 * N_ELEMENTS - 1:  # and success
                return []  # whatever that is not None (and is a list, to follow type hint)

        return self.set_combo(n)

