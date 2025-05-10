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
    
    def update_blit(self, surface, sqsize):
        if self.dragging and self.piece and self.piece.texture:
            # วางภาพตรงกลางเมาส์
            rect = self.piece.texture.get_rect(center=(self.mouseX, self.mouseY))
            # หรือถ้าต้องการให้ขนาดเปลี่ยนตาม sqsize
            # self.piece.texture = pygame.transform.scale(self.piece.texture, (sqsize, sqsize))
            surface.blit(self.piece.texture, rect)

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def drag_piece(self, piece, row, col):
        self.piece = piece
        self.dragging = True
        self.initial_row = row
        self.initial_col = col

    def undrag_piece(self):
        self.piece = None
        self.dragging = False