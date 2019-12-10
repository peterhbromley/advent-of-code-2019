from computer import Computer
from itertools import cycle, permutations

AMPLIFIERS = ['A', 'B', 'C', 'D', 'E']

INPUT_VALUE = 0

def get_input(input_path):
    with open(input_path) as f:
        line = f.readline()

    return list(map(int, line.split(',')))


def run_amplifiers(tape, phases):
    """Part 1: Run all amplifiers once and get the output"""
    in_val = INPUT_VALUE
    for phase in phases:
        computer = Computer(tape=tape, ptr=0, in_vals=[phase, in_val])
        out = computer.run(output_mode=False)
        in_val = out
    return computer.out


def run_amplifier_circuit(tape, phases):
    """Part 2: Run amplifiers in a circuit until they have halted"""
    amplifiers = {
        amp : Computer(tape=tape.copy(), ptr=0, in_vals=[phase])
        for amp, phase in zip(AMPLIFIERS, phases)
    }

    # Generator that loops around the amplifiers
    amp_gen = cycle(AMPLIFIERS)
    which_amp = next(amp_gen)
    in_val = INPUT_VALUE
    while not amplifiers['E'].halted:
        amp = amplifiers[which_amp]
        amp.add_in_val(in_val)
        out = amp.run(output_mode=True)
        in_val = out
        which_amp = next(amp_gen)

    return amplifiers['E'].out


def optimize(tape, perms, run_func):
    """Find the max output given a list of permutations"""
    outputs = [run_func(tape, phases) for phases in perms]
    return max(outputs)



def main():
    tape = get_input('input.txt')

    part_1_perms = permutations([0, 1, 2, 3, 4])
    part_2_perms = permutations([5, 6, 7, 8, 9])

    part_1 = optimize(tape, part_1_perms, run_amplifiers)
    part_2 = optimize(tape, part_2_perms, run_amplifier_circuit)

    print('Answer to part 1: {}'.format(part_1))
    print('Answer to part 2: {}'.format(part_2))



main()