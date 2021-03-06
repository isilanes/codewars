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

    def prepare_to_go_back(self, i_placement):
        self.skipped_for_step[i_placement] = 0
        self.placement_to_index[i_placement] = None
        self.skipped_for_step[i_placement - 1] += 1
        self.combo_for_step[i_placement] = None
        self.combos_for_rows_at_step[i_placement] = [None for _ in range(N_ELEMENTS)]
        self.combos_for_cols_at_step[i_placement] = [None for _ in range(N_ELEMENTS)]

    def solve(self):
        print([len(self.combos_for_row[i]) for i in range(7)])
        print([len(self.combos_for_col[i]) for i in range(7)])

        i_placement = 0
        while i_placement < 5:
            if i_placement < 0:
                print("fallo")
                break

            combo = self.place_nth_combo(i_placement)

            if combo is None:
                self.prepare_to_go_back(i_placement)
                i_placement -= 1
                continue

            i_placement += 1

        print("\n---")
        return self.solution

    def choose_combo(self, i_placement) -> bool:
        idx = self.placement_to_index[i_placement]
        skipped = self.skipped_for_step[i_placement]

        if self.is_row_or_col[i_placement] == "row":
            valids = self.combos_for_rows_at_step[i_placement]
        else:
            valids = self.combos_for_cols_at_step[i_placement]

        try:
            self.combo_for_step[i_placement] = valids[idx][skipped]
            return True
        except IndexError:
            return False

    def prune_next_valids(self, i_placement):
        previous_row_indices, previous_col_indices = [], []
        for prev_index in range(i_placement):
            if self.is_row_or_col[prev_index] == "row":
                previous_row_indices.append(self.placement_to_index[prev_index])
            else:
                previous_col_indices.append(self.placement_to_index[prev_index])

        i_current = self.placement_to_index[i_placement]
        combo = self.combo_for_step[i_placement]
        if self.is_row_or_col[i_placement] == "row":
            for i_col, v in enumerate(combo):
                if i_col in previous_col_indices:
                    #self.combos_for_cols_at_step[i_placement+1][i_col] = []
                    continue

                new_valids = [c for c in self.combos_for_cols_at_step[i_placement][i_col] if c[i_current] == v]
                if not new_valids:
                    return False

                self.combos_for_cols_at_step[i_placement+1][i_col] = new_valids

            for i_row in range(N_ELEMENTS):
                if i_row == i_current or i_row in previous_row_indices:
                    #self.combos_for_rows_at_step[i_placement+1][i_row] = []
                    continue

                new_valids = [c for c in self.combos_for_rows_at_step[i_placement][i_row] if are_parallel_combos_congruent(combo, c)]
                if not new_valids:
                    return False

                self.combos_for_rows_at_step[i_placement+1][i_row] = new_valids

        else:  # col
            for i_col in range(N_ELEMENTS):
                if i_col == i_current or i_col in previous_col_indices:
                    #self.combos_for_cols_at_step[i_placement+1][i_col] = []
                    continue

                new_valids = [c for c in self.combos_for_cols_at_step[i_placement][i_col] if are_parallel_combos_congruent(combo, c)]
                if not new_valids:
                    return False

                self.combos_for_cols_at_step[i_placement+1][i_col] = new_valids

            for i_row, v in enumerate(combo):
                if i_row in previous_row_indices:
                    #self.combos_for_rows_at_step[i_placement+1][i_row] = []
                    continue

                new_valids = [c for c in self.combos_for_rows_at_step[i_placement][i_row] if c[i_current] == v]
                if not new_valids:
                    return False

                self.combos_for_rows_at_step[i_placement+1][i_row] = new_valids

        return True

    def calc_min_location(self, i_placement: int) -> None:
        previous_row_indices, previous_col_indices = [], []
        for prev_index in range(i_placement):
            if self.is_row_or_col[prev_index] == "row":
                previous_row_indices.append(self.placement_to_index[prev_index])
            else:
                previous_col_indices.append(self.placement_to_index[prev_index])

        min_index, min_n_valids, min_which = None, None, None
        for i, combos in enumerate(self.combos_for_rows_at_step[i_placement]):
            if i in previous_row_indices:
                continue

            if combos is None:
                print(i_placement, self.combos_for_rows_at_step[i_placement])

            if min_index is None or len(combos) < min_n_valids:
                min_index, min_n_valids, min_which = i, len(combos), "row"

        for i, combos in enumerate(self.combos_for_cols_at_step[i_placement]):
            if i in previous_col_indices:
                continue

            if min_index is None or len(combos) < min_n_valids:
                min_index, min_n_valids, min_which = i, len(combos), "col"

        self.is_row_or_col[i_placement] = min_which
        self.placement_to_index[i_placement] = min_index

        print("DEBUG285", min_which, min_index)

    def place_nth_combo(self, i_placement: int) -> Union[list, None]:
        if self.placement_to_index[i_placement] is None:
            self.calc_min_location(i_placement)

        success = self.choose_combo(i_placement)
        if not success:
            print("esto no debe pasar nunca")
            return None

        print("DEBUG339", i_placement, self.is_row_or_col[i_placement],
              self.placement_to_index[i_placement], self.combo_for_step[i_placement])

        if i_placement < (2 * N_ELEMENTS - 1):
            success = self.prune_next_valids(i_placement)
            if not success:
                print("pruned to death")
                return None

        return self.combo_for_step[i_placement]

