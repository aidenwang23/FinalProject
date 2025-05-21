import pygame
import random
import time
import math
import os
from sprite import Player

# screen setup
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont("Arial", 40)
SCREEN_HEIGHT = 1020
SCREEN_WIDTH = 1920
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

# game settings
valid = True
run = False
pause = False
# physics components
gravity = 1500
x_position = SCREEN_HEIGHT/2
y_position = SCREEN_WIDTH/2
# time
clock = pygame.time.Clock()
start_time = time.time()
pause_time = 0
# keybinds
left = False
right = False

# display texts
display_time = my_font.render("0", True, (0, 0, 0))
display_time_rect = display_time.get_rect(center = (10, 20))
test = my_font.render("paused", True, (0, 0, 0))
test_rect = test.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# loads sprite
a = Player(x_position, y_position, 0.2)

while valid: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            valid = False
            run = False
            pause = False
        # press down keys
        elif event.type == pygame.KEYDOWN:
            # escape key to pause/unpause
            if event.key == pygame.K_ESCAPE:
                # to unpause
                if pause:
                    pause = False
                # to pause
                else:
                    pause = True
                    start_pause_time = time.time()
            # a or left arrow key to move left
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left = True
            # d or right arrow key to move right
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right = True
            # space or up arrow key to jump
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                acceleration = -gravity # ill fix this later (jumping)
        # release keys
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right = False

    if True: # change to run after
        if pause:
            pause_time = int(time.time() - start_pause_time)
        else:
            # displays the time elapsed
            elapsed_time = int(time.time() - start_time) - pause_time
            display_time = my_font.render(f"{elapsed_time}", True, (0, 0, 0))
            # sets horizontal boundaries
            if x_position < 0:
                x_position = 0
            elif x_position > SCREEN_WIDTH: 
                x_position = SCREEN_WIDTH
            # sets vertical boundaries
            if y_position < 0:
                y_position = 0
            elif y_position > SCREEN_HEIGHT:
                y_position = SCREEN_HEIGHT
            # moves horizontally
            if left:
                x_position-=5
            elif right:
                x_position+=5

        # moves sprite
        a.move(x_position, y_position)

    screen.fill((255, 255, 255))
    screen.blit(display_time, display_time_rect)
    screen.blit(a.surface, a.position())
    
    if pause:
        screen.blit(test, test_rect)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()