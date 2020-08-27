# https://www.codewars.com/kata/5917a2205ffc30ec3a0000a8

import sys
import argparse

from cases import CASES
from solution_06 import solve_puzzle


CLUES = [
    [7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4],
    [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 5, 2, 2, 2, 2, 4, 1],
    [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0],
    [6, 4, 0, 2, 0, 0, 3, 0, 3, 3, 3, 0, 0, 4, 0, 5, 0, 5, 0, 2, 0, 0, 0, 0, 4, 0, 0, 3],  # slow
    [0, 0, 0, 5, 0, 0, 3, 0, 6, 3, 4, 0, 0, 0, 3, 0, 0, 0, 2, 4, 0, 2, 6, 2, 2, 2, 0, 0],
    [0, 0, 5, 0, 0, 0, 6, 4, 0, 0, 2, 0, 2, 0, 0, 5, 2, 0, 0, 0, 5, 0, 3, 0, 5, 0, 0, 3],
    [0, 0, 5, 3, 0, 2, 0, 0, 0, 0, 4, 5, 0, 0, 0, 0, 0, 3, 2, 5, 4, 2, 2, 0, 0, 0, 0, 5],  # slow
    [3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3],
]


def parse_args(args=sys.argv[1:]):

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--case",
                        default="medium")

    parser.add_argument("--rotate",
                        action="store_true",
                        default=False)

    parser.add_argument("--no-rotate",
                        action="store_true",
                        default=False)

    return parser.parse_args(args)


def main():
    opts = parse_args()
    clues = CASES[opts.case]["clues"]
    expected = CASES[opts.case]["expected"]

    solution = solve_puzzle(clues)
    for combo in solution:
        print(combo)

    print("Success:", solution == expected)


if __name__ == "__main__":
    main()
