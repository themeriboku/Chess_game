import pygame
from board import Board
from dragger import DragHandler
from square import Square
from clock import Clock

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

        self.black_clock = Clock(3600)
        self.white_clock = Clock(3600)
        
        self.game_over = False
        self.winner = None
    
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
        if not self.game_over:
            self.next_player = 'white' if self.next_player == 'black' else 'black'
    def show_clocks(self, surface):
        # Draw a panel on the right side (from x=800 to 1000)
        panel_rect = pygame.Rect(self.WIDTH, 0, 200, self.HEIGHT)
        pygame.draw.rect(surface, (200, 200, 200), panel_rect)

        # Create a font to render text
        font = pygame.font.Font(None, 36)

        # Get current times from clocks
        white_time = self.white_clock.time_record()
        black_time = self.black_clock.time_record()

        # Format time into MM:SS
        def format_time(t):
            minutes = int(t) // 60
            seconds = int(t) % 60
            return f"{minutes:02d}:{seconds:02d}"

        white_text = font.render("White: " + format_time(white_time), True, (0, 0, 0))
        black_text = font.render("Black: " + format_time(black_time), True, (0, 0, 0))

        # Swap positions: black clock on top, white clock below
        black_rect = black_text.get_rect(center=(self.WIDTH + 100, self.HEIGHT // 3))
        white_rect = white_text.get_rect(center=(self.WIDTH + 100, 2 * self.HEIGHT // 3))
        surface.blit(black_text, black_rect)
        surface.blit(white_text, white_rect)
    
    def show_clocks(self, surface):
        # Draw a panel on the right side (from x=800 to 1000)
        panel_rect = pygame.Rect(self.WIDTH, 0, 200, self.HEIGHT)
        pygame.draw.rect(surface, (200, 200, 200), panel_rect)

        # Create a font to render text
        font = pygame.font.Font(None, 36)

        # Get current times from clocks
        white_time = self.white_clock.time_record()
        black_time = self.black_clock.time_record()

        # Format time into MM:SS
        def format_time(t):
            minutes = int(t) // 60
            seconds = int(t) % 60
            return f"{minutes:02d}:{seconds:02d}"

        white_text = font.render("White: " + format_time(white_time), True, (0, 0, 0))
        black_text = font.render("Black: " + format_time(black_time), True, (0, 0, 0))

        # Swap positions: black clock on top, white clock below
        black_rect = black_text.get_rect(center=(self.WIDTH + 100, self.HEIGHT // 3))
        white_rect = white_text.get_rect(center=(self.WIDTH + 100, 2 * self.HEIGHT // 3))
        surface.blit(black_text, black_rect)
        surface.blit(white_text, white_rect)

    def check_game_over(self):
        # ถ้าไม่มี move เลย → game over
        if self.board.is_checkmate(self.next_player):
            self.game_over = True
            # ฝ่ายที่เพิ่งเดินชนะ (opponent of next_player)
            self.winner = 'black' if self.next_player == 'white' else 'white'
            # หยุดนาฬิกา
            self.white_clock.stop()
            self.black_clock.stop()
            
    def reset(self):
        self.__init__()