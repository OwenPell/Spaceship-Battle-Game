import pygame
import os
import random
# from powerups import PowerUps

pygame.font.init()
pygame.mixer.init()

pygame.init()

WIDTH = 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Practice Game')
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10,HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('arial', 40)
WINNER_FONT = pygame.font.SysFont('arial', 100)

FPS = 60
red_vel = 5
yellow_vel = 5
BULLET_VEL = 7
max_bullets = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health): #Draws winner_text on screen when win conditions are met
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    #YELLOW SHIP MOVEMENT
    if keys_pressed[pygame.K_a] and yellow.x - yellow_vel > 0: #:LEFT
        yellow.x -= yellow_vel
    if keys_pressed[pygame.K_d] and yellow.x + yellow_vel + yellow.width < BORDER.x: #:RIGHT
        yellow.x += yellow_vel
    if keys_pressed[pygame.K_w] and yellow.y - yellow_vel > 0: #:UP
        yellow.y -= yellow_vel
    if keys_pressed[pygame.K_s] and yellow.y + yellow_vel + yellow.height < HEIGHT - 15: #:DOWN
        yellow.y += yellow_vel

def red_handle_movement(keys_pressed, red):
        #RED MOVEMENT
    if keys_pressed[pygame.K_LEFT] and red.x - red_vel > BORDER.x + BORDER.width: #LEFT
        red.x -= red_vel
    if keys_pressed[pygame.K_RIGHT] and red.x + red_vel + red.width < WIDTH: #RIGHT
        red.x += red_vel
    if keys_pressed[pygame.K_UP] and red.y - red_vel > 0: # UP
         red.y -= red_vel
    if keys_pressed[pygame.K_DOWN] and red.y + red_vel + red.height < HEIGHT - 15: #DOWN
        red.y += red_vel

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)
            

    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

def gen_power_ups():
    x = random.randint(50, 850)
    y = random.randint(50, 450)
    

def handle_power_ups(power_ups, red_power_ups, yellow_power_ups):
    pass

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    power_ups = []
    red_power_ups = []
    yellow_power_ups = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_m and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                yellow_health -= 1

            if event.type == YELLOW_HIT:
                red_health -= 1


        winner_text = ''
        if red_health <= 0:
            winner_text = 'Yellow Wins!'
        
        if yellow_health <= 0:
            winner_text = 'Red Wins!'
        
        if winner_text != '':
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(red_bullets, yellow_bullets, red, yellow)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


main()