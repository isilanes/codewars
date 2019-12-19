# https://www.codewars.com/kata/54eb33e5bc1a25440d000891/train/python

import math


def decompose(n):
    snake = [n-1]
    rem = n**2 - (n-1)**2

    while True:
        print("DEBUG11", snake, rem)
        next = min(snake[-1]-1, int(math.sqrt(rem)))
        rem -= next**2

        if rem == 0:
            snake.append(next)
            return snake[::-1]

        if next > 1:
            snake.append(next)
            continue

        if snake[-1] == 1:
            snake = snake[:-1]

        snake[-1] -= 1

    return None



if __name__ == "__main__":
    #assert decompose(5) == [3, 4]
    #assert decompose(8) is None
    #assert decompose(11) == [1, 2, 4, 10]
    assert decompose(12) == [1, 2, 3, 7, 9]
    assert decompose(50) == [1, 2, 5, 8, 49]
    assert decompose(7100) == [2, 3, 5, 119, 7099]
    assert decompose(7654321) == [6, 10, 69, 39,12, 7654320]
