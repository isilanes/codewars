# https://www.codewars.com/kata/5917a2205ffc30ec3a0000a8

import sys
import argparse

from cases import CASES
from solution_08 import solve_puzzle


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
