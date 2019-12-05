def intcode(code):
    for i in range(0, len(code), 4):
        op = code[i]
        if op == 99:
            break

        val1 = code[code[i+1]]
        val2 = code[code[i+2]]
        outi = code[i+3]

        if op == 1:
            code[outi] = val1 + val2
        elif op == 2:
            code[outi] = val1 * val2
        else:
            raise ValueError('Do not recognize code {} at index {}'.format(op, i))

    return code

def run_intcode(code, noun, verb):
    code[1] = noun
    code[2] = verb
    return intcode(code)[0]



if __name__ == '__main__':
    """
    Each of the two input values will be between 0 and 99, inclusive.
    Find the input noun and verb that cause the program to produce the output 19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2, the answer would be 1202.)
    """
    # gravity assist program
    fp = './input/day2.txt'
    with open(fp) as f:
        gap = [int(x) for x in f.read().strip().split(',')]

    for i in range(0,100):
        for j in range(0, 100):
            if run_intcode(gap.copy(), i, j) == 19690720:
                print(100 * i + j)
                break
