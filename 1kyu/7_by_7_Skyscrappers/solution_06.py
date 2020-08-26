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


def are_cross_compatible(c1, c2):
    combo_1, idx_1 = c1
    combo_2, idx_2 = c2

    return combo_1[idx_2] == combo_2[idx_1]


class Puzzle:

    def __init__(self, clues):
        self.clues = clues
        self.all_combos = list(permutations(range(1, N_ELEMENTS+1)))

        self.skipped_for_step = [0 for _ in range(2 * N_ELEMENTS)]
        self.combo_for_step = [None for _ in range(2 * N_ELEMENTS)]
        self.placement_to_index = [None for _ in range(2 * N_ELEMENTS)]

        self._row_clues = None
        self._col_clues = None
        self._seen_from_sides = None
        self._combos_for_row = None
        self._combos_for_col = None

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
        s = []
        for p in range(0, 2 * N_ELEMENTS, 2):
            s.append(self.combo_for_step[p])

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
        import time

        t0 = time.time()
        print([len(self.combos_for_row[i]) for i in range(7)])
        print([len(self.combos_for_col[i]) for i in range(7)])

        sorted_row_indices = [i for _, i in sorted([(len(self.combos_for_row[i]), i) for i in range(N_ELEMENTS)])]
        sorted_col_indices = [i for _, i in sorted([(len(self.combos_for_col[i]), i) for i in range(N_ELEMENTS)])]

        print()
        print("rows:", sorted_row_indices)
        print("cols:", sorted_col_indices)

        combos_with_digit_in_position_in_row = {}
        for i_row in range(N_ELEMENTS):
            combos_with_digit_in_position_in_row[i_row] = {}
            for row_combo in self.combos_for_row[i_row]:
                for i, d in enumerate(row_combo):
                    combos_with_digit_in_position_in_row[i_row][i] = combos_with_digit_in_position_in_row[i_row].get(i, {})
                    combos_with_digit_in_position_in_row[i_row][i][d] = combos_with_digit_in_position_in_row[i_row][i].get(d, [])
                    combos_with_digit_in_position_in_row[i_row][i][d].append(row_combo)

        combos_with_digit_in_position_in_col = {}
        for i_col in range(N_ELEMENTS):
            combos_with_digit_in_position_in_col[i_col] = {}
            for col_combo in self.combos_for_col[i_col]:
                for i, d in enumerate(col_combo):
                    combos_with_digit_in_position_in_col[i_col][i] = combos_with_digit_in_position_in_col[i_col].get(i, {})
                    combos_with_digit_in_position_in_col[i_col][i][d] = combos_with_digit_in_position_in_col[i_col][i].get(d, [])
                    combos_with_digit_in_position_in_col[i_col][i][d].append(col_combo)

        t1 = time.time()
        print(f"dt={1000*(t1-t0):5.1f} ms")
        print()

        # row0-col0:
        i_row = sorted_row_indices[0]
        i_col = sorted_col_indices[0]
        combos = []
        for row_combo in self.combos_for_row[i_row]:
            d = row_combo[i_col]
            combos.extend([(row_combo, c) for c in combos_with_digit_in_position_in_col[i_col][i_row].get(d, [])])

        dt = 1000*(time.time() - t1)
        print("step0", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1:
        i_row = sorted_row_indices[1]
        i_col = sorted_col_indices[0]
        new_combos = []
        for row0, col0 in combos:
            d = col0[i_row]
            new_combos.extend([(row0, col0, r) for r in combos_with_digit_in_position_in_row[i_row][i_col].get(d, [])])

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step1", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1-col1:
        i_row0, i_row1 = sorted_row_indices[:2]
        i_col = sorted_col_indices[1]
        new_combos = []
        cols_for = {}
        for row0, col0, row1 in combos:
            d0, d1 = row0[i_col], row1[i_col]
            try:
                valids = cols_for[(d0, d1)]
            except KeyError:
                valids = [c for c in combos_with_digit_in_position_in_col[i_col][i_row0].get(d0, []) if c[i_row1] == d1]
                cols_for[(d0, d1)] = valids
            valid_combos = [(row0, col0, row1, c) for c in valids]
            new_combos.extend(valid_combos)

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step2", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1-col1-row2:
        i_row = sorted_row_indices[2]
        i_col0, i_col1 = sorted_col_indices[:2]
        new_combos = []
        rows_for = {}
        for row0, col0, row1, col1 in combos:
            d0, d1 = col0[i_row], col1[i_row]
            try:
                valids = rows_for[(d0, d1)]
            except KeyError:
                valids = [c for c in combos_with_digit_in_position_in_row[i_row][i_col0].get(d0, []) if c[i_col1] == d1]
                rows_for[(d0, d1)] = valids
            valid_combos = [(row0, col0, row1, col1, c) for c in valids]
            new_combos.extend(valid_combos)

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step3", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1-col1-row2-col2:
        i_row0, i_row1, i_row2 = sorted_row_indices[:3]
        i_col = sorted_col_indices[2]
        new_combos = []
        cols_for = {}
        for row0, col0, row1, col1, row2 in combos:
            d0, d1, d2 = row0[i_col], row1[i_col], row2[i_col]
            try:
                valids = cols_for[(d0, d1, d2)]
            except KeyError:
                valids = [c for c in combos_with_digit_in_position_in_col[i_col][i_row0].get(d0, [])
                          if c[i_row1] == d1 and c[i_row2] == d2]
                cols_for[(d0, d1, d2)] = valids

            valid_combos = [(row0, col0, row1, col1, row2, c) for c in valids]
            new_combos.extend(valid_combos)

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step4", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1-col1-row2-col2-row3:
        i_row = sorted_row_indices[3]
        i_col0, i_col1, i_col2 = sorted_col_indices[:3]
        new_combos = []
        rows_for = {}
        for row0, col0, row1, col1, row2, col2 in combos:
            d0, d1, d2 = col0[i_row], col1[i_row], col2[i_row]
            try:
                valids = rows_for[(d0, d1, d2)]
            except KeyError:
                valids = [c for c in combos_with_digit_in_position_in_row[i_row][i_col0].get(d0, [])
                          if c[i_col1] == d1 and c[i_col2] == d2]
                rows_for[(d0, d1, d2)] = valids

            valid_combos = [(row0, col0, row1, col1, row2, col2, c) for c in valids]
            new_combos.extend(valid_combos)

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step5", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1-col1-row2-col2-row3-col3:
        i_row0, i_row1, i_row2, i_row3 = sorted_row_indices[:4]
        i_col = sorted_col_indices[3]
        new_combos = []
        cols_for = {}
        for row0, col0, row1, col1, row2, col2, row3 in combos:
            d0, d1, d2, d3 = row0[i_col], row1[i_col], row2[i_col], row3[i_col]
            try:
                valids = cols_for[(d0, d1, d2, d3)]
            except KeyError:
                valids = [c for c in combos_with_digit_in_position_in_col[i_col][i_row0].get(d0, [])
                          if c[i_row1] == d1 and c[i_row2] == d2 and c[i_row3] == d3]
                cols_for[(d0, d1, d2, d3)] = valids
            valid_combos = [(row0, col0, row1, col1, row2, col2, row3, c) for c in valids]
            new_combos.extend(valid_combos)

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step6", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1-col1-row2-col2-row3-col3-row4:
        i_row = sorted_row_indices[4]
        i_col0, i_col1, i_col2, i_col3 = sorted_col_indices[:4]
        new_combos = []
        combos_for = {}
        for row0, col0, row1, col1, row2, col2, row3, col3 in combos:
            d0, d1, d2, d3 = col0[i_row], col1[i_row], col2[i_row], col3[i_row]
            try:
                valids = combos_for[(d0, d1, d2, d3)]
            except KeyError:
                valids = [c for c in combos_with_digit_in_position_in_row[i_row][i_col0].get(d0, [])
                          if c[i_col1] == d1 and c[i_col2] == d2 and c[i_col3] == d3]
                combos_for[(d0, d1, d2, d3)] = valids

            valid_combos = [(row0, col0, row1, col1, row2, col2, row3, col3, c) for c in valids]
            new_combos.extend(valid_combos)

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step7", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1-col1-row2-col2-row3-col3-row4-col4:
        i_row0, i_row1, i_row2, i_row3, i_row4 = sorted_row_indices[:5]
        i_col = sorted_col_indices[4]
        new_combos = []
        combos_for = {}
        for row0, col0, row1, col1, row2, col2, row3, col3, row4 in combos:
            d0, d1, d2, d3, d4 = row0[i_col], row1[i_col], row2[i_col], row3[i_col], row4[i_col]
            try:
                valids = combos_for[(d0, d1, d2, d3, d4)]
            except KeyError:
                valids = [c for c in combos_with_digit_in_position_in_col[i_col][i_row0].get(d0, [])
                          if c[i_row1] == d1 and c[i_row2] == d2 and c[i_row3] == d3 and c[i_row4] == d4]
                combos_for[(d0, d1, d2, d3, d4)] = valids

            valid_combos = [(row0, col0, row1, col1, row2, col2, row3, col3, row4, c) for c in valids]
            new_combos.extend(valid_combos)

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step8", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1-col1-row2-col2-row3-col3-row4-col4-row5:
        i_row = sorted_row_indices[5]
        i_col0, i_col1, i_col2, i_col3, i_col4 = sorted_col_indices[:5]
        new_combos = []
        combos_for = {}
        for row0, col0, row1, col1, row2, col2, row3, col3, row4, col4 in combos:
            d0, d1, d2, d3, d4 = col0[i_row], col1[i_row], col2[i_row], col3[i_row], col4[i_row]
            try:
                valids = combos_for[(d0, d1, d2, d3, d4)]
            except KeyError:
                valids = [c for c in combos_with_digit_in_position_in_row[i_row][i_col0].get(d0, [])
                          if c[i_col1] == d1 and c[i_col2] == d2 and c[i_col3] == d3 and c[i_col4] == d4]
                combos_for[(d0, d1, d2, d3, d4)] = valids
            valid_combos = [(row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, c) for c in valids]
            new_combos.extend(valid_combos)

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step9", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1-col1-row2-col2-row3-col3-row4-col4-row5-col5:
        i_row0, i_row1, i_row2, i_row3, i_row4, i_row5 = sorted_row_indices[:6]
        i_col = sorted_col_indices[5]
        new_combos = []
        combos_for = {}
        for row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, row5 in combos:
            d0, d1, d2, d3, d4, d5 = row0[i_col], row1[i_col], row2[i_col], row3[i_col], row4[i_col], row5[i_col]
            try:
                valids = combos_for[(d0, d1, d2, d3, d4, d5)]
            except KeyError:
                valids = [c for c in combos_with_digit_in_position_in_col[i_col][i_row0].get(d0, [])
                          if c[i_row1] == d1 and c[i_row2] == d2 and c[i_row3] == d3 and c[i_row4] == d4 and c[i_row5] == d5]
                combos_for[(d0, d1, d2, d3, d4, d5)] = valids

            valids = [(row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, row5, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step10", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        # row0-col0-row1-col1-row2-col2-row3-col3-row4-col4-row5-col5-row6:
        i_row = sorted_row_indices[6]
        i_col0, i_col1, i_col2, i_col3, i_col4, i_col5 = sorted_row_indices[:6]
        new_combos = []
        combos_for = {}
        for row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, row5, col5 in combos:
            d0, d1, d2, d3, d4, d5 = col0[i_row], col1[i_row], col2[i_row], col3[i_row], col4[i_row], col5[i_row]
            try:
                valids = combos_for[(d0, d1, d2, d3, d4, d5)]
            except KeyError:
                valids = [c for c in combos_with_digit_in_position_in_row[i_row][i_col0].get(d0, [])
                          if c[i_col1] == d1 and c[i_col2] == d2 and c[i_col3] == d3 and c[i_col4] == d4 and c[i_col5] == d5]
                combos_for[(d0, d1, d2, d3, d4, d5)] = valids

            valids = [(row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, row5, col5, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos
        dt = 1000*(time.time() - t1)
        print("step11", f"dt={dt:6.0f} ms", f"c={len(combos)}")
        t1 = time.time()

        print()
        solution = [None for _ in range(N_ELEMENTS)]
        for i, combo in enumerate(combos[0]):
            if not i % 2:  # even, row
                i_row = sorted_row_indices[i // 2]
                solution[i_row] = combo

        for row in solution:
            print(row)

        print("\n---")
        return self.solution
