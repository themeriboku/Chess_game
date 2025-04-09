from piece import Piece
from square import Square
from board import Board

class Move:
    def __init__(self, player, from_square, to_square, move_history=None):
        self.player = player
        self.from_square = from_square
        self.to_square = to_square
        self.move_history = move_history if move_history else []
        self.piece = None
        self.captured_piece = None
        self.promotion = None
        self.castling = False
        self.check = False
        self.checkmate = False
        self.stalemate = False
        self.value = 0
        
    def move_history(self):
        return self.move_history
    
    def add_move(self, move):
        self.move_history.append(move)

    def add_move_to_data(self, move_data):
        pass

    def clear_moves(self):
        self.move_history = []

    def cal_value(self):
        pass
    


