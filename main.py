import pygame
import random
import time
import math
import os
from sprites import Player, Background, BackgroundManager, Popup, Platform, Heart

def main():
    # screen setup
    pygame.init()
    pygame.font.init()
    SCREEN_HEIGHT = 1020
    SCREEN_WIDTH = 1920
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)

    # text fonts
    important_text_font = pygame.font.SysFont("Arial Bold", 250)
    time_display_font = pygame.font.SysFont("Arial Bold", 55)
    keybind_display_font = pygame.font.SysFont("Arial Bold", 60)
    keybind_text_font = pygame.font.SysFont("Arial Bold", 100)
    question_text_font = pygame.font.SysFont("Arial Bold", 70)
    answer_text_font = pygame.font.SysFont("Arial Bold", 45)
    subheading_text_font = pygame.font.SysFont("Arial Bold", 125)
    name_text_font = pygame.font.SysFont("Arial Bold", 75)
    credits_text_font = pygame.font.SysFont("Arial Bold", 55)
    rules_text_font = pygame.font.SysFont("Arial Bold", 55)
    title_text_font = pygame.font.SysFont("Arial Bold", 150)
    body_text_font = pygame.font.SysFont("Arial Bold", 70)

    # background setup
    background_paths = [
        "cavern.png",  # https://assetstore.unity.com/packages/tools/sprite-management/2d-cave-parallax-background-149247 credit
        "underwater.png",  # https://craftpix.net/freebies/free-underwater-world-pixel-art-backgrounds/ credit
        "forest.png",  # https://wallpapers.com/background/cartoon-forest-background-1920-x-1080-367aqc08v63mo7qc.html credit
        "sky.png",  # https://free-game-assets.itch.io/free-sky-with-clouds-background-pixel-art-set credit
        "space.png"  # https://opengameart.org/content/space-star-background credit
    ]
    bg_manager = BackgroundManager(background_paths, 1.0)

    # screen setup
    loading_screen = Popup("loading.png", 1)
    credits_screen = Popup("credits.png", 1)
    subject_screen = Popup("subject.png", 1)
    settings_screen = Popup("settings.png", 1)
    changing_screen = Popup("changing.png", 1)
    rules_screen = Popup("rules.png", 1)
    question_screen = Popup("question.png", 1)
    paused_screen = Popup("paused.png", 1)
    end_screen = Popup("end.png", 1)

    # game settings
    valid = True
    load = True
    credits = False
    run = False
    select = False
    subject = None
    question = False
    settings = False
    customize = False
    rules = False
    pause = False
    paused_to_settings = False
    stage = 0 
    lives = 3
    start_lives = lives
    win = False
    lose = False
    mouse_clicked = False
    changed_screens = False
    landed_platform = None

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
    answer_choice = None
    incorrect_choices = []
    question_lines = []
    correct_questions = 0

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

    # time setup
    clock = pygame.time.Clock()
    total_time = 0
    elapsed_minutes = 0
    elapsed_seconds = 0
    timer = time_display_font.render("00:00", True, (255, 255, 255))
    timer_rect = timer.get_rect(topright=(SCREEN_WIDTH, 5))
    last_active_time = None

    # keybinds (last saved)
    with open("config.txt", "r") as file:
        lines = file.readlines()
        right_key = int(lines[0].strip())
        left_key = int(lines[1].strip())
        jump_key = int(lines[2].strip())
    # character (last saved)
        character = str(lines[4].strip())

    # character setup
    characters = ["Bear", "Bunny", "Cat"]
    character_index = characters.index(character)
    character_scale = 1

    # movement states
    moving_left = False
    moving_right = False 
    jumping = False
    current_movement = None
    direction = None

    # changing keybind states
    changing_right = False
    changing_left = False
    changing_jump = False
    changing_keys = False
    changing_duplicate = False

    # loads sprite
    player = Player(x_position, y_position, f"{character}/idleRight.png", character_scale)

    # loads platforms
    platforms = Platform.generate_platforms(stage)

    while valid:
        dt = clock.tick(120) / 1000  # delta time in seconds
        keys = pygame.key.get_pressed()  # list of all keys; used for detection

        if changed_screens:
            mouse_clicked = False
            changed_screens = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                valid = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if run:
                        if pause:
                            pause = False
                        elif not pause:
                            pause = True
                elif event.key == jump_key:
                    jumping = True
                elif changing_keys:
                    if changing_right:
                        if not (event.key == left_key or event.key == jump_key or event.key == pygame.K_ESCAPE):
                            right_key = event.key
                            changing_right = False
                            changing_keys = False
                            changing_duplicate = False
                            settings = True
                        else:
                            changing_duplicate = True
                    elif changing_left:
                        if not (event.key == right_key or event.key == jump_key or event.key == pygame.K_ESCAPE):
                            left_key = event.key
                            changing_left = False
                            changing_keys = False
                            changing_duplicate = False
                            settings = True
                        else:
                            changing_duplicate = True
                    elif changing_jump:
                        if not (event.key == left_key or event.key == right_key or event.key == pygame.K_ESCAPE):
                            jump_key = event.key
                            changing_jump = False
                            changing_keys = False
                            changing_duplicate = False
                            settings = True
                        else:
                            changing_duplicate = True
                    with open("config.txt", "w") as file:
                        file.write(f"{str(right_key)}\n{str(left_key)}\n{str(jump_key)}\n\n{str(character)}")
            elif event.type == pygame.KEYUP:
                if event.key == jump_key:
                    jumping = False

        if valid:
            screen.fill((0, 0, 0))
            player_rect = player.rect
        
            # timer settings
            if (run or question) and not pause:
                if last_active_time == None:
                    last_active_time = time.time()
                current_time = time.time()
                total_time += current_time - last_active_time
                last_active_time = current_time
                elapsed_minutes = int(total_time) // 60
                elapsed_seconds = int(total_time) % 60
                if elapsed_minutes < 10:
                    elapsed_minutes = "0" + str(elapsed_minutes)
                if elapsed_seconds < 10:
                    elapsed_seconds = "0" + str(elapsed_seconds)
                elapsed_time = f"{elapsed_minutes}:{elapsed_seconds}"
                timer = time_display_font.render(f"{elapsed_time}", True, (255, 255, 255))
            else:
                last_active_time = None

            # character model scale (files are slightly smaller)
            character_scale = 0.125
            if character == "Bunny" or character == "Cat":
                character_scale *= (4 / 3)

            if run:
                # horizontal movement
                if keys[left_key]:
                    x_position -= 400 * dt
                    moving_left = True
                else: 
                    moving_left = False
                if keys[right_key]:
                    x_position += 400 * dt
                    moving_right = True
                else:
                    moving_right = False

                player.move(x_position, y_position)
                player_rect = player.rect

                # horizontal collision
                for platform in platforms:
                    platform_rect = platform.rect
                    if player_rect.colliderect(platform_rect):
                        if x_position < platform_rect.centerx:
                            x_position = platform_rect.left - player.rect.width // 2
                        else:
                            x_position = platform_rect.right + player.rect.width // 2
                        player.move(x_position, y_position)
                        player_rect = player.rect

                # vertical movement
                if (on_ground or on_platform) and jumping:
                    velocity_y = -jump_strength
                    on_ground = False
                    on_platform = False
                    landed = False
                velocity_y += gravity * dt
                y_position += velocity_y * dt

                player.move(x_position, y_position)
                player_rect = player.rect

                # horizontal boundary
                if x_position < player.image.get_width():
                    x_position = player.image.get_width()
                elif x_position > SCREEN_WIDTH - player.image.get_width():
                    x_position = SCREEN_WIDTH - player.image.get_width()

                # vertical boundary
                if y_position < 0:
                    if stage < 4:
                        stage+=1
                    else: 
                        win = True
                        run = False
                    bg_manager.next()
                    platforms = Platform.generate_platforms(stage) 
                    questions.clear()
                    answer_As.clear()
                    answer_Bs.clear()
                    answer_Cs.clear()
                    answer_Ds.clear()
                    correct_answers.clear()
                    question_lines.clear()
                    x_position = SCREEN_WIDTH / 2
                    y_position = SCREEN_HEIGHT - player.image.get_height()
                    velocity_y = 0
                    on_ground = False
                elif y_position >= SCREEN_HEIGHT - player.image.get_height():
                    y_position = SCREEN_HEIGHT - player.image.get_height()
                    velocity_y = 0
                    on_ground = True

                # vertical collision
                for platform in platforms:
                    platform_rect = platform.rect
                    if player_rect.colliderect(platform_rect):
                        if velocity_y > 0 and player_rect.bottom <= platform_rect.top + 15:
                            y_position = platform_rect.top
                            velocity_y = 0
                            on_platform = True
                            if not landed and len(questions) > 0:
                                question = True
                                run = False
                                landed = True
                                landed_platform = platform
                        elif velocity_y < 0 and player_rect.top >= platform_rect.bottom - 15:
                            y_position = platform_rect.bottom + player.rect.height
                            velocity_y = 0
                            on_platform = False

                        player.move(x_position, y_position)
                        player_rect = player.rect

                # question setup
                if subject == "Math":
                    topic = math_topics[stage]
                elif subject == "Science":
                    topic = science_topics[stage]

                # refill questions 
                if len(questions) <= 0:
                    with open(f"Questions/{subject}/{topic}.txt", "r") as file:
                        lines = file.readlines()
                        for i in range(0, len(lines), 7):
                            questions.append(lines[i].strip())
                            answer_As.append(lines[i+1].strip())
                            answer_Bs.append(lines[i+2].strip())
                            answer_Cs.append(lines[i+3].strip())
                            answer_Ds.append(lines[i+4].strip())
                            correct_answers.append(lines[i+5].strip())

                # choosing a question
                if not landed and len(questions) > 0:
                    index = random.randint(0, len(questions) - 1)
                    current_question = {
                        "question": questions[index],
                        "choiceA": answer_As[index],
                        "choiceB": answer_Bs[index],
                        "choiceC": answer_Cs[index],
                        "choiceD": answer_Ds[index],
                        "correctChoice": correct_answers[index]
                    }
                    question_lines.clear()
                    if len(current_question["question"]) > 75:
                        split = current_question["question"].rfind(" ", 0, 75)
                        question_lines.append(current_question["question"][:split])
                        question_lines.append(current_question["question"][split:])
                    else:
                        question_lines.append(current_question["question"])
                    choiceA_text = answer_text_font.render(current_question["choiceA"], True, (0, 0, 0))
                    choiceA_text_rect = choiceA_text.get_rect(center=(SCREEN_WIDTH / 2, 535))
                    choiceB_text = answer_text_font.render(current_question["choiceB"], True, (0, 0, 0))
                    choiceB_text_rect = choiceB_text.get_rect(center=(SCREEN_WIDTH / 2, 650))
                    choiceC_text = answer_text_font.render(current_question["choiceC"], True, (0, 0, 0))
                    choiceC_text_rect = choiceC_text.get_rect(center=(SCREEN_WIDTH / 2, 765))
                    choiceD_text = answer_text_font.render(current_question["choiceD"], True, (0, 0, 0))
                    choiceD_text_rect = choiceD_text.get_rect(center=(SCREEN_WIDTH / 2, 880))

            # movement for sprite display
            if moving_left:
                direction = "Left"
            elif moving_right:
                direction = "Right"
            if not (on_ground or on_platform):
                if velocity_y > 0:
                    current_movement = "fall"
                elif velocity_y < 0:
                    current_movement = "jump"
            elif moving_right:
                current_movement = "right"
            elif moving_left:
                current_movement = "left"
            else:
                current_movement = "idle"
            if direction == None:
                direction = "Right"
        
            # end conditions
            if int(elapsed_minutes) >= 20 and not (win or lose):
                lose = True
            if win or lose:
                run = False

        if load:
            loading_screen.draw(screen)
            name_text = important_text_font.render("QUIZ QUEST", True, (0, 0, 0))
            name_text_rect = name_text.get_rect(center=(SCREEN_WIDTH / 2, 255))
            screen.blit(name_text, name_text_rect)
            
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_clicked:
                mouse_clicked = True
                mouse_x, mouse_y = event.pos
                if name_text_rect.collidepoint(event.pos):
                    credits = True
                    load = False
                elif 550 <= mouse_x <= 1370 and 430 <= mouse_y <= 535:
                    select = True
                    load = False
                elif 550 <= mouse_x <= 1370 and 545 <= mouse_y <= 650:
                    settings = True
                    load = False
                elif 550 <= mouse_x <= 1370 and 660 <= mouse_y <= 765:
                    customize = True
                    load = False
                elif 550 <= mouse_x <= 1370 and 775 <= mouse_y <= 880:
                    rules = True
                    load = False
                elif 550 <= mouse_x <= 1370 and 890 <= mouse_y <= 995:
                    valid = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
                changed_screens = True

        if credits:
            credits_screen.draw(screen)

            line_count = 1
            credits_y = 80
            with open("credits.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line_count == 1 or line_count == 7 or line_count == 11:
                        credits_text = subheading_text_font.render(line.strip(), True, (0, 0, 0))
                        credits_text_rect = credits_text.get_rect(center=(SCREEN_WIDTH / 2, credits_y))
                        screen.blit(credits_text, credits_text_rect)
                        credits_y += 85
                    elif line_count == 2 or line_count == 4 or line_count == 8 or line_count == 12:
                        credits_text = name_text_font.render(line.strip(), True, (0, 0, 0))
                        credits_text_rect = credits_text.get_rect(center=(SCREEN_WIDTH / 2, credits_y))
                        screen.blit(credits_text, credits_text_rect)
                        credits_y += 60
                    elif line_count == 3 or line_count == 5 or line_count == 9 or line_count == 13 or line_count == 15:               
                        credits_text_font.set_italic(True)
                        if line_count == 15:
                            credits_y -= 15
                            credits_text_font.set_italic(False)
                        credits_text = credits_text_font.render(line.strip(), True, (0, 0, 0))
                        credits_text_rect = credits_text.get_rect(center=(SCREEN_WIDTH / 2, credits_y))
                        screen.blit(credits_text, credits_text_rect) 
                        credits_y += 75
                    else:
                        credits_text = credits_text_font.render(line.strip(), True, (0, 0, 0))
                        credits_text_rect = credits_text.get_rect(center=(SCREEN_WIDTH / 2, credits_y))
                        screen.blit(credits_text, credits_text_rect) 
                        credits_y += 35
                    line_count += 1

            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_clicked:
                mouse_clicked = True
                mouse_x, mouse_y = event.pos
                if 10 <= mouse_x <= 160 and 880 <= mouse_y <= 1015:
                    credits = False
                    load = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
                changed_screens = True

        if select:
            subject_screen.draw(screen)
            title_text = title_text_font.render("Subject Selection", True, (0, 0, 0))
            title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 285))
            screen.blit(title_text, title_text_rect)

            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_clicked:
                mouse_clicked = True
                mouse_x, mouse_y = event.pos
                if 550 <= mouse_x <= 1370 and 500 <= mouse_y <= 605:
                    subject = "Science"
                    run = True
                    select = False
                elif 550 <= mouse_x <= 1370 and 675 <= mouse_y <= 780:
                    subject = "Math"
                    run = True
                    select = False
                elif 10 <= mouse_x <= 160 and 880 <= mouse_y <= 1015:
                    select = False
                    load = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
                changed_screens = True

        if run:
            bg_manager.draw(screen)
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

            if current_movement == "right" or current_movement == "left":
                if (0 < total_time % 1 < 0.25) or (0.5 < total_time % 1 < 0.75):
                    player = Player(x_position, y_position, f"{character}/{current_movement}1.png", character_scale)
                elif (0.25 <= total_time % 1 <= 0.5) or (0.75 <= total_time % 1 < 1):
                    player = Player(x_position, y_position, f"{character}/{current_movement}2.png", character_scale)
            else:
                player = Player(x_position, y_position, f"{character}/{current_movement}{direction}.png", character_scale)
            screen.blit(player.image, player.position())


        if question:
            question_screen.draw(screen)

            question_y = 250
            if len(question_lines) > 1:
                for line in question_lines:
                    question_text = question_text_font.render(line, True, (0, 0, 0))
                    question_text_rect = question_text.get_rect(center=(SCREEN_WIDTH / 2, question_y))
                    screen.blit(question_text, question_text_rect)
                    question_y += 50
            elif len(question_lines) == 1:
                question_text = question_text_font.render(question_lines[0], True, (0, 0, 0))
                question_text_rect = question_text.get_rect(center=(SCREEN_WIDTH / 2, 275))
                screen.blit(question_text, question_text_rect)
            screen.blit(choiceA_text, choiceA_text_rect)
            screen.blit(choiceB_text, choiceB_text_rect)
            screen.blit(choiceC_text, choiceC_text_rect)
            screen.blit(choiceD_text, choiceD_text_rect)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
                mouse_x, mouse_y = event.pos
                if 550 <= mouse_x <= 1370 and 480 <= mouse_y <= 585:
                    answer_choice = "A"
                elif 550 <= mouse_x <= 1370 and 595 <= mouse_y <= 700:
                    answer_choice = "B"
                elif 550 <= mouse_x <= 1370 and 710 <= mouse_y <= 815:
                    answer_choice = "C"
                elif 550 <= mouse_x <= 1370 and 825 <= mouse_y <= 930:
                    answer_choice = "D"
                if answer_choice == current_question["correctChoice"]:
                    correct_questions += 1
                    question = False
                    run = True

                    if landed_platform:
                        platform_rect = landed_platform.rect
                        y_position = platform_rect.top
                        velocity_y = 0
                        on_platform = True
                        on_ground = False
                        landed = True
                        player.move(x_position, y_position)
                        landed_platform = None

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
                            choiceA_text = answer_text_font.render(current_question["choiceA"], True, (255, 0, 0))
                        elif answer_choice == "B":
                            choiceB_text = answer_text_font.render(current_question["choiceB"], True, (255, 0, 0))
                        elif answer_choice == "C":
                            choiceC_text = answer_text_font.render(current_question["choiceC"], True, (255, 0, 0))
                        elif answer_choice == "D":
                            choiceD_text = answer_text_font.render(current_question["choiceD"], True, (255, 0, 0))
                        lives-=1
                        if lives <= 0:
                            lose = True
                            question = False
                        answer_choice = None
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
                changed_screens = True

        if pause:
            paused_screen.draw(screen)
            title_text = title_text_font.render("Paused", True, (0, 0, 0))
            title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 300))
            screen.blit(title_text, title_text_rect)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 550 <= mouse_x <= 1370 and 500 <= mouse_y <= 605:
                    settings = True
                    run = False
                    paused_to_settings = True
                    pause = False
                elif 550 <= mouse_x <= 1370 and 675 <= mouse_y <= 780:
                    pause = False
                    load = True
                    main()
            elif event.type == pygame.MOUSEBUTTONUP:
                changed_screens = True

        if settings:
            settings_screen.draw(screen)
            title_text = title_text_font.render("Keybind Settings", True, (0, 0, 0))
            title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 200))
            body_text = body_text_font.render("Click on one of the following current keybinds to change", True, (0, 0, 0))
            body_text_rect = body_text.get_rect(center=(SCREEN_WIDTH / 2, 375))
            screen.blit(title_text, title_text_rect)
            screen.blit(body_text, body_text_rect)

            change_right = keybind_display_font.render(pygame.key.name(right_key), True, (0, 0, 0))
            change_right_rect = change_right.get_rect(center=(1405, 560))
            change_left = keybind_display_font.render(pygame.key.name(left_key), True, (0, 0, 0))
            change_left_rect = change_left.get_rect(center=(1405, 675))
            change_jump = keybind_display_font.render(pygame.key.name(jump_key), True, (0, 0, 0))
            change_jump_rect = change_jump.get_rect(center=(1405, 790))
            screen.blit(change_right, change_right_rect)
            screen.blit(change_left, change_left_rect)
            screen.blit(change_jump, change_jump_rect)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 1170 <= mouse_x <= 1640 and 515 <= mouse_y <= 605:
                    changing_keys = True
                    changing_right = True
                    settings = False
                elif 1170 <= mouse_x <= 1640 and 635 <= mouse_y <= 725:
                    changing_keys = True
                    changing_left = True
                    settings = False
                elif 1170 <= mouse_x <= 1640 and 755 <= mouse_y <= 845:
                    changing_keys = True
                    changing_jump = True
                    settings = False
                elif 10 <= mouse_x <= 160 and 880 <= mouse_y <= 1015:
                    if not paused_to_settings:
                        load = True
                    elif paused_to_settings:
                        pause = True
                        paused_to_settings = False
                        run = True
                    settings = False
            elif event.type == pygame.MOUSEBUTTONUP:
                changed_screens = True

        if changing_keys:
            changing_screen.draw(screen)
            if changing_right:
                changing_text = keybind_text_font.render("Press a key to change the right keybind", True, (0, 0, 0))
            elif changing_left:
                changing_text = keybind_text_font.render("Press a key to change the left keybind", True, (0, 0, 0))
            elif changing_jump:
                changing_text = keybind_text_font.render("Press a key to change the jump keybind", True, (0, 0, 0))
            changing_text_rect = changing_text.get_rect(center=(SCREEN_WIDTH / 2, 400))
            changing_error_text = keybind_text_font.render("The same key cannot be used more than once", True, (225, 0, 0))
            changing_error_text_rect = changing_error_text.get_rect(center=(SCREEN_WIDTH / 2, 700))
            screen.blit(changing_text, changing_text_rect)
            if changing_duplicate:
                screen.blit(changing_error_text, changing_error_text_rect)

        if customize:
            character = characters[character_index]
            customize_screen = Popup(f"customize{character}.png", 1)
            customize_screen.draw(screen)
            title_text = title_text_font.render("Customize", True, (0, 0, 0))
            title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 100))
            screen.blit(title_text, title_text_rect)

            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_clicked:
                mouse_clicked = True
                mouse_x, mouse_y = event.pos
                if 415 <= mouse_x <= 545 and 480 <= mouse_y <= 595:
                    character_index -= 1
                    if character_index <= -1:
                        character_index = len(characters) - 1
                elif 1375 <= mouse_x <= 1505 and 480 <= mouse_y <= 595:
                    character_index += 1
                    if character_index >= len(characters):
                        character_index = 0
                elif 10 <= mouse_x <= 160 and 880 <= mouse_y <= 1015:
                    customize = False
                    load = True
                with open("config.txt", "w") as file:
                    file.write(f"{str(right_key)}\n{str(left_key)}\n{str(jump_key)}\n\n{str(character)}")
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
                changed_screens = True

        if rules:
            rules_screen.draw(screen)
            title_text = title_text_font.render("Rules", True, (0, 0, 0))
            title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 120))
            screen.blit(title_text, title_text_rect)

            rules_y = 220
            with open("rules.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    text_surface = rules_text_font.render(line.strip(), True, (0, 0, 0))
                    screen.blit(text_surface, (90, rules_y)) 
                    rules_y += 65

            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_clicked:
                mouse_clicked = True
                mouse_x, mouse_y = event.pos
                if 10 <= mouse_x <= 160 and 880 <= mouse_y <= 1015:
                    rules = False
                    load = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
                changed_screens = True

        if win:
            end_screen.draw(screen)
            title_text = title_text_font.render("YOU WON", True, (0, 0, 0))
            title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 280))
            body_text = body_text_font.render(f"Your took {elapsed_time} to correctly answer {correct_questions} question(s)", True, (0, 0, 0))
            body_text_rect = body_text.get_rect(center=(SCREEN_WIDTH / 2, 400))
            screen.blit(title_text, title_text_rect)
            screen.blit(body_text, body_text_rect)

            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_clicked:
                mouse_clicked = True
                mouse_x, mouse_y = event.pos
                if 550 <= mouse_x <= 1370 and 480 <= mouse_y <= 585:
                    win = False
                    load = True
                    main()
                elif 550 <= mouse_x <= 1370 and 675 <= mouse_y <= 780:
                    valid = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
                changed_screens = True
        
        if lose: 
            end_screen.draw(screen)
            title_text = title_text_font.render("YOU LOST", True, (0, 0, 0))
            title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 280))
            body_text = body_text_font.render(f"You survived for {elapsed_time} and answered {correct_questions} question(s) correctly", True, (0, 0, 0))
            body_text_rect = body_text.get_rect(center=(SCREEN_WIDTH / 2, 400))
            screen.blit(title_text, title_text_rect)
            screen.blit(body_text, body_text_rect)

            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_clicked:
                mouse_clicked = True
                mouse_x, mouse_y = event.pos
                if 550 <= mouse_x <= 1370 and 480 < mouse_y < 585:
                    lose = False
                    load = True
                    main()
                elif 550 <= mouse_x <= 1370 and 675 < mouse_y < 780:
                    valid = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
                changed_screens = True
        
        pygame.display.flip()
    pygame.quit()
main()