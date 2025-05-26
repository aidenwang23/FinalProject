import pygame
import random
import time
import math
import os
from sprites import Player, Background, BackgroundManager, Popup, Platform, Heart

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
stage_names = ["cavern", "underwater", "forest", "sky", "space"]

# screen setup
loading_screen = Popup("loading.png", 1)
subject_screen = Popup("subject.png", 1)
settings_screen = Popup("settings.png", 1)
changing_screen = Popup("changing.png", 1)
customize_screen = Popup("customize.png", 1)
rules_screen = Popup("rules.png", 1)
question_screen = Popup("question.png", 1)
paused_screen = Popup("paused.png", 1)
end_screen = Popup("end.png", 1)

# game settings
valid = True  # game running
load = True  # loading screen
run = False  # in a stage
select = False # selecting subject
subject = None # selected subject
question = False # answering question
settings = False  # changing settings
customize = False  # customizing character
rules = False  # rules page
pause = False  # paused
stage = 0 
lives = 10
start_lives = lives
win = False # completed
lose = False # lost

# question setup
math_topics = ["algebra", "geometry", "statistics", "trigonometry", "calculus"]
science_topics = ["biology", "earthScience", "environmentalScience", "chemistry", "physics"]
topic = None
questions = []
answer_As = []
answer_Bs = []
answer_Cs = []
answer_Ds = []
correct_answers = []
uploaded = False
answer_choice = None
incorrect_choices = []

# physics components
gravity = 1500
jump_strength = 775
velocity_y = 0
on_ground = True
on_platform = False
landed = False

# sprite location
x_position = SCREEN_WIDTH / 2
y_position = SCREEN_HEIGHT

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
timer = my_font.render("00:00", True, (255, 255, 255))
timer_rect = timer.get_rect(topright=(SCREEN_WIDTH, 0))

# keybind changing text
changing_text = my_font.render("press a key to change the keybind", True, (0, 0, 0))
changing_text_rect = changing_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
changing_error_text = my_font.render("the same key cannot be used for more than one keybind", True, (255, 0, 0))
changing_error_text_rect = changing_error_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 5))

# loads sprite
a = Player(x_position, y_position, "idle.png", 0.135)

