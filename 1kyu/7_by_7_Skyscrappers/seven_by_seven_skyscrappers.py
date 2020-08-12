# https://www.codewars.com/kata/5917a2205ffc30ec3a0000a8

import sys
import argparse

from solution_02 import solve_puzzle


CLUES = [
    [7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4],
]


def parse_args(args=sys.argv[1:]):

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--case",
                        type=int,
                        default=0)

    parser.add_argument("--rotate",
                        action="store_true",
                        default=False)

    parser.add_argument("--no-rotate",
                        action="store_true",
                        default=False)

    return parser.parse_args(args)


def main():
    opts = parse_args()
    clues = CLUES[opts.case]

    solution = solve_puzzle(clues)
    for combo in solution:
        print(combo)


if __name__ == "__main__":
    main()
