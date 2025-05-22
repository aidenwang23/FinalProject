import pygame
class background1:
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.image = pygame.image.load("pixel-art-game-background-underground-600nw-2389206031.png") #from shutterstock
        self.image = pygame.transform.scale_by(self.image, scale)
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
        self.surface = self.image

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])

    def position(self):
        return ((self.x - int(self.image_size[0] / 2)), (self.y - int(self.image_size[1] / 2)))