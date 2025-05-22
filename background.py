import pygame

class Background:
    def __init__(self, image_path, scale):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale_by(self.image, scale)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class BackgroundManager:
    def __init__(self, image_paths, scale):
        self.backgrounds = [Background(path, scale) for path in image_paths]
        self.index = 0

    def draw(self, screen):
        self.backgrounds[self.index].draw(screen)

    def next(self):
        if self.index < len(self.backgrounds) - 1:
            self.index += 1
