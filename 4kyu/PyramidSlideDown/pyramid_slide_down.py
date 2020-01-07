# https://www.codewars.com/kata/551f23362ff852e2ab000037


def longest_slide_down(pyramid):

    # This list will contain the maximum possible sum of values below each position in current row:
    accumulated_row = pyramid[-1]

    for i in range(len(pyramid) - 2, -1, -1):  # go from 2nd-to-last row upwards until first
        new_accumulated_row = []
        for j in range(i+1):  # len of i-th row is i+1
            # For each number in each row, we add to it the largest of the two below. Note that each number in row
            # below is already the largest sum from the bottom to that position:
            a, b = accumulated_row[j:j + 2]

            new_accumulated_row.append(pyramid[i][j] + max(a, b))

        accumulated_row = new_accumulated_row

    return accumulated_row[0]


def main():
    pyramid = [[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]]
    print(longest_slide_down(pyramid))


if __name__ == "__main__":
    main()
