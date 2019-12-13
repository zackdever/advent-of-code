import collections
import itertools


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
        # group all asteroids along their line of site
        monitor_lines = collections.defaultdict(list)
        for asteroid in coords:
            if monitor == asteroid:
                continue
            eq = sight_lines[coord_key(monitor, asteroid)]
            monitor_lines[eq].append(asteroid)

        # for each lines of site, only count the visible ones
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


if __name__ == '__main__':
    fp = './input/day10.txt'
    with open(fp) as f:
        asteroid_map = f.read()
    coordinate, detected = best_line_of_sight(asteroid_map)
    print('The best location is {}, where {} asteroids can be detected.'.format(coordinate, detected))
