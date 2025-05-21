import pygame
import random
import time
import math
import os
from sprites import Player

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
jump_strength = 700
velocity_y = 0
on_ground = False

x_position = SCREEN_WIDTH / 2
y_position = SCREEN_HEIGHT / 2

# time
clock = pygame.time.Clock()
start_time = time.time()
pause_time = 0

# keybinds
left = False
right = False

# display texts
display_time = my_font.render("0", True, (0, 0, 0))
display_time_rect = display_time.get_rect(center=(10, 20))
test = my_font.render("paused", True, (0, 0, 0))
test_rect = test.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

# loads sprite
a = Player(x_position, y_position, 0.2)

while valid:
    dt = clock.tick(120) / 1000  # delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            valid = False
            run = False
            pause = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if pause:
                    pause = False
                else:
                    pause = True
                    start_pause_time = time.time()
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right = True
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if on_ground:
                    velocity_y = -jump_strength
                    on_ground = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right = False

    if True:  # replace with `if run:` when needed
        if pause:
            pause_time = int(time.time() - start_pause_time)
        else:
            # elapsed time
            elapsed_time = int(time.time() - start_time) - pause_time
            display_time = my_font.render(f"{elapsed_time}", True, (0, 0, 0))

            # horizontal movement
            if left:
                x_position -= 400 * dt
            if right:
                x_position += 400 * dt

            # gravity and vertical movement
            velocity_y += gravity * dt
            y_position += velocity_y * dt

            # floor collision
            if y_position >= SCREEN_HEIGHT - a.surface.get_height():
                y_position = SCREEN_HEIGHT - a.surface.get_height()
                velocity_y = 0
                on_ground = True
            else:
                on_ground = False

            # horizontal bounds
            if x_position < 0:
                x_position = 0
            elif x_position > SCREEN_WIDTH - a.surface.get_width():
                x_position = SCREEN_WIDTH - a.surface.get_width()

            # vertical bounds (ceiling)
            if y_position < 0:
                y_position = 0

            # update sprite
            a.move(x_position, y_position)

    # draw
    screen.fill((255, 255, 255))
    screen.blit(display_time, display_time_rect)
    screen.blit(a.surface, a.position())   

    if pause:
        screen.blit(test, test_rect)

    pygame.display.flip()
