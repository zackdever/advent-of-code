def build_layers(data, width, height):
    """
    Given data, return a list of layers of 2d arrays width x height.
    Converts data to int.
    e.g.
    build_layers(data='123456789012', width=3, height=2)
    returns [
        [[1, 2, 3], [4, 5, 6]], # layer 1
        [[7, 8, 9], [0, 1, 2]] # layer 2
    ]
    """
    # TODO seems backwards, can't i loop through data?
    i = 0
    layers = []
    for start_idx in range(0, len(data), width * height):
        layer = []
        for row_idx in range(height):
            row = []
            for col_idx in range(width):
                row.append(int(data[i]))
                i += 1
            layer.append(row)
        layers.append(layer)
    return layers


def count_digits(layers):
    """
    Return a list of dicts of digit counts.
    e.g. [{0: 10, 1: 90}, {0: 50, 1: 50}]
    """
    digit_layers = []
    for layer in layers:
        counts = {}
        for row in layer:
            for digit in row:
                if digit not in counts:
                    counts[digit] = 0
                counts[digit] += 1
        digit_layers.append(counts)
    return digit_layers


def checksum(layers):
    """
    Part 1: To make sure the image wasn't corrupted during
    transmission, the Elves would like you to find the layer
    that contains the fewest 0 digits. On that layer, what is
    the number of 1 digits multiplied by the number of 2 digits?
    """
    layer_digits = count_digits(layers)
    target = None
    for digits in layer_digits:
        if not target:
            target = digits if 0 in digits else None
        elif 0 in digits and digits[0] < target[0]:
            target = digits
    return target[1] * target[2]


def flatten_layers(layers):
    """
    First layer in front, last layer in back.
    0 is black, 1 is white, and 2 is transparent.
    The final value for a position is the first visible (non-transparent) value.
    """
    final = []
    width, height = len(layers[0][0]), len(layers[0])
    layer_count = len(layers)
    for row in range(height):
        final_row = []
        for col in range(width):
            visible = 2 # default, in case they're all transparent
            for i in range(layer_count):
                if layers[i][row][col] != 2:
                    visible = layers[i][row][col]
                    break
            final_row.append(visible)
        final.append(final_row)
    return final

def print_image(data, width, height):
    def render(digit):
        if digit == 0:
            return '\u2B1B' # black
        elif digit == 1:
            return '\u2B1C' # white
        return ' ' #clear

    for row in flatten_layers(build_layers(data, width, height)):
        print(''.join(render(digit) for digit in row))


if __name__ == '__main__':
    fp = 'input/day8.txt'
    with open(fp) as f:
        data = f.read().strip()
    width, height = 25, 6
    layers = build_layers(data, width, height)
    print('Image checksum: {}'.format(checksum(layers)))
    print_image(data, width, height)
