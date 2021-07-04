from settings import *
from grid_class import *
from queue import Queue
from queue import PriorityQueue
import pygame


class BreadthFirstSearch:
    def __init__(self, app, start, end, grid):
        self.app = app
        self.start = start
        self.end = end
        self.grid = grid
        self.par = {}
    # If there exits a path then retrace path from end to start

    def construct_path(self, curr):
        while curr in self.par:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.running = False
                    pygame.quit()
            curr = self.par[curr]
            curr.make_path()
            self.grid.draw()
            pygame.display.update()

        curr.make_start()
        self.grid.draw()
        pygame.display.update()
    # BFS algorithm Implementation

    def execute(self):
        # dist represents no.of steps to reach any cell from start node
        dist = {cell: float("inf") for row in self.grid.grid for cell in row}
        par = {}
        q = Queue()
        dist[self.start] = 0
        q.put(self.start)
        while not q.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.running = False
                    pygame.quit()

            curr = q.get()
            if curr == self.end:
                self.end.make_end()
                self.construct_path(curr)
                return True
            # Iterate through all neighbors of curr cell and if we can relax any of the neighbor then update it and add to queue
            for neighbor in curr.neighbors:
                if dist[neighbor] > dist[curr] + 1:
                    dist[neighbor] = dist[curr] + 1
                    self.par[neighbor] = curr
                    q.put(neighbor)
                    neighbor.make_open()

            self.grid.draw()
            pygame.display.update()
            if curr != self.end and curr != self.start:
                curr.make_closed()

        return False


class Dijkastra:
    def __init__(self, app, start, end, grid):
        self.app = app
        self.start = start
        self.end = end
        self.grid = grid
        self.par = {}

    def construct_path(self, curr):
        while curr in self.par:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.running = False
                    pygame.quit()
            curr = self.par[curr]
            curr.make_path()
            self.grid.draw()
            pygame.display.update()

        curr.make_start()
        self.grid.draw()
        pygame.display.update()

    def execute(self):
        dist = {cell: float("inf") for row in self.grid.grid for cell in row}
        dist[self.start] = 0
        pq = PriorityQueue()
        pq.put((0, self.start))
        while not pq.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.running = False
                    pygame.quit()
            d, curr = pq.get()
            if curr == self.end:
                self.end.make_end()
                self.construct_path(curr)
                return True
            if d > dist[curr]:
                continue
            for neighbor in curr.neighbors:
                if dist[neighbor] > dist[curr] + 1:
                    dist[neighbor] = dist[curr] + 1
                    self.par[neighbor] = curr
                    pq.put((dist[neighbor], neighbor))
                    neighbor.make_open()

            self.grid.draw()
            pygame.display.update()

            if curr != self.end and curr != self.start:
                curr.make_closed()

        return False


class DepthFirstSearch:
    def __init__(self, app, start, end, grid):
        self.app = app
        self.start = start
        self.end = end
        self.grid = grid
        self.par = None
        self.vis = None

    def construct_path(self, curr):
        while curr in self.par:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.running = False
                    pygame.quit()
            curr = self.par[curr]
            curr.make_path()
            self.grid.draw()
            pygame.display.update()

        curr.make_start()
        self.grid.draw()
        pygame.display.update()

    def execute(self, curr):
        if self.vis == None:
            self.vis = set()
        if self.par == None:
            self.par = {}
        self.vis.add(curr)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if curr == self.end:
            self.end.make_end()
            self.construct_path(curr)
            self.start.make_start()
            return True
        for neighbor in curr.neighbors:
            if neighbor not in self.vis:
                self.par[neighbor] = curr
                neighbor.make_open()
                self.grid.draw()
                pygame.display.update()
                if self.execute(neighbor):
                    return True

        curr.make_closed()
        return False


