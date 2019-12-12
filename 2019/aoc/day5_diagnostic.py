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
    RELATIVE_BASE = 9


class ParamMode(IntEnum):
    INDEX = 0
    VALUE = 1
    RELATIVE = 2

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


class Ram:
    def __init__(self, code):
        self.default = 0
        self.code = code
        self.extended = {}

    def __getitem__(self, index):
        if index < 0:
            raise Exception('Cannot access negative address')
        if index < len(self.code):
            return self.code[index]
        if index not in self.extended:
            self.extended[index] = self.default
        return self.extended[index]

    def __setitem__(self, index, value):
        if index < 0:
            raise Exception('Cannot access negative address')
        if index < len(self.code):
            self.code[index] = value
        else:
            self.extended[index] = value
        

def get_param(ram, i, mode, relative_base):
    if mode == ParamMode.VALUE:
        return ram[i]
    elif mode == ParamMode.RELATIVE:
        return ram[ram[i] + relative_base]
    else:
        return ram[ram[i]]


def write(ram, i, mode, relative_base, value):
    if mode == ParamMode.VALUE:
        raise Exception('ParamMode.VALUE ({}) not supported for writes'.format(ParamMode.VALUE))
    elif mode == ParamMode.RELATIVE:
        ram[ram[i] + relative_base] = value
    else:
        ram[ram[i]] = value



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
    relative_base = 0
    ram = Ram(code)
    while i < len(code):
        modes, opcode = modes_and_opcode(code[i])
        if opcode == OpCode.HALT:
            break

        if opcode in (OpCode.ADD, OpCode.MULTIPLY, OpCode.LESS_THAN, OpCode.EQUAL):
            # operate on first two params. 3rd param: store result
            val1 = get_param(ram, i+1, modes.pop(), relative_base)
            val2 = get_param(ram, i+2, modes.pop(), relative_base)
            i += 3
            output = None
            if opcode == OpCode.ADD:
                output = val1 + val2
            elif opcode == OpCode.MULTIPLY:
                output = val1 * val2
            elif opcode == OpCode.LESS_THAN:
                output = 1 if val1 < val2 else 0
            elif opcode == OpCode.EQUAL:
                output = 1 if val1 == val2 else 0
            write(ram, i, modes.pop(), relative_base, output)
        elif opcode in (OpCode.INPUT, OpCode.OUTPUT):
            # write or read based on the next param
            i += 1
            if opcode == OpCode.INPUT:
                write(ram, i, modes.pop(), relative_base, msg_in.get())
            else:
                msg_out.put(get_param(ram, i, modes.pop(), relative_base))
        elif opcode in (OpCode.JUMP_IF_TRUE, OpCode.JUMP_IF_FALSE):
            # maybe jump to the address represented by the next param
            val1 = get_param(ram, i+1, modes.pop(), relative_base)
            if ((opcode == OpCode.JUMP_IF_TRUE and val1 != 0) or
                (opcode == OpCode.JUMP_IF_FALSE and val1 == 0)):
                i = get_param(ram, i+2, modes.pop(), relative_base)
                continue
            else:
                # we didn't jump, so move the instruction pointer past the params
                i += 2
        elif opcode == OpCode.RELATIVE_BASE:
            relative_base += get_param(ram, i+1, modes.pop(), relative_base)
            i += 1
        else:
            raise ValueError('Do not recognize code {} at index {}'.format(opcode, i))
        i += 1
    return


def intcode_helper(code, input_val=None):
    in_msg = SimpleQueue()
    if input_val is not None:
        in_msg.put(input_val)
    out_msg = SimpleQueue()
    intcode(code, in_msg, out_msg)
    output = []
    while not out_msg.empty():
        output.append(out_msg.get())
    return output


if __name__ == '__main__':
    input_val = 5 # part 1: 1, part 2: 5
    fp = './input/day5.txt'
    with open(fp) as f:
        code = [int(x) for x in f.read().strip().split(',')]

    output = intcode_helper(code, input_val)
    for val in output[:-1]:
        if val != 0:
            print('Houston, we have a problem')
            break
    else:
        print('Diagnostic code: {}'.format(output[-1]))
