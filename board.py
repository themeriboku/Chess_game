from square import Square
from piece import *
from clock import Clock

class Board:
    WIDTH = 800
    HEIGHT = 800
    ROWS = 8
    COLS = 8
    SQSIZE = WIDTH // COLS

    def __init__(self):
        self._create_board()
        self._place_pieces()

    def _create_board(self):
        pass

    def _place_pieces(self, color):
        pass

    def straight_line_moves(self, piece, pos, directions, validate_checks=True):
        pass

    def filter_moves(self, piece, pos, moves):
        pass

    def causes_check(self, piece, pos, move):
        pass

    def _copy_board(self):
        pass

    def apply_move(self, move):
        pass

    def is_in_check(self, color):
        pass

    def move_piece(self, piece, move):
        pass

    def create_clock(self, time_limit, turn=None):
        pass

    def count_check(self):
        pass
    
    def capture_piece(self):
        pass