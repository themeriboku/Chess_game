import pygame
from game import Game

class Main:
    WIDTH = 800
    HEIGHT = 800
    ROWS = 8
    COLS = 8

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (self.WIDTH, self.HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        pass