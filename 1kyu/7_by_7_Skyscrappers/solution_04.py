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

        self.skipped_for_position = [0 for _ in range(2 * N_ELEMENTS)]
        self.valids_for_position = [None for _ in range(2 * N_ELEMENTS)]
        self.combo_for_position = [None for _ in range(2 * N_ELEMENTS)]
        self.placement_to_row_or_col = [None for _ in range(2 * N_ELEMENTS)]
        self.is_row_or_col = [None for _ in range(2 * N_ELEMENTS)]

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
    def solution(self) -> list:
        s = [None for _ in range(N_ELEMENTS)]
        for p in range(0, 2 * N_ELEMENTS):
            if self.is_row_or_col[p] == "row":
                i_row = self.placement_to_row_or_col[p]
                if i_row is not None:
                    s[i_row] = list(self.combo_for_position[p])

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
        self.skipped_for_position[i_placement] = 0
        self.valids_for_position[i_placement] = None
        self.placement_to_row_or_col[i_placement] = None
        self.skipped_for_position[i_placement - 1] += 1

    def solve(self):
        i_placement = 0
        while i_placement < 2 * N_ELEMENTS:
            combo = self.place_nth_combo(i_placement)
            if combo is None:
                self.prepare_to_go_back(i_placement)
                i_placement -= 1
                continue

            i_placement += 1

        return self.solution

    def calc_valids_for_nth_placement(self, i_placement) -> bool:
        previous_rows = [self.placement_to_row_or_col[i] for i in range(i_placement) if self.is_row_or_col[i] == "row"]
        previous_cols = [self.placement_to_row_or_col[i] for i in range(i_placement) if self.is_row_or_col[i] == "col"]

        # Rows:
        min_index, min_valids, min_n_valids, min_which = -1, [], None, None
        for i, combos in enumerate(self.combos_for_row):
            if i in previous_rows:
                continue

            valids = []
            for combo in combos:
                can_be = True
                for prev_placement in range(i_placement):
                    # Row vs col:
                    if self.is_row_or_col[prev_placement] == "col":
                        i_row_cross = i
                        i_col_cross = self.placement_to_row_or_col[prev_placement]
                        if self.combo_for_position[prev_placement][i_row_cross] != combo[i_col_cross]:
                            can_be = False
                            break

                    # Row vs row:
                    else:
                        if not are_parallel_combos_congruent(combo, self.combo_for_position[prev_placement]):
                            can_be = False
                            break

                if can_be:
                    valids.append(combo)

            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids, min_which = i, valids, n_valids, "row"

        # Cols:
        for i, combos in enumerate(self.combos_for_col):
            if i in previous_cols:
                continue

            valids = []
            for combo in combos:
                can_be = True
                for prev_placement in range(i_placement):
                    # Col vs row:
                    if self.is_row_or_col[prev_placement] == "row":
                        i_col_cross = i
                        i_row_cross = self.placement_to_row_or_col[prev_placement]
                        if self.combo_for_position[prev_placement][i_col_cross] != combo[i_row_cross]:
                            can_be = False
                            break

                    # Col vs col:
                    else:
                        if not are_parallel_combos_congruent(combo, self.combo_for_position[prev_placement]):
                            can_be = False
                            break

                if can_be:
                    valids.append(combo)

            n_valids = len(valids)
            if min_n_valids is None or n_valids < min_n_valids:
                if n_valids == 0:
                    return False

                min_index, min_valids, min_n_valids, min_which = i, valids, n_valids, "col"

        self.valids_for_position[i_placement] = min_valids
        self.placement_to_row_or_col[i_placement] = min_index
        self.is_row_or_col[i_placement] = min_which

        return True

    def set_combo(self, i) -> Union[list, None]:
        try:
            proposed_combo = self.valids_for_position[i][self.skipped_for_position[i]]
            self.combo_for_position[i] = proposed_combo

            return proposed_combo
        except IndexError:
            return None

    def place_nth_combo(self, n: int) -> Union[list, None]:
        if self.placement_to_row_or_col[n] is None:
            success = self.calc_valids_for_nth_placement(n)
            if not success:
                return None

        return self.set_combo(n)

