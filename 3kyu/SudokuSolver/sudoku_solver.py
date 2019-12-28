# https://www.codewars.com/kata/5296bc77afba8baa690002d7


class Board:

    # For each cell i in 0..80, list of cells j affected by i-th cell.
    AFFECTS = {
        0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72],
        1: None,
        2: [0, 1, 3, 4, 5, 6, 7, 8, 11, 20, 29, 38, 47, 56, 65, 74, 9, 10, 18, 19],
        3: [0, 1, 2, 4, 5, 6, 7, 8, 12, 21, 30, 39, 48, 57, 66, 75, 13, 14, 22, 23],
        4: None,
        5: [0, 1, 2, 3, 4, 6, 7, 8, 14, 23, 32, 41, 50, 59, 68, 77, 12, 13, 21, 22],
        6: [0, 1, 2, 3, 4, 5, 7, 8, 15, 24, 33, 42, 51, 60, 69, 78, 16, 17, 25, 26],
        7: [0, 1, 2, 3, 4, 5, 6, 8, 16, 25, 34, 43, 52, 61, 70, 79, 15, 17, 24, 26],
        8: [0, 1, 2, 3, 4, 5, 6, 7, 17, 26, 35, 44, 53, 62, 71, 80, 15, 16, 24, 25],
        9: None,
        10: [9, 11, 12, 13, 14, 15, 16, 17, 1, 19, 28, 37, 46, 55, 64, 73, 0, 2, 18, 20],
        11: [0, 10, 12, 13, 14, 15, 16, 17, 2, 20, 29, 38, 47, 56, 65, 74, 0, 1, 18, 19],
        12: None,
        13: None,
        14: None,
        15: [9, 10, 11, 12, 13, 14, 16, 17, 6, 24, 33, 42, 51, 60, 69, 78, 7, 8, 25, 26],
        16: [9, 10, 11, 12, 13, 14, 15, 17, 7, 25, 34, 43, 52, 61, 70, 79, 6, 8, 24, 26],
        17: [9, 10, 11, 12, 13, 14, 15, 16, 8, 26, 35, 44, 53, 62, 71, 80, 6, 7, 24, 25],
        18: [19, 20, 21, 22, 23, 24, 25, 26, 0, 9, 27, 36, 45, 54, 63, 72, 1, 2, 10, 11],
        19: None,
        20: None,
        21: [18, 19, 20, 22, 23, 24, 25, 26, 3, 12, 30, 39, 48, 57, 66, 75, 4, 5, 13, 14],
        22: [18, 19, 20, 21, 23, 24, 25, 26, 4, 13, 31, 40, 49, 58, 67, 76, 3, 5, 12, 14],
        23: [18, 19, 20, 21, 22, 24, 25, 26, 5, 14, 32, 41, 50, 59, 68, 77, 3, 4, 12, 13],
        24: [18, 19, 20, 21, 22, 23, 25, 26, 6, 15, 33, 42, 51, 60, 69, 78, 7, 8, 16, 17],
        25: None,
        26: [18, 19, 20, 21, 22, 23, 24, 25, 8, 17, 35, 44, 53, 62, 71, 80, 6, 7, 15, 16],
        27: None,
        28: [27, 29, 30, 31, 32, 33, 34, 35, 1, 10, 19, 37, 46, 55, 64, 73, 36, 38, 45, 47],
        29: [27, 28, 30, 31, 32, 33, 34, 35, 2, 11, 20, 38, 47, 56, 65, 74, 36, 37, 45, 46],
        30: [27, 28, 29, 31, 32, 33, 34, 35, 3, 12, 21, 39, 48, 57, 66, 75, 40, 41, 49, 50],
        31: None,
        32: [27, 28, 29, 30, 31, 33, 34, 35, 5, 14, 23, 41, 50, 59, 68, 77, 39, 40, 48, 49],
        33: [27, 28, 29, 30, 31, 32, 34, 35, 6, 15, 24, 42, 51, 60, 69, 78, 43, 44, 52, 53],
        34: [27, 28, 29, 30, 31, 32, 33, 35, 7, 16, 25, 43, 52, 61, 70, 79, 42, 43, 51, 52],
        35: None,
        36: None,
        37: [36, 38, 39, 40, 41, 42, 43, 44, 1, 10, 19, 28, 46, 55, 64, 73, 27, 29, 45, 47],
        38: [36, 37, 39, 40, 41, 42, 43, 44, 2, 11, 20, 29, 47, 56, 65, 74, 27, 28, 45, 46],
        39: None,
        40: [36, 37, 38, 39, 41, 42, 43, 44, 4, 13, 22, 31, 49, 58, 67, 76, 30, 32, 48, 50],
        41: None,
        42: [36, 37, 38, 39, 40, 41, 43, 44, 6, 15, 24, 33, 51, 60, 69, 78, 34, 35, 52, 53],
        43: [36, 37, 38, 39, 40, 41, 42, 44, 7, 16, 25, 34, 52, 61, 70, 79, 33, 35, 51, 53],
        44: None,
        45: None,
        46: [45, 47, 48, 49, 50, 51, 52, 53, 1, 10, 19, 28, 37, 55, 64, 73, 27, 29, 45, 47],
        47: [45, 46, 48, 49, 50, 51, 52, 53, 2, 11, 20, 29, 38, 56, 65, 74, 27, 28, 45, 46],
        48: [45, 46, 47, 49, 50, 51, 52, 53, 3, 12, 21, 30, 39, 57, 66, 75, 31, 32, 40, 41],
        49: None,
        50: [45, 46, 47, 48, 49, 51, 52, 53, 5, 14, 23, 32, 41, 49, 68, 77, 30, 31, 39, 40],
        51: [45, 46, 47, 48, 49, 50, 52, 53, 6, 15, 24, 33, 42, 60, 69, 78, 34, 35, 43, 44],
        52: [45, 46, 47, 48, 49, 50, 51, 53, 7, 16, 25, 34, 43, 61, 70, 79, 33, 35, 42, 44],
        53: None,
        54: [55, 56, 57, 58, 59, 60, 61, 62, 0, 9, 18, 27, 36, 45, 63, 72, 64, 65, 73, 74],
        55: None,
        56: [54, 55, 57, 58, 59, 60, 61, 62, 2, 11, 20, 29, 38, 47, 65, 74, 63, 64, 72, 72],
        57: [54, 55, 56, 58, 59, 60, 61, 62, 3, 12, 21, 30, 39, 48, 66, 75, 67, 68, 76, 77],
        58: [54, 55, 56, 57, 59, 60, 61, 62, 4, 13, 22, 31, 40, 49, 67, 76, 66, 68, 75, 77],
        59: [54, 55, 56, 57, 58, 60, 61, 62, 5, 14, 23, 32, 41, 50, 68, 77, 66, 67, 75, 76],
        60: None,
        61: None,
        62: [54, 55, 56, 57, 58, 59, 60, 61, 8, 17, 26, 35, 44, 53, 71, 80, 69, 70, 78, 79],
        63: [64, 65, 66, 67, 68, 69, 70, 71, 0, 9, 18, 27, 36, 45, 54, 72, 55, 56, 73, 74],
        64: [63, 65, 66, 67, 68, 69, 70, 71, 1, 10, 19, 28, 37, 46, 55, 73, 54, 56, 72, 74],
        65: [63, 64, 66, 67, 68, 69, 70, 71, 2, 11, 20, 29, 38, 47, 56, 74, 54, 55, 72, 73],
        66: None,
        67: None,
        68: None,
        69: [63, 64, 65, 66, 67, 68, 70, 71, 6, 15, 24, 33, 42, 51, 60, 78, 61, 62, 79, 80],
        70: [63, 64, 65, 66, 67, 68, 69, 71, 7, 16, 25, 34, 43, 52, 61, 79, 60, 62, 78, 80],
        71: None,
        72: [73, 74, 75, 76, 77, 78, 79, 80, 0, 9, 18, 27, 36, 45, 54, 63, 55, 56, 64, 65],
        73: [72, 74, 75, 76, 77, 78, 79, 80, 1, 10, 19, 28, 37, 46, 55, 64, 54, 56, 63, 65],
        74: [72, 73, 75, 76, 77, 78, 79, 80, 2, 11, 20, 29, 38, 47, 56, 65, 54, 55, 63, 64],
        75: [72, 73, 74, 76, 77, 78, 79, 80, 3, 12, 21, 30, 39, 48, 57, 66, 58, 59, 67, 68],
        76: None,
        77: [72, 73, 74, 75, 76, 78, 79, 80, 5, 14, 23, 32, 41, 50, 59, 68, 57, 58, 66, 67],
        78: [72, 73, 74, 75, 76, 77, 79, 80, 6, 15, 24, 33, 42, 51, 60, 69, 61, 62, 70, 71],
        79: None,
        80: None,
    }
    MAX_CYCLES = 10**6  # just in case something goes wrong

    def __init__(self, initial):
        self.initial = self._to_1d(initial)
        self.vacant_indices = [i for i, v in enumerate(self.initial) if v == 0]
        self.vacant_allowed = self._get_vacant_allowed()
        self.reduced_vacant_affected_by = self._get_reduced_vacant_affected_by()

    def _get_vacant_allowed(self):
        """
        For every vacant cell, build list of values allowed on that cell.
        Return list of lists, where i-th value is list of allowed values in i-th empty cell.
        """
        allowed = []
        for i in self.vacant_indices:
            forbidden = [self.initial[k] for k in self.AFFECTS[i] if self.initial[k] != 0]
            a = [j for j in range(1, 10) if j not in forbidden]
            allowed.append(a)

        return allowed

    def _get_reduced_vacant_affected_by(self):
        """
        For every vacant cell, give list of indices of cells this cell is affected by (or it affects, which is
        the same) and are also in vacant cell list. Give only indices smaller than oneself (say each cell is affected
        by previous cells). For each i-th vacant cell give list of affecting/affected cell indices
        with respect to reduced (vacant-cell) index list, not 0-80 list of all cells.

        :return: list of int lists.
        """
        affected_by = []
        for i in self.vacant_indices:
            a = [self.vacant_indices.index(j) for j in self.AFFECTS[i] if j < i and j in self.vacant_indices]
            affected_by.append(a)

        return affected_by

    def solve(self):
        """Return solved sudoku."""

        # i-th element in index_allowed is j if we are proposing as solution for cell with i-th index in
        # self.vacant_indices the j-th value in its vacant_allowed values.
        index_allowed = [0 for _ in self.vacant_indices]

        # Index in self.vacant_indices of cell currently being considered:
        curr_reduced_vacant_i = 0

        for cycle in range(self.MAX_CYCLES):
            # For current vacant cell, list of values that are forbidden, because they appear in some other previous
            # cell that affects current cell:
            forbidden = []
            for i_prev in self.reduced_vacant_affected_by[curr_reduced_vacant_i]:
                v_prev = self.vacant_allowed[i_prev][index_allowed[i_prev]]
                forbidden.append(v_prev)

            chosen_j = None
            for j_curr in range(index_allowed[curr_reduced_vacant_i], len(self.vacant_allowed[curr_reduced_vacant_i])):
                v_curr = self.vacant_allowed[curr_reduced_vacant_i][j_curr]
                if v_curr not in forbidden:
                    chosen_j = j_curr
                    break

            if chosen_j is None:  # then no available value was valid. Go back.
                if curr_reduced_vacant_i == 0:  # unsolvable sudoku
                    return None

                index_allowed[curr_reduced_vacant_i] = 0
                index_allowed[curr_reduced_vacant_i-1] += 1
                curr_reduced_vacant_i -= 1
            else:
                index_allowed[curr_reduced_vacant_i] = chosen_j
                curr_reduced_vacant_i += 1
                if curr_reduced_vacant_i >= len(self.vacant_indices):
                    values = [self.vacant_allowed[i][j] for i, j in enumerate(index_allowed)]
                    result = [x for x in self.initial]
                    for i, v in zip(self.vacant_indices, values):
                        result[i] = v

                    return self._to_2d(result)

    @staticmethod
    def _to_1d(two_d_array):
        res = []
        for line in two_d_array:
            res.extend(line)

        return res

    @staticmethod
    def _to_2d(one_d_array):
        """Inverse of _to_1d()."""

        return [one_d_array[i*9:i*9+9] for i in range(9)]


def sudoku(puzzle):
    board = Board(puzzle)
    return board.solve()


def main():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    answer = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    assert sudoku(puzzle) == answer


if __name__ == "__main__":
    main()
