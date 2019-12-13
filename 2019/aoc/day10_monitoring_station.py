import collections
import itertools
import math


def asteroid_map_to_coords(asteroid_map):
    """
    Takes a string/ascii art asteroid map
    and returns a sorted list of coordinates.
    """
    asteroid_coords = []
    y = 0
    for line in asteroid_map.strip().split('\n'):
        x = 0
        for ch in line:
            if ch == '#':
                asteroid_coords.append((x, y))
            x += 1
        y += 1
    return sorted(asteroid_coords)


def coord_key(c1, c2):
    return (c1, c2) if c1 <= c2 else (c2, c1)


def linear_eq(c1, c2):
    """
    Return the slope and y-intercept for the two given points.
    Undefined is None.
    e.g. m=3.0 b=1.0 -> (3.0, 1.0)
    """
    run = c2[0] - c1[0]
    if run == 0:
        return (None, None)

    m = (c2[1] - c1[1]) / run
    b = c1[1] - (m * c1[0])
    # try to be precise enough for grouping (rounding errors)
    return round(m, 10), round(b, 10)


def best_line_of_sight(asteroid_map):
    # convert the strip map to a list of asteroid coordinates
    coords = asteroid_map_to_coords(asteroid_map)

    # precompute a dict of (c1, c2) -> (m, b)
    sight_lines = {}
    for c1, c2 in itertools.combinations(coords, 2):
        sight_lines[coord_key(c1, c2)] = linear_eq(c1, c2)

    best = (None, -1)
    for monitor in coords:
        # group all asteroids along their line of sight
        monitor_lines = collections.defaultdict(list)
        for asteroid in coords:
            if monitor == asteroid:
                continue
            eq = sight_lines[coord_key(monitor, asteroid)]
            monitor_lines[eq].append(asteroid)

        # for each lines of sight, only count the visible ones
        visible = 0
        for (m, b), asteroids in monitor_lines.items():
            if m is None and (monitor[1] < asteroids[0][1] or
                              monitor[1] > asteroids[-1][1]):
                # vertical line should check y value
                visible += 1
            elif monitor[0] < asteroids[0][0] or monitor[0] > asteroids[-1][0]:
                # monitor is at the end of the line, so only one is visible
                visible += 1
            else:
                # monitor is somewhere in the middle, so potentially 2 are visible
                visible += min(2, len(asteroids))
        if visible > best[1]:
            best = (monitor, visible)
    return best


def spiral_order(asteroid_map, monitor):
    """
    Not quite spiral, but like a spiral laser that hits the first
    visible thing, and then on the next rotation anything behind what
    it hit the previous rotation.
    """
    coords = [(x, -1 * y) for x, y in asteroid_map_to_coords(asteroid_map)]
    monitor = (monitor[0], -1 * monitor[1])
    # 'right' is the right half (including top of vertical line)
    # 'left' is the left half (including bottom half of verticle line)
    sight_lines = {'right': collections.defaultdict(list),
                   'left': collections.defaultdict(list)}
    
    # build a list of satellites along the same sight lines,
    # left and right of the monitor
    for sat in coords:
        if sat == monitor:
            continue
        m, _ = linear_eq(monitor, sat)
        if (m is None and sat[1] > monitor[1]) or sat[0] > monitor[0]:
                sight_lines['right'][m].append(sat)
        else:
            sight_lines['left'][m].append(sat)

    # order the satellites on each sight line, closest to farthest from monitor
    distance = lambda coord: math.sqrt((monitor[0] - coord[0])**2 + (monitor[1] - coord[1])**2)
    for direction, line_maps in sight_lines.items():
        for slope, sats in line_maps.items():
            line_maps[slope] = sorted(sats, reverse=True, key=distance)

    all_coords = set(coords)
    all_coords.remove(monitor)
    direction = 'left'
    slope_sort = lambda x: float('inf') if x is None else x

    results = []
    while all_coords:
        direction = 'right' if direction == 'left' else 'left'
        # slope goes from undefined, to large, to small
        for m in sorted(sight_lines[direction], reverse=True, key=slope_sort):
            sats = sight_lines[direction][m]
            if sats:
                sat = sats.pop()
                results.append((sat[0], sat[1] * -1))
                all_coords.remove(sat)
    return results
                

if __name__ == '__main__':
    fp = './input/day10.txt'
    with open(fp) as f:
        asteroid_map = f.read()
    coordinate, detected = best_line_of_sight(asteroid_map)
    print('The best location is {}, where {} asteroids can be detected.'.format(coordinate, detected))


    laser_order = spiral_order(asteroid_map, coordinate)
    part2 = laser_order[199]
    print('Part 2 answer is {}'.format(part2[0] * 100 + part2[1]))
