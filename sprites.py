import pygame
import math
import random

SCREEN_HEIGHT = 1020
SCREEN_WIDTH = 1920

class Player:
    def __init__(self, x, y, image_path, scale):
        self.image = pygame.image.load(f"Sprites/Character/{image_path}")
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect(midbottom=(x, y))

    def move(self, new_x, new_y):
        self.rect.midbottom = (new_x, new_y)

    def position(self):
        return self.rect.topleft

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
    
    def restart(self):
        self.index = 0
    
class Popup:
    def __init__(self, image_path, scale):
        self.image = pygame.image.load(f"Sprites/Screens/{image_path}")
        self.image = pygame.transform.scale_by(self.image, scale)
        self.image_size = self.image.get_size()
    
    def position(self):
        return (SCREEN_WIDTH/2-int(self.image_size[0] / 2), SCREEN_HEIGHT/2-int(self.image_size[1] / 2))

    def draw(self, screen):
        screen.blit(self.image, self.position())

class Platform:
    def __init__(self, x, y, image_path, scale):
        self.image = pygame.image.load(f"Sprites/Platforms/{image_path}")
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def generate_platforms(stage_index):

        #space: https://opengameart.org/content/space-star-background
        #sky: https://free-game-assets.itch.io/free-sky-with-clouds-background-pixel-art-set
        #cavern: https://assetstore.unity.com/packages/tools/sprite-management/2d-cave-parallax-background-149247
        #forest: https://itch.io/games-like/44717/day-light-forest-background
        #underwater: https://craftpix.net/freebies/free-underwater-world-pixel-art-backgrounds/
        stage_names = ["cavern", "underwater", "forest", "sky", "space"] 
        platform_sets = [
            # Set 1: Straight vertical climb 
            [
                (960, 820, 1.5),
                (960, 640, 1.5),
                (960, 460, 1.5),
                (960, 280, 1.5),
                (960, 100, 1.5),
            ],
            # Set 2: Diagonal rightward climb
            [
                (960, 820, 1.5),
                (1100, 650, 1.5),
                (1240, 480, 1.5),
                (1380, 310, 1.5),
                (1520, 140, 1.5),
            ],
            # Set 3: Diagonal leftward climb
            [
                (960, 850, 1.5),
                (820, 680, 1.5),
                (680, 510, 1.5),
                (540, 340, 1.5),
                (400, 170, 1.5),
            ],
            # Set 4: Zig-zag pattern
            [
                (960, 740, 1.5),   
                (680, 570, 1.5),    
                (900, 390, 1.5),  
                (640, 220, 1.5),  
                (1000, 100, 1.5),  
            ],
            # Set 5: Mixed offsets
            [
                (960, 870, 1.5),  
                (1000, 700, 1.5),  
                (700, 530, 1.5),  
                (1000, 360, 1.5),
                (650, 190, 1.5),   
            ],
        ]

        selected = random.choice(platform_sets)
        return [Platform(x, y, f"{stage_names[stage_index]}Platform.png", scale) for (x, y, scale) in selected]
    
class Heart:
    def __init__(self, x, y, image_path, scale):
        self.image = pygame.image.load(f"Sprites/Misc/{image_path}")
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)