import pygame
import os
###################################################################################################
pygame.init() # reset (반드시 필요)

# screen size
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# screen tile
pygame.display.set_caption('Pang Game') # game name

# FPS (Frame Per Second)
clock = pygame.time.Clock()
###################################################################################################

# 1. initial game setting (background, game image, position, speed, font etc)
current_path = os.path.dirname(__file__) # 현재 파일 위치 반환
image_path = os.path.join(current_path, "images")

# background
background = pygame.image.load(os.path.join(image_path, "C:\programming\pygame\pygame_project\photo\character.jpg"))

# stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# character
character = pygame.image.load(os.path.join(image_path, "C:\programming\pygame\pygame_project\photo\\background.jpg"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = (screen_height - character_height - stage_height)

# character direction
character_to_x = 0

# character speed
character_speed = 10

# weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# multiple attack at the same time
weapons = []

# weapon speed
weapon_speed = 10

# ball (4 different types)
ball_images =  [
    pygame.image.load(os.path.join(image_path, 'balloon1.png')),
    pygame.image.load(os.path.join(image_path, 'balloon2.png')),
    pygame.image.load(os.path.join(image_path, 'balloon3.png')),
    pygame.image.load(os.path.join(image_path, 'balloon4.png'))
    ]

# 4 different speed of balls
ball_speed_y = [-20, -18, -15, -12]

# balls
balls = []

# first ball appearance
balls.append({
    "pos_x" : 50, # ball x_pos
    "pos_y" : 50, # ball y_pos
    "img_idx" : 0, # ball image index
    "to_x" : 3,
    "to_y" : -6,
    "int_speed_y" : ball_speed_y[0]
})

# remove weapon, ball
weapon_to_remove = -1
ball_to_remove = -1

# Font
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # starting time

# game over message
# TimeOut, Mission Complete, Game Over
game_result = "Game Over"

running = True 
while running:
    dt = clock.tick(60)


    # 2. event setting (keybaord, mounse etc)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: # weapon
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                character_to_x = 0

    # 3. define character position
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # weapon postion
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    # once weapon touch sky
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # ball position
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # ball once touch wall
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # ball once touch stage
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["int_speed_y"]
        else: # increase speed
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. collision

    # character rect, info update
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # ball rect info. upadate
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # ball & character collision check
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # ball & weapon collision
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # weapon rect info.
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # collision check
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx
                
                # split ball (not last ball)
                if ball_img_idx < 3:
                    # current ball info
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # splitted ball info
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # bounce left ball
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # ball x_pos
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # ball y_pos
                        "img_idx" : ball_img_idx + 1, # ball image index
                        "to_x" : -3, # x축 이동방향, -3 = 왼쪽 +3 = 오른쪽
                        "to_y" : -10, # y축 이동방향
                        "int_speed_y" : ball_speed_y[ball_img_idx + 1] # y 최초 속도
                    })

                    # bounce right ball
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # ball x_pos
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # ball y_pos
                        "img_idx" : ball_img_idx + 1, # ball image index
                        "to_x" : +3,
                        "to_y" : -10,
                        "int_speed_y" : ball_speed_y[ball_img_idx + 1]
                    })
                break
        else: # continue game
            continue
        break
    
    # remove ball, weapon once collide
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
        
    # end game once all game removed
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. show on the screen
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # time calcuation
    elapsed_time = (pygame.time.get_ticks() - start_ticks)     / 1000
    timer = game_font.render("Time: {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # time over
    if total_time - elapsed_time <= 0:
        game_result = "Time Out"
        running = False

    pygame.display.update()

# game end message
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 2sec. wait
pygame.time.delay(2000)

pygame.quit()