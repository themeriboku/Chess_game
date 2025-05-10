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
            piece = PieceCls('black')
            piece.move(0, col)
            self.board[0][col].piece = piece

            pawn = Pawn('black')
            pawn.move(1, col)
            self.board[1][col].piece = pawn
        # White
        for col, PieceCls in enumerate(order):
            piece = PieceCls('white')
            piece.move(7, col)
            self.board[7][col].piece = piece

            pawn = Pawn('white')
            pawn.move(6, col)
            self.board[6][col].piece = pawn

        # Assign castling rooks to kings
        self._assign_castling()
    
    def _assign_castling(self):
        # Assign for Black king (expected starting at row 0, col 4)
        black_king = self.board[0][4].piece
        if black_king and isinstance(black_king, King):
            black_king.left_rook = self.board[0][0].piece
            black_king.right_rook = self.board[0][7].piece
        # Assign for White king (expected starting at row 7, col 4)
        white_king = self.board[7][4].piece
        if white_king and isinstance(white_king, King):
            white_king.left_rook = self.board[7][0].piece
            white_king.right_rook = self.board[7][7].piece

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

    def apply_move(self, move: tuple[tuple[int,int], tuple[int,int]]):
        """
        move: ((r0,c0), (r1,c1))
        ย้าย piece จาก src -> dst ของกระดาน และบันทึก history
        คืนค่า piece ที่ถูกจับ (หรือ None)
        """
        (r0, c0), (r1, c1) = move
        src_sq = self.get_square((r0, c0))
        dst_sq = self.get_square((r1, c1))
        moving_piece = src_sq.piece
        captured_piece = dst_sq.piece
        # บันทึก history
        self.history.append({
            'move': move,
            'piece': moving_piece,
            'captured': captured_piece,
            'from': (r0, c0),
            'to': (r1, c1),
        })
        # ทำการย้าย
        dst_sq.piece = moving_piece
        src_sq.piece = None
        moving_piece.moved = True
        return captured_piece

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
        from_row, from_col = piece.row, piece.col
        to_row, to_col = move

        # Remove piece from source square
        self.board[from_row][from_col].piece = None

        captured = None
        # En passant capture: pawn moves diagonally to an empty square
        if piece.name == 'pawn' and from_col != to_col and self.board[to_row][to_col].isempty():
            # Capture enemy pawn from adjacent square (same row as start)
            captured = self.board[from_row][to_col].piece
            self.board[from_row][to_col].piece = None
        else:
            captured = self.board[to_row][to_col].piece

        # Move the piece
        piece.move(to_row, to_col)  # update internal position
        self.board[to_row][to_col].piece = piece
        piece.moved = True

        # Check for castling move: king moves two squares horizontally
        if piece.name == 'king' and abs(to_col - from_col) == 2:
            # King-side castling
            if to_col > from_col:
                rook = self.board[from_row][7].piece
                if rook:
                    self.board[from_row][7].piece = None
                    rook.move(from_row, from_col + 1)
                    self.board[from_row][from_col + 1].piece = rook
                    rook.moved = True
            else:
                # Queen-side castling
                rook = self.board[from_row][0].piece
                if rook:
                    self.board[from_row][0].piece = None
                    rook.move(from_row, from_col - 1)
                    self.board[from_row][from_col - 1].piece = rook
                    rook.moved = True

        # Append move to history (optional, for undo)
        self.history.append({
            'move': ((from_row, from_col), (to_row, to_col)),
            'piece': piece,
            'captured': captured,
            'from': (from_row, from_col),
            'to': (to_row, to_col)
        })

    def create_clock(self, time_limit, turn=None):
        self.clock = Clock(time_limit, turn)
        return self.clock
    
    def get_square(self, pos: tuple[int,int]) -> Square:
        r, c = pos
        return self.board[r][c]
    
    def capture_piece(self):
        if not self.history:
            return None
        return self.history[-1]['captured']
