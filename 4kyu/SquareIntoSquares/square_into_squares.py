# https://www.codewars.com/kata/54eb33e5bc1a25440d000891/train/python

import math


def decompose(n):
    alive = []
    for i in range(1, n):
        e = {
            "members": [i],
            "remainder": n**2 - i**2,
        }
        alive.append(e)

    final_alive = []
    for i in range(6):
        next_alive = []
        for e in alive:
            rem = e["remainder"]
            members = e["members"]
            largest_so_far = members[-1]

            for new in range(largest_so_far+1, int(math.sqrt(rem))+1):
                if new in members:
                    continue

                new_rem = rem - new**2
                new_e = {
                    "members": members + [new],
                    "remainder": new_rem,
                }

                if new_rem == 0:
                    final_alive.append(new_e)
                    continue

                next_alive.append(new_e)

        if not next_alive:
            break

        alive = next_alive

    if not final_alive:
        return None

    return sorted([e["members"][::-1] for e in final_alive])[-1][::-1]


if __name__ == "__main__":
    print(decompose(11))
