from settings import *
import pygame
pygame.init()


class Cell:
    def __init__(self, app, row, col, width, height, total_rows, total_cols):
        self.row = row
        self.col = col
        self.prev = WHITE
        self.x = (col * width) + GS_X
        self.y = row * height
        self.color = WHITE
        self.width = width
        self.height = height
        self.neighbors = []
        self.total_rows = total_rows
        self.total_cols = total_cols

    def is_closed(self):
        return (self.color == CRIMSON)

    def is_open(self):
        return (self.color == GREEN)

    def is_obstacle(self):
        return (self.color == BLACK)

    def is_start(self):
        return (self.color == ORANGE)

    def is_end(self):
        return (self.color == BLUE)

    def reset(self):
        self.color = WHITE
        self.prev = WHITE

    def make_closed(self):
        self.color = CRIMSON

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
        self.prev = WHITE

    def make_end(self):
        self.prev = self.color
        self.color = BLUE

    def make_path(self):
        self.color = YELLOW

    def revert(self):
        self.color = self.prev

    def make_start(self):
        self.prev = self.color
        self.color = ORANGE

    def __lt__(self, other):
        return False

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))
    # To find the neighbors of current cell

    def update_neighbors(self, grid):
        self.neighbors = []
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        for i in range(4):
            nrow = self.row + dx[i]
            ncol = self.col + dy[i]
            if nrow >= 0 and ncol >= 0 and nrow < self.total_rows and ncol < self.total_cols and not grid[nrow][ncol].is_obstacle():
                self.neighbors.append(grid[nrow][ncol])

    def heuristic(self, other):
        x1, y1 = self.row, self.col
        x2, y2 = other.row, other.col
        return abs(x1 - y1) + abs(x2 - y2)

# Grid contains N*M cell objects


class Grid:
    def __init__(self, app, rows=ROWS, cols=COLS, width=WIDTH, height=HEIGHT):
        self.app = app
        self.rows = rows
        self.cols = cols
        self.width = width
        self.cell_width = (width - GS_X) // cols
        self.cell_height = height // rows
        self.grid = []
    # Initialize a 2D grid

    def make_grid(self):
        self.grid = []
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                cell = Cell(self.app, i, j, self.cell_width,
                            self.cell_height, self.rows, self.cols)
                self.grid[i].append(cell)
    # Draws rows and cols on pygame window

    def draw_grid(self):
        for i in range(self.rows):
            pygame.draw.line(self.app.WIN, GREY, (GS_X, i * self.cell_height),
                             (WIDTH, i * self.cell_height), LINE_WIDTH)
            for j in range(self.cols):
                pygame.draw.line(self.app.WIN, GREY, (GS_X + j * self.cell_width, 0),
                                 (GS_X + j * self.cell_width, HEIGHT), LINE_WIDTH)
    # Draws border of each cell

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw(self.app.WIN)
        self.draw_grid()

    def get_row_col(self, pos):
        x, y = pos
        row = y // self.cell_height
        col = (x - GS_X) // self.cell_width
        if(row < self.rows and col < self.cols and row >= 0 and col >= 0):
            return row, col
        else:
            return -1, -1

    def get_cell(self, row, col):
        return self.grid[row][col]
    # Updates neighbors of all cells in the grid

    def set_neighbors(self):
        for row in self.grid:
            for cell in row:
                cell.update_neighbors(self.grid)

    def set_default(self):
        self.app.start = self.grid[ROWS // 2][COLS // 2 - 10]
        self.app.start.make_start()
        self.app.end = self.grid[ROWS // 2][COLS // 2 + 10]
        self.app.end.make_end()
