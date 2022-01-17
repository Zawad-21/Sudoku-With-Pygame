from math import sqrt
import math
import random
import re
import pygame
pygame.font.init()

WIN_WIDTH = 900
BOX_WIDTH = 100
CELL_COUNT = 81
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))
pygame.display.set_caption('Sudoku')

WHITE = (245, 245, 245)
BLACK = (10, 10, 10)
BLUE = (25, 25, 112)
GREEN = (0, 100, 0)
RED = (245, 0, 0)

FONT = pygame.font.Font('freesansbold.ttf', 50)

LINE_THICKNESS = 2

WIN.fill(WHITE)

RUNNING = True


class Cell:
    def __init__(self, x, y, width, total_rows):
        self.width = width
        self.total_rows = total_rows
        self.x = int(x * 100)
        self.y = int(y * 100)
        self.number = ''
        self.pre_added = False
        self.text_color = BLUE

    def write_num(self):
        num = FONT.render(self.number, True, self.text_color)
        WIN.blit(num, (self.x + 37, self.y + 37))

    def erase_num(self):
        pygame.draw.rect(WIN, WHITE, (self.x + 7, self.y + 7,
                         self.width - 14, self.width - 14))

    def alert_player(self):
        pygame.draw.rect(WIN, RED, (self.x + 5, self.y + 5,
                         self.width - 10, self.width - 10), 2)

    def remove_alert(self):
        pygame.draw.rect(WIN, WHITE, (self.x + 5, self.y + 5,
                         self.width - 10, self.width - 10), 2)


def make_grid(cell_count, box_width):
    grid = []
    total_rows = int(sqrt(cell_count))
    gap = box_width
    for i in range(cell_count):
        cell = Cell(i % total_rows, math.floor(
            i / total_rows), gap, total_rows)
        grid.append(cell)
    fill_clue_cells(grid)

    return grid


def make_groups():
    groups = []
    start = 0
    end = 3
    for i in range(9):
        groups.append([])
        for j in range(start, end):
            indices = [j, j+9, j+9*2]
            for index in indices:
                groups[i].append(index)
        if end != 9 and end != 36:
            start = start + 3
            end = end + 3
        else:
            start = start + 21
            end = end + 21

    return groups


def generate_rand_cell_indices():
    rand_cell_indices = []
    while len(rand_cell_indices) < 17:
        random_number = random.randint(0, 80)
        if random_number not in rand_cell_indices:
            rand_cell_indices.append(random_number)

    return rand_cell_indices


def fill_clue_cells(grid):
    grid = grid
    rand_cell_indices = generate_rand_cell_indices()
    for i in rand_cell_indices:
        random_number = int(random.random() * 9)
        cell = grid[i]
        cell.number = str(random_number)
        cell.pre_added = True
        cell.text_color = BLUE
        cell.write_num()


def get_clicked_index(pos):
    x, y = pos
    column = math.floor(x / 100)
    row = math.floor(y / 100)

    return(column + row * 9)


def draw_grid_borders(win, total_rows, box_width, win_width):
    row_gap = box_width
    for i in range(total_rows):
        pygame.draw.line(win, BLACK, (0, i * row_gap),
                         (win_width, i * row_gap), LINE_THICKNESS)
        for j in range(total_rows):
            pygame.draw.line(win, BLACK, (j * row_gap, 0),
                             (j * row_gap, win_width), LINE_THICKNESS)

    for i in range(total_rows//3):
        pygame.draw.line(win, BLACK, (0, i * row_gap * 3),
                         (win_width, i * row_gap * 3), LINE_THICKNESS * 2)
        for j in range(total_rows):
            pygame.draw.line(win, BLACK, (j * row_gap * 3, 0),
                             (j * row_gap * 3, win_width), LINE_THICKNESS * 2)


def draw_window():
    pygame.display.update()


def main(state):
    grid = make_grid(CELL_COUNT, BOX_WIDTH)
    draw_grid_borders(WIN, int(sqrt(CELL_COUNT)), BOX_WIDTH, WIN_WIDTH)
    typing = False
    cell = None
    prev_cell = None
    draw_window()
    make_groups()
    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False

            if pygame.mouse.get_pressed()[0]:
                if prev_cell and not prev_cell.pre_added:
                    cell = prev_cell
                    cell.remove_alert()
                typing = True
                pos = pygame.mouse.get_pos()
                grid_index = get_clicked_index(pos)
                cell = grid[grid_index]
                if not cell.pre_added:
                    cell.alert_player()
                draw_window()
                prev_cell = cell

            if typing and not cell.pre_added and event.type == pygame.KEYDOWN:
                player_input = pygame.key.name(event.key)
                print(player_input)
                input_num = re.findall(r'\d+', player_input)
                if input_num:
                    cell.erase_num()
                    cell.number = str(input_num[0])
                    cell.text_color = GREEN
                    cell.write_num()
                elif event.key == pygame.K_BACKSPACE:
                    cell.erase_num()

                draw_window()


main(RUNNING)
