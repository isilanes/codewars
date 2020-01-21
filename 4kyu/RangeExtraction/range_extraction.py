# https://www.codewars.com/kata/51ba717bb08c1cd60f00002f/train/python


def flush_streak(streak):
    if len(streak) >= 3:
        return f"{streak[0]}-{streak[-1]}"
    else:
        return ",".join([str(c) for c in streak])


def solution(args):
    if not args:
        return ""

    output_string = ""
    current_streak = []
    for arg in args:
        if not current_streak or arg == current_streak[-1]+1:
            current_streak.append(arg)

        else:
            output_string = ",".join([output_string, flush_streak(current_streak)])
            current_streak = [arg]

    # Leftovers:
    output_string = ",".join([output_string, flush_streak(current_streak)])

    return output_string[1:]


def main():
    inputs = [
        [-6, -3, -2, -1, 0, 1, 3, 4, 5, 7, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20],
        [-3, -2, -1, 2, 10, 15, 16, 18, 19, 20],
    ]
    outputs = [
        '-6,-3-1,3-5,7-11,14,15,17-20',
        '-3--1,2,10,15,16,18-20',
    ]
    for args, expected in zip(inputs, outputs):
        assert solution(args) == expected


if __name__ == "__main__":
    main()
