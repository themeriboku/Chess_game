from square import Square
from piece import *
from clock import Clock
import copy

class Board:
    WIDTH = 800
    HEIGHT = 800
    ROWS = 8
    COLS = 8
    SQSIZE = WIDTH // COLS

    def __init__(self):
        self.board = []
        self._create_board()
        self._place_pieces()
        self.history = []  # เก็บสถานะก่อนหน้า สำหรับ undo / causes_check
        self.clock = None
        self.count_check = 0

    def _create_board(self):
        self.board = [[Square(row, col, piece=None) for col in range(self.COLS)]
        for row in range(self.ROWS)]

    def _place_pieces(self):
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        # Black
        for col, PieceCls in enumerate(order):
            self.board[0][col].piece = PieceCls('black')
            self.board[1][col].piece = Pawn('black')
        # White
        for col, PieceCls in enumerate(order):
            self.board[7][col].piece = PieceCls('white')
            self.board[6][col].piece = Pawn('white')

    def straight_line_moves(self, piece, pos, directions, validate_checks=True):
        moves = []
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr; c += dc
                if not Square.in_range((r, c)): break
                sq = self.get_square((r, c))
                if sq.isempty():
                    moves.append((r, c))
                else:
                    if sq.has_enemy_piece(piece.color):
                        moves.append((r, c))
                    break
        # ถ้าต้องกรองเช็ค
        if validate_checks:
            return [m for m in moves if not self.causes_check(piece, pos, m)]
        return moves

    def filter_moves(self, piece, pos, moves):
        valid = []
        for dest in moves:
            if not Square.in_range(dest): continue
            sq = self.get_square(dest)
            if sq.has_team_piece(piece.color): continue
            valid.append(dest)
        return valid

    def causes_check(self, piece, from_pos, to_pos):
        snapshot = self._copy_board()
        # ทำการเดินจริงบน self
        self.apply_move((from_pos, to_pos))
        in_check = self.is_in_check(piece.color)
        # คืนกระดานเดิม
        self.board = snapshot
        self.count_check += 1
        return in_check

    def _copy_board(self):
        return copy.deepcopy(self.board)

    def apply_move(self, move):
        pass

    def is_in_check(self, color):
        # หา pos ของ king
        for row in self.board:
            for sq in row:
                if sq.has_piece() and isinstance(sq.piece, King) and sq.piece.color == color:
                    king_pos = (sq.row, sq.cols)
                    break
        # ตรวจทุก piece ฝ่ายตรงข้าม
        for row in self.board:
            for sq in row:
                if sq.has_enemy_piece(color):
                    moves = sq.piece.get_moves(self, (sq.row, sq.cols), validate_checks=False)
                    if king_pos in moves:
                        return True
        return False

    def move_piece(self, piece, move):
        pass

    def create_clock(self, time_limit, turn=None):
        self.clock = Clock(time_limit, turn)
        return self.clock
    
    def capture_piece(self):
        pass