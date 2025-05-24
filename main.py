import pygame
import random
import time
import math
import os
from sprites import Player, Background, BackgroundManager, Popup

# screen setup
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont("Arial", 40)
SCREEN_HEIGHT = 1020
SCREEN_WIDTH = 1920
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

# background setup
background_paths = [
    "cavern.png",  #https://assetstore.unity.com/packages/tools/sprite-management/2d-cave-parallax-background-149247 credit
    "underwater.png",  # https://craftpix.net/freebies/free-underwater-world-pixel-art-backgrounds/ credit
    "forest.png",  # https://www.freepik.com/free-photos-vectors/sprite-forest-background credit
    "sky.png",  # https://craftpix.net/freebies/free-sky-with-clouds-background-pixel-art-set/ credit
    "space.png"  # https://opengameart.org/content/space-star-background credit
]
bg_manager = BackgroundManager(background_paths, 1.0)

# loading screen setup
loading_screen = Popup("loading.png", 0.875)
settings_screen = Popup("settings.png", 0.875)
changing_screen = Popup("changing.png", 0.875)
customize_screen = Popup("customize.png", 0.875)
rules_screen = Popup("rules.png", 0.875)
play_button = my_font.render("play", True, (0, 0, 0))
play_button_rect = play_button.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
settings_button = my_font.render("settings", True, (0, 0, 0))
settings_button_rect = settings_button.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 13 / 22))
customize_button = my_font.render("customize", True, (0, 0, 0))
customize_button_rect = customize_button.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 15 / 22))
rules_button = my_font.render("rules", True, (0, 0, 0))
rules_button_rect = rules_button.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 17 / 22))
quit_button = my_font.render("quit", True, (0, 0, 0))
quit_button_rect = quit_button.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 19 / 22))
back_text = my_font.render("back", False, (0, 0, 0))
back_text_rect = back_text.get_rect(center=(SCREEN_WIDTH / 11, SCREEN_HEIGHT * 14 / 15))
paused_text = my_font.render("paused", True, (0, 0, 0))
paused_text_rect = paused_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

# game settings
valid = True  # game running
load = True  # loading screen
run = False  # in a stage
settings = False  # changing settings
customize = False  # customizing character
rules = False  # rules page
pause = False  # paused

# physics components
gravity = 1500
jump_strength = 750
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
start_pause_time = time.time()

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
changing_duplicate = False

# clock text
timer = my_font.render(f"{elapsed_time}", True, (255, 255, 255))
timer_rect = timer.get_rect(center=(10, 20))

# keybind changing text
changing_text = my_font.render("press a key to change the keybind", True, (0, 0, 0))
changing_text_rect = changing_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
changing_error_text = my_font.render("the same key cannot be used for more than one keybind", True, (255, 0, 0))
changing_error_text_rect = changing_error_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 5))

# loads sprite
a = Player(x_position, y_position, "idle", 0.135)

