import math
import unittest


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


class FuelCounterTest(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(calculate_fuel(12), 2)
        self.assertEqual(calculate_fuel(14), 2)
        self.assertEqual(calculate_fuel(1969), 966)
        self.assertEqual(calculate_fuel(100756), 50346)

if __name__ == '__main__':
    f = 'input.txt'
    print('Reading from {}'.format(f))
    print('Total fuel sum: {}'.format(sum_fuel(f)))
