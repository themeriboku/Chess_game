from square import Square
from abc import ABC, abstractmethod
from board import Board

class Piece(ABC):
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

    def get_moves(self, board:Square, pos, validate_checks=True):
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
        
    def get_moves(self, board:Square, pos, valid_checks=True):
        possible_square = [
            (pos[0] + 2, pos[1] + 1), (pos[0] + 2, pos[1] - 1),
            (pos[0] - 2, pos[1] + 1), (pos[0] - 2, pos[1] - 1),
            (pos[0] + 1, pos[1] + 2), (pos[0] + 1, pos[1] - 2),
            (pos[0] - 1, pos[1] + 2), (pos[0] - 1, pos[1] - 2)
        ]
        moves = []
        for square in possible_square:
            if Square.in_range(square):
                if board.get_square(square).isempty() or board.get_square(square).has_enemy_piece(self.color):
                    moves.append(square)
        return moves
        
class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.0)

    def get_moves(self, board:Square, pos, validate_checks=True):
        moves = []
        directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr; c += dc
                if not Square.in_range((r,c)): break
                sq = board.get_square((r,c))
                if sq.isempty():
                    moves.append((r,c))
                else:
                    if sq.has_enemy_piece(self.color):
                        moves.append((r,c))
                    break
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

    def get_moves(self, board:Square, pos, validate_checks=True):
        pass

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

    def get_moves(self, board:Square, pos, validate_checks=True):
        pass

class King(Piece):
    def __init__(self, color):
        super().__init__('king', color, 100.0)
        self.moved = False
        self.castle = False
        self.left_rook = None
        self.right_rook = None

    def get_moves(self, board:Square, pos, validate_checks=True):
        
        row, col = pos
        moves = []
        # 8 ทิศรอบตัว
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr==0 and dc==0: continue
                dest = (row+dr, col+dc)
                if Square.in_range(dest):
                    sq = board.get_square(dest)
                    if sq.isempty() or sq.has_enemy_piece(self.color):
                        moves.append(dest)

        # Castling: หาทางขวา (king-side) และซ้าย (queen-side)
        if not self.moved and validate_checks:
            # King-side
            if self.right_rook and not self.right_rook.moved:
                # ระหว่าง King และ Rook ไม่มีชิ้นกีดขวาง
                path = [(row, col+1), (row, col+2)]
                if all(board.get_square(p).isempty() for p in path):
                    # ตรวจว่าผ่าน check หรือไม่
                    if not any(board.causes_check(self.color, pos, p) for p in [(row, col+1), (row, col+2)]):
                        moves.append((row, col+2))
            # Queen-side
            if self.left_rook and not self.left_rook.moved:
                path = [(row, col-1), (row, col-2), (row, col-3)]
                if all(board.get_square(p).isempty() for p in path[:-1]):
                    if not any(board.causes_check(self.color, pos, p) for p in [(row, col-1), (row, col-2)]):
                        moves.append((row, col-2))

        return moves
