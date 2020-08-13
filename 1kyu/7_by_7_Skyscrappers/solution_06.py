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


def are_parallel_combos_congruent(combo_a, combo_b):
    for ca, cb in zip(combo_a, combo_b):
        if ca == cb:
            return False

    return True


def are_compatible(c1, c2):
    what_1, idx_1, combo_1 = c1
    what_2, idx_2, combo_2 = c2

    if what_1 == what_2:
        return are_parallel_combos_congruent(combo_1, combo_2)

    else:
        return combo_1[idx_2] == combo_2[idx_1]

    print(what_1, what_2)

    raise Exception


class Puzzle:

    def __init__(self, clues):
        self.clues = clues
        self.all_combos = list(permutations(range(1, N_ELEMENTS+1)))

        self.skipped_for_step = [0 for _ in range(2 * N_ELEMENTS)]
        self.combo_for_step = [None for _ in range(2 * N_ELEMENTS)]
        self.placement_to_index = [None for _ in range(2 * N_ELEMENTS)]
        self.is_row_or_col = [None for _ in range(2 * N_ELEMENTS)]

        self._row_clues = None
        self._col_clues = None
        self._seen_from_sides = None
        self._combos_for_row = None
        self._combos_for_col = None

        self.combos_for_rows_at_step = [[None for _ in range(N_ELEMENTS)] for _ in range(2 * N_ELEMENTS)]
        self.combos_for_rows_at_step[0] = self.combos_for_row

        self.combos_for_cols_at_step = [[None for _ in range(N_ELEMENTS)] for _ in range(2 * N_ELEMENTS)]
        self.combos_for_cols_at_step[0] = self.combos_for_col

        self.sorted_data = []

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
    def solution(self) -> list:
        s = [None for _ in range(N_ELEMENTS)]
        for p in range(0, 2 * N_ELEMENTS):
            if self.is_row_or_col[p] == "row":
                i_row = self.placement_to_index[p]
                if i_row is not None:
                    s[i_row] = list(self.combo_for_step[p])

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
        print([len(self.combos_for_row[i]) for i in range(7)])
        print([len(self.combos_for_col[i]) for i in range(7)])

        dsu = []
        for i in range(N_ELEMENTS):
            dsu.append([len(self._combos_for_row[i]), "row", i])
            dsu.append([len(self._combos_for_col[i]), "col", i])

        self.sorted_data = list(sorted(dsu))

        # Step 0:
        n, what, idx = self.sorted_data[0]
        if what == "row":
            combos_of_one = [("row", idx, c) for c in self.combos_for_row[idx]]
        else:
            combos_of_one = [("col", idx, c) for c in self.combos_for_col[idx]]

        cum = n
        print(f"DEBUG161 {what} {idx} -> {len(combos_of_one)}/{cum}")

        # Step 1:
        n, what, idx = self.sorted_data[1]
        cum *= n

        if what == "row":
            combo_list = self.combos_for_row[idx]
        else:
            combo_list = self.combos_for_col[idx]

        combos_of_two = []
        for combo in combo_list:
            c2 = (what, idx, combo)
            new_combos = [(c1, c2) for c1 in combos_of_one if are_compatible(c1, c2)]
            combos_of_two.extend(new_combos)

        print(f"DEBUG193 {what} {idx} -> {len(combos_of_two)}/{cum}")

        # Step 3:
        n, what, idx = self.sorted_data[2]
        cum *= n

        if what == "row":
            combo_list = self.combos_for_row[idx]
        else:
            combo_list = self.combos_for_col[idx]

        combos_of_three = []
        for combo in combo_list:
            c3 = (what, idx, combo)
            new_combos = [(c1, c2, c3) for c1, c2 in combos_of_two if are_compatible(c1, c3) and are_compatible(c2, c3)]
            combos_of_three.extend(new_combos)

        print(f"DEBUG210 {what} {idx} -> {len(combos_of_three)}/{cum}")

        # Step 4:
        n, what, idx = self.sorted_data[3]
        cum *= n

        if what == "row":
            combo_list = self.combos_for_row[idx]
        else:
            combo_list = self.combos_for_col[idx]

        combos_of_four = []
        for combo in combo_list:
            c4 = (what, idx, combo)
            new_combos = [(c1, c2, c3, c4) for c1, c2, c3 in combos_of_three if are_compatible(c1, c4) and are_compatible(c2, c4) and are_compatible(c3, c4)]
            combos_of_four.extend(new_combos)

        print(f"DEBUG232 {what} {idx} -> {len(combos_of_four)}/{cum}")

        # Step 5:
        n, what, idx = self.sorted_data[4]
        cum *= n

        if what == "row":
            combo_list = self.combos_for_row[idx]
        else:
            combo_list = self.combos_for_col[idx]

        combos_of_five = []
        for combo in combo_list:
            c5 = (what, idx, combo)
            new_combos = [(c1, c2, c3, c4, c5) for c1, c2, c3, c4 in combos_of_four if are_compatible(c1, c5) and are_compatible(c2, c5) and are_compatible(c3, c5) and are_compatible(c4, c5)]
            combos_of_five.extend(new_combos)

        print(f"DEBUG249 {what} {idx} -> {len(combos_of_five)}/{cum}")

        # Step 6:
        n, what, idx = self.sorted_data[5]
        cum *= n

        if what == "row":
            combo_list = self.combos_for_row[idx]
        else:
            combo_list = self.combos_for_col[idx]

        combos_of_six = []
        for combo in combo_list:
            c6 = (what, idx, combo)
            new_combos = [(c1, c2, c3, c4, c5, c6) for c1, c2, c3, c4, c5 in combos_of_five if are_compatible(c1, c6) and are_compatible(c2, c6) and are_compatible(c3, c6) and are_compatible(c4, c6) and are_compatible(c5, c6)]
            combos_of_six.extend(new_combos)

        print(f"DEBUG266 {what} {idx} -> {len(combos_of_six)}/{cum}")

        # Step 7:
        n, what, idx = self.sorted_data[6]
        cum *= n

        if what == "row":
            combo_list = self.combos_for_row[idx]
        else:
            combo_list = self.combos_for_col[idx]

        combos_of_seven = []
        for combo in combo_list:
            c7 = (what, idx, combo)
            new_combos = [(c1, c2, c3, c4, c5, c6, c7) for c1, c2, c3, c4, c5, c6 in combos_of_six if
                          are_compatible(c1, c7) and are_compatible(c2, c7) and are_compatible(c3, c7)
                          and are_compatible(c4, c7) and are_compatible(c5, c7) and are_compatible(c6, c7)]
            combos_of_seven.extend(new_combos)

        print(f"DEBUG285 {what} {idx} -> {len(combos_of_seven)}/{cum}")

        # Step 8:
        n, what, idx = self.sorted_data[7]
        cum *= n

        if what == "row":
            combo_list = self.combos_for_row[idx]
        else:
            combo_list = self.combos_for_col[idx]

        combos_of_eight = []
        for combo in combo_list:
            c8 = (what, idx, combo)
            new_combos = [(c1, c2, c3, c4, c5, c6, c7, c8) for c1, c2, c3, c4, c5, c6, c7 in combos_of_seven if
                          are_compatible(c1, c8) and are_compatible(c2, c8) and are_compatible(c3, c8)
                          and are_compatible(c4, c8) and are_compatible(c5, c8) and are_compatible(c6, c8)
                          and are_compatible(c7, c8)]
            combos_of_eight.extend(new_combos)

        print(f"DEBUG305 {what} {idx} -> {len(combos_of_eight)}/{cum}")

        print("\n---")
        return self.solution
