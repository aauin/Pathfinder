import pygame
import button
import colorspy as color
from queue import PriorityQueue

SIZE = 800
EXTENDED_WINDOW = pygame.display.set_mode((SIZE, SIZE+100))
cropped = (0, 0, SIZE, SIZE+1)
WINDOW = EXTENDED_WINDOW.subsurface(cropped)
pygame.display.set_caption("A* Search Visualizer by Erwin Laird")

# load button images
search_img = pygame.image.load('search.png').convert_alpha()
generate_img = pygame.image.load('generate.png').convert_alpha()
clear_img = pygame.image.load('clear.png').convert_alpha()

# create button instances
search_button = button.Button(100, 820, search_img, .5)
generate_button = button.Button(330, 820, generate_img, .5)
clear_button = button.Button(580, 820, clear_img, .5)


class Cell:
    def __init__(self, row, column, size, rowcols):  #rowcols is the total number of rows, which is equal to the total number of columns
        self._row = row
        self._column = column
        self._x = row * size
        self._y = column * size
        self._color = color.black
        self._neighbors = []
        self._size = size
        self._rowcols = rowcols

    def get_position(self):
        return self._row, self._column

    def get_neighbors(self):
        return self._neighbors

    def is_barrier(self):
        return self._color == color.white

    def reset(self):
        self._color = color.black

    def make_closed(self):
        self._color = color.medium_blue

    def make_open(self):
        self._color = color.steel_blue

    def make_barrier(self):
        self._color = color.white

    def make_start(self):
        self._color = color.yellow

    def make_goal(self):
        self._color = color.red

    def make_path(self):
        self._color = color.orange

    def draw(self, window):
        pygame.draw.rect(window, self._color, (self._x, self._y, self._size, self._size))

    def update_neighbors(self, grid):
        self._neighbors = []
        if self._row > 0 and not grid[self._row - 1][self._column].is_barrier():  # up
            self._neighbors.append(grid[self._row - 1][self._column])
        if self._row < self._rowcols - 1 and not grid[self._row + 1][self._column].is_barrier():  # down
            self._neighbors.append(grid[self._row + 1][self._column])
        if self._column > 0 and not grid[self._row][self._column - 1].is_barrier():  # left
            self._neighbors.append(grid[self._row][self._column - 1])
        if self._column < self._rowcols - 1 and not grid[self._row][self._column + 1].is_barrier():  # right
            self._neighbors.append(grid[self._row][self._column + 1])

    def __lt__(self, other):
        return False


def h_score(point1, point2):  # heuristic distance from goal
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2 / 2


def trace_path(previous_cells, current, draw):
    current.make_goal()
    while current in previous_cells:
        current = previous_cells[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, goal):
    count = 0
    open_set = PriorityQueue()  # contains a heap of tuples (f_score, count, cell)
    open_set.put((0, count, start))
    open_set_hash = {start}  # keeps track of cells in open_set
    previous_cells = {}
    g_score = {cell: float('inf') for row in grid for cell in row}
    g_score[start] = 0  # distance from start
    f_score = {cell: float('inf') for row in grid for cell in row}
    f_score[start] = h_score(start.get_position(), goal.get_position())  # total calculated distance

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # gets the cell object only in the tuple
        open_set_hash.remove(current)

        if current == goal:
            trace_path(previous_cells, goal, draw)
            start.make_start()
            return True

        for neighbor in current.get_neighbors():
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                previous_cells[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h_score(neighbor.get_position(), goal.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()

    return False


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
    for row in range(rowcols+1):
        pygame.draw.line(window, color.gray, (0, row * gap), (size, row * gap))
    for column in range(rowcols):
        pygame.draw.line(window, color.gray, (column * gap, 0), (column * gap, size))


def draw(window, grid, rowcols, size):
    window.fill(color.black)
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
    goal = None
    is_running = True

    while is_running:
        draw(window, grid, rowcols, size)

        if search_button.draw(EXTENDED_WINDOW):
            print('START')
        if generate_button.draw(EXTENDED_WINDOW):
            print('EXIT')
        if clear_button.draw(EXTENDED_WINDOW):
            print('EXITfsdgdf')


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if pygame.mouse.get_pressed()[0]:  # left-click
                position = pygame.mouse.get_pos()
                if position[0] > SIZE or position[1] > SIZE:
                    break
                row, column = get_clicked_pos(position, rowcols, size)
                cell = grid[row][column]
                if start is None:
                    start = cell
                    start.make_start()
                elif goal is None:
                    goal = cell
                    goal.make_goal()
                elif cell != start and cell != goal:
                    cell.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # right-click
                position = pygame.mouse.get_pos()
                if position[0] > SIZE or position[1] > SIZE:
                    break
                row, column = get_clicked_pos(position, rowcols, size)
                cell = grid[row][column]
                cell.reset()
                if cell is start:
                    start = None
                if cell is goal:
                    goal = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and goal:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    algorithm(lambda: draw(window, grid, rowcols, size), grid, start, goal)

                if event.key == pygame.K_c:
                    start = None
                    goal = None
                    grid = make_grid(rowcols, size)

        pygame.display.update()

    pygame.quit()

main(WINDOW, SIZE)
