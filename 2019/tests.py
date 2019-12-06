import unittest

from aoc import day1_fuel_counter as d1
from aoc import day2_program_alarm as d2
from aoc import day3_distance as d3
from aoc import day4_password as d4
from aoc import day5_diagnostic as d5
from aoc import day6_orbit_checksum as d6

class AOCTest(unittest.TestCase):

    def test_d1_fuel_counter(self):
        self.assertEqual(d1.calculate_fuel(12), 2)
        self.assertEqual(d1.calculate_fuel(14), 2)
        self.assertEqual(d1.calculate_fuel(1969), 966)
        self.assertEqual(d1.calculate_fuel(100756), 50346)

    def test_d2_gravity_assist_program(self):
        self.assertEqual(d2.intcode([1,0,0,0,99]), [2,0,0,0,99])
        self.assertEqual(d2.intcode([2,3,0,3,99]), [2,3,0,6,99])
        self.assertEqual(d2.intcode([2,4,4,5,99,0]), [2,4,4,5,99,9801])
        self.assertEqual(d2.intcode([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])

    def test_d3_distance(self):
        wire1 = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
        wire2 = ['U62','R66','U55','R34','D71','R55','D58','R83']
        distance = 159
        self.assertEqual(d3.solve_min_distance(wire1, wire2), distance)
        steps = 610
        self.assertEqual(d3.solve_min_steps(wire1, wire2), steps)


        wire1 = ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51']
        wire2 = ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
        distance = 135
        self.assertEqual(d3.solve_min_distance(wire1, wire2), distance)
        steps = 410
        self.assertEqual(d3.solve_min_steps(wire1, wire2), steps)

    def test_d4_password_count(self):
        pass # TODO

    def test_d5_diagnostic_program(self):
        # jump: position / index mode
        code = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
        self.assertEqual(d5.diagnostic_program(code.copy(), 0), [0])
        self.assertEqual(d5.diagnostic_program(code.copy(), 42), [1])

        # jump: immediate / value mode
        code = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
        self.assertEqual(d5.diagnostic_program(code.copy(), 0), [0])
        self.assertEqual(d5.diagnostic_program(code.copy(), 42), [1])

    def test_d6_orbit_checksum(self):
        orbits = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G',
                  'G)H', 'D)I', 'E)J', 'J)K', 'K)L']
        self.assertEqual(d6.orbit_checksum(orbits), 42)
