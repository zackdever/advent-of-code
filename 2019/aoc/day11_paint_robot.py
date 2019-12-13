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
    def __init__(self):
        self.direction = Direction.UP
        self.squares = {}
        self.pos = (0, 0)
        self.squares[self.pos] = None
        self._mailman = None
        self._inbox = None
        self._outbox = None

    def current_color(self):
        if self.squares[self.pos] is None:
            return Colors.default()
        return self.squares[self.pos]

    def paint(self, color):
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
        Two outputs: 1) Color to paint the square it is on 2) 90 deg turn direction
        Move forward 1 space after it turns
        """
        while True:
            self._outbox.put(self.current_color())
            msg = self._inbox.get()
            if msg is None:
                break
            self.paint(msg)
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


def mr_robot(code):
    """
    Return the count of unique panels it painted.
    """
    robot = PaintRobot()
    inbox, outbox = robot.start()
    d5.intcode(code, outbox, inbox)
    robot.stop()
    return len(robot.painted())

if __name__ == '__main__':
    fp = './input/day11.txt'
    with open(fp) as f:
        code = [int(x) for x in f.read().strip().split(',')]
    print('Unique panels painted: {}'.format(mr_robot(code)))
