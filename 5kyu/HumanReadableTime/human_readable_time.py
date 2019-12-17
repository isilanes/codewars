# https://www.codewars.com/kata/52685f7382004e774f0001f7

def make_readable(seconds):
    ss = seconds % 60
    seconds = seconds - ss
    mm = (seconds % 3600) // 60
    seconds = seconds - mm*60
    hh = seconds // 3600

    return f"{hh:02d}:{mm:02d}:{ss:02d}"

if __name__ == "__main__":
    print(make_readable(86399))
