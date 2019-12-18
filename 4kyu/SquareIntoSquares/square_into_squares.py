# https://www.codewars.com/kata/54eb33e5bc1a25440d000891/train/python

import math

def decompose(n):
    result = [n-1]
    remainder = 2*n - 1  # n**2 - (n-1)**2
    while remainder > 0:
        # 'next' is largest N such that N**2 <= remainder:
        next = int(math.sqrt(remainder))
        result.append(next)
        remainder -= next**2

    return result[::-1]


if __name__ == "__main__":
    print(decompose(11))
    print(decompose(8))
