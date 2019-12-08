# https://adventofcode.com/2019/day/5

from enum import IntEnum
from queue import SimpleQueue


class OpCode(IntEnum):
    HALT = 99
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUAL = 8


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


def intcode(code, msg_in, msg_out):
    """
    code: sequence of int codes
    msg_in: queue for messages in
    msg_out: queue for messages out
    
    Does not return any values, but stops on HALT.
    """
    code = code.copy()
    # Parameters that an instruction writes to will never be in immediate mode.
    # This does not include output though, only writes back to the code!
    i = 0 # instruction pointer
    while i < len(code):
        modes, opcode = modes_and_opcode(code[i])
        if opcode == OpCode.HALT:
            break

        if opcode in (OpCode.ADD, OpCode.MULTIPLY, OpCode.LESS_THAN, OpCode.EQUAL):
            # operate on first two params. 3rd param: store result
            val1 = get_param(code, i+1, modes.pop())
            val2 = get_param(code, i+2, modes.pop())
            outi = code[i+3]
            i += 3
            if opcode == OpCode.ADD:
                code[outi] = val1 + val2
            elif opcode == OpCode.MULTIPLY:
                code[outi] = val1 * val2
            elif opcode == OpCode.LESS_THAN:
                code[outi] = 1 if val1 < val2 else 0
            elif opcode == OpCode.EQUAL:
                code[outi] = 1 if val1 == val2 else 0
        elif opcode in (OpCode.INPUT, OpCode.OUTPUT):
            # write or read based on the next param
            outi = code[i+1]
            i += 1
            if opcode == OpCode.INPUT:
                code[outi] = msg_in.get()
            else:
                msg_out.put(get_param(code, i, modes.pop()))
        elif opcode in (OpCode.JUMP_IF_TRUE, OpCode.JUMP_IF_FALSE):
            # maybe jump to the address represented by the next param
            val1 = get_param(code, i+1, modes.pop())
            if ((opcode == OpCode.JUMP_IF_TRUE and val1 != 0) or
                (opcode == OpCode.JUMP_IF_FALSE and val1 == 0)):
                i = get_param(code, i+2, modes.pop())
                continue
            else:
                # we didn't jump, so move the instruction pointer past the params
                i += 2
        else:
            raise ValueError('Do not recognize code {} at index {}'.format(opcode, i))
        i += 1
    return


if __name__ == '__main__':
    input_val = 5 # part 1: 1, part 2: 5
    fp = './input/day5.txt'
    with open(fp) as f:
        code = [int(x) for x in f.read().strip().split(',')]


    in_msg = SimpleQueue()
    in_msg.put(input_val)
    out_msg = SimpleQueue()
    intcode(code, in_msg, out_msg)
    output = []
    while not out_msg.empty():
        output.append(out_msg.get())

    for val in output[:-1]:
        if val != 0:
            print('Houston, we have a problem')
            break
    else:
        print('Diagnostic code: {}'.format(output[-1]))
