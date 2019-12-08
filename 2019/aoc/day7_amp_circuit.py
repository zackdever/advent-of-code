import itertools
import queue

from aoc import day5_diagnostic as d5


def thruster_signal(code, phase_sequence):
    # taking advantage of the fac that -1 in python is the last elemnt
    # so, the first queue in msg_qs is output queue of the first "amp",
    # and the last queue is it's input.
    msg_qs = [None for _ in phase_sequence]
    for i, setting in enumerate(phase_sequence):
        q = queue.SimpleQueue()
        q.put(setting)
        # first input is 0, per AOC instructions
        if i == 0:
            q.put(0)
        msg_qs[i-1] = q

    for i in range(len(phase_sequence)):
        d5.intcode(code, msg_qs[i-1], msg_qs[i])

    return msg_qs[-1].get()


def max_thruster_signal(code, feedback=False):
    phase_range = range(5, 10) if feedback else range(5)
    phase_seqs = itertools.permutations(phase_range)
    # TODO run in parallel
    return max(thruster_signal(code, seq) for seq in phase_seqs)


if __name__ == '__main__':
    fp = './input/day7.txt'
    with open(fp) as f:
        code = [int(x) for x in f.read().strip().split(',')]
    signal = max_thruster_signal(code, feedback=False)
    print('Highest signal, without feedback, for thrusters: {}'.format(signal))
    # signal = max_thruster_signal(code, feedback=True)
    # print('Highest signal, WITH feedback, for thrusters: {}'.format(signal))
