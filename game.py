import pygame
from board import Board
from dragger import DragHandler
from square import Square


class Game:
    WIDTH = 800
    HEIGHT = 800
    ROWS = 8
    COLS = 8
    SQSIZE = WIDTH // COLS

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = DragHandler()
        self.background = self.create_background()
    
    def create_background(self):
        background = pygame.Surface((self.WIDTH, self.HEIGHT))
        for row in range(self.ROWS):
            for col in range(self.COLS):
                # สมมุติให้สีเขียวสำหรับช่องที่มีค่าสูงสุด และสีขาวสำหรับอีกช่องหนึ่ง
                color = ((0, 100, 0)) if (row + col) % 2 == 0 else (255, 255, 255)
                pygame.draw.rect(background, color, (col * self.SQSIZE, row * self.SQSIZE, self.SQSIZE, self.SQSIZE))
        return background

    def show_back_ground(self, surface):
        surface.blit(self.background, (0, 0))
        pygame.display.flip()
        
    def show_piece(self):
        surface = pygame.display.get_surface()
    
        # วนลูปผ่านแต่ละแถวในกระดาน
        for row in self.board.board:
            # สำหรับแต่ละ square ในแถวนั้น
            for square in row:
                # ถ้ามี piece ใน square นั้น
                if square.has_piece():
                    piece = square.piece
                    # หาก piece กำลังถูกลากอยู่ (dragging) ให้ข้ามการวาด เพราะจะมี DragHandler ดูแลแยกวาดให้แล้ว
                    if self.dragger.dragging and self.dragger.piece == piece:
                        continue
                    # คำนวณตำแหน่งพิกเซลบนหน้าจอสำหรับ square นี้
                    x = square.cols * self.SQSIZE
                    y = square.row * self.SQSIZE
                    # ตรวจสอบว่ามี texture ของ piece อยู่หรือไม่ ก่อนวาด
                    if piece.texture:
                        surface.blit(piece.texture, (x, y))

    def show_available_moves(self):
        pass

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
    
    def reset(self):
        self.__init__()