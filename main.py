import pygame
from game import Game
from square import Square

class Main:
    WIDTH = 1000
    HEIGHT = 800
    ROWS = 8
    COLS = 8

    def __init__(self):
        pygame.init()
        # เปิด double buffering ช่วยลด flicker
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT),
            pygame.DOUBLEBUF
        )
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.game.white_clock.start()

    def mainloop(self):
        running = True
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 48)
        while running:
            for event in pygame.event.get():
                # Allow window to close using the window close button
                if event.type == pygame.QUIT:
                    running = False

                # Restart game on Space if game over is active
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game.game_over:
                        self.game.reset()
                        self.game.white_clock.start()

                # Handle other events only if game is not over
                elif not self.game.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = event.pos
                        row = my // self.game.SQSIZE
                        col = mx // self.game.SQSIZE
                        sq = self.game.board.board[row][col]
                        if sq.has_piece() and sq.piece.color == self.game.next_player:
                            self.game.dragger.drag_piece(sq.piece, row, col)
                            self.game.highlighted_moves = sq.piece.valid_moves(self.game.board, (row, col))
                    
                    elif event.type == pygame.MOUSEMOTION:
                        mx, my = event.pos
                        self.game.dragger.update_mouse((mx, my))
                    
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if self.game.dragger.dragging:
                            mx, my = event.pos
                            nr, nc = my // self.game.SQSIZE, mx // self.game.SQSIZE

                            if (nr, nc) in self.game.highlighted_moves:
                                self.game.board.move_piece(self.game.dragger.piece, (nr, nc))
                                self.game.check_game_over()
                                if self.game.next_player == 'white':
                                    self.game.white_clock.stop()
                                    self.game.black_clock.start()
                                else:
                                    self.game.black_clock.stop()
                                    self.game.white_clock.start()
                                self.game.next_turn()

                            self.game.dragger.undrag_piece()
                            self.game.highlighted_moves = []

            # Draw everything in every frame
            self.game.show_back_ground(self.screen)
            self.game.show_piece()
            self.game.show_available_moves()
            self.game.show_clocks(self.screen)

            # Display game over message if active
            if self.game.game_over:
                msg = f"Checkmate: {self.game.winner} wins! Press Space to restart."
                msg_text = font.render(msg, True, (255, 0, 0))
                msg_rect = msg_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
                self.screen.blit(msg_text, msg_rect)

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main = Main()
    main.mainloop()
    pygame.quit()