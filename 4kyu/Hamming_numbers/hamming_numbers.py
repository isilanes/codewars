# https://www.codewars.com/kata/526d84b98f428f14a60008da

import math


TWO_TO_THREE = math.log(3)/math.log(2)
TWO_TO_FIVE = math.log(5)/math.log(2)
THREE_TO_FIVE = math.log(5)/math.log(3)


def hamming(n):
    i, j, k, index = 0, 0, 0, 1

    while index < n:
        print(index, i, j, k)
        index += 1

    return 1


print(hamming(5))