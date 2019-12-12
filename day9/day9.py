from computer import Computer

EXTRA_MEMORY = 10000
MEMORY_INIT_VALUE = 0

def get_input(input_path):
    with open(input_path) as f:
        line = f.readline()

    return list(map(int, line.split(',')))


def main():
    tape = get_input('input.txt')
    extra_memory = [MEMORY_INIT_VALUE]*EXTRA_MEMORY
    tape += extra_memory

    computer = Computer(
        tape=tape,
        ptr=0,
        in_vals=None,
        base=0,
    )

    out = computer.run()
    print("Final Output: {}".format(out))


main()