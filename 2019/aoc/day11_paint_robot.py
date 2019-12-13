from enum import IntEnum
from queue import SimpleQueue
from threading import Thread

from aoc import day5_diagnostic as d5


class Colors(IntEnum):
    BLACK = 0
    WHITE = 1

    @classmethod
    def default(cls):
        return cls.BLACK


class Turn(IntEnum):
    LEFT = 0
    RIGHT = 1


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class PaintRobot:
    def __init__(self, initial_color=Colors.default()):
        """
        The intial color is only for the *first* panel,
        not the default color for all panels.
        """
        self.direction = Direction.UP
        self.squares = {}
        self.pos = (0, 0)
        self.squares[self.pos] = initial_color
        self._mailman = None
        self._inbox = None
        self._outbox = None

    def print_hull(self):
        coord = self.pos
        min_x, min_y = self.pos[0], self.pos[1]
        max_x, max_y = self.pos[0], self.pos[1]

        for x, y in self.squares:
            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x, max_x)
            max_y = max(y, max_y)

        for row in range(max_y, min_y-1, -1):
            rowstr = ''
            for panel in range(min_x, max_x+1):
                color = self._color_at((panel, row))
                rowstr += '\u2B1C' if color == Colors.WHITE else '\u2B1B'
            print(rowstr)

    def _color_at(self, pos):
        if self.squares.get(pos) is None:
            return Colors.default()
        return self.squares[pos]

    def current_color(self):
        return self._color_at(self.pos)

    def paint_panel(self, color):
        self.squares[self.pos] = color

    def turn_and_move(self, turn):
        if turn == Turn.LEFT:
            if self.direction == 0:
                self.direction = 3
            else:
                self.direction -= 1
        elif turn == Turn.RIGHT:
            if self.direction == 3:
                self.direction = 0
            else:
                self.direction += 1

        x, y = 0, 0
        if self.direction == Direction.UP:
            y = 1
        elif self.direction == Direction.RIGHT:
            x = 1
        elif self.direction == Direction.DOWN:
            y = -1
        elif self.direction == Direction.LEFT:
            x = -1

        self.pos = (self.pos[0] + x, self.pos[1] + y)
        if self.pos not in self.squares:
            self.squares[self.pos] = None

    def painted(self):
        return [pos for pos, color in self.squares.items() if color is not None]

    def _postoffice(self):
        """
        Should not be called directly, but by start. Assumes setup is done.
        Input should be the color the robot is on.
        Two outputs: 1) Color to paint the panel it is on 2) 90 deg turn direction
        Move forward 1 space after it turns
        """
        while True:
            self._outbox.put(self.current_color())
            msg = self._inbox.get()
            if msg is None:
                break
            self.paint_panel(msg)
            msg = self._inbox.get()
            if msg is None:
                break
            self.turn_and_move(msg)

    def start(self):
        """
        Returns the robots inbox and outbox queues, and starts a background
        thread to process them. Call stop() to cleanly shutdown.
        """
        self._inbox = SimpleQueue()
        self._outbox = SimpleQueue()
        self._mailman = Thread(target=self._postoffice)
        self._mailman.start()
        return (self._inbox, self._outbox)

    def stop(self):
        self._inbox.put(None)
        self._mailman.join()


def mr_robot(code, initial_color=None):
    robot = PaintRobot(initial_color=initial_color)
    inbox, outbox = robot.start()
    d5.intcode(code, outbox, inbox)
    robot.stop()
    return robot

if __name__ == '__main__':
    fp = './input/day11.txt'
    with open(fp) as f:
        code = [int(x) for x in f.read().strip().split(',')]
    print('Unique panels painted: {}'.format(len(mr_robot(code).painted())))
    print()
    robot = mr_robot(code, initial_color=Colors.WHITE)
    robot.print_hull()
