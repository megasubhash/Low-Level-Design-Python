from collections import deque


class SnakeGame:
    def __init__(self, row, column, current_snake, food) -> None:
        self.row = row
        self.column = column
        self.food = food
        self.grid = [["." for __ in range(column)] for __ in range(row)]
        # self.snake = 
        # print(self.grid)
        self.snake_size = len(current_snake)
        self.snake = deque(current_snake)
        self.snake_position = set(current_snake)
        self._fill_snake()
        self.directions = {
            "R": (0, 1),
            "D": (1, 0),
            "L": (0, -1),
            "U": (-1, 0),
        }
        self.game_over = False
        self.move_count = 0
        pass
    
    

    def _fill_snake(self):
        self.grid = [["." for __ in range(self.column)] for __ in range(self.row)]
        for row, column in self.snake:
            self.grid[row][column] = "SNAKE"
    def moveSnake(self, direction):
        row, column = self.directions[direction]

        current_head = self.snake[-1]
        if not (0 <= current_head[0] + row < self.row and 0 <= current_head[1] + column < self.column):
            self.game_over = True
            return
        if (current_head[0]+row, current_head[1] + column) in self.snake_position:
            self.game_over = True
            return
        
            
        food_found = False
        if (current_head[0]+row, current_head[1] + column) in self.food:
            food_found = True
            self.food.remove((current_head[0]+row, current_head[1] + column))
        self.snake.append((current_head[0]+row, current_head[1] + column))
        self.snake_position.add((current_head[0]+row, current_head[1] + column))
        self.move_count += 1
        if self.move_count % 5 != 0 and not food_found:
            emitted_row, emitted_column = self.snake.popleft()
            self.grid[emitted_row][emitted_column] = "."
            self.snake_position.remove((emitted_row, emitted_column))
            
        self._fill_snake()
        self.display()
        pass

    def isGameOver(self):
        return self.game_over, self.move_count
        pass
    def display(self):
        # print(self.snake_size)
        for i in range(self.row):
            print(self.grid[i])
            print("\n")
                

current_snake = [(0, 0), (0, 1), (0, 2)]
food = set([(1,2)])
game = SnakeGame(6,6, current_snake, food)
# game.display()
game.moveSnake("D")
print("Game Over", game.isGameOver())
game.moveSnake("D")
print("Game Over", game.isGameOver())

game.moveSnake("D")
print("Game Over", game.isGameOver())

game.moveSnake("L")
print("Game Over", game.isGameOver())
game.moveSnake("L")
print("Game Over", game.isGameOver())
game.moveSnake("U")
print("Game Over", game.isGameOver())
# game.moveSnake("R")
# print("Game Over", game.isGameOver())
# game.moveSnake("D")
# print("Game Over", game.isGameOver())
