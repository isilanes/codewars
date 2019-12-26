# https://www.codewars.com/kata/54eb33e5bc1a25440d000891/train/python

import math


class Snake:

    def __init__(self, n):
        self.members = [n-1]
        self.remaining = n**2 - (n-1)**2

    def next_value(self):
        return min(self.last-1, int(math.sqrt(self.remaining)))

    def grow(self, value):
        self.members.append(value)
        self.remaining -= value**2

    def chomp(self):
        self.remaining += self.last**2
        self.members = self.members[:-1]

    def decrement_last(self):
        last = self.last
        self.members[-1] -= 1
        self.remaining += last**2 - (last-1)**2

    @property
    def last(self):
        return self.members[-1]

    @property
    def size(self):
        return len(self.members)


def decompose(n):
    snake = Snake(n)

    while True:
        if snake.remaining == 0:
            return snake.members[::-1]

        next_value = snake.next_value()

        if next_value == 1 and snake.remaining != 1:
            snake.decrement_last()
            while snake.last == 1:
                snake.chomp()
                if snake.size == 0:
                    return None

                snake.decrement_last()

            continue

        snake.grow(next_value)

    return None


if __name__ == "__main__":
    assert decompose(5) == [3, 4]
    assert decompose(8) is None
    assert decompose(11) == [1, 2, 4, 10]
    assert decompose(12) == [1, 2, 3, 7, 9]
    assert decompose(50) == [1, 3, 5, 8, 49]
    assert decompose(7100) == [2, 3, 5, 119, 7099]
    assert decompose(7654321) == [6, 10, 69, 3912, 7654320]
