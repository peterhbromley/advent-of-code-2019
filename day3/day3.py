from collections import namedtuple

Coordinate = namedtuple('Coordinate', ['x', 'y'])

instruction_ops = {
    'R': lambda coord, steps: Coordinate(x=coord.x + steps,
                                         y=coord.y),
    'L': lambda coord, steps: Coordinate(x=coord.x - steps,
                                         y=coord.y),
    'U': lambda coord, steps: Coordinate(x=coord.x,
                                         y=coord.y + steps),
    'D': lambda coord, steps: Coordinate(x=coord.x,
                                         y=coord.y - steps),
}

class WirePath:
    def __init__(self, location):
        self.location = location
        # Dict of Coordinates -> steps taken upon first arrival
        self.seen_and_steps = {}
        self.steps_taken = 0
    
    def apply_instruction(self, direction, steps):
        # Given a direction and number of steps, move along the path and
        # record all coordinates along the way
        op = instruction_ops[direction]
        for step in range(steps):
            self.steps_taken += 1
            self.location = op(self.location, 1)
            self.update_seen_and_steps()

    def update_seen_and_steps(self):
        if self.location not in self.seen_and_steps:
            self.seen_and_steps[self.location] = self.steps_taken

    @classmethod
    def get_traced_path(cls, instructions):
        wire_path = cls(location=Coordinate(x=0, y=0))
        for direction, steps in instructions:
            wire_path.apply_instruction(direction, steps)
        return wire_path


def process_instructions(raw_instructions):
    # Split instructions into pairs of directions and steps
    return [(ins[0], int(ins[1:])) for ins in raw_instructions]
    

def run():
    with open('input.txt') as f:
        raw_instructions_1 = f.readline().split(',')
        raw_instructions_2 = f.readline().split(',')
        instructions_1 = process_instructions(raw_instructions_1)
        instructions_2 = process_instructions(raw_instructions_2)

    wire_path_1 = WirePath.get_traced_path(instructions_1)
    wire_path_2 = WirePath.get_traced_path(instructions_2)
    
    # Find the overlaps
    intersections = set(wire_path_1.seen_and_steps.keys()) & \
                    set(wire_path_2.seen_and_steps.keys())
    
    # Manhattan distance of intersections
    part1 = min(abs(coord.x) + abs(coord.y) for coord in intersections)

    # Combined total steps
    part2 = min(
        wire_path_1.seen_and_steps[coord] + wire_path_2.seen_and_steps[coord]
        for coord in intersections
    )

    print("Answer to part 1: {}".format(part1))
    print("Answer to part 2: {}".format(part2))

run()
