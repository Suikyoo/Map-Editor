import pygame, editor

class Program:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 600))
        self.editor = editor.Editor(self.screen.get_size())

    def update(self):
        self.editor.update(self.screen)

Program().update()
