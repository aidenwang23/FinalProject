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
valid = True # game running
run = False # in a stage
pause = False # paused
settings = False # changing settings

# physics components
gravity = 1500
jump_strength = 700
velocity_y = 0
on_ground = False

# sprite location
x_position = SCREEN_WIDTH / 2
y_position = SCREEN_HEIGHT / 2

# time
clock = pygame.time.Clock()
start_time = time.time()
pause_time = 0
elapsed_time = 0

# keybinds
left_key = pygame.K_LEFT
right_key = pygame.K_RIGHT
jump_key = pygame.K_UP

# movement states
moving_left = False
moving_right = False
jumping = False

# changing keybind states
changing_right = False
changing_left = False
changing_jump = False
changing_keys = False

# clock text
display_time = my_font.render(f"{elapsed_time}", True, (0, 0, 0))
display_time_rect = display_time.get_rect(center=(10, 20))

# paused screen text
paused_text = my_font.render("paused", True, (0, 0, 0))
paused_text_rect = paused_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

#settings screen text
settings_text = my_font.render("settings", True, (0, 0, 0))
settings_text_rect = settings_text.get_rect(center=(SCREEN_WIDTH/2, 20))
back_text = my_font.render("back", True, (0, 0, 0))
back_text_rect = back_text.get_rect(center=(40, SCREEN_HEIGHT-25))

# keybind changing text
change_right = my_font.render(f"right keybind: {pygame.key.name(right_key)}", True, (0, 0, 0))
change_right_rect = change_right.get_rect(center=(SCREEN_WIDTH/2, 20))
change_left = my_font.render(f"left keybind: {pygame.key.name(left_key)}", True, (0, 0, 0))
change_left_rect = change_left.get_rect(center=(SCREEN_WIDTH/2, 65))
change_jump = my_font.render(f"jump keybind: {pygame.key.name(jump_key)}", True, (0, 0, 0))
change_jump_rect = change_jump.get_rect(center=(SCREEN_WIDTH/2, 110))
changing_text = my_font.render("press a key to change the keybind", True, (0, 0, 0))
changing_text_rect = changing_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# loads sprite
a = Player(x_position, y_position, 0.2)

while valid:
    dt = clock.tick(120) / 1000  # delta time in seconds
    keys = pygame.key.get_pressed() # list of all keys; used for detection

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            valid = False
            run = False
            pause = False
            settings = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # to pause
                if pause:
                    pause = False
                else:
                    pause = True
                    start_pause_time = time.time()
            elif event.key == jump_key: # to jump; idk why it cannot use keys[]
                jumping = True
            elif keys[left_key]: # to move left
                moving_left = True
            elif keys[right_key]: # to move right
                moving_right = True
        elif event.type == pygame.KEYUP:
            if event.key == jump_key: # to stop jumping
                jumping = False
            elif keys[left_key]: # to stop moving left
                moving_left = False
            elif keys[right_key]: # to stop moving right
                moving_right = False
         
        if settings:
            if event.type == pygame.MOUSEBUTTONDOWN: # detect click location
                if change_right_rect.collidepoint(event.pos) and not changing_keys: # changing right keybind
                    changing_right = True
                    changing_keys = True
                elif change_left_rect.collidepoint(event.pos) and not changing_keys: # changing left keybind
                    changing_left = True
                    changing_keys = True
                elif change_jump_rect.collidepoint(event.pos) and not changing_keys: # changing jump keybind
                    changing_jump = True
                    changing_keys = True
            if event.type == pygame.KEYDOWN:
                if changing_right and changing_keys: # change right keybind
                    right_key = event.key
                    changing_right = False
                    changing_keys = False
                elif changing_left and changing_keys: # change left keybind
                    left_key = event.key
                    changing_left = False
                    changing_keys = False
                elif changing_jump and changing_keys: # changing jump keybind
                    jump_key = event.key
                    changing_jump = False
                    changing_keys = False

    # updates if keybind gets changed
    change_right = my_font.render(f"right keybind: {pygame.key.name(right_key)}", True, (0, 0, 0))
    change_right_rect = change_right.get_rect(center=(SCREEN_WIDTH/2, 20))
    change_left = my_font.render(f"left keybind: {pygame.key.name(left_key)}", True, (0, 0, 0))
    change_left_rect = change_left.get_rect(center=(SCREEN_WIDTH/2, 65))
    change_jump = my_font.render(f"jump keybind: {pygame.key.name(jump_key)}", True, (0, 0, 0))
    change_jump_rect = change_jump.get_rect(center=(SCREEN_WIDTH/2, 110))

    if True:
        if pause:
            pause_time = int(time.time() - start_pause_time) # pause duration
        else:
            # elapsed time
            elapsed_time = int(time.time() - start_time) - pause_time # unpause duration
            display_time = my_font.render(f"{elapsed_time}", True, (0, 0, 0))

            # horizontal movement
            if keys[left_key]:
                x_position -= 400 * dt
            if keys[right_key]:
                x_position += 400 * dt

            # gravity and vertical movement
            if on_ground and jumping:
                    velocity_y = -jump_strength
                    on_ground = False
            velocity_y += gravity * dt
            y_position += velocity_y * dt

            # horizontal bounds
            if x_position < a.surface.get_width():
                x_position = a.surface.get_width()
            elif x_position > SCREEN_WIDTH - a.surface.get_width():
                x_position = SCREEN_WIDTH - a.surface.get_width()

            # vertical bounds
            if y_position < 0:
                y_position = 0
            elif y_position >= SCREEN_HEIGHT - a.surface.get_height():
                y_position = SCREEN_HEIGHT - a.surface.get_height()
                velocity_y = 0
                on_ground = True
            else:
                on_ground = False

            # update sprite
            a.move(x_position, y_position)

    # draw
    screen.fill((255, 255, 255))
    screen.blit(a.surface, a.position())

    if run:
        screen.blit(display_time, display_time_rect)

    if not settings:
        screen.blit(settings_text, settings_text_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if settings_text_rect.collidepoint(event.pos):
                settings = True

    if settings:
        screen.blit(change_right, change_right_rect)
        screen.blit(change_left, change_left_rect)
        screen.blit(change_jump, change_jump_rect)
        screen.blit(back_text, back_text_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_text_rect.collidepoint(event.pos):
                settings = False

    if changing_keys:
        screen.blit(changing_text, changing_text_rect)

    if pause:
        screen.blit(paused_text, paused_text_rect)

    pygame.display.flip()