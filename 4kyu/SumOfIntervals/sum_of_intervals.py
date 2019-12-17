# https://www.codewars.com/kata/sum-of-intervals/train/python

def merge_two_intervals(interval_a, interval_b):
    """
    Given interval_a as [int, int] and interval_b as [int, int], return either a merged interval [int, int] if they 
    overlap, or None if they don't. Beware input intervals can be either list() or tuple() elements.

    Examples:
    [1, 3], [3, 6] -> [1, 6]
    [1, 2], [7, 8] -> None
    [1, 6], [3, 5] -> [1, 6]

    :param interval_a -> [int, int]: numeric interval A
    :param interval_b -> [int, int]: numeric interval B
    :return: either merged interval [int, int] or None
    """
    new_a, new_b = sorted([list(interval_a), list(interval_b)])  # now A[0] <= B[0]
    a0, a1 = new_a
    b0, b1 = new_b
    if a1 < b0:
        return None

    return [a0, max(a1, b1)]


def get_non_overlapping_intervals(intervals):
    """
    Given a list of intervals, return a new list of equivalent non-overlapping intervals, spanning the same, 
    merged, ranges.
    """
    clean = []  # definitely non-overlapping intervals
    dirty = intervals  # maybe overlapping intervals
    while dirty:
        tmp_dirty = []
        selected_interval = dirty[0]
        selected_is_clean = True
        for i, current_interval in enumerate(dirty[1:]):
            merged = merge_two_intervals(selected_interval, current_interval)

            if merged is None:  # then they don't overlap
                tmp_dirty.append(current_interval)

            else:
                tmp_dirty.append(merged)
                tmp_dirty.extend(dirty[i+2:])
                selected_is_clean = False
                break

        if selected_is_clean:
            clean.append(selected_interval)

        dirty = tmp_dirty

    return clean


def sum_of_intervals(intervals):
    clean = get_non_overlapping_intervals(intervals)

    return sum([j-i for i, j in clean])


if __name__ == "__main__":
    c = sum_of_intervals([(1, 4), (7, 10), (3, 5)])

    print(c)
