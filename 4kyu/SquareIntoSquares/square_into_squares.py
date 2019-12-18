# https://www.codewars.com/kata/54eb33e5bc1a25440d000891/train/python

import math

def decompose(n):
    result = [n-1]
    remainder = 2*n - 1  # n**2 - (n-1)**2
    while remainder > 0:
        if remainder == 2:  # because then last two insertions are 1, 1
            return None
        
        # 'next' is largest N such that N**2 <= remainder:
        next = int(math.sqrt(remainder))
        if remainder == 2*next:
            next -= 1

        remainder -= next**2
        result.append(next)

    return result[::-1]


if __name__ == "__main__":
    print(decompose(11))
    print(decompose(8))
