import pygame
from game import Game
from square import Square

class Main:
    WIDTH = 800
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

    def mainloop(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                # ปิดเกม
                if event.type == pygame.QUIT:
                    running = False

                # เริ่มลาก
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    row = my // self.game.SQSIZE
                    col = mx // self.game.SQSIZE
                    sq = self.game.board.board[row][col]
                    if sq.has_piece() and sq.piece.color == self.game.next_player:
                    # เริ่ม drag และบันทึกตำแหน่งต้นทาง
                        self.game.dragger.drag_piece(sq.piece, row, col)
                        # คำนวณ legal moves
                        self.game.highlighted_moves = sq.piece.valid_moves(self.game.board, (row, col))
                # ระหว่างลาก
                elif event.type == pygame.MOUSEMOTION:
                    mx, my = event.pos
                    self.game.dragger.update_mouse((mx, my))

                # วาง piece
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.game.dragger.dragging:
                        mx, my = event.pos
                        nr, nc = my // self.game.SQSIZE, mx // self.game.SQSIZE

                        # ถ้าตำแหน่งปล่อยอยู่ใน highlighted_moves (legal move) ให้ย้าย
                        if (nr, nc) in self.game.highlighted_moves:
                            self.game.board.move_piece(self.game.dragger.piece, (nr, nc))
                            # สลับคนเล่นก็ต่อเมื่อย้ายจริง
                            self.game.next_player = 'black' if self.game.next_player == 'white' else 'white'

                        # ไม่ว่าจะย้ายได้หรือไม่ ก็ดับการลากและล้าง highlight
                        self.game.dragger.undrag_piece()
                        self.game.highlighted_moves = []


            # วาดทุกอย่างตามลำดับ
            self.game.show_back_ground(self.screen)
            self.game.show_piece()
            self.game.show_available_moves()

            # อัปเดตหน้าจอครั้งเดียว
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main = Main()
    main.mainloop()
    pygame.quit()