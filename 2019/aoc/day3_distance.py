UPDATES = {
        'U': (0, 1),
        'R': (1, 0),
        'D': (0, -1),
        'L': (-1, 0),
        }


def positions(wire):
    cur = [0, 0]
    steps = 0
    pos = {}
    for move in wire:
        direction, distance = move[0], int(move[1:])
        update = UPDATES[direction]
        for i in range(distance):
            steps += 1
            cur[0] += update[0]
            cur[1] += update[1]
            new = (cur[0], cur[1])
            if new not in pos:
                pos[new] = steps
    return pos


def distance(pos, origin=(0, 0)):
    return abs(pos[0] - origin[0]) + abs(pos[1] - origin[1])


def solve_min_distance(wire1, wire2):
    pos1 = positions(wire1)
    pos2 = positions(wire2)
    # find all positions where the paths cross
    cross = set(pos1).intersection(pos2)
    # calculate distance for each
    distances = [distance(c) for c in cross]
    # choose min
    return min(distances)

def solve_min_steps(wire1, wire2):
    pos1 = positions(wire1)
    pos2 = positions(wire2)
    # find all positions where the paths cross
    cross = set(pos1).intersection(pos2)
    # calculate steps for each
    distances = [pos1[c] + pos2[c] for c in cross]
    # choose min
    return min(distances)


if __name__ == '__main__':
    wire1, wire2 = None, None
    with open('./input/day3.txt') as f:
        wire1, wire2 = [l.strip().split(',') for l in f.readlines()]
        
    print('distance: {}'.format(solve_min_distance(wire1, wire2)))
    print('steps: {}'.format(solve_min_steps(wire1, wire2)))
