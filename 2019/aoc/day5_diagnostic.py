from enum import IntEnum


def dumb_input():
    return 1


class OpCode(IntEnum):
    HALT = 99
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4


class ParamMode(IntEnum):
    INDEX = 0
    VALUE = 1

    @classmethod
    def default(cls):
        cls.INDEX


class Modes:
    """A list of modes with an infinite default pop()."""
    def __init__(self, modes=None):
        self.modes = modes

    def pop(self):
        if self.modes:
            return self.modes.pop()
        return ParamMode.default()


def modes_and_opcode(instruction):
    """
    1004 -> ([1, 0], 4)
    """
    modes, opcode = Modes(), int(instruction)
    instr = str(instruction)
    if len(instr) > 2:
        modes = Modes([int(x) for x in instr[:-2]])
        opcode = int(instr[-2:])
    return modes, opcode


def get_param(code, i, mode):
    return code[i] if mode == ParamMode.VALUE else code[code[i]]


def diagnostic_program(code):
    output = []
    i = 0
    while i < len(code):
        modes, opcode = modes_and_opcode(code[i])
        if opcode == OpCode.HALT:
            break

        if opcode in (OpCode.ADD, OpCode.MULTIPLY):
            val1 = get_param(code, i+1, modes.pop())
            val2 = get_param(code, i+2, modes.pop())
            outi = code[i+3]
            i += 3
            if opcode == OpCode.ADD:
                code[outi] = val1 + val2
            else:
                code[outi] = val1 * val2
        elif opcode in (OpCode.INPUT, OpCode.OUTPUT):
            # Parameters that an instruction writes to will never be in immediate mode.
            outi = code[i+1]
            i += 1
            if opcode == OpCode.INPUT:
                code[outi] = dumb_input()
            else:
                output.append(get_param(code, i, modes.pop()))
        else:
            raise ValueError('Do not recognize code {} at index {}'.format(opcode, i))
        i += 1
    return output


if __name__ == '__main__':
    fp = './input/day5.txt'
    with open(fp) as f:
        code = [int(x) for x in f.read().strip().split(',')]

    output = diagnostic_program(code)
    for val in output[:-1]:
        if val != 0:
            print('Houston, we have a problem')
            break
    else:
        print('Diagnostic code: {}'.format(output[-1]))
