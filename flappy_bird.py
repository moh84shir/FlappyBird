import pygame
import sys
import random
from time import sleep

# START PYGAME MODULES
pygame.init()


# ALL VARIABLES
display_width = 285
display_height = 510
floor_x = 0
gravity = 0.25
bird_movement = 0
pipe_list = []
game_status = True
bird_list_index = 0
game_font = pygame.font.Font('assets/font/Flappy.TTF', 30)
score = 0
high_score = 0
active_score = True


def generate_pipe_rect() -> pygame.Rect:
    random_pipe = random.randrange(190, 400)
    pipe_rect_bottom = pipe_image.get_rect(midtop=(500, random_pipe))
    pipe_rect_top = pipe_image.get_rect(midbottom=(500, random_pipe - 150))
    return pipe_rect_bottom, pipe_rect_top


def move_pipe_rect(pipes: list) -> list:
    for pipe in pipes:
        pipe.centerx -= 5
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipes


def display_pipes(pipes: list) -> None:
    for pipe in pipes:
        if pipe.bottom >= 510:
            main_screen.blit(pipe_image, pipe)
        else:
            reversed_pipe = pygame.transform.flip(pipe_image, False, True)
            main_screen.blit(reversed_pipe, pipe)


def image_load(image_name: str) -> pygame.Surface:
    image = pygame.image.load(f'assets/img/{image_name}.png')
    return image


def check_collision(pipes: list) -> bool:
    global game_status
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe):
            game_over_sound.play()
            sleep(3)
            return False
        if bird_image_rect.top <= -50 or bird_image_rect.bottom >= 450:
            game_over_sound.play()
            sleep(3)
            return False
    return True


def bird_animation():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_image_rect.centery))
    return new_bird, new_bird_rect


def display_score(status):
    if status == 'active':
        text1 = game_font.render(str(score), False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(142, 50))
        main_screen.blit(text1, text1_rect)

    if status == 'game_over':
        # SCORE
        text1 = game_font.render(f"Score: {score}", False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(142, 50))
        main_screen.blit(text1, text1_rect)

        # HIGH SCORE
        text2 = game_font.render(
            f"High Score: {high_score}", False, (255, 255, 255))
        text2_rect = text1.get_rect(center=(110, 400))
        main_screen.blit(text2, text2_rect)


def update_score():
    global score, high_score, active_score
    if pipe_list and active_score:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score:
                win_sound.play()
                score += 1
                active_score = False
            if pipe.right > 50:
                active_score = True

    if high_score < score:
        high_score = score


# LOAD IMAGES
background_image = image_load('bg2')
floor_image = image_load('floor')
pipe_image = image_load('pipe_red')
bird_image_down = image_load('red_bird_down_flap')
bird_image_mid = image_load('red_bird_mid_flap')
bird_image_up = image_load('red_bird_up_flap')

bird_list = [
    bird_image_down,
    bird_image_mid,
    bird_image_up
]
bird_image = bird_list[bird_list_index]

# LOAD SOUNDS
game_over_sound = pygame.mixer.Sound('assets/sound/smb_mario_die.wav')
win_sound = pygame.mixer.Sound('assets/sound/smb_stomp.wav')


# USER EVENTS
create_pipe = pygame.USEREVENT
create_flap = pygame.USEREVENT + 1

# SET TIMWE
pygame.time.set_timer(create_pipe, 1000)
pygame.time.set_timer(create_flap, 100)

# REACANGLES IMAGE
bird_image_rect = bird_image.get_rect(center=(50, 260))

# GAME DISPLAY
main_screen = pygame.display.set_mode((display_width, display_height))

# GAME TIMER
clock = pygame.time.Clock()


# GAME LOGIC
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # END PYGAME MODULES
            pygame.quit()
            # TERMINATE PROGRAM
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6

            if event.key == pygame.K_r and not game_status:
                game_status = True
                pipe_list.clear()
                bird_image_rect.center = (50, 260)
                bird_movement = 0
                score = 0
                active_score = True

        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())

        if event.type == create_flap:
            if bird_list_index < 2:
                bird_list_index += 1
            else:
                bird_list_index = 0

            bird_image, bird_image_rect = bird_animation()

    # SHOW IMAGES
    # DISPLAY BACKGROUND IMAGE
    main_screen.blit(background_image, (0, 0))

    if game_status:
        # DISPLAY BIRD IMAGE
        main_screen.blit(bird_image, bird_image_rect)

        # CHECK FOR COLLISIONS
        game_status = check_collision(pipe_list)
        # DISPLAY PIPES IMAGE
        pipe_list = move_pipe_rect(pipe_list)
        display_pipes(pipe_list)

        # FLOOR GRAVITY AND BIRD MOVEMENT
        bird_movement += gravity
        bird_image_rect.centery += bird_movement
        # SHOW SCORE
        update_score()
        display_score('active')
    else:
        display_score('game_over')

    # DISPLAY FLOOR IMAGE
    main_screen.blit(floor_image, (floor_x, 450))
    main_screen.blit(floor_image, (floor_x + 285, 450))

    # SET FLOOR IMAGE ANIMATIONS
    floor_x -= 1

    # CHECK FLOOR IMAGE
    if floor_x == -285:
        floor_x = 0

    # UPDATE MAIN SCREEN
    pygame.display.update()
    # SET GAME SPEED
    clock.tick(60)
