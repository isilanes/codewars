CASES = {
    "medium": {
        "clues": [7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4],
        "expected": [
            [1, 5, 6, 7, 4, 3, 2],
            [2, 7, 4, 5, 3, 1, 6],
            [3, 4, 5, 6, 7, 2, 1],
            [4, 6, 3, 1, 2, 7, 5],
            [5, 3, 1, 2, 6, 4, 7],
            [6, 2, 7, 3, 1, 5, 4],
            [7, 1, 2, 4, 5, 6, 3]
        ]
    },
    "case2": {
        "clues": [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 5, 2, 2, 2, 2, 4, 1],
        "expected": [
            [7, 6, 2, 1, 5, 4, 3],
            [1, 3, 5, 4, 2, 7, 6],
            [6, 5, 4, 7, 3, 2, 1],
            [5, 1, 7, 6, 4, 3, 2],
            [4, 2, 1, 3, 7, 6, 5],
            [3, 7, 6, 2, 1, 5, 4],
            [2, 4, 3, 5, 6, 1, 7]
        ]
    },
    "case2extra": {
        "clues": [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0],
        "expected": [
            [7, 6, 2, 1, 5, 4, 3],
            [1, 3, 5, 4, 2, 7, 6],
            [6, 5, 4, 7, 3, 2, 1],
            [5, 1, 7, 6, 4, 3, 2],
            [4, 2, 1, 3, 7, 6, 5],
            [3, 7, 6, 2, 1, 5, 4],
            [2, 4, 3, 5, 6, 1, 7]
        ]
    },
    "hard": {
        "clues": [6, 4, 0, 2, 0, 0, 3, 0, 3, 3, 3, 0, 0, 4, 0, 5, 0, 5, 0, 2, 0, 0, 0, 0, 4, 0, 0, 3],
        "expected": [
            [2, 1, 6, 4, 3, 7, 5],
            [3, 2, 5, 7, 4, 6, 1],
            [4, 6, 7, 5, 1, 2, 3],
            [1, 3, 2, 6, 7, 5, 4],
            [5, 7, 1, 3, 2, 4, 6],
            [6, 4, 3, 2, 5, 1, 7],
            [7, 5, 4, 1, 6, 3, 2]
        ]
    },
    "hard2": {
        "clues": [0, 0, 0, 5, 0, 0, 3, 0, 6, 3, 4, 0, 0, 0, 3, 0, 0, 0, 2, 4, 0, 2, 6, 2, 2, 2, 0, 0],
        "expected": [
            [3, 5, 6, 1, 7, 2, 4],
            [7, 6, 5, 2, 4, 3, 1],
            [2, 7, 1, 3, 6, 4, 5],
            [4, 3, 7, 6, 1, 5, 2],
            [6, 4, 2, 5, 3, 1, 7],
            [1, 2, 3, 4, 5, 7, 6],
            [5, 1, 4, 7, 2, 6, 3]
        ]
    },
    "very_hard": {
        "clues": [0, 0, 5, 0, 0, 0, 6, 4, 0, 0, 2, 0, 2, 0, 0, 5, 2, 0, 0, 0, 5, 0, 3, 0, 5, 0, 0, 3],
        "expected": [
            [3, 4, 1, 7, 6, 5, 2],
            [7, 1, 2, 5, 4, 6, 3],
            [6, 3, 5, 2, 1, 7, 4],
            [1, 2, 3, 6, 7, 4, 5],
            [5, 7, 6, 4, 2, 3, 1],
            [4, 5, 7, 1, 3, 2, 6],
            [2, 6, 4, 3, 5, 1, 7]
        ]
    },
    "very_hard2": {
        "clues": [0, 0, 5, 3, 0, 2, 0, 0, 0, 0, 4, 5, 0, 0, 0, 0, 0, 3, 2, 5, 4, 2, 2, 0, 0, 0, 0, 5],
        "expected": [
            [2, 3, 1, 4, 6, 5, 7],
            [1, 7, 4, 6, 5, 2, 3],
            [3, 6, 5, 7, 2, 1, 4],
            [7, 5, 6, 3, 1, 4, 2],
            [6, 2, 7, 5, 4, 3, 1],
            [5, 4, 2, 1, 3, 7, 6],
            [4, 1, 3, 2, 7, 6, 5]
        ]
    },
    "medved": {
        "clues": [3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3],
        "expected": [
            [2, 1, 4, 7, 6, 5, 3],
            [6, 4, 7, 3, 5, 1, 2],
            [1, 2, 3, 6, 4, 7, 5],
            [5, 7, 6, 2, 3, 4, 1],
            [4, 3, 5, 1, 2, 6, 7],
            [7, 6, 2, 5, 1, 3, 4],
            [3, 5, 1, 4, 7, 2, 6]
        ]
    },
    "random1": {
        "clues": [0, 0, 0, 0, 5, 0, 4, 7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0],
        "expected": [
            [7, 6, 5, 4, 3, 2, 1],
            [1, 2, 3, 6, 4, 7, 5],
            [2, 7, 1, 3, 5, 4, 6],
            [4, 3, 2, 1, 6, 5, 7],
            [5, 1, 6, 2, 7, 3, 4],
            [6, 5, 4, 7, 2, 1, 3],
            [3, 4, 7, 5, 1, 6, 2]
        ]
    },
    "random2": {
        "clues": [0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4, 7, 0, 0, 0, 2, 2, 3],
        "expected": [
            [2, 6, 1, 5, 7, 4, 3],
            [3, 1, 2, 7, 4, 5, 6],
            [4, 3, 7, 2, 6, 1, 5],
            [7, 5, 6, 1, 2, 3, 4],
            [6, 4, 5, 3, 1, 7, 2],
            [5, 7, 4, 6, 3, 2, 1],
            [1, 2, 3, 4, 5, 6, 7]
        ]
    },
    "random3": {
        "clues": [3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4, 7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0],
        "expected": [
            [3, 6, 5, 4, 2, 1, 7],
            [4, 5, 1, 3, 7, 2, 6],
            [7, 4, 6, 2, 1, 3, 5],
            [5, 7, 2, 1, 3, 6, 4],
            [1, 2, 7, 6, 5, 4, 3],
            [6, 1, 3, 5, 4, 7, 2],
            [2, 3, 4, 7, 6, 5, 1]
        ]
    }
}
