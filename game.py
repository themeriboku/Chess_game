import pygame
from board import Board
from dragger import Dragger
from square import Square


class Game:
    WIDTH = 800
    HEIGHT = 800
    ROWS = 8
    COLS = 8
    SQSIZE = WIDTH // COLS

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()

    def show_back_ground(self, surface):
        pass

    def show_piece(self):
        pass

    def show_available_moves(self):
        pass

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
    
    def reset(self):
        self.__init__()