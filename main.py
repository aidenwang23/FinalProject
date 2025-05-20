
import random
import time
import math
import os
# from sprites import 

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont("Arial", 50)

SCREEN_HEIGHT = 1020
SCREEN_WIDTH = 1920
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

run = True

while run: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False 

pygame.quit()