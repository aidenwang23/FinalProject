import pygame
import math
import random

SCREEN_HEIGHT = 1020
SCREEN_WIDTH = 1920

class Player:
    def __init__(self, x, y, state, scale):
        self.x = x
        self.y = y
        self.image = pygame.image.load(f"Sprites/Character/{state}.png")
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
    
class Background:
    def __init__(self, image_path, scale):
        self.image = pygame.image.load(f"Sprites/Backgrounds/{image_path}")
        self.image = pygame.transform.scale_by(self.image, scale)
        self.image_size = self.image.get_size()

    def position(self):
        return (SCREEN_WIDTH/2-int(self.image_size[0] / 2), SCREEN_HEIGHT/2-int(self.image_size[1] / 2))

    def draw(self, screen):
        screen.blit(self.image, self.position())

class BackgroundManager:
    def __init__(self, image_paths, scale):
        self.backgrounds = [Background(path, scale) for path in image_paths]
        self.index = 0

    def draw(self, screen):
        self.backgrounds[self.index].draw(screen)

    def next(self):
        if self.index < len(self.backgrounds) - 1:
            self.index += 1
    
class LoadingScreen:
    def __init__(self, scale):
        self.image = pygame.image.load("Sprites/Screens/loading.png")
        self.image = pygame.transform.scale_by(self.image, scale)
        self.image_size = self.image.get_size()
    
    def position(self):
        return (SCREEN_WIDTH/2-int(self.image_size[0] / 2), SCREEN_HEIGHT/2-int(self.image_size[1] / 2))

    def draw(self, screen):
        screen.blit(self.image, self.position())