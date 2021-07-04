import pygame
from settings import *


class Buttons:
    def __init__(self, app, color, x, y, width, height, text=""):
        self.app = app
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw_button(self):
        pygame.draw.rect(self.app.WIN, self.color,
                         (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont(FONT, 24)
            IMG = font.render(self.text, 1, (0, 0, 0))
            self.app.WIN.blit(
                IMG, (self.x + (self.width // 2 - IMG.get_width() // 2),
                      self.y + (self.height // 2 - IMG.get_height() // 2)))
    # To check if cursor is on any button

    def is_over(self, pos):
        x, y = pos[0], pos[1]
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                return True
        return False
