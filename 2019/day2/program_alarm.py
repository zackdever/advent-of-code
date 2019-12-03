# gravity assist program
gap = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,2,19,9,23,1,23,5,27,2,6,27,31,1,31,5,35,1,35,5,39,2,39,6,43,2,43,10,47,1,47,6,51,1,51,6,55,2,55,6,59,1,10,59,63,1,5,63,67,2,10,67,71,1,6,71,75,1,5,75,79,1,10,79,83,2,83,10,87,1,87,9,91,1,91,10,95,2,6,95,99,1,5,99,103,1,103,13,107,1,107,10,111,2,9,111,115,1,115,6,119,2,13,119,123,1,123,6,127,1,5,127,131,2,6,131,135,2,6,135,139,1,139,5,143,1,143,10,147,1,147,2,151,1,151,13,0,99,2,0,14,0]


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

import unittest

class Test(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(intcode([1,0,0,0,99]), [2,0,0,0,99])
        self.assertEqual(intcode([2,3,0,3,99]), [2,3,0,6,99])
        self.assertEqual(intcode([2,4,4,5,99,0]), [2,4,4,5,99,9801])
        self.assertEqual(intcode([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])


if __name__ == '__main__':
    """
    Each of the two input values will be between 0 and 99, inclusive.
    Find the input noun and verb that cause the program to produce the output 19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2, the answer would be 1202.)
    """
    for i in range(0,100):
        for j in range(0, 100):
            if run_intcode(gap.copy(), i, j) == 19690720:
                print(100 * i + j)
                break

