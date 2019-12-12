import numpy as np


op_dict = {
    1: lambda x, y: x + y,
    2: lambda x, y: x * y,
    5: lambda x: x != 0,
    6: lambda x: x == 0,
    7: lambda x, y: int(x < y),
    8: lambda x, y: int(x == y),
}

class Computer:
    def __init__(self, tape, ptr, in_vals, base, verbose=False):
        self.tape = tape
        self.ptr = ptr
        self.in_vals = in_vals
        self.base = base
        self.out = None
        self.running = True
        self.verbose = verbose

    # Get the value directly at ptr
    def direct_lookup(self, ptr):
        return self.tape[ptr]

    # Set the value at ptr to `val`
    def direct_assign(self, ptr, val):
        self.tape[ptr] = val

    # Lookup the value at the address given by the value at the tapehead
    def address_lookup(self, ptr):
        return self.tape[self.tape[ptr]]
    
    # Set the value at the address given by the tapehead to val
    def address_assign(self, ptr, val):
        self.tape[self.tape[ptr]] = val

    # Handle which lookup to use given mode
    def getter(self, mode, ix):
        if mode == 0:
            return self.address_lookup(ix)
        elif mode == 1:
            return self.direct_lookup(ix)
        elif mode == 2:
            offset = self.direct_lookup(ix)
            return self.direct_lookup(self.base + offset)
    
    # Handle which assign to use given mode
    def setter(self, mode, ix, val):
        if mode == 0:
            self.address_assign(ix, val)
        elif mode == 1:
            self.direct_assign(ix, val)
        elif mode == 2:
            offset = self.direct_lookup(ix)
            return self.direct_assign(self.base + offset, val)

    @property
    def tape_head(self):
        return self.direct_lookup(self.ptr)

    @property
    def halted(self):
        return self.tape_head == 99

    def lookup(self, mode, ix):
        return self.getter(mode, ix)

    def assign(self, mode, ix, val):
        return self.setter(mode, ix, val)

    def add_in_val(self, val):
        self.in_vals.append(val)

    # Lookup the first two params
    def get_params(self, *modes):
        return tuple(
            self.lookup(mode, self.ptr + i + 1)
            for i, mode in enumerate(modes)
        )

    # FUNCTIONS FOR PERFORMING OPERATIONS
    # ------------------------------------

    def binary_op(self, op_val, *modes):
        mode1, mode2, mode3 = modes
        p1, p2 = self.get_params(mode1, mode2)
        op = op_dict[op_val]

        val = op(p1, p2)
        self.assign(mode3, self.ptr + 3, val)
        self.ptr += 4


    def jump(self, op_val, mode1, mode2, *modes):
        p1, p2 = self.get_params(mode1, mode2)
        op = op_dict[op_val]        

        self.ptr = p2 if op(p1) else self.ptr + 3

    
    def adjust_base(self, mode, *modes):
        p, = self.get_params(mode)
        self.base += p
        self.ptr += 2
        

    def get_input(self, mode, *modes, in_val=None):
        if not self.in_vals:
            in_val = int(input("Enter input: "))
        else:
            in_val = self.in_vals.pop(0)
        self.assign(mode, self.ptr + 1, in_val)
        self.ptr += 2


    def get_output(self, mode, *modes):
        self.out, = self.get_params(mode)
        self.ptr += 2
        self.running = False
        if self.verbose:
            print("PROGRAM OUTPUT: {}".format(self.out))


    @property
    def ops(self):
        return { 
            1 : self.chooser(self.binary_op, 1),
            2 : self.chooser(self.binary_op, 2),
            3 : self.get_input,
            4 : self.get_output,
            5 : self.chooser(self.jump, 5),
            6 : self.chooser(self.jump, 6),
            7 : self.chooser(self.binary_op, 7),
            8 : self.chooser(self.binary_op, 8),
            9 : self.adjust_base,
        }
    
    # For the functions that depend on op_val, pass the op_val here
    # so the ops dict generalizes to only take mode
    def chooser(self, func, op_val):
        return lambda *modes: func(op_val, *modes)

    # Get the opcode value and 3 modes
    def parse_opcode(self):
        op_code = self.direct_lookup(self.ptr)
        digits = [int(d) for d in str(op_code).zfill(5)]
        mode3, mode2, mode1, _, op_val = digits
        return op_val, (mode1, mode2, mode3)

    # Given a ptr to the op, perform the op
    def perform_op(self):
        op_val, modes = self.parse_opcode()
        op_function = self.ops[op_val]
        op_function(*modes)

    def run(self, output_mode=False, extra_in_vals=None):
        # For output mode, can be used to stop the computer when it
        # has just given *output* but not necessarily halted
        self.running = True

        if extra_in_vals:
            self.in_vals += extra_in_vals

        while not self.halted:
            self.perform_op()

            if not self.running and output_mode:
                return self.out

        self.running = False
        return self.out
