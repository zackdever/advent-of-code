import itertools

from aoc import day5_diagnostic as d5


def thruster_signal(code, phase_sequence):
    # first input is 0, per AOC instructions
    input_val = 0
    for i, seq in enumerate(phase_sequence):
        [input_val] = d5.intcode(code, (phase_sequence[i], input_val))
    return input_val

def max_thruster_signal(code):
    # phase setting is 0-4, each used exactly once
    phase_seqs = itertools.permutations(range(5))
    return max(thruster_signal(code, seq) for seq in phase_seqs)


if __name__ == '__main__':
    fp = './input/day7.txt'
    with open(fp) as f:
        code = [int(x) for x in f.read().strip().split(',')]
    signal = max_thruster_signal(code)
    print('Highest signal for thrusters: {}'.format(signal))
