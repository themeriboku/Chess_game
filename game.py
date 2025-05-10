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
        self.highlighted_moves = []
    
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
        
    def show_piece(self):
        surface = pygame.display.get_surface()
    
        # วนลูปผ่านแต่ละแถวในกระดาน
        for row in self.board.board:
            for square in row:
                if square.has_piece():
                    piece = square.piece
                    if self.dragger.dragging and self.dragger.piece == piece:
                        continue
                    # คำนวณตำแหน่งพิกเซลกลางใน square
                    x = square.cols * self.SQSIZE + (self.SQSIZE - piece.texture.get_width()) // 2
                    y = square.row * self.SQSIZE + (self.SQSIZE - piece.texture.get_height()) // 2
                    if piece.texture:
                        surface.blit(piece.texture, (x, y))

    def show_available_moves(self):
        surface = pygame.display.get_surface()
        for r, c in self.highlighted_moves:
            center = (c*self.SQSIZE + self.SQSIZE//2, r*self.SQSIZE + self.SQSIZE//2)
            pygame.draw.circle(surface, (0, 0, 255), center, 8)
        self.dragger.update_blit(surface, self.SQSIZE)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
    
    def reset(self):
        self.__init__()