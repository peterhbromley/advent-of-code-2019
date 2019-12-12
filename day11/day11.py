from collections import namedtuple

import numpy as np

from computer import Computer

Point = namedtuple('Point', ['x', 'y'])

BLACK = '.'
WHITE = '#'
ROBO_CHAR = {
    'up'    : '^',
    'down'  : 'v',
    'left'  : '<',
    'right' : '>',
}
DIR_LABELS = {
    0 : 'up',
    1 : 'right',
    2 : 'down',
    3 : 'left',
}

class Robot:
    def __init__(self,
                 brain,
                 grid,
                 location,
                 direction,
                 painted=set()):
        self.brain = brain
        self.grid = grid
        self.location = location
        self.direction = direction
        self.painted = painted

        self.rotater = {
            0 : lambda x: (x - 1) % 4,
            1 : lambda x: (x + 1) % 4,
        }

        self.mover = {
            0 : lambda p: Point(p.x, p.y + 1),
            1 : lambda p: Point(p.x + 1, p.y),
            2 : lambda p: Point(p.x, p.y - 1),
            3 : lambda p: Point(p.x - 1, p.y),
        }

        self.color_map = {
            0 : BLACK,
            BLACK : 0,
            1 : WHITE,
            WHITE : 1,
        }

    def getter(self, point):
        return self.grid[point.y][point.x]

    def setter(self, point, char):
        self.grid[point.y][point.x] = char
    
    @property
    def current_color(self):
        return self.getter(self.location)

    def move(self):
        mover_function = self.mover[self.direction]
        self.location = mover_function(self.location)

    def rotate(self, direction):
        rotater_function = self.rotater[direction]
        self.direction = rotater_function(self.direction)

    def paint(self, color):
        self.setter(self.location, self.color_map[color])
        if self.location not in self.painted:
            self.painted.add(self.location)

    def print_grid(self):
        for i in range(len(self.grid)-1, -1, -1):
            for j in range(len(self.grid[0])):
                print(self.grid[i][j], end=" ")
            print("")

    def run(self):
        while not self.brain.halted:
            in_val = self.color_map[self.current_color]
            out1 = self.brain.run(output_mode=True, extra_in_vals=[in_val])
            self.paint(out1)
            out2 = self.brain.run(output_mode=True)
            self.rotate(out2)
            self.move()
        return self.painted



EXTRA_MEMORY = 10000
MEMORY_INIT_VALUE = 0

GRID_DIMS = 100, 100
ROBOT_START = Point(50, 50)

def get_input(input_path):
    with open(input_path) as f:
        line = f.readline()

    return list(map(int, line.split(',')))


def get_robot(tape, grid):
    brain = Computer(
        tape=tape,
        ptr=0,
        in_vals=[],
        base=0,
    )

    robot = Robot(
        brain=brain,
        grid=grid,
        location=ROBOT_START,
        direction=0,
        painted=set()
    )

    return robot


def main():
    tape = get_input('input.txt')
    extra_memory = [MEMORY_INIT_VALUE]*EXTRA_MEMORY
    tape += extra_memory

    brain = Computer(
        tape=tape,
        ptr=0,
        in_vals=[],
        base=0,
    )

    grid_width, grid_height = GRID_DIMS

    grid_1 = np.zeros((grid_height, grid_width), 'U1')
    grid_1.fill(WHITE)

    robot_1 = get_robot(tape, grid_1)
    painted_1 = robot_1.run()

    print('Answer to part 1: {}'.format(len(painted_1)))

    grid_2 = np.zeros((grid_height, grid_width), 'U1')
    grid_2.fill(BLACK)
    grid_2[ROBOT_START.y][ROBOT_START.x] = WHITE

    robot_2 = get_robot(tape, grid_2)
    painted_2 = robot_2.run()

    robot_2.print_grid()

main()
    


    