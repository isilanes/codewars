# https://www.codewars.com/kata/551f23362ff852e2ab000037


def longest_slide_down(pyramid):

    n_rows = len(pyramid)
    n_cols_last_row = n_rows  # because pyramid

    maximum = pyramid[:]  # clone a triangle with equal shape

    for i in range(n_cols_last_row):
        maximum[-1][i] = pyramid[-1][i]
    
    for i in range(n_rows - 2, -1, -1):
        for j in range(i+1):  # len of i-th row is i+1
            # "a" will end up with biggest number among two below current:
            [a, b] = pyramid[i + 1][j:j + 2]
            if b > a:
                a = b

            maximum[i][j] = pyramid[i][j] + a

    return maximum[0][0]


def main():
    pyramid = [[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]]
    print(longest_slide_down(pyramid))


if __name__ == "__main__":
    main()