class Astar:
    def __init__(self, app, start, end, grid):
        self.app = app
        self.start = start
        self.end = end
        self.grid = grid
        self.par = None
        self.vis = None
        self.pq = PriorityQueue()

    def construct_path(self, curr):
        while curr in self.par:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.running = False
                    pygame.quit()
            curr = self.par[curr]
            curr.make_path()
            self.grid.draw()
            pygame.display.update()

        curr.make_start()
        self.grid.draw()
        pygame.display.update()

    def execute(self):
        self.par = {}
        self.g_score = {cell: float("inf") for row in self.grid.grid for cell in row}
        self.g_score[self.start] = 0
        self.f_score = {cell: float("inf") for row in self.grid.grid for cell in row}
        self.f_score[self.start] = self.start.heuristic(self.end)
        self.vis = set()
        self.vis.add(self.start)
        self.pq.put((self.f_score[self.start], self.start))
        while not self.pq.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.running = False
                    pygame.quit()
            curr = self.pq.get()[1]
            self.vis.remove(curr)

            if curr == self.end:
                self.end.make_end()
                self.construct_path(curr)
                self.start.make_start()
                return True

            for neighbor in curr.neighbors:
                if self.g_score[neighbor] > self.g_score[curr] + 1:
                    self.g_score[neighbor] = self.g_score[curr] + 1
                    self.par[neighbor] = curr
                    self.f_score[neighbor] = self.g_score[neighbor] + neighbor.heuristic(self.end)
                    if neighbor not in self.vis:
                        self.pq.put((self.f_score[neighbor], neighbor))
                        self.vis.add(neighbor)
                        neighbor.make_open()

            self.grid.draw()
            pygame.display.update()

            if curr != self.end and curr != self.start:
                curr.make_closed()

        return False


class Bidirectional():
    def __init__(self, app, start, end, grid):
        self.app = app
        self.start = start
        self.end = end
        self.grid = grid
        self.fwd_par = {}
        self.back_par = {}
        self.dist = {}
        self.fwd_q = Queue()
        self.back_q = Queue()
        self.vis_fwd = set()
        self.vis_back = set()

    def construct_path(self, curr):
        fwd_curr = curr
        back_curr = curr
        curr.make_path()
        while fwd_curr in self.fwd_par and back_curr in self.back_par:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.running = False
                    pygame.quit()
            fwd_curr = self.fwd_par[fwd_curr]
            back_curr = self.back_par[back_curr]
            fwd_curr.make_path()
            back_curr.make_path()
            self.grid.draw()
            pygame.display.update()

        while fwd_curr in self.fwd_par:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.running = False
                    pygame.quit()
            fwd_curr = self.fwd_par[fwd_curr]
            fwd_curr.make_path()
            self.grid.draw()
            pygame.display.update()

        while back_curr in self.back_par:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.running = False
                    pygame.quit()
            back_curr = self.back_par[back_curr]
            back_curr.make_path()
            self.grid.draw()
            pygame.display.update()

        back_curr.make_end()
        self.grid.draw()
        pygame.display.update()

    def execute(self):
        self.fwd_q.put(self.start)
        self.back_q.put(self.end)
        self.vis_fwd.add(self.start)
        self.vis_back.add(self.end)
        while not self.fwd_q.empty() and not self.back_q.empty():
            curr_f = self.fwd_q.get()
            curr_b = self.back_q.get()

            for n_f, n_b in zip(curr_f.neighbors, curr_b.neighbors):
                if n_f not in self.vis_fwd:
                    self.vis_fwd.add(n_f)
                    self.fwd_par[n_f] = curr_f
                    self.fwd_q.put(n_f)
                    n_f.make_open()

                if n_b not in self.vis_back:
                    self.vis_back.add(n_b)
                    self.back_par[n_b] = curr_b
                    self.back_q.put(n_b)
                    n_b.make_open()

                if curr_f in self.vis_back:
                    self.construct_path(curr_f)
                    self.start.make_start()
                    return True

                elif curr_b in self.vis_fwd:
                    self.end.make_end()
                    self.construct_path(curr_b)
                    self.start.make_start()
                    return True

            self.grid.draw()
            pygame.display.update()
            if curr_f != self.start or curr_b != self.end:
                curr_f.make_closed()
                curr_b.make_closed()
        return False
