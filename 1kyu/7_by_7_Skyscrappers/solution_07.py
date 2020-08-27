from functools import lru_cache
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


@lru_cache(maxsize=512000)
def are_parallel_combos_congruent(combo_a, *others):
    for d in zip(combo_a, *others):
        if d[0] in d[1:]:
            return False

    return True


def rotated_solution(solution):
    r = []
    for i_col in range(N_ELEMENTS):
        row = [solution[N_ELEMENTS - 1 - j][i_col] for j in range(N_ELEMENTS)]
        r.append(row)

    return r


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
        self._sorted_row_indices = None
        self._sorted_col_indices = None

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
    def sorted_row_indices(self):
        if self._sorted_row_indices is None:
            self._sorted_row_indices = [i for _, i in sorted([(len(self.combos_for_row[i]), i)
                                                              for i in range(N_ELEMENTS)])]

        return self._sorted_row_indices

    @property
    def sorted_col_indices(self):
        if self._sorted_col_indices is None:
            self._sorted_col_indices = [i for _, i in sorted([(len(self.combos_for_col[i]), i)
                                                              for i in range(N_ELEMENTS)])]

        return self._sorted_col_indices

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

    def must_rotate(self):
        second_best_row = len(self.combos_for_row[self.sorted_row_indices[1]])
        second_best_col = len(self.combos_for_col[self.sorted_col_indices[1]])

        return second_best_row > second_best_col

    def pre_rotate(self):
        # Rotate input clues:
        self.clues = self.clues[N_ELEMENTS:] + self.clues[:N_ELEMENTS]

        # Clean:
        self.skipped_for_step = [0 for _ in range(2 * N_ELEMENTS)]
        self.combo_for_step = [None for _ in range(2 * N_ELEMENTS)]
        self.placement_to_index = [None for _ in range(2 * N_ELEMENTS)]

        self._row_clues = None
        self._col_clues = None
        self._seen_from_sides = None
        self._combos_for_row = None
        self._combos_for_col = None
        self._sorted_row_indices = None
        self._sorted_col_indices = None

    def solve(self):
        print([len(self.combos_for_row[i]) for i in range(7)])
        print([len(self.combos_for_col[i]) for i in range(7)])
        do_rotate = self.must_rotate()
        print(do_rotate)
        import time

        t0 = time.time()

        if do_rotate:
            self.pre_rotate()

        t1 = time.time()
        print(f"pre: {1000*(t1 - t0):.0f} ms")

        # row0-col0:
        i_row = self.sorted_row_indices[0]
        i_col = self.sorted_col_indices[0]
        combos = []
        for row_combo in self.combos_for_row[i_row]:
            d = row_combo[i_col]
            combos.extend([(row_combo, c) for c in self.combos_for_col[i_col] if c[i_row] == d])

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f" step0: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1:
        i_row = self.sorted_row_indices[1]
        i_col = self.sorted_col_indices[0]
        new_combos = []
        for row0, col0 in combos:
            d = col0[i_row]
            valids = [c for c in self.combos_for_row[i_row] if c[i_col] == d]
            valids = [r for r in valids if are_parallel_combos_congruent(row0, r)]
            new_combos.extend([(row0, col0, r) for r in valids])

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f" step1: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1:
        i_row0, i_row1 = self.sorted_row_indices[:2]
        i_col = self.sorted_col_indices[1]
        new_combos = []
        cols_for = {}
        for row0, col0, row1 in combos:
            d0, d1 = row0[i_col], row1[i_col]
            try:
                valids = cols_for[(d0, d1)]
            except KeyError:
                valids = [c for c in self._combos_for_col[i_col] if c[i_row0] == d0 and c[i_row1] == d1]
                cols_for[(d0, d1)] = valids
            valids = [c for c in valids if are_parallel_combos_congruent(col0, c)]
            valids = [(row0, col0, row1, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f" step2: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1-row2:
        i_row = self.sorted_row_indices[2]
        i_col0, i_col1 = self.sorted_col_indices[:2]
        new_combos = []
        rows_for = {}
        for row0, col0, row1, col1 in combos:
            d0, d1 = col0[i_row], col1[i_row]
            p = (d0, d1)
            try:
                valids = rows_for[p]
            except KeyError:
                valids = [c for c in self.combos_for_row[i_row] if (c[i_col0], c[i_col1]) == p]
                rows_for[p] = valids

            # Recall that are_parallel_combos_congruent() function uses caching:
            valids = [(row0, col0, row1, col1, c) for c in valids if are_parallel_combos_congruent(c, row0, row1)]
            new_combos.extend(valids)

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f" step3: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1-row2-col2:
        i_row0, i_row1, i_row2 = self.sorted_row_indices[:3]
        i_col = self.sorted_col_indices[2]
        new_combos = []
        cols_for = {}
        for row0, col0, row1, col1, row2 in combos:
            p = (row0[i_col], row1[i_col], row2[i_col])
            try:
                valids = cols_for[p]
            except KeyError:
                valids = [c for c in self.combos_for_col[i_col] if (c[i_row0], c[i_row1], c[i_row2]) == p]
                cols_for[p] = valids

            # Recall that are_parallel_combos_congruent() function uses caching:
            valids = [c for c in valids if are_parallel_combos_congruent(c, col0, col1)]
            valids = [(row0, col0, row1, col1, row2, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f" step4: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1-row2-col2-row3:
        i_row = self.sorted_row_indices[3]
        i_col0, i_col1, i_col2 = self.sorted_col_indices[:3]
        new_combos = []
        rows_for = {}
        for row0, col0, row1, col1, row2, col2 in combos:
            d0, d1, d2 = col0[i_row], col1[i_row], col2[i_row]
            try:
                valids = rows_for[(d0, d1, d2)]
            except KeyError:
                valids = [c for c in self.combos_for_row[i_row]
                          if c[i_col0] == d0 and c[i_col1] == d1 and c[i_col2] == d2]
                rows_for[(d0, d1, d2)] = valids

            # Recall that are_parallel_combos_congruent() function uses caching:
            valids = [c for c in valids if are_parallel_combos_congruent(c, row0, row1, row2)]
            valids = [(row0, col0, row1, col1, row2, col2, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f" step5: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1-row2-col2-row3-col3:
        i_row0, i_row1, i_row2, i_row3 = self.sorted_row_indices[:4]
        i_col = self.sorted_col_indices[3]
        new_combos = []
        cols_for = {}
        for row0, col0, row1, col1, row2, col2, row3 in combos:
            d0, d1, d2, d3 = row0[i_col], row1[i_col], row2[i_col], row3[i_col]
            try:
                valids = cols_for[(d0, d1, d2, d3)]
            except KeyError:
                valids = [c for c in self.combos_for_col[i_col]
                          if c[i_row0] == d0 and c[i_row1] == d1 and c[i_row2] == d2 and c[i_row3] == d3]
                cols_for[(d0, d1, d2, d3)] = valids

            # Recall that are_parallel_combos_congruent() function uses caching:
            valids = [c for c in valids if are_parallel_combos_congruent(c, col0, col1, col2)]
            valids = [(row0, col0, row1, col1, row2, col2, row3, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f" step6: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1-row2-col2-row3-col3-row4:
        i_row = self.sorted_row_indices[4]
        i_col0, i_col1, i_col2, i_col3 = self.sorted_col_indices[:4]
        new_combos = []
        combos_for = {}
        for row0, col0, row1, col1, row2, col2, row3, col3 in combos:
            d0, d1, d2, d3 = col0[i_row], col1[i_row], col2[i_row], col3[i_row]
            try:
                valids = combos_for[(d0, d1, d2, d3)]
            except KeyError:
                valids = [c for c in self.combos_for_row[i_row]
                          if c[i_col0] == d0 and c[i_col1] == d1 and c[i_col2] == d2 and c[i_col3] == d3]
                combos_for[(d0, d1, d2, d3)] = valids

            valids = [c for c in valids if are_parallel_combos_congruent(c, row0, row1, row2, row3)]
            valids = [(row0, col0, row1, col1, row2, col2, row3, col3, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f" step7: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1-row2-col2-row3-col3-row4-col4:
        i_row0, i_row1, i_row2, i_row3, i_row4 = self.sorted_row_indices[:5]
        i_col = self.sorted_col_indices[4]
        new_combos = []
        combos_for = {}
        for row0, col0, row1, col1, row2, col2, row3, col3, row4 in combos:
            d0, d1, d2, d3, d4 = row0[i_col], row1[i_col], row2[i_col], row3[i_col], row4[i_col]
            try:
                valids = combos_for[(d0, d1, d2, d3, d4)]
            except KeyError:
                valids = [c for c in self.combos_for_col[i_col]
                          if c[i_row0] == d0 and c[i_row1] == d1 and c[i_row2] == d2 and c[i_row3] == d3
                          and c[i_row4] == d4]
                combos_for[(d0, d1, d2, d3, d4)] = valids

            valids = [c for c in valids if are_parallel_combos_congruent(c, col0, col1, col2, col3)]
            valids = [(row0, col0, row1, col1, row2, col2, row3, col3, row4, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f" step8: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1-row2-col2-row3-col3-row4-col4-row5:
        i_row = self.sorted_row_indices[5]
        i_col0, i_col1, i_col2, i_col3, i_col4 = self.sorted_col_indices[:5]
        new_combos = []
        combos_for = {}
        for row0, col0, row1, col1, row2, col2, row3, col3, row4, col4 in combos:
            d0, d1, d2, d3, d4 = col0[i_row], col1[i_row], col2[i_row], col3[i_row], col4[i_row]
            try:
                valids = combos_for[(d0, d1, d2, d3, d4)]
            except KeyError:
                valids = [c for c in self.combos_for_row[i_row]
                          if c[i_col0] == d0 and c[i_col1] == d1 and c[i_col2] == d2 and c[i_col3] == d3
                          and c[i_col4] == d4]
                combos_for[(d0, d1, d2, d3, d4)] = valids

            valids = [c for c in valids if are_parallel_combos_congruent(c, row0, row1, row2, row3, row4)]
            valids = [(row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f" step9: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1-row2-col2-row3-col3-row4-col4-row5-col5:
        i_row0, i_row1, i_row2, i_row3, i_row4, i_row5 = self.sorted_row_indices[:6]
        i_col = self.sorted_col_indices[5]
        new_combos = []
        combos_for = {}
        for row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, row5 in combos:
            d0, d1, d2, d3, d4, d5 = row0[i_col], row1[i_col], row2[i_col], row3[i_col], row4[i_col], row5[i_col]
            try:
                valids = combos_for[(d0, d1, d2, d3, d4, d5)]
            except KeyError:
                valids = [c for c in self.combos_for_col[i_col]
                          if c[i_row0] == d0 and c[i_row1] == d1 and c[i_row2] == d2 and c[i_row3] == d3
                          and c[i_row4] == d4 and c[i_row5] == d5]
                combos_for[(d0, d1, d2, d3, d4, d5)] = valids

            valids = [c for c in valids if are_parallel_combos_congruent(c, col0, col1, col2, col3, col4)]
            valids = [(row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, row5, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f"step10: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1-row2-col2-row3-col3-row4-col4-row5-col5-row6:
        i_row = self.sorted_row_indices[6]
        i_col0, i_col1, i_col2, i_col3, i_col4, i_col5 = self.sorted_col_indices[:6]
        new_combos = []
        combos_for = {}
        for row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, row5, col5 in combos:
            d0, d1, d2, d3, d4, d5 = col0[i_row], col1[i_row], col2[i_row], col3[i_row], col4[i_row], col5[i_row]
            try:
                valids = combos_for[(d0, d1, d2, d3, d4, d5)]
            except KeyError:
                valids = [c for c in self.combos_for_row[i_row]
                          if c[i_col0] == d0 and c[i_col1] == d1 and c[i_col2] == d2 and c[i_col3] == d3
                          and c[i_col4] == d4 and c[i_col5] == d5]
                combos_for[(d0, d1, d2, d3, d4, d5)] = valids

            valids = [c for c in valids if are_parallel_combos_congruent(c, row0, row1, row2, row3, row4, row5)]
            valids = [(row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, row5, col5, c) for c in valids]
            new_combos.extend(valids)

        combos = new_combos

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f"step11: {dt:5.0f} ms, c={len(combos)}")

        # row0-col0-row1-col1-row2-col2-row3-col3-row4-col4-row5-col5-row6-col6:
        i_col = self.sorted_col_indices[6]
        new_combos = []
        for row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, row5, col5, row6 in combos:
            rows = [row0, row1, row2, row3, row4, row5, row6]
            combo = [None for _ in range(N_ELEMENTS)]
            for i, i_row in enumerate(self.sorted_row_indices):
                combo[i_row] = rows[i][i_col]
            combo = tuple(combo)
            if combo in self.combos_for_col[i_col]:
                valid = (row0, col0, row1, col1, row2, col2, row3, col3, row4, col4, row5, col5, row6, combo)
                new_combos.append(valid)

        if len(new_combos) != 1:
            raise ValueError  # this should never happen

        combos = new_combos
        solution = [None for _ in range(N_ELEMENTS)]
        for i, combo in enumerate(combos[0]):
            if not i % 2:  # even, row
                i_row = self.sorted_row_indices[i // 2]
                solution[i_row] = list(combo)

        dt = 1000*(time.time() - t1); t1 = time.time()
        print(f"step12: {dt:5.0f} ms, c={len(combos)}")

        if do_rotate:
            return rotated_solution(solution)
        else:
            return solution
