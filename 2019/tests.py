import queue
import unittest

from aoc import day1_fuel_counter as d1
from aoc import day2_program_alarm as d2
from aoc import day3_distance as d3
from aoc import day4_password as d4
from aoc import day5_diagnostic as d5
from aoc import day6_orbit_checksum as d6
from aoc import day7_amp_circuit as d7

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

    def test_d5_intcode(self):
        def queue_helper(code, in_msg):
            in_q = queue.SimpleQueue()
            in_q.put(in_msg)
            out_q = queue.SimpleQueue()
            d5.intcode(code, in_q, out_q)
            out = []
            while not out_q.empty():
                out.append(out_q.get())
            return out

        # jump: position / index mode
        code = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
        out = queue_helper(code, 0)
        self.assertEqual(out, [0])
        out = queue_helper(code, 42)
        self.assertEqual(out, [1])

        # jump: immediate / value mode
        code = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
        out = queue_helper(code, 0)
        self.assertEqual(out, [0])
        out = queue_helper(code, 42)
        self.assertEqual(out, [1])

    def test_d6_orbit_checksum(self):
        orbits = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G',
                  'G)H', 'D)I', 'E)J', 'J)K', 'K)L']
        self.assertEqual(d6.orbit_checksum(orbits), 42)

        orbits = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G',
                  'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN']
        self.assertEqual(d6.min_orbital_transfers(orbits), 4)

    def test_d7_amp_circuit(self):
        # phase setting sequence 4,3,2,1,0
        code = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
        self.assertEqual(d7.max_thruster_signal(code), 43210)

        # phase setting sequence 0,1,2,3,4
        code = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,
                24,23,23,4,23,99,0,0]
        self.assertEqual(d7.max_thruster_signal(code), 54321)

        # phase setting sequence 1,0,4,3,2
        code = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
        self.assertEqual(d7.max_thruster_signal(code), 65210)

        # Testing with FEEDBACK
        # phase setting sequence 9,8,7,6,5):
        code = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
        self.assertEqual(d7.max_thruster_signal(code, feedback=True), 139629729)

        # phase setting sequence 9,7,8,5,6):
        code = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
                -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
                53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
        self.assertEqual(d7.max_thruster_signal(code, feedback=True), 18216)
