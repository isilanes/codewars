# https://www.codewars.com/kata/text-align-justify/train/python

RESULT = """Lorem  ipsum  dolor  sit amet,
consectetur  adipiscing  elit.
Vestibulum    sagittis   dolor
mauris,  at  elementum  ligula
tempor  eget.  In quis rhoncus
nunc,  at  aliquet orci. Fusce
at   dolor   sit   amet  felis
suscipit   tristique.   Nam  a
imperdiet   tellus.  Nulla  eu
vestibulum    urna.    Vivamus
tincidunt  suscipit  enim, nec
ultrices   nisi  volutpat  ac.
Maecenas   sit   amet  lacinia
arcu,  non dictum justo. Donec
sed  quam  vel  risus faucibus
euismod.  Suspendisse  rhoncus
rhoncus  felis  at  fermentum.
Donec lorem magna, ultricies a
nunc    sit    amet,   blandit
fringilla  nunc. In vestibulum
velit    ac    felis   rhoncus
pellentesque. Mauris at tellus
enim.  Aliquam eleifend tempus
dapibus. Pellentesque commodo,
nisi    sit   amet   hendrerit
fringilla,   ante  odio  porta
lacus,   ut   elementum  justo
nulla et dolor."""


def justify(text, width):
    lines = []
    words_in_current_line = []
    width_if_add_current_word = -1

    for word in text.split():
        width_if_add_current_word += len(word) + 1

        if width_if_add_current_word == width:  # with current word line would fit exactly with single spaces
            # Add current word to current line buffer, save current line string, and empty current line buffer:
            words_in_current_line.append(word)
            line = " ".join(words_in_current_line)
            lines.append(line)
            words_in_current_line = []
            width_if_add_current_word = -1
            continue

        if width_if_add_current_word > width:  # adding current word would overflow
            if len(words_in_current_line) == 1:  # single-word lines have no spaces or frills
                line = words_in_current_line[0]

            else:
                # Multi-word lines have amount_big_spaces of big_space gaps, and the rest of gaps of width
                # small_space_width. big_space equals small_space plus one space.
                word_len = sum([len(w) for w in words_in_current_line])
                needed_spaces = width - word_len
                gaps = len(words_in_current_line) - 1
                small_space_width = needed_spaces // gaps
                amount_big_spaces = needed_spaces % gaps
                small_space = " " * small_space_width
                big_space = small_space + " "

                # Words separated by big gaps:
                big_separated_words = words_in_current_line[:amount_big_spaces + 1]
                big_separated_part = big_space.join(big_separated_words)

                # Words separated by small gaps:
                small_separated_words = words_in_current_line[amount_big_spaces + 1:]
                small_separated_part = small_space.join(small_separated_words)

                # Line is union or both:
                line = small_space.join([big_separated_part, small_separated_part])

            # Single-word or not, add current line string to list of lines, and start next line buffer
            # with current word (which would have overflown if included in current line, remember).
            lines.append(line)
            words_in_current_line = [word]
            width_if_add_current_word = len(word)

        else:  # adding current word to current line would not overflow it, so add it
            words_in_current_line.append(word)

    # If words left, add last line:
    if words_in_current_line:
        line = " ".join(words_in_current_line)
        lines.append(line)

    return "\n".join(lines)


def main():
    text = " ".join(RESULT.split())

    result = justify(text, 30)

    assert result == RESULT


if __name__ == "__main__":
    main()
