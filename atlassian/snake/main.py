
import collections
from enum import Enum


class Direction(Enum):

    UP = "UP"
    DOWN = "DOWN"
    RIGHT = "RIGHT"
    LEFT = "LEFT"


class SnakeGame:
    def __init__(self, size, position, row, column) -> None:
        self.row = row
        self.column = column
        self.board = [[" " for __ in range(column)] for __ in range(row)]
        self.size = size
        self.snake_position = set(position)
        self.snake = collections.deque(position)
        self.current_direction = Direction.RIGHT
        self.game_over = False
        self._refill_snake()
        self.moves = {
            Direction.UP : (-1, 0),
            Direction.DOWN : (1, 0),
            Direction.RIGHT : (0, 1),
            Direction.LEFT : (0, -1)
        }
        pass
    
    def _refill_snake(self):
        for i in range(self.row):
            for j in range(self.column):
                if (i,j) in self.snake_position:
                    self.board[i][j] = "#"
    def display(self):
        for i in range(self.row):
            print(self.board[i])
            print("\n")
    def move_snake(self, direction :Direction):
        pass
    def is_game_over(self):
        return self.game_over


initial_size = 3
initial_position = [(0,0), (0,1), (0,2)]
game = SnakeGame(initial_size, initial_position, 5, 5)
game.display()
