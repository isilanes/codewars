# https://www.codewars.com/kata/52742f58faf5485cae000b9a/train/python


PERIODS = [
    (365*24*3600, "year"),
    (24*3600, "day"),
    (3600, "hour"),
    (60, "minute"),
    (1, "second"),
]


def format_duration(seconds):
    if not seconds:
        return "now"

    fragments = []
    for dt, unit in PERIODS:
        if seconds >= dt:
            n = seconds // dt
            if n > 1:
                unit = f"{unit}s"
            fragments.append(f"{n} {unit}")
            seconds = seconds % dt

    if len(fragments) == 1:
        return fragments[0]

    comma_separated = ", ".join(fragments[:-1])

    return f"{comma_separated} and {fragments[-1]}"


def main():
    in_and_out = [
        (0, "now"),
        (1, "1 second"),
        (62, "1 minute and 2 seconds"),
        (120, "2 minutes"),
        (3600, "1 hour"),
        (3662, "1 hour, 1 minute and 2 seconds"),
    ]
    for seconds, duration in in_and_out:
        print(f"{seconds} -> {duration}")
        assert format_duration(seconds) == duration, format_duration(seconds)


if __name__ == "__main__":
    main()
