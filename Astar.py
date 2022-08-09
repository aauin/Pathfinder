import pygame
import colorspy as color
import math
from queue import PriorityQueue

SIZE = 800
WINDOW = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("A* Search Visualizer")


class Cell:
    def __init__(self, row, column, size, rowcols):  #rowcols is the total number of rows, which is equal to the total number of columns
        self._row = row
        self._column = column
        self._x = row * size
        self._y = column * size
        self._color = color.white
        self._neighbors = []
        self._size = size
        self._rowcols = rowcols

    def get_position(self):
        return self._row, self._column

    def is_occupied(self):
        return self._color == color.red

    def is_vacant(self):
        return self._color == color.green

    def is_barrier(self):
        return self._color == color.black

    def is_start(self):
        return self._color == color.orange

    def is_end(self):
        return self._color == color.turquoise

    def reset(self):
        self._color = color.white

    def make_occupied(self):
        self._color = color.red

    def make_vacant(self):
        self._color = color.green

    def make_barrier(self):
        self._color = color.black

    def make_start(self):
        self._color = color.orange

    def make_end(self):
        self._color = color.turquoise

    def make_path(self):
        self._color = color.purple

    def draw(self, window):
        pygame.draw.rect(window, self._color, (self._x, self._y, self._size, self._size))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False


def manhattan_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rowcols, size):
    grid = []
    gap = size // rowcols
    for row in range(rowcols):
        grid.append([])
        for column in range(rowcols):
            cell = Cell(row, column, gap, rowcols)
            grid[row].append(cell)
    return grid


def draw_grid(window, rowcols, size):
    gap = size // rowcols
    for row in range(rowcols):
        pygame.draw.line(window, color.gray, (0, row * gap), (size, row * gap))
        for column in range(rowcols):
            pygame.draw.line(window, color.gray, (column * gap, 0), (column * gap, size))


def draw(window, grid, rowcols, size):
    window.fill(color.white)
    for row in grid:
        for cell in row:
            cell.draw(window)
    draw_grid(window, rowcols, size)
    pygame.display.update()


def get_clicked_pos(position, rowcols, size):
    gap = size // rowcols
    y, x = position
    row = y // gap
    column = x // gap
    return row, column


def main(window, size):
    rowcols = 50
    grid = make_grid(rowcols, size)
    start = None
    end = None
    is_running = True
    is_started = False

    while is_running:
        draw(window, grid, rowcols, size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if is_started:
                continue

            if pygame.mouse.get_pressed()[0]:  # left-click
                position = pygame.mouse.get_pos()
                row, column = get_clicked_pos(position, rowcols, size)
                cell = grid[row][column]
                if start is None:
                    start = cell
                    start.make_start()
                elif end is None:
                    end = cell
                    end.make_end()
                elif cell != start and cell != end:
                    cell.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # right-click
                position = pygame.mouse.get_pos()
                row, column = get_clicked_pos(position, rowcols, size)
                cell = grid[row][column]
                if cell is start:
                    start = None
                elif cell is end:
                    end = None
                cell.reset()

    pygame.quit()


main(WINDOW, SIZE)