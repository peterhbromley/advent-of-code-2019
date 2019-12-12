from collections import namedtuple
from fractions import Fraction
from itertools import cycle, product

import numpy as np

ASTEROID = '#'
BLANK = '.'

QUADRANTS = ['first', 'fourth', 'third', 'second']

Point = namedtuple('Point', ['x', 'y'])

# This is a hack to add the vertical line slope
ZeroDivisionFraction = namedtuple('ZeroDivisionFraction',
                                 ['numerator', 'denominator'])

# Calculate the next point on a line given the current point and the slope.
# The keys refer to graph quadrants.
# The operations might look confusing due to the representation of the grid.
# In the grid representation, the y-axis increases pointing down instead of
# up so these operations are flipped.
#      0 1 2 3 4       
#    0 . . . . .      (-,-)|(+,-)
#    1 . . . . .        Q2 | Q1
#    2 . . X . .  -->  ----|----
#    3 . . . . .        Q3 | Q4
#    4 . . . . .      (-,+)|(+,+) 
#
next_point = {
    'first'  : lambda point, slope: Point(point.x + slope.denominator,
                                          point.y - slope.numerator),
    'second' : lambda point, slope: Point(point.x - slope.denominator,
                                          point.y - slope.numerator),
    'third'  : lambda point, slope: Point(point.x - slope.denominator,
                                          point.y + slope.numerator),
    'fourth' : lambda point, slope: Point(point.x + slope.denominator,
                                          point.y + slope.numerator),
}

special_slopes = {
    'first'  : [ZeroDivisionFraction(1, 0)],
    'second' : [Fraction(0, 1)],
    'third'  : [ZeroDivisionFraction(1, 0)],
    'fourth' : [Fraction(0, 1)],
}

def get_grid(input_path):
    grid = []
    with open(input_path) as f:
        line = f.readline()
        while line:
            grid.append(list(line.strip('\n')))
            line = f.readline()
    
    return grid


class AsteroidGrid:
    def __init__(self, grid, asteroid, blank):
        self.grid = np.array(grid)
        self.asteroid = asteroid
        self.blank = blank
        self.height = len(self.grid) - 1
        self.width = len(self.grid[0]) - 1

    def get_point(self, point):
        return self.grid[point.y][point.x]

    def is_asteroid(self, point):
        return self.get_point(point) == self.asteroid 

    def point_in_bounds(self, point):
        return 0 <= point.x <= self.width and \
               0 <= point.y <= self.height

    def vaporize(self, asteroid):
        self.grid[asteroid.y][asteroid.x] = self.blank

    @property
    def all_asteroids(self):
        asteroid_ys, asteroid_xs = np.where(self.grid == self.asteroid)
        return [
            Point(asteroid_x, asteroid_y) 
            for asteroid_x, asteroid_y in zip(asteroid_xs, asteroid_ys) 
        ]

    @property
    def all_slopes_in_quadrant(self):
        larger_dim = max(self.width, self.height) + 1
        products = product(range(1, larger_dim), repeat=2)
        non_zero_slopes = set(Fraction(p[0], p[1]) for p in products)
        return sorted(list(non_zero_slopes))[::-1]

    @property
    def all_slopes(self):
        slopes = self.all_slopes_in_quadrant
        return {
            'first'  : special_slopes['first'] + slopes,
            'second' : special_slopes['second'] + slopes[::-1],
            'third'  : special_slopes['third'] + slopes,
            'fourth' : special_slopes['fourth'] + slopes[::-1],
        }

    def asteroid_on_line(self, point, slope, quadrant, give_asteroid=False):
        point = next_point[quadrant](point, slope)
        while self.point_in_bounds(point):
            if self.is_asteroid(point):
                return point if give_asteroid else True
            point = next_point[quadrant](point, slope)
            
        return False

    def total_visible_asteroids(self, asteroid):
        total = 0
        for quadrant in QUADRANTS:
            slopes = self.all_slopes[quadrant]
            total += sum(self.asteroid_on_line(asteroid, slope, quadrant) 
                         for slope in slopes)
        return total

    def best_asteroid_count(self):
        counts = [
            self.total_visible_asteroids(asteroid)
            for asteroid in self.all_asteroids
        ]
        return np.max(counts), self.all_asteroids[np.argmax(counts)]

    def clockwise_vaporize(self, start):
        vaporized = 0
        while True:
            for quadrant in cycle(QUADRANTS):
                slopes = self.all_slopes[quadrant]
                for slope in slopes:
                    asteroid = self.asteroid_on_line(start,
                                                     slope,
                                                     quadrant,
                                                     give_asteroid=True)
                    if asteroid:
                        self.vaporize(asteroid)
                        vaporized += 1

                        if vaporized == 200:
                            return asteroid


grid = get_grid('input.txt')
a = AsteroidGrid(grid, ASTEROID, BLANK)
visible, asteroid = a.best_asteroid_count()
print("Answer to part 1: {}".format(visible))
asteroid_200 = a.clockwise_vaporize(Point(23, 29))
print("Answer to part 2: {}".format(asteroid_200.x * 100 + asteroid_200.y))