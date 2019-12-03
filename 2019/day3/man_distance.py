import unittest


UPDATES = {
        'U': (0, 1),
        'R': (1, 0),
        'D': (0, -1),
        'L': (-1, 0),
        }


def positions(wire):
    cur = [0, 0]
    pos = set()
    for move in wire:
        direction, distance = move[0], int(move[1:])
        update = UPDATES[direction]
        for i in range(distance):
            cur[0] += update[0]
            cur[1] += update[1]
            pos.add((cur[0], cur[1]))
    return pos


def distance(pos, origin=(0, 0)):
    return abs(pos[0] - origin[0]) + abs(pos[1] - origin[1])


def solve(wire1, wire2):
    pos1 = positions(wire1)
    pos2 = positions(wire2)
    # find all positions where the paths cross
    cross = pos1.intersection(pos2)
    # calculate distance for each
    distances = [distance(c) for c in cross]
    # choose min
    return min(distances)


class Test(unittest.TestCase):
    def test_examples(self):
        wire1 = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
        wire2 = ['U62','R66','U55','R34','D71','R55','D58','R83']
        distance = 159
        self.assertEqual(solve(wire1, wire2), distance)


        wire1 = ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51']
        wire2 = ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
        distance = 135
        self.assertEqual(solve(wire1, wire2), distance)


if __name__ == '__main__':
    wire1, wire2 = None, None
    with open('./input.txt') as f:
        wire1, wire2 = [l.strip().split(',') for l in f.readlines()]
        
    print(solve(wire1, wire2))