from piece import Piece
from square import Square
from board import Board

class Move:
    def __init__(self, player, from_square, to_square, move_history=None):
        self.player = player
        self.from_square = from_square
        self.to_square = to_square
        self.history = move_history if move_history else []
        self.piece = from_square.piece if from_square else None
        self.captured_piece = to_square.piece if to_square and to_square.is_occupied() else None
        self.promotion = None
        self.castling = False
        self.check = False
        self.checkmate = False
        self.stalemate = False
        self.value = 0
        
    def get_history(self):
        return self.history
    
    def add_move(self, move):
        self.history.append(move)

    def add_move_to_data(self, move_data):
        move_data.append({
            'player': self.player,
            'from': (self.from_square.row, self.from_square.col),
            'to': (self.to_square.row, self.to_square.col),
            'piece': self.piece.name if self.piece else None,
            'captured': self.captured_piece.name if self.captured_piece else None,
            'promotion': self.promotion,
            'castling': self.castling,
            'check': self.check,
            'checkmate': self.checkmate,
            'stalemate': self.stalemate,
            'value': self.value
        })

    def clear_moves(self):
        self.history = []

    def cal_value(self):
        piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0  
        }

        if self.captured_piece:
            self.value = piece_values.get(self.captured_piece.name.lower(), 0)
        else:
            self.value = 0
