from square import Square
from piece import Piece
from board import Board

class DragHandler:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
    
    def update_blit(self, surface):
        pass

    def update_mouse(self, pos):
        pass

    def drag_piece(self, piece):
        pass

    def undrag_piece(self):
        pass