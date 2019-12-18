import queue
import unittest

from aoc import day1_fuel_counter as d1
from aoc import day2_program_alarm as d2
from aoc import day3_distance as d3
from aoc import day4_password as d4
from aoc import day5_diagnostic as d5
from aoc import day6_orbit_checksum as d6
from aoc import day7_amp_circuit as d7
from aoc import day8_space_image_format as d8
from aoc import day10_monitoring_station as d10
from aoc import day11_paint_robot as d11
from aoc import day12_drops_of_jupiter as d12


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

    @unittest.skip('These are slow, renable if messing with intcode')
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

    def test_d8_space_image_format(self):
        code = '123456789012'
        width, height = 3, 2
        expected = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]]
        self.assertEqual(d8.build_layers(code, width, height), expected)

        code = '0222112222120000'
        width, height = 2, 2
        layers = d8.build_layers(code, width, height)
        self.assertEqual(d8.flatten_layers(layers), [[0, 1], [1, 0]])

    def test_d9_sensor_boost(self):
        code = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        output = d5.intcode_helper(code)
        self.assertEqual(output, code)

        code = [1102,34915192,34915192,7,4,7,99,0]
        output = d5.intcode_helper(code)
        self.assertEqual(len(output), 1)
        self.assertEqual(len(str(output[0])), 16)

        code = [104,1125899906842624,99]
        output = d5.intcode_helper(code)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], 1125899906842624)

    def test_d10_monitoring_station(self):
        asteroid_map = '.#..#\n' + \
                       '.....\n' + \
                       '#####\n' + \
                       '....#\n' + \
                       '...##\n'
        coordinate, detected = d10.best_line_of_sight(asteroid_map)
        self.assertEqual(coordinate, (3, 4))
        self.assertEqual(detected, 8)

        asteroid_map = '......#.#.\n' + \
                       '#..#.#....\n' + \
                       '..#######.\n' + \
                       '.#.#.###..\n' + \
                       '.#..#.....\n' + \
                       '..#....#.#\n' + \
                       '#..#....#.\n' + \
                       '.##.#..###\n' + \
                       '##...#..#.\n' + \
                       '.#....####\n'
        coordinate, detected = d10.best_line_of_sight(asteroid_map)
        self.assertEqual(coordinate, (5, 8))
        self.assertEqual(detected, 33)

        asteroid_map = '#.#...#.#.\n' + \
                       '.###....#.\n' + \
                       '.#....#...\n' + \
                       '##.#.#.#.#\n' + \
                       '....#.#.#.\n' + \
                       '.##..###.#\n' + \
                       '..#...##..\n' + \
                       '..##....##\n' + \
                       '......#...\n' + \
                       '.####.###.\n'
        coordinate, detected = d10.best_line_of_sight(asteroid_map)
        self.assertEqual(coordinate, (1, 2))
        self.assertEqual(detected, 35)

        asteroid_map = '.#..#..###\n' + \
                       '####.###.#\n' + \
                       '....###.#.\n' + \
                       '..###.##.#\n' + \
                       '##.##.#.#.\n' + \
                       '....###..#\n' + \
                       '..#.#..#.#\n' + \
                       '#..#.#.###\n' + \
                       '.##...##.#\n' + \
                       '.....#.#..\n'
        coordinate, detected = d10.best_line_of_sight(asteroid_map)
        self.assertEqual(coordinate, (6, 3))
        self.assertEqual(detected, 41)

        asteroid_map = '.#..##.###...#######\n' + \
                       '##.############..##.\n' + \
                       '.#.######.########.#\n' + \
                       '.###.#######.####.#.\n' + \
                       '#####.##.#.##.###.##\n' + \
                       '..#####..#.#########\n' + \
                       '####################\n' + \
                       '#.####....###.#.#.##\n' + \
                       '##.#################\n' + \
                       '#####.##.###..####..\n' + \
                       '..######..##.#######\n' + \
                       '####.##.####...##..#\n' + \
                       '.#####..#.######.###\n' + \
                       '##...#.##########...\n' + \
                       '#.##########.#######\n' + \
                       '.####.#.###.###.#.##\n' + \
                       '....##.##.###..#####\n' + \
                       '.#.#.###########.###\n' + \
                       '#.#.#.#####.####.###\n' + \
                       '###.##.####.##.#..##\n'
        coordinate, detected = d10.best_line_of_sight(asteroid_map)
        self.assertEqual(coordinate, (11, 13))
        self.assertEqual(detected, 210)

        results = d10.laser_order(asteroid_map, coordinate)
        self.assertEqual(len(results), 299)
        self.assertEqual(results[0], (11,12))
        self.assertEqual(results[1], (12,1))
        self.assertEqual(results[2], (12,2))
        self.assertEqual(results[9], (12,8))
        self.assertEqual(results[19], (16,0))
        self.assertEqual(results[49], (16,9))
        self.assertEqual(results[99], (10,16))
        self.assertEqual(results[198], (9,6))
        self.assertEqual(results[199], (8,2))
        self.assertEqual(results[200], (10,9))
        self.assertEqual(results[298], (11,1))

    def test_d11_painting_robot(self):
        robot = d11.PaintRobot() 
        inbox, outbox = robot.start()
        for x in [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0]:
            inbox.put(x)
        robot.stop()
        self.assertEqual(len(robot.painted()), 6)

    def test_d12_jupiters_moons(self):
        lines = ['<x=-1, y=0, z=2>', '<x=2, y=-10, z=-7>',
                 '<x=4, y=-8, z=8>', '<x=3, y=5, z=-1>']
        positions = d12.parse(lines)
        jupiter = d12.Jupiter(positions)
        self.assertEqual(jupiter.time, 0)
        self.assertEqual(jupiter.moons[0]['pos'], {'x': -1, 'y': 0, 'z': 2})
        self.assertEqual(jupiter.moons[0]['vel'], {'x': 0, 'y': 0, 'z': 0})

        jupiter.advance_time(1)
        self.assertEqual(jupiter.time, 1)
        self.assertEqual(jupiter.moons[0]['pos'], {'x': 2, 'y': -1, 'z': 1})
        self.assertEqual(jupiter.moons[0]['vel'], {'x': 3, 'y': -1, 'z': -1})

        jupiter.advance_time(9)
        self.assertEqual(jupiter.time, 10)
        self.assertEqual(jupiter.energy(), 179)
        self.assertEqual(jupiter.moons[0]['pos'], {'x': 2, 'y': 1, 'z': -3})
        self.assertEqual(jupiter.moons[0]['vel'], {'x': -3, 'y': -2, 'z': 1})
