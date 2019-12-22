from typing import List, Tuple

from random import randint

import mas

import pygame
from pygame.locals import *

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 5) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        listik = mas.bad_mas  # self.create_grid(randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid(listik)
            self.draw_lines()
            listik = self.get_next_generation(listik)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        """
        ourgrid = List[List(int)]
        if randomize == 0:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    ourgrid[i][j] = 0
        else:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    ourgrid[i][j] = randint(0, 1)
        return ourgrid
        """
        if randomize:
            return [[randint(0, 1) for x in range(self.cell_width)] for y in range(self.cell_height)]
        else:
            return [[0 for x in range(self.cell_width)] for y in range(self.cell_height)]
            # return get_next_generation()

    def get_next_generation(self, grid: Grid) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_mas = []
        for y in range(self.cell_height):
            new_mas.append([])
            for x in range(self.cell_width):
                if 2 <= self.get_neighbours(grid, [y, x]) <= 3:
                    new_mas[y].append(1)
                else:
                    new_mas[y].append(0)
        return new_mas

    def get_neighbours(self, grid: Grid, cell: Cell) -> int:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """

        # В этой функции я возвращаю количество соседних клеток, котрые живи,
        # чтобы не делать лишних действий и сразу, используя функцию, определить,
        # жива ли клетка в следующем поколении

        """
        if 0 < cell[0] < self.cell_height and 0 < cell[1] < self.cell_width:
            return [[cell[0] + 1, cell[1] - 1], [cell[0], cell[1] - 1], [cell[0] - 1, cell[1] - 1],
                    [cell[0] - 1, cell[1]], [cell[0] - 1, cell[1] + 1], [cell[0], cell[1] + 1],
                    [cell[0] + 1, cell[1] + 1], [cell[0] + 1, cell[1]]]
        """
        k = 0
        if cell[1] - 1 >= 0:
            k += grid[cell[0]][cell[1] - 1]
        if cell[1] - 1 >= 0 and cell[0] - 1 >= 0:
            k += grid[cell[0] - 1][cell[1] - 1]
        if cell[0] - 1 >= 0:
            k += grid[cell[0] - 1][cell[1]]
        if cell[1] + 1 < self.cell_width and cell[0] - 1 >= 0:
            k += grid[cell[0] - 1][cell[1] + 1]
        if cell[1] + 1 < self.cell_width:
            k += grid[cell[0]][cell[1] + 1]
        if cell[1] + 1 < self.cell_width and cell[0] + 1 < self.cell_height:
            k += grid[cell[0] + 1][cell[1] + 1]
        if cell[0] + 1 < self.cell_height:
            k += grid[cell[0] + 1][cell[1]]
        if cell[1] - 1 >= 0 and cell[0] + 1 < self.cell_height:
            k += grid[cell[0] + 1][cell[1] - 1]

        return k

    def draw_grid(self, grid: Grid) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if grid[i][j]:
                    pygame.draw.rect(self.screen, pygame.Color('hotpink'),
                        (self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                        (self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size))


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
