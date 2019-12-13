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
    """Guarantees same order no matter the order of c1, c2."""
    return (c1, c2) if c1 <= c2 else (c2, c1)


def linear_eq(c1, c2):
    """
    Return the slope and y-intercept for the two given points.
    Undefined slope is float('inf'), and undefined y-intercept is None.
    e.g. m=3.0 b=1.0 -> (3.0, 1.0)

    Values are rounded to the 10th decimal place.
    """
    run = c2[0] - c1[0]
    if run == 0:
        return (float('inf'), None)

    m = (c2[1] - c1[1]) / run
    b = c1[1] - (m * c1[0])
    # try to be precise enough for grouping (rounding errors)
    return (round(m, 10), round(b, 10))


def best_line_of_sight(asteroid_map):
    # convert the strip map to a list of asteroid coordinates
    coords = asteroid_map_to_coords(asteroid_map)

    # precompute a dict of (c1, c2) -> slope
    slopes = {}
    for c1, c2 in itertools.combinations(coords, 2):
        slopes[coord_key(c1, c2)] = linear_eq(c1, c2)[0]

    best = (None, -1)
    for station in coords:
        # group all asteroids along their line of sight
        sight_lines = collections.defaultdict(list)
        for asteroid in coords:
            if station == asteroid:
                continue
            slope = slopes[coord_key(station, asteroid)]
            sight_lines[slope].append(asteroid)

        # for each lines of sight, only count the visible ones
        visible = 0
        for slope, asteroids in sight_lines.items():
            if math.isinf(slope) and (station[1] < asteroids[0][1] or
                                      station[1] > asteroids[-1][1]):
                # station is at the end of a vertical line
                visible += 1
            elif station[0] < asteroids[0][0] or station[0] > asteroids[-1][0]:
                # station is at the end of the line, so only one is visible
                visible += 1
            else:
                # station is somewhere in the middle, so potentially 2 are visible
                visible += min(2, len(asteroids))
        if visible > best[1]:
            best = (station, visible)
    return best


def laser_order(asteroid_map, station):
    """
    Spiral laser on station that starts pointing up, and rotates clockwise.
    It hits the first visible asteroid in the line of sight, and then on the
    next rotation anything behind what it hit the previous rotation.
    """
    # converting y coord to be in the Cartesian grid b/c it's easier
    # for me to think about it
    coords = [(x, -1 * y) for x, y in asteroid_map_to_coords(asteroid_map)]
    station = (station[0], -1 * station[1])

    # split the asteroids between two halves because the laser only
    # points in one direction from the station
    sight_lines = {'right': collections.defaultdict(list),
                   'left': collections.defaultdict(list)}
    
    # build a list of asteroids along the same sight lines,
    # left and right of the station
    for asteroid in coords:
        if asteroid == station:
            continue
        slope, _ = linear_eq(station, asteroid)
        if ((math.isinf(slope) and asteroid[1] > station[1]) or
            asteroid[0] > station[0]):
                sight_lines['right'][slope].append(asteroid)
        else:
            sight_lines['left'][slope].append(asteroid)

    # order the asteroids on each sight line,
    # ordered closest to farthest from station
    distance = lambda coord: math.sqrt((station[0] - coord[0])**2 +
                                       (station[1] - coord[1])**2)
    for direction, line_maps in sight_lines.items():
        for slope, asteroids in line_maps.items():
            line_maps[slope] = sorted(asteroids, key=distance, reverse=True)

    all_coords = set(coords)
    all_coords.remove(station)
    direction = 'left'
    results = []
    while all_coords:
        direction = 'right' if direction == 'left' else 'left'
        # to rotate clockwise: slope goes from undefined, to large, to small
        for slope in sorted(sight_lines[direction], reverse=True):
            asteroids = sight_lines[direction][slope]
            if asteroids:
                asteroid = asteroids.pop()
                # translate it back to the flipped y coordinates
                results.append((asteroid[0], asteroid[1] * -1))
                all_coords.remove(asteroid)
    return results
                

if __name__ == '__main__':
    fp = './input/day10.txt'
    with open(fp) as f:
        asteroid_map = f.read()
    station, detected = best_line_of_sight(asteroid_map)
    print('The best location is {}, where {} asteroids can be detected.'.format(station, detected))


    laser_order = laser_order(asteroid_map, station)
    part2 = laser_order[199]
    print('Part 2 answer is {}'.format(part2[0] * 100 + part2[1]))