while valid:
    dt = clock.tick(120) / 1000  # delta time in seconds
    keys = pygame.key.get_pressed()  # list of all keys; used for detection

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            valid = False
            run = False
            pause = False
            settings = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # to pause
                if pause:
                    pause = False
                else:
                    pause = True
                    start_pause_time = time.time()
            elif event.key == jump_key:  # to jump; idk why it cannot use keys[]
                jumping = True
            elif keys[left_key]:  # to move left
                moving_left = True
            elif keys[right_key]:  # to move right
                moving_right = True
        elif event.type == pygame.KEYUP:
            if event.key == jump_key:  # to stop jumping
                jumping = False
            elif keys[left_key]:  # to stop moving left
                moving_left = False
            elif keys[right_key]:  # to stop moving right
                moving_right = False

        if load:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    run = True
                    load = False
                if settings_button_rect.collidepoint(event.pos):
                    settings = True
                    load = False
                if customize_button_rect.collidepoint(event.pos):
                    customize = True
                    load = False
                if rules_button_rect.collidepoint(event.pos):
                    rules = True
                    load = False
                if quit_button_rect.collidepoint(event.pos):
                    valid = False
                    load = False

        if settings:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if change_right_rect.collidepoint(event.pos) and not changing_keys:  # changing right keybind
                    changing_right = True
                    changing_keys = True
                elif change_left_rect.collidepoint(event.pos) and not changing_keys:  # changing left keybind
                    changing_left = True
                    changing_keys = True
                elif change_jump_rect.collidepoint(event.pos) and not changing_keys:  # changing jump keybind
                    changing_jump = True
                    changing_keys = True
            if event.type == pygame.KEYDOWN:
                if changing_right and changing_keys:  # change right keybind
                    if not event.key == left_key and not event.key == jump_key:  # redo right keybind until no duplicate
                        right_key = event.key
                        changing_right = False
                        changing_keys = False
                        changing_duplicate = False
                    else:
                        changing_duplicate = True
                elif changing_left and changing_keys:  # change left keybind
                    if not event.key == right_key and not event.key == jump_key:  # redo left keybind until no duplicate
                        left_key = event.key
                        changing_left = False
                        changing_keys = False
                        changing_duplicate = False
                    else:
                        changing_duplicate = True
                elif changing_jump and changing_keys:  # change jump keybind
                    if not event.key == left_key and not event.key == right_key:  # redo jump keybind until no duplicate
                        jump_key = event.key
                        changing_jump = False
                        changing_keys = False
                        changing_duplicate = False
                    else:
                        changing_duplicate = True

    # updates if keybind gets changed
    change_right = my_font.render(f"right keybind: {pygame.key.name(right_key)}", True, (0, 0, 0))
    change_right_rect = change_right.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 6))
    change_left = my_font.render(f"left keybind: {pygame.key.name(left_key)}", True, (0, 0, 0))
    change_left_rect = change_left.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    change_jump = my_font.render(f"jump keybind: {pygame.key.name(jump_key)}", True, (0, 0, 0))
    change_jump_rect = change_jump.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 6))

    if True:
        screen.fill((0, 0, 0))  # refreshes the screen

        if not run or pause:
            pause_time = int(time.time() - start_pause_time)  # pause duration
        else:
            # elapsed time
            elapsed_seconds = int(time.time() - start_time) - pause_time  # unpause duration
            elapsed_minutes = int(elapsed_seconds/60)
            elapsed_seconds %= 60
            if elapsed_minutes < 10:
                elapsed_minutes = "0" + str(elapsed_minutes)
            if elapsed_seconds < 10:
                elapsed_seconds = "0" + str(elapsed_seconds)
            elapsed_time = str(elapsed_minutes) + ":" + str(elapsed_seconds)
            timer = my_font.render(f"{elapsed_time}", True, (255, 255, 255))

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
                bg_manager.next()  # switch background
                y_position = SCREEN_HEIGHT - a.surface.get_height()  # respawn at bottom
                velocity_y = 0
                on_ground = False
            elif y_position >= SCREEN_HEIGHT - a.surface.get_height():
                y_position = SCREEN_HEIGHT - a.surface.get_height()
                velocity_y = 0
                on_ground = True
            else:
                on_ground = False

            # update sprite
            if run:
                a.move(x_position, y_position)

    # draw
    bg_manager.draw(screen)

    if load:
        loading_screen.draw(screen)
        screen.blit(play_button, play_button_rect)
        screen.blit(settings_button, settings_button_rect)
        screen.blit(customize_button, customize_button_rect)
        screen.blit(rules_button, rules_button_rect)
        screen.blit(quit_button, quit_button_rect)

    if run:
        screen.blit(timer, timer_rect)
        sprite_image = pygame.image.load("Sprites/Misc/cavernPlatform.png")
        screen.blit(a.surface, a.position())

    if settings:
        settings_screen.draw(screen)
        screen.blit(change_right, change_right_rect)
        screen.blit(change_left, change_left_rect)
        screen.blit(change_jump, change_jump_rect)
        screen.blit(back_text, back_text_rect)
        if event.type == pygame.MOUSEBUTTONDOWN: # cannot go back if changing keybinds
            if back_text_rect.collidepoint(event.pos):
                settings = False
                load = True

    if changing_keys:
        changing_screen.draw(screen)
        screen.blit(changing_text, changing_text_rect)
        if changing_duplicate:
            screen.blit(changing_error_text, changing_error_text_rect)

    if customize:
        customize_screen.draw(screen)
        screen.blit(back_text, back_text_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_text_rect.collidepoint(event.pos):
                customize = False
                load = True

    if rules:
        rules_screen.draw(screen)
        screen.blit(back_text, back_text_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_text_rect.collidepoint(event.pos):
                rules = False
                load = True

    if pause:
        screen.blit(paused_text, paused_text_rect)

    pygame.display.flip()