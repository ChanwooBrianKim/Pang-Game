import pygame
import os
###################################################################################################
pygame.init() # reset (반드시 필요)

# 화면 크기 설정
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption('Pang Game') # game name

# FPS (Frame Per Second)
clock = pygame.time.Clock()
###################################################################################################

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) # 현재 파일 위치 반환
image_path = os.path.join(current_path, "images") # 이미지 폴더 위치 반환

# background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지 위에 캐릭터 두기 위해

###############################################
# CHARACTER

# character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = (screen_height - character_height - stage_height)

# character direction
character_to_x = 0

# character speed
character_speed = 5
################################################

################################################
# WEAPON

# weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 스테이지 별 무기 쏘는 회수 차별
weapons = []

# weapon speed
weapon_speed = 10

# 사라질 무기 정보 저장 변수
weapon_to_remove = -1

##################################################

##################################################
# BALL

# ball (4개 크기에 대해 따로 처리)
ball_images =  [
    pygame.image.load(os.path.join(image_path, 'balloon1.png')),
    pygame.image.load(os.path.join(image_path, 'balloon2.png')),
    pygame.image.load(os.path.join(image_path, 'balloon3.png')),
    pygame.image.load(os.path.join(image_path, 'balloon4.png'))
    ]

# 공 크기에 따른 최초 스피드 (bounce range)
ball_speed_y = [-20, -18, -15, -12]

# balls
balls = []

# 사라지리 공 정보 저장 변수
ball_to_remove = -1

##################################################

# stage no.
stage = 1

# Font
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # starting time

# game over message
game_result = "Game Over"


running = True 
while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_x_pos -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_x_pos += character_speed
            elif event.key == pygame.K_SPACE: # weapon
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                character_to_x = 0

    # 3. 게임 케릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()
    
pygame.quit()