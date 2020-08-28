# https://www.codewars.com/kata/5671d975d81d6c1c87000022

import sys
import argparse

from cases import CASES
from solution_08 import solve_puzzle


def parse_args(args=sys.argv[1:]):

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--case",
                        default="default")

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
