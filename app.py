from settings import *
from grid_class import *
from buttons_class import *
from Algorithms import *
import pygame
import os
import sys
pygame.init()


class App:
    def __init__(self):
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.state = "main menu"
        self.algorithm = ""
        self.clock = pygame.time.Clock()
        self.mouse_drag = 0
        self.Left_button = False
        self.right_button = False
        self.start = None
        self.end = None
        self.grid = Grid(self, ROWS, COLS, WIDTH, HEIGHT)
        self.grid.make_grid()
        pygame.display.set_caption("Path Finding Visualizer")
        # Main Menu Buttons
        self.bfs_button = Buttons(
            self, CYAN, 150, MAIN_BUTTON_Y_POS, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGTH, 'Breadth-First-Search'
        )
        self.dfs_button = Buttons(
            self, CYAN, 400, MAIN_BUTTON_Y_POS, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGTH, 'Depth-First-Search'
        )
        self.astar_button = Buttons(
            self, CYAN, 650, MAIN_BUTTON_Y_POS, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGTH, 'A-star-Search'
        )
        self.dijkstra_button = Buttons(
            self, CYAN, 900, MAIN_BUTTON_Y_POS, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGTH, 'Dijkstra Search'
        )
        self.bidirectional_button = Buttons(
            self, CYAN, 1150, MAIN_BUTTON_Y_POS, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGTH, 'Bidirectional Search'
        )
        self.start_button = Buttons(
            self, CYAN, 20, GRID_BUTTON_Y, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGTH, 'Start Node'
        )
        # Grid Menu Buttons
        self.start_button = Buttons(
            self, GREY, 20, GRID_BUTTON_Y, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGTH, 'Start'
        )
        self.end_button = Buttons(
            self, GREY, 20, GRID_BUTTON_Y + GRID_BUTTON_HEIGTH + GRID_SPACE, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGTH, 'End'
        )
        self.wall_button = Buttons(
            self, GREY, 20, GRID_BUTTON_Y + 2 * GRID_BUTTON_HEIGTH + 2 * GRID_SPACE, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGTH, 'Wall'
        )
        self.reset_button = Buttons(
            self, GREY, 20, GRID_BUTTON_Y + 3 * GRID_BUTTON_HEIGTH + 3 * GRID_SPACE, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGTH, 'Reset'
        )
        self.visualize_button = Buttons(
            self, GREY, 20, GRID_BUTTON_Y + 4 * GRID_BUTTON_HEIGTH + 4 * GRID_SPACE, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGTH, 'Visualize path'
        )
        self.main_menu_button = Buttons(
            self, GREY, 20, GRID_BUTTON_Y + 5 * GRID_BUTTON_HEIGTH + 5 * GRID_SPACE, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGTH, "Main Menu"
        )

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self.state == "main menu":
                self.main_menu_events()
            elif self.state == "grid_menu":
                self.grid_menu_events()
            elif self.state == "Start":
                self.start_event()
            elif self.state == "reset":
                self.reset_event()
            elif self.state == "End":
                self.end_event()
            elif self.state == "wall":
                self.wall_event()
            elif self.state == "visualize":
                self.execute_search_algorithm()
        pygame.quit()
        sys.exit()

    def draw_main_menu(self):
        self.WIN.fill(WHITE)
        font = pygame.font.SysFont(FONT, 90)
        IMG = font.render("Path Finding Algorithms Visualizer", 1, (150, 0, 150))
        self.WIN.blit(
            IMG, (WIDTH // 2 - IMG.get_width() // 2, HEIGHT // 2 - IMG.get_height() // 2 - 50))
        self.bfs_button.draw_button()
        self.dfs_button.draw_button()
        self.dijkstra_button.draw_button()
        self.bidirectional_button.draw_button()
        self.astar_button.draw_button()
        pygame.display.update()

    def draw_sub_grid(self):
        if self.algorithm == "dfs":
            font = pygame.font.SysFont(FONT, 50)
            IMG1 = font.render("Depth", 1, (150, 0, 150))
            IMG2 = font.render("First", 1, (150, 0, 150))
            IMG3 = font.render("Search", 1, (150, 0, 150))
            self.WIN.blit(
                IMG1, ((WIDTH - GW) // 2 - IMG1.get_width() // 2, 50))
            self.WIN.blit(
                IMG2, ((WIDTH - GW) // 2 - IMG2.get_width() // 2, 120))
            self.WIN.blit(
                IMG3, ((WIDTH - GW) // 2 - IMG3.get_width() // 2, 190))
        if self.algorithm == "bfs":
            font = pygame.font.SysFont(FONT, 50)
            IMG1 = font.render("Breadth", 1, (150, 0, 150))
            IMG2 = font.render("First", 1, (150, 0, 150))
            IMG3 = font.render("Search", 1, (150, 0, 150))
            self.WIN.blit(
                IMG1, ((WIDTH - GW) // 2 - IMG1.get_width() // 2, 50))
            self.WIN.blit(
                IMG2, ((WIDTH - GW) // 2 - IMG2.get_width() // 2, 120))
            self.WIN.blit(
                IMG3, ((WIDTH - GW) // 2 - IMG3.get_width() // 2, 190))

        if self.algorithm == "dijkstra":
            font = pygame.font.SysFont(FONT, 50)
            IMG1 = font.render("Dijkstra", 1, (150, 0, 150))
            IMG2 = font.render("Search", 1, (150, 0, 150))
            self.WIN.blit(
                IMG1, ((WIDTH - GW) // 2 - IMG1.get_width() // 2, 100))
            self.WIN.blit(
                IMG2, ((WIDTH - GW) // 2 - IMG2.get_width() // 2, 170))

        if self.algorithm == "astar":
            font = pygame.font.SysFont(FONT, 50)
            IMG1 = font.render("A-star", 1, (150, 0, 150))
            IMG2 = font.render("Search", 1, (150, 0, 150))
            self.WIN.blit(
                IMG1, ((WIDTH - GW) // 2 - IMG1.get_width() // 2, 100))
            self.WIN.blit(
                IMG2, ((WIDTH - GW) // 2 - IMG2.get_width() // 2, 170))

        if self.algorithm == "bidirectional":
            font = pygame.font.SysFont(FONT, 40)
            IMG1 = font.render("Bidirectional", 1, (150, 0, 150))
            IMG2 = font.render("Search", 1, (150, 0, 150))
            self.WIN.blit(
                IMG1, ((WIDTH - GW) // 2 - IMG1.get_width() // 2, 100))
            self.WIN.blit(
                IMG2, ((WIDTH - GW) // 2 - IMG2.get_width() // 2, 170))

    def draw_grid_menu(self):
        self.WIN.fill(WHITE)
        self.grid.draw()
        self.draw_sub_grid()
        self.start_button.draw_button()
        self.end_button.draw_button()
        self.wall_button.draw_button()
        self.reset_button.draw_button()
        self.visualize_button.draw_button()
        self.main_menu_button.draw_button()
        pygame.display.update()

    def grid_menu_buttons(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.start_button.is_over(pos):
                self.state = "Start"
                self.start_button.color = CYAN
            elif self.end_button.is_over(pos):
                self.state = "End"
                self.end_button.color = CYAN
            elif self.wall_button.is_over(pos):
                self.state = "wall"
                self.wall_button.color = CYAN
            elif self.reset_button.is_over(pos):
                self.state = "reset"
                self.reset_button.color = CYAN
            elif self.main_menu_button.is_over(pos):
                self.state = "main menu"
                self.main_menu_button.color = CYAN
            elif self.visualize_button.is_over(pos):
                self.state = "visualize"
                self.start_button.color = GREY
                self.end_button.color = GREY
                self.wall_button.color = GREY
                self.reset_button.color = GREY
                self.main_menu_button.color = GREY
                self.visualize_button.color = CYAN
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if self.start_button.is_over(pos):
                self.start_button.color = CYAN
            elif self.end_button.is_over(pos):
                self.end_button.color = CYAN
            elif self.wall_button.is_over(pos):
                self.wall_button.color = CYAN
            elif self.reset_button.is_over(pos):
                self.reset_button.color = CYAN
            elif self.main_menu_button.is_over(pos):
                self.main_menu_button.color = CYAN
            elif self.visualize_button.is_over(pos):
                self.visualize_button.color = CYAN
            else:
                self.start_button.color = GREY
                self.end_button.color = GREY
                self.wall_button.color = GREY
                self.reset_button.color = GREY
                self.visualize_button.color = GREY
                self.main_menu_button.color = GREY

    def grid_menu_events(self):
        self.draw_grid_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.grid_menu_buttons(event)

    # Choose any one of the algorithm in the main menu
    def main_menu_events(self):
        self.draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.bfs_button.is_over(pos):
                    self.algorithm = "bfs"
                    self.state = "grid_menu"
                if self.dfs_button.is_over(pos):
                    self.algorithm = 'dfs'
                    self.state = "grid_menu"
                if self.astar_button.is_over(pos):
                    self.algorithm = 'astar'
                    self.state = 'grid_menu'
                if self.dijkstra_button.is_over(pos):
                    self.algorithm = 'dijkstra'
                    self.state = 'grid_menu'
                if self.bidirectional_button.is_over(pos):
                    self.algorithm = 'bidirectional'
                    self.state = 'grid_menu'

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()

                if self.bfs_button.is_over(pos):
                    self.bfs_button.color = RED

                elif self.dfs_button.is_over(pos):
                    self.dfs_button.color = RED

                elif self.astar_button.is_over(pos):
                    self.astar_button.color = RED

                elif self.dijkstra_button.is_over(pos):
                    self.dijkstra_button.color = RED

                elif self.bidirectional_button.is_over(pos):
                    self.bidirectional_button.color = RED
                else:
                    self.bfs_button.color = CYAN
                    self.dfs_button.color = CYAN
                    self.dijkstra_button.color = CYAN
                    self.bidirectional_button.color = CYAN
                    self.astar_button.color = CYAN

            for row in self.grid.grid:
                for cell in row:
                    cell.reset()

            self.grid.set_default()
    # To change the position of starting node by clicking on start in start menu

    def start_event(self):
        self.start_button.color = CYAN
        self.draw_grid_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.grid_menu_buttons(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_drag = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row, col = self.grid.get_row_col(pos)
                self.mouse_drag = True
                if row == -1 and col == -1:
                    continue
                cell = self.grid.get_cell(row, col)
                if not self.start and cell != self.end:
                    self.start = cell
                    self.start.make_start()
                elif self.end != cell:
                    self.start.revert()
                    self.start = cell
                    self.start.make_start()
            if event.type == pygame.MOUSEMOTION:
                if self.mouse_drag:
                    pos = event.pos
                    row, col = self.grid.get_row_col(pos)
                    if row == -1 and col == -1:
                        continue
                    cell = self.grid.get_cell(row, col)
                    if cell != self.end:
                        self.start.revert()
                        self.start = cell
                        self.start.make_start()
    # To change the position of end node by clicking on end in grid menu

    def end_event(self):
        self.end_button.color = CYAN
        self.draw_grid_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.grid_menu_buttons(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_drag = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row, col = self.grid.get_row_col(pos)
                self.mouse_drag = True
                if row == -1 and col == -1:
                    continue
                cell = self.grid.get_cell(row, col)
                print(row, col)
                if not self.end and cell != self.start:
                    self.end = cell
                    self.end.make_end()
                elif self.start != cell:
                    self.end.revert()
                    self.end = cell
                    self.end.make_end()

            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_drag:
                    pos = event.pos
                    row, col = self.grid.get_row_col(pos)
                    if row == -1 and col == -1:
                        continue
                    cell = self.grid.get_cell(row, col)
                    if cell != self.start:
                        self.end.revert()
                        self.end = cell
                        self.end.make_end()
    # To add walls in the grid by click on walls in grid menu

    def wall_event(self):
        self.wall_button.color = CYAN
        self.draw_grid_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.grid_menu_buttons(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_drag = False
                self.right_button = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    row, col = self.grid.get_row_col(pos)
                    if row == -1 and col == -1:
                        continue
                    cell = self.grid.get_cell(row, col)
                    if cell != self.start and cell != self.end:
                        self.mouse_drag = True
                        cell.make_barrier()
                elif event.button == 3:
                    self.right_button = True
                    pos = event.pos
                    row, col = self.grid.get_row_col(pos)
                    if row == -1 and col == -1:
                        continue
                    cell = self.grid.get_cell(row, col)
                    if cell.is_obstacle():
                        cell.reset()

            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_drag:
                    pos = event.pos
                    row, col = self.grid.get_row_col(pos)
                    if row == -1 and col == -1:
                        continue
                    cell = self.grid.get_cell(row, col)
                    if cell != self.start and cell != self.end:
                        cell.make_barrier()
                if self.right_button:
                    pos = event.pos
                    row, col = self.grid.get_row_col(pos)
                    if row == -1 and col == -1:
                        continue
                    cell = self.grid.get_cell(row, col)
                    if cell.is_obstacle():
                        cell.reset()
    # To Clear the grid

    def reset_event(self):
        self.reset_button.color = CYAN
        self.draw_grid_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.grid_menu_buttons(event)
            for row in self.grid.grid:
                for cell in row:
                    cell.reset()
            self.grid.set_default()
    #  If visualize path is executed

    def execute_search_algorithm(self):
        self.visualize_button.color = CYAN
        self.draw_grid_menu()
        self.grid.set_neighbors()
        if self.algorithm == "bfs":
            self.bfs = BreadthFirstSearch(self, self.start, self.end, self.grid)
            self.bfs.execute()

            self.state = "grid_menu"

        if self.algorithm == "dijkstra":
            self.dijkstra = Dijkastra(self, self.start, self.end, self.grid)
            self.dijkstra.execute()
            self.state = "grid_menu"

        if self.algorithm == "dfs":
            self.dfs = DepthFirstSearch(self, self.start, self.end, self.grid)
            self.dfs.execute(self.start)
            self.state = "grid_menu"

        if self.algorithm == "astar":
            self.astar = Astar(self, self.start, self.end, self.grid)
            self.astar.execute()
            self.state = "grid_menu"

        if self.algorithm == "bidirectional":
            self.bidirectional = Bidirectional(self, self.start, self.end, self.grid)
            self.bidirectional.execute()
            self.state = "grid_menu"


if __name__ == '__main__':
    app = App()
    app.run()
