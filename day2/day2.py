import numpy as np

op_dict = {
    1: lambda x, y: x + y,
    2: lambda x, y: x * y,
}

class Tape:
    def __init__(self, tape):
        self.tape = tape

    def ix_lookup(self, ix):
        return self.tape[ix]

    def ix_assign(self, ix, val):
        self.tape[ix] = val

    def full_lookup(self, ix):
        return self.tape[self.tape[ix]]
    
    def full_assign(self, ix, val):
        self.tape[self.tape[ix]] = val

    def apply_op(self, op, ix_1, ix_2, ix_3):
        val = op(self.full_lookup(ix_1), self.full_lookup(ix_2))
        self.full_assign(ix_3, val)

    def get_full_tape(self):
        return self.tape

def perform_op(tape, op_ix):
    op = op_dict[tape.ix_lookup(op_ix)]
    tape.apply_op(op, op_ix + 1, op_ix + 2, op_ix + 3)


def get_tape(input_file='input.txt'):
    with open(input_file) as f:
        line = f.readline()
    return Tape(list(map(int, line.split(','))))


def run_computer(tape, configure=None):
    if configure:
        replace_1, replace_2 = configure
        tape.ix_assign(1, replace_1)
        tape.ix_assign(2, replace_2)

    ix = 0
    while tape.ix_lookup(ix) != 99:
        perform_op(tape, ix)
        ix += 4

    return tape.ix_lookup(0)
    
    
def part_1():
    tape = get_tape()
    answer = run_computer(tape, configure=(12, 2))
    print('Answer to part 1: {}'.format(answer))

def part_2():
    tape = get_tape()
    tape_contents = tape.get_full_tape()
    for noun in range(100):
        for verb in range(100):
            memory = Tape(tape_contents.copy())
            out = run_computer(memory, configure=(noun, verb))
            if out == 19690720:
                print('Answer to part 2: {}'.format(100 * noun + verb))
                return
    print('target not found')

part_1()
part_2()
