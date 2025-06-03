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
        stage_names = ["cavern", "underwater", "forest", "sky", "space"] 
        platform_sets = [
            
            [     
            (700, 830, 0.85),  
            (1050, 690, 0.8),   
            (900, 540, 0.75),  
            (900, 360, 0.9),   
            (1300, 190, 0.4),  
            (1750, 90, 0.3),   
            ],

            [
                (200, 850, 1.2),
                (550, 675, 0.9),
                (200, 580, 0.9),
                (200, 400, 0.9),
                (620, 250, 0.8),
                (1000, 400, 1.2),
                (1300, 300, 1.1),
                (1300, 100, 1.1)
            ],

            [
                (200, 980, 1.1),    
                (600, 840, 0.9),         
                (1000, 840, 0.8),      
                (600, 700, 0.8),        
                (600, 550, 0.75),       
                (950, 550, 0.8),        
                (700, 400, 0.75),      
                (1100, 400, 0.75),    
                (950, 270, 0.2),        
                (1200, 130, 0.2),       
            ],


            [
                (400, 750, 1),   
                (700, 600, 1),  
                (1000, 450, 1),  
                (1300, 300, 1), 
                (1600, 150, 1), 
                (1350, 50, 1),   
                (1050, 200, 1), 
                (750, 350, 1),   
                (450, 500, 1), 
                (250, 650, 1),  
                (600, 800, 1),   
            ],

            [
                (700, 730, 0.9),    
                (950, 600, 0.9),    
                (1200, 470, 1.1),    
                (950, 370, 0.9),    
                (700, 450, 1),     
                (450, 320, 0.9),   
                (700, 200, 1),    
                (950, 120, 1.2),    
                (1200, 70, 1),     
                (1000, 220, 0.8),    
                (800, 300, 0.9),    
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