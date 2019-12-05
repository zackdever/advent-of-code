import math


def calculate_fuel(mass):
    fuel = math.floor(mass / 3) - 2
    if fuel <= 0:
        return 0
    return fuel + calculate_fuel(fuel)

def sum_fuel(mass_file):
    fuelsum = 0
    with open(mass_file) as f:
        for l in f:
            fuelsum += calculate_fuel(int(l.strip()))
    return fuelsum


if __name__ == '__main__':
    f = './input/day1.txt'
    print('Reading from {}'.format(f))
    print('Total fuel sum: {}'.format(sum_fuel(f)))
