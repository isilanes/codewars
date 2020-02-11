# https://www.codewars.com/kata/52742f58faf5485cae000b9a/train/python


def format_duration(seconds):
    return None


def main():
    in_and_out = [
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
