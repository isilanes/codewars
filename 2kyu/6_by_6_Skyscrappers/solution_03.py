# https://www.codewars.com/kata/5679d5a3f2272011d700000d

from typing import Union
from itertools import permutations


N_ELEMENTS = 6


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
        #self.valids_for_row = [None for _ in range(N_ELEMENTS)]
        #self.valids_for_col = [None for _ in range(N_ELEMENTS)]

        self.skipped_for_position = [0 for _ in range(2 * N_ELEMENTS)]
        #self.solution_rows = [None for _ in range(N_ELEMENTS)]
        #self.solution_cols = [None for _ in range(N_ELEMENTS)]
        self.valids_for_position = [None for _ in range(2 * N_ELEMENTS)]
        self.combo_for_position = [None for _ in range(2 * N_ELEMENTS)]
        self.position_to_row_or_col = [None for _ in range(2 * N_ELEMENTS)]

        self._row_clues = None
        self._col_clues = None
        self._seen_from_sides = None
        self._combos_for_row = None
        self._combos_for_col = None
        #self._sorted_rows = None
        #self._sorted_cols = None

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
        s = [None for _ in range(6)]
        for p in range(0, 2 * N_ELEMENTS, 2):
            i_row = self.position_to_row_or_col[p]
            if i_row is not None:
                s[i_row] = self.combo_for_position[p]

        return s

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
        while i_placement < 8:
            combo = self.place_combo(i_placement)
            if combo is None:
                self.skipped_for_position[i_placement] = 0
                self.valids_for_position[i_placement] = None
                self.position_to_row_or_col[i_placement] = None
                self.skipped_for_position[i_placement - 1] += 1
                i_placement -= 1
                continue

            i_placement += 1

        return self.solution

    def calc_valids_for_first_row(self):
        min_index, min_valids, min_n_valids = -1, [], None
        for i, combos in enumerate(self.combos_for_row):
            n_valids = len(combos)
            if min_n_valids is None or n_valids < min_n_valids:
                min_index, min_valids, min_n_valids = i, combos, n_valids

        self.valids_for_position[0] = self.combos_for_row[min_index]
        self.position_to_row_or_col[0] = min_index

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

    def place_combo(self, i_placement: int) -> Union[list, None]:
        if i_placement == 0:
            return self.place_first_row()

        elif i_placement == 1:
            return self.place_first_col()

        elif i_placement == 2:
            return self.place_second_row()

        elif i_placement == 3:
            return self.place_second_col()

        elif i_placement == 4:
            return self.place_third_row()

        elif i_placement == 5:
            return self.place_third_col()

        elif i_placement == 6:
            return self.place_fourth_row()

        elif i_placement == 7:
            return self.place_fourth_col()

        elif i_placement == 8:
            return self.place_ninth_combo()

        elif i_placement == 9:
            return self.place_tenth_combo()

        elif i_placement == 10:
            return self.place_eleventh_combo()

        elif i_placement == 11:
            return self.check_twelfth_combo()

    def place_first_row(self) -> Union[list, None]:
        buena = (2, 1, 4, 3, 5, 6)
        self.combo_for_position[0] = buena
        self.position_to_row_or_col[0] = 0
        print(f"row {self.position_to_row_or_col[0]} = {buena}")
        return buena

        if self.valids_for_position[0] is None:
            self.calc_valids_for_first_row()

        # This should always work, unless there is no solution:
        proposed_combo = self.valids_for_position[0][self.skipped_for_position[0]]
        self.combo_for_position[0] = proposed_combo
        print(f"row {self.position_to_row_or_col[0]} = {proposed_combo}")

        return proposed_combo

    def place_first_col(self) -> Union[list, None]:
        buena = (1, 6, 3, 5, 4, 2)
        self.combo_for_position[1] = buena
        self.position_to_row_or_col[1] = 1
        print(f"col {self.position_to_row_or_col[1]} = {buena}")
        return buena

        if self.valids_for_position[1] is None:
            success = self.calc_valids_for_first_col()
            if not success:
                return None

        try:
            proposed_combo = self.valids_for_position[1][self.skipped_for_position[1]]
            self.combo_for_position[1] = proposed_combo
            print(f"col {self.position_to_row_or_col[1]} = {proposed_combo}")

            return proposed_combo
        except IndexError:
            return None

    def place_second_row(self) -> Union[list, None]:
        buena = (6, 5, 2, 1, 3, 4)
        self.combo_for_position[2] = buena
        self.position_to_row_or_col[2] = 3
        print(f"row {self.position_to_row_or_col[2]} = {buena}")
        return buena

        if self.valids_for_position[2] is None:
            success = self.calc_valids_for_second_row()
            if not success:
                return None

        print(self.position_to_row_or_col[2])
        print(buena in self.valids_for_position[2])
        exit()

        try:
            proposed_combo = self.valids_for_position[2][self.skipped_for_position[2]]
            self.combo_for_position[2] = proposed_combo
            print(f"row {self.position_to_row_or_col[2]} = {proposed_combo}")

            return proposed_combo
        except IndexError:
            return None

    def place_second_col(self) -> Union[list, None]:
        buena = (4, 3, 6, 2, 1, 5)
        self.combo_for_position[3] = buena
        self.position_to_row_or_col[3] = 2
        print(f"col {self.position_to_row_or_col[3]} = {buena}")
        return buena

        if self.valids_for_position[3] is None:
            success = self.calc_valids_for_second_col()
            if not success:
                return None

        print(self.position_to_row_or_col[3])
        print(buena in self.valids_for_position[3])
        exit()

        try:
            proposed_combo = self.valids_for_position[3][self.skipped_for_position[3]]
            self.combo_for_position[3] = proposed_combo
            print(f"col {self.position_to_row_or_col[3]} = {proposed_combo}")

            return proposed_combo
        except IndexError:
            return None

    def place_third_row(self) -> Union[list, None]:
        buena = (5, 4, 1, 6, 2, 3)
        self.combo_for_position[4] = buena
        self.position_to_row_or_col[4] = 4
        print(f"row {self.position_to_row_or_col[4]} = {buena}")
        return buena

        if self.valids_for_position[4] is None:
            success = self.calc_valids_for_third_row()
            if not success:
                return None

        print(self.position_to_row_or_col[4])
        print(buena in self.valids_for_position[4])
        exit()

        try:
            proposed_combo = self.valids_for_position[4][self.skipped_for_position[4]]
            self.combo_for_position[4] = proposed_combo
            print(f"row {self.position_to_row_or_col[4]} = {proposed_combo}")

            return proposed_combo
        except IndexError:
            return None

    def place_third_col(self) -> Union[list, None]:
        buena = (5, 4, 1, 3, 2, 6)
        self.combo_for_position[5] = buena
        self.position_to_row_or_col[5] = 4
        print(f"col {self.position_to_row_or_col[5]} = {buena}")
        return buena

        if self.valids_for_position[5] is None:
            success = self.calc_valids_for_third_col()
            if not success:
                return None

        print(self.position_to_row_or_col[5])
        print(buena in self.valids_for_position[5])
        exit()

        try:
            proposed_combo = self.valids_for_position[5][self.skipped_for_position[5]]
            self.combo_for_position[5] = proposed_combo
            print(f"col {self.position_to_row_or_col[5]} = {proposed_combo}")

            return proposed_combo
        except IndexError:
            return None

    def place_fourth_row(self) -> Union[list, None]:
        buena = (1, 6, 3, 2, 4, 5)
        self.combo_for_position[6] = buena
        self.position_to_row_or_col[6] = 1
        print(f"row {self.position_to_row_or_col[6]} = {buena}")
        return buena

        if self.valids_for_position[6] is None:
            success = self.calc_valids_for_fourth_row()
            if not success:
                return None

        print(self.position_to_row_or_col[6])
        print(buena in self.valids_for_position[6])
        exit()

        try:
            proposed_combo = self.valids_for_position[6][self.skipped_for_position[6]]
            self.combo_for_position[6] = proposed_combo
            print(f"row {self.position_to_row_or_col[6]} = {proposed_combo}")

            return proposed_combo
        except IndexError:
            return None

    def place_fourth_col(self) -> Union[list, None]:
        buena = (2, 1, 4, 6, 5, 3)
        self.combo_for_position[7] = buena
        self.position_to_row_or_col[7] = 0
        print(f"col {self.position_to_row_or_col[7]} = {buena}")
        return buena

        if self.valids_for_position[7] is None:
            success = self.calc_valids_for_fourth_col()
            if not success:
                return None

        print(self.position_to_row_or_col[7])
        print(buena in self.valids_for_position[7])
        exit()

        try:
            proposed_combo = self.valids_for_position[7][self.skipped_for_position[7]]
            self.combo_for_position[7] = proposed_combo
            print(f"col {self.position_to_row_or_col[7]} = {proposed_combo}")

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

        if self.skipped_for_position[8] == 0:
            self.valids_for_row[i_row] = [c for c in self.combos_for_row[i_row] if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3]

        try:
            proposed_combo = self.valids_for_row[i_row][self.skipped_for_position[8]]
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

        if self.skipped_for_position[9] == 0:
            self.valids_for_col[i_col] = [c for c in self.combos_for_col[i_col] if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3 and c[i4] == v4]  # NOQA

        try:
            proposed_combo = self.valids_for_col[i_col][self.skipped_for_position[9]]
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

        if self.skipped_for_position[10] == 0:
            self.valids_for_row[i_row] = [c for c in self.combos_for_row[i_row] if c[i0] == v0 and c[i1] == v1 and c[i2] == v2 and c[i3] == v3 and c[i4] == v4]  # NOQA

        try:
            proposed_combo = self.valids_for_row[i_row][self.skipped_for_position[10]]
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
