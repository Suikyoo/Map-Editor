import pygame, sys
from scripts import editor
pygame.init()

class Program:
    def __init__(self):
        self.screen = pygame.display.set_mode((1100, 600))
        pygame.mouse.set_visible(False)

        self.editor = editor.Editor(self.screen.get_size())
        self.clock = pygame.time.Clock()

    def start(self):
        self.update()

    def update(self):
        while True:
            #events
            self.editor.pre_event_handler()
            for i in pygame.event.get():
                self.editor.event_handler(i)
                if i.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() * 0.001
            self.editor.update(self.screen, dt)
            pygame.display.update()

Program().start()