# platforms
platforms = [
    Platform(425, 800, f"{stage_names[stage]}Platform.png", 2),
    Platform(700, 630, f"{stage_names[stage]}Platform.png", 2),
    Platform(900, 465, f"{stage_names[stage]}Platform.png", 2),
    Platform(1100, 330, f"{stage_names[stage]}Platform.png", 2),
    Platform(1300, 150, f"{stage_names[stage]}Platform.png", 2)
]

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
            if event.key == pygame.K_ESCAPE:
                if pause and not run:
                    pause = False
                    run = True
                elif not pause and run:
                    pause = True
                    run = False
                    start_pause_time = time.time()
            elif event.key == jump_key:
                jumping = True
            elif keys[left_key]:
                moving_left = True
            elif keys[right_key]:
                moving_right = True
            if changing_right and changing_keys:
                if not event.key == left_key and not event.key == jump_key and not event.key == pygame.K_ESCAPE:
                    right_key = event.key
                    changing_right = False
                    changing_keys = False
                    changing_duplicate = False
                else:
                    changing_duplicate = True
            elif changing_left and changing_keys:
                if not event.key == right_key and not event.key == jump_key and not event.key == pygame.K_ESCAPE:
                    left_key = event.key
                    changing_left = False
                    changing_keys = False
                    changing_duplicate = False
                else:
                    changing_duplicate = True
            elif changing_jump and changing_keys:
                if not event.key == left_key and not event.key == right_key and not event.key == pygame.K_ESCAPE:
                    jump_key = event.key
                    changing_jump = False
                    changing_keys = False
                    changing_duplicate = False
                else:
                    changing_duplicate = True
        elif event.type == pygame.KEYUP:
            if event.key == jump_key:
                jumping = False
            elif keys[left_key]:
                moving_left = False
            elif keys[right_key]:
                moving_right = False
            

    if True:
        screen.fill((0, 0, 0))

        if pause or not run:
            pause_time = int(time.time() - start_pause_time)
        elif run or question:
            elapsed_seconds = int(time.time() - start_time) - pause_time
            pause_time = 0
            elapsed_minutes = int(elapsed_seconds / 60)
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

            a.move(x_position, y_position)
            player_rect = a.rect

            # horizontal collision
            for platform in platforms:
                platform_rect = platform.rect
                if player_rect.colliderect(platform_rect):
                    if x_position < platform_rect.centerx:
                        x_position = platform_rect.left - a.image_size[0] // 2
                    else:
                        x_position = platform_rect.right + a.image_size[0] // 2
                    a.move(x_position, y_position)
                    player_rect = a.rect

            if (on_ground or on_platform) and jumping:
                velocity_y = -jump_strength
                on_ground = False
                on_platform = False
                landed = False

            velocity_y += gravity * dt
            y_position += velocity_y * dt

            a.move(x_position, y_position)
            player_rect = a.rect

            # horizontal boundary
            if x_position < a.surface.get_width():
                x_position = a.surface.get_width()
            elif x_position > SCREEN_WIDTH - a.surface.get_width():
                x_position = SCREEN_WIDTH - a.surface.get_width()

            # vertical boundary
            if y_position < 0:
                if stage < 4:
                    stage+=1
                else: 
                    win = True
                    run = False
                bg_manager.next()
                uploaded = False
                x_position = SCREEN_WIDTH / 2
                y_position = SCREEN_HEIGHT - a.surface.get_height()
                velocity_y = 0
                on_ground = False
            elif y_position >= SCREEN_HEIGHT - a.surface.get_height():
                y_position = SCREEN_HEIGHT - a.surface.get_height()
                velocity_y = 0
                on_ground = True
            
            # platforms
            platforms = [
                Platform(425, 800, f"{stage_names[stage]}Platform.png", 2),
                Platform(700, 630, f"{stage_names[stage]}Platform.png", 2),
                Platform(900, 465, f"{stage_names[stage]}Platform.png", 2),
                Platform(1100, 330, f"{stage_names[stage]}Platform.png", 2),
                Platform(1300, 150, f"{stage_names[stage]}Platform.png", 2)
            ]

            # vertical collision
            for platform in platforms:
                platform_rect = platform.rect
                if player_rect.colliderect(platform_rect):
                    if velocity_y > 0 and player_rect.bottom <= platform_rect.top + 10:
                        y_position = platform_rect.top - a.image_size[1] // 2
                        velocity_y = 0
                        on_platform = True
                        if not landed:
                            question = True
                            run = False
                            landed  = True
                    elif velocity_y < 0 and player_rect.top >= platform_rect.bottom - 10:
                        y_position = platform_rect.bottom + a.image_size[1] // 2
                        velocity_y = 0
                        on_platform = False
                    a.move(x_position, y_position)
                    player_rect = a.rect

            if subject == "math":
                topic = math_topics[stage]
            elif subject == "science":
                topic = science_topics[stage]

            if not uploaded:
                if subject == "math":
                    file = open(f"Questions/Math/{topic}.txt", "r")
                    lines = file.readlines()
                    for i in range(0, len(lines), 7):
                        questions.append(lines[i].strip())
                        answer_As.append(lines[i+1].strip())
                        answer_Bs.append(lines[i+2].strip())
                        answer_Cs.append(lines[i+3].strip())
                        answer_Ds.append(lines[i+4].strip())
                        correct_answers.append(lines[i+5].strip())
                    uploaded = True
                elif subject == "science":
                    file = open(f"Questions/Science/{topic}.txt", "r")
                    lines = file.readlines()
                    for i in range(0, len(lines), 7):
                        questions.append(lines[i].strip())
                        answer_As.append(lines[i+1].strip())
                        answer_Bs.append(lines[i+2].strip())
                        answer_Cs.append(lines[i+3].strip())
                        answer_Ds.append(lines[i+4].strip())
                        correct_answers.append(lines[i+5].strip())
                    uploaded = True

            if(len(questions) > 0):
                index = random.randint(0,len(questions) - 1)
                current_question = {
                    "question": questions[index],
                    "choiceA": answer_As[index],
                    "choiceB": answer_Bs[index],
                    "choiceC": answer_Cs[index],
                    "choiceD": answer_Ds[index],
                    "correctChoice": correct_answers[index]
                }

            question_text = my_font.render(current_question["question"], True, (0, 0, 0))
            question_text_rect = question_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 5))
            choiceA_text = my_font.render(current_question["choiceA"], True, (0, 0, 0))
            choiceA_text_rect = choiceA_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 13 / 22))
            choiceB_text = my_font.render(current_question["choiceB"], True, (0, 0, 0))
            choiceB_text_rect = choiceB_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 15 / 22))
            choiceC_text = my_font.render(current_question["choiceC"], True, (0, 0, 0))
            choiceC_text_rect = choiceC_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 17 / 22))
            choiceD_text = my_font.render(current_question["choiceD"], True, (0, 0, 0))
            choiceD_text_rect = choiceD_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 19 / 22))

            if elapsed_minutes == 20:
                lose = True
            if win or lose:
                run = False
                question = False

            if run:
                a.move(x_position, y_position)

        if not win and not lose:
            bg_manager.draw(screen)

        if load:
            loading_screen.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 550 < mouse_x < 1370 and 430 < mouse_y < 535:
                    select = True
                    load = False
                elif 550 < mouse_x < 1370 and 545 < mouse_y < 650:
                    settings = True
                    load = False
                elif 550 < mouse_x < 1370 and 660 < mouse_y < 765:
                    customize = True
                    load = False
                elif 550 < mouse_x < 1370 and 775 < mouse_y < 880:
                    rules = True
                    load = False
                elif 550 < mouse_x < 1370 and 890 < mouse_y < 995:
                    valid = False
                    load = False


        if select:
            subject_screen.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 550 < mouse_x < 1370 and 500 < mouse_y < 605:
                    subject = "science"
                    run = True
                    select = False
                elif 550 < mouse_x < 1370 and 675 < mouse_y < 780:
                    subject = "math"
                    run = True
                    select = False
                elif 10 < mouse_x < 160 and 880 < mouse_y < 1015:
                    select = False
                    load = True

        if run:
            screen.blit(timer, timer_rect)
            for platform in platforms:
                platform.draw(screen)
            heart_x = 0
            for i in range(lives):
                full_heart = Heart(heart_x, 0, "fullHeart.png", 0.2)
                full_heart.draw(screen)
                heart_x += 37.5
            for i in range(start_lives - lives):
                empty_heart = Heart(heart_x, 0, "emptyHeart.png", 0.2)
                empty_heart.draw(screen)
                heart_x += 37.5
            heart_x = 0
            screen.blit(a.surface, a.position())

        if question:
            question_screen.draw(screen)
            screen.blit(question_text, question_text_rect)
            screen.blit(choiceA_text, choiceA_text_rect)
            screen.blit(choiceB_text, choiceB_text_rect)
            screen.blit(choiceC_text, choiceC_text_rect)
            screen.blit(choiceD_text, choiceD_text_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if choiceA_text_rect.collidepoint(event.pos):
                    answer_choice = "A"
                elif choiceB_text_rect.collidepoint(event.pos):
                    answer_choice = "B"
                elif choiceC_text_rect.collidepoint(event.pos):
                    answer_choice = "C"
                elif choiceD_text_rect.collidepoint(event.pos):
                    answer_choice = "D"
            elif event.type == pygame.MOUSEBUTTONUP:
                if answer_choice == current_question["correctChoice"]:
                    question = False
                    run = True
                    answer_choice = None
                    incorrect_choices.clear()
                    if len(questions) > 0:
                        questions.pop(index)
                        answer_As.pop(index)
                        answer_Bs.pop(index)
                        answer_Cs.pop(index)
                        answer_Ds.pop(index)
                        correct_answers.pop(index)
                elif answer_choice != None:
                    if answer_choice not in incorrect_choices:
                        incorrect_choices.append(answer_choice)
                        if answer_choice == "A":
                            choiceA_text = my_font.render(current_question["choiceA"], True, (255, 0, 0))
                        elif answer_choice == "B":
                            choiceB_text = my_font.render(current_question["choiceB"], True, (255, 0, 0))
                        elif answer_choice == "C":
                            choiceC_text = my_font.render(current_question["choiceC"], True, (255, 0, 0))
                        elif answer_choice == "D":
                            choiceD_text = my_font.render(current_question["choiceD"], True, (255, 0, 0))
                        lives-=1
                        if lives <= 0:
                            lose = True
                        answer_choice = None

        if pause:
            paused_screen.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 550 < mouse_x < 1370 and 500 < mouse_y < 605:
                    settings = True
                    run = False
                elif 550 < mouse_x < 1370 and 675 < mouse_y < 780:
                    load = True
                    pause = False
                    run = False

        if settings:
            settings_screen.draw(screen)
            change_right = my_font.render(pygame.key.name(right_key), True, (0, 0, 0))
            change_right_rect = change_right.get_rect(center=(1405, 560))
            change_left = my_font.render(pygame.key.name(left_key), True, (0, 0, 0))
            change_left_rect = change_left.get_rect(center=(1405, 675))
            change_jump = my_font.render(pygame.key.name(jump_key), True, (0, 0, 0))
            change_jump_rect = change_jump.get_rect(center=(1405, 790))
            screen.blit(change_right, change_right_rect)
            screen.blit(change_left, change_left_rect)
            screen.blit(change_jump, change_jump_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 1215 < mouse_x < 1595 and 510 < mouse_y < 615 and not changing_keys:
                    changing_right = True
                    changing_keys = True
                elif 1215 < mouse_x < 1595 and 625 < mouse_y < 730 and not changing_keys:
                    changing_left = True
                    changing_keys = True
                elif 1215 < mouse_x < 1595 and 740 < mouse_y < 845 and not changing_keys:
                    changing_jump = True
                    changing_keys = True
                elif 10 < mouse_x < 160 and 880 < mouse_y < 1015 and not pause:
                    settings = False
                    load = True
                elif 10 < mouse_x < 160 and 880 < mouse_y < 1015 and pause:
                    settings = False

        if changing_keys:
            changing_screen.draw(screen)
            screen.blit(changing_text, changing_text_rect)
            if changing_duplicate:
                screen.blit(changing_error_text, changing_error_text_rect)

        if customize:
            customize_screen.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 10 < mouse_x < 160 and 880 < mouse_y < 1015:
                        customize = False
                        load = True

        if rules:
            rules_screen.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 10 < mouse_x < 160 and 880 < mouse_y < 1015:
                        rules = False
                        load = True

        if win:
            end_screen.draw(screen)
        
        if lose: 
            end_screen.draw(screen)

        pygame.display.flip()