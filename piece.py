from square import Square
from abc import ABC, abstractmethod
from board import Board

class Piece(ABC):
    ROWS = 8
    COLS = 8
    def __init__(self, name, color, value, texture=None,texture_rect = None):
        self.name = name
        self.color = color
        self.value = value if color == 'white' else -value
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
        
    def set_texture(self, size=80):
        pass
    
    @abstractmethod
    def get_moves(self, board, pos, validate_checks=True):
        """Return pseudo‑legal moves."""
        pass

    def valid_moves(self, board:Board, pos):
        raw = self.get_moves(board, pos, validate_checks=False)
        return [m for m in raw if not board.causes_check(self.color, pos, m)]

class Pawn(Piece):
    def __init__(self, color):
        super().__init__('pawn', color, 1.0)
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False

    def get_moves(self, board: Square, pos, validate_checks=True): #ต้องแก้
        row, col = pos
        moves = []
        # ก้าวเดียวข้างหน้า
        forward = (row + self.dir, col)
        if Square.in_range(forward) and board.get_square(forward).isempty():
            moves.append(forward)
            # ก้าวสองช่องเมื่อยังไม่เคลื่อนที่
            if not self.moved:
                double = (row + 2*self.dir, col)
                if board.get_square(double).isempty():
                    moves.append(double)
        # จับกินเฉียงซ้าย–ขวา
        for dc in (-1, +1):
            diag = (row + self.dir, col + dc)
            if Square.in_range(diag) and board.get_square(diag).has_enemy_piece(self.color):
                moves.append(diag)
        # TODO: en passant logic
        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)
        
    def get_moves(self, board, pos, validate_checks=True):
        possible_square = [
            (pos[0] + 2, pos[1] + 1), (pos[0] + 2, pos[1] - 1),
            (pos[0] - 2, pos[1] + 1), (pos[0] - 2, pos[1] - 1),
            (pos[0] + 1, pos[1] + 2), (pos[0] + 1, pos[1] - 2),
            (pos[0] - 1, pos[1] + 2), (pos[0] - 1, pos[1] - 2)
        ]
        valid_moves = []
        for square in possible_square:
            if Square.in_range(square):
                if board.get_square(square).isempty() or board.get_square(square).has_enemy_piece(self.color):
                    valid_moves.append(square)
        return valid_moves
        
class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.0)

    def get_moves(self, board, pos, validate_checks=True):
        pass

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

    def get_moves(self, board, pos, validate_checks=True):
        pass

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

    def get_moves(self, board, pos, validate_checks=True):
        pass

class King(Piece):
    def __init__(self, color):
        super().__init__('king', color, 100.0)
        self.left_rook = None
        self.right_rook = None

    def get_moves(self, board, pos, validate_checks=True):
        pass
