import pygame
from game import Game

class Main:
    WIDTH = 800
    HEIGHT = 800
    ROWS = 8
    COLS = 8

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (self.WIDTH, self.HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        running = True
        clock = pygame.time.Clock()  # เพื่อควบคุม FPS
        while running:
            # ตรวจสอบ event ต่างๆ
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            self.game.show_back_ground(self.screen)
            self.game.show_piece()
            self.game.show_available_moves()
            
            # อัปเดตหน้าจอ
            pygame.display.flip()
            
            # จำกัด FPS ที่ 60 frame ต่อวินาที
            clock.tick(60)




if __name__ == "__main__":
    main = Main()
    main.mainloop()
    pygame.quit()