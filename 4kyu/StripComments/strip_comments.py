# https://www.codewars.com/kata/51c8e37cee245da6b40000bd/train/python

def solution(string, markers):
    output = []
    for line in string.split("\n"):
        for marker in markers:
            try:
                marker_pos = line.index(marker)
                line = line[:marker_pos]
            except ValueError:
                continue

        output.append(line.rstrip())

    return "\n".join(output)

if __name__ == "__main__":
    print(solution("apples, pears # and bananas\ngrapes\nbananas !apples", ["#", "!"]))
