from square import Square
from abc import ABC, abstractmethod
import os
import pygame

class Piece(ABC):
    def __init__(self, name, color, value, texture=None,texture_rect = None):
        self.name = name
        self.color = color
        self.value = value if color == 'white' else -value
        self.moved = False
        self.row = None
        self.col = None
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

        
    def set_texture(self, size=80):
        if size <= 80:
            folder = r"D:\forlearning\Chess_game\picture\imgs-80px"
        else:
            folder = r"D:\forlearning\Chess_game\picture\imgs-128px"

        # ตั้งชื่อไฟล์: เช่น "white_pawn.png"
        filename = f"{self.color}_{self.name}.png"
        full_path = os.path.join(folder, filename)
        try:
            # โหลดภาพพร้อม alpha channel (transparency)
            self.texture = pygame.image.load(full_path).convert_alpha()
            # ปรับขนาดภาพให้ตรงกับ size ที่ต้องการ ถ้าจำเป็น
            if self.texture.get_width() != size or self.texture.get_height() != size:
                self.texture = pygame.transform.scale(self.texture, (size, size))
            self.texture_rect = self.texture.get_rect()
        except Exception as e:
            print(f"Error loading texture from {full_path}: {e}")
            self.texture = None
    
    @abstractmethod
    def get_moves(self, board: "Board", pos: tuple[int,int], validate_checks: bool = True) -> list[tuple[int,int]]:
        """Return pseudo-legal moves from pos"""
        pass

    def valid_moves(self, board: "Board", pos: tuple[int,int]) -> list[tuple[int,int]]:
        raw = self.get_moves(board, pos, validate_checks=False)
        return [m for m in raw if not board.causes_check(self, pos, m)]
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state['texture'] = None
        state['texture_rect'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.set_texture()

    def move(self, row, col):
        self.row = row
        self.col = col

class Pawn(Piece):
    def __init__(self, color):
        super().__init__('pawn', color, 1.0)
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False

    def get_moves(self, board, pos, validate_checks=True):
        row, col = pos
        moves = []
        # ก้าวเดียวข้างหน้า
        forward = (row + self.dir, col)
        if Square.in_range(forward) and board.get_square(forward).isempty():
            moves.append(forward)
            # ก้าวสองช่องเมื่อยังไม่เคลื่อนที่
            if not self.moved:
                double = (row + 2 * self.dir, col)
                if Square.in_range(double) and board.get_square(double).isempty():
                    moves.append(double)
        # จับกินเฉียงซ้าย–ขวา
        for dc in (-1, +1):
            diag = (row + self.dir, col + dc)
            if Square.in_range(diag):
                target_sq = board.get_square(diag)
                if target_sq.has_enemy_piece(self.color):
                    moves.append(diag)
                # En passant check:
                adjacent = (row, col + dc)
                if Square.in_range(adjacent):
                    adj_sq = board.get_square(adjacent)
                    if (adj_sq.has_enemy_piece(self.color) and 
                        adj_sq.piece.name == 'pawn'):
                        # Check last move if enemy pawn moved two squares:
                        if board.history:
                            last_move = board.history[-1]
                            last_pawn = last_move['piece']
                            if (last_pawn.name == 'pawn' and 
                                abs(last_move['from'][0] - last_move['to'][0]) == 2 and
                                last_move['to'] == adjacent):
                                moves.append(diag)
        return moves
class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)
        
    def get_moves(self, board, pos, validate_checks=False):
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

    def get_moves(self, board, pos, validate_checks=False):
        return board.straight_line_moves(self, pos, [(1,1),(1,-1),(-1,1),(-1,-1)], validate_checks)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

    def get_moves(self, board, pos, validate_checks=False):
        return board.straight_line_moves(self, pos, [(1,0),(-1,0),(0,1),(0,-1)], validate_checks)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

    def get_moves(self, board, pos, validate_checks=False):
        dirs = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        return board.straight_line_moves(self, pos, dirs, validate_checks)

class King(Piece):
    def __init__(self, color):
        super().__init__('king', color, 100.0)
        self.moved = False
        self.castle = False
        self.left_rook = None
        self.right_rook = None

    def get_moves(self, board, pos, validate_checks=False):
        row, col = pos
        moves = []
        # 8 ทิศรอบตัว
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                dest = (row + dr, col + dc)
                if Square.in_range(dest):
                    sq = board.get_square(dest)
                    if sq.isempty() or sq.has_enemy_piece(self.color):
                        moves.append(dest)

        # Castling: หาทางขวา (king-side) และซ้าย (queen-side)
        if not self.moved:
            # King-side
            if self.right_rook and not self.right_rook.moved:
                path = [(row, col+1), (row, col+2)]
                if all(board.get_square(p).isempty() for p in path):
                    if not any(board.causes_check(self, pos, p) for p in [(row, col+1), (row, col+2)]):
                        moves.append((row, col+2))
            # Queen-side
            if self.left_rook and not self.left_rook.moved:
                path = [(row, col-1), (row, col-2), (row, col-3)]
                if all(board.get_square(p).isempty() for p in path[:-1]):
                    if not any(board.causes_check(self, pos, p) for p in [(row, col-1), (row, col-2)]):
                        moves.append((row, col-2))
        return moves
