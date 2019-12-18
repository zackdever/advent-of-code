import itertools
import re


class Jupiter:
    """Works for n-dimensional positions"""
    def __init__(self, moon_positions):
        self.time = 0
        self.axes = list(moon_positions[0].keys())
        self.moons = [{'pos': pos, 'vel': {k: 0 for k in self.axes}} for pos in moon_positions]

    def advance_time(self, step):
        """
        1. Update velocity by applying gravity
        2. Update position by applying velocity
        """
        for _ in range(step):
            self.apply_gravity()
            self.apply_velocity()
            self.time += 1

    def energy(self):
        total = 0
        for moon in self.moons:
            potential = sum(abs(val) for val in moon['pos'].values())
            kinetic = sum(abs(val) for val in moon['vel'].values())
            total += potential * kinetic
        return total

    def apply_gravity(self):
        """
        Consider every pair of moons. On each axis (x, y, and z),
        the velocity of each moon changes by exactly +1 or -1 to
        pull the moons together.
        """
        for moon1, moon2 in itertools.combinations(self.moons, 2):
            for axis in self.axes:
                if moon2['pos'][axis] > moon1['pos'][axis]:
                    moon2['vel'][axis] -= 1
                    moon1['vel'][axis] += 1
                elif moon2['pos'][axis] < moon1['pos'][axis]:
                    moon2['vel'][axis] += 1
                    moon1['vel'][axis] -= 1

    def apply_velocity(self):
        """
        Add the velocity of each moon to its own position.
        """
        for moon in self.moons:
            for axis, vel in moon['vel'].items():
                moon['pos'][axis] += vel


def parse(lines):
    """'<x=8, y=0, z=8>' -> {'x': 8, 'y': 0, 'z': 8}"""
    positions = []
    for line in lines:
        m = re.match(r'<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>', line.strip())
        positions.append({k: int(v) for k, v in m.groupdict().items()})
    return positions


if __name__ == '__main__':
    fp = './input/day12.txt'
    with open(fp) as f:
        lines = f.readlines()
    moon_positions = parse(lines)

    jupiter = Jupiter(moon_positions)
    jupiter.advance_time(1000)
    print('Total energy after 1000 steps: {}'.format(jupiter.energy()))
