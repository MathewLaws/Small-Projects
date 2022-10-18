import pygame
from random import randint,choice
from sys import exit
import time
from pygame.constants import K_DOWN, K_SPACE, K_UP, MOUSEBUTTONDOWN
from pygame.sprite import collide_rect

from pygame.time import Clock

def collisions():
    global ball_speed_x,ball_speed_y,col1,col2
    if ball_rect.colliderect(player1_rect)and not col2:
        ball_speed_x *= -1
        ball_speed_y *= -1
        rand = randint(0,4)
        if rand == 1:
            ball_speed_x += 1
            ball_speed_y += randint(0,3)
        elif rand == 2:
            ball_speed_x += 2
            ball_speed_y += randint(0,3)
        elif rand == 3:
            ball_speed_x += 3
            ball_speed_y += randint(0,4)
        else:
            ball_speed_x = 6
            ball_speed_y = 4
        col1 = False
        col2 = True
    if ball_rect.colliderect(player1_2_rect)and not col2:
        ball_speed_x *= -1
        rand = randint(0,4)
        if rand == 1:
            ball_speed_x += 1
            ball_speed_y += randint(0,3)
        elif rand == 2:
            ball_speed_x += 2
            ball_speed_y += randint(0,3)
        elif rand == 3:
            ball_speed_x += 3
            ball_speed_y += randint(0,4)
        else:
            ball_speed_x = 6
            ball_speed_y = 4
        col1 = False
        col2 = True
    if ball_rect.colliderect(player2_rect) and not col1:
        ball_speed_x *= -1
        ball_speed_y *= -1
        rand = randint(0,4)
        if rand == 1:
            ball_speed_x -= 1
            ball_speed_y -= randint(0,3)
        elif rand == 2:
            ball_speed_x -= 2
            ball_speed_y -= randint(0,3)
        elif rand == 3:
            ball_speed_x -= 3
            ball_speed_y -= randint(0,4)
        else:
            ball_speed_x = -6
            ball_speed_y = -4
        col1 = True
        col2 = False
    if ball_rect.colliderect(player2_2_rect) and not col1:
        ball_speed_x *= -1
        rand = randint(0,4)
        if rand == 1:
            ball_speed_x -= 1
            ball_speed_y -= randint(0,3)
        elif rand == 2:
            ball_speed_x -= 2
            ball_speed_y -= randint(0,3)
        elif rand == 3:
            ball_speed_x -= 3
            ball_speed_y -= randint(0,4)
        else:
            ball_speed_x = -6
            ball_speed_y = -4
        col1 = True
        col2 = False

def restart():
    start = True
    global game_active,x_pos,y_pos
    game_active = False
    x_pos = width/2
    y_pos = height/2

pygame.init()
width = 1280
height = 960
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(),30)
font2 = pygame.font.Font(pygame.font.get_default_font(),50)
game_active = False
p1_score = 0
p2_score = 0
col1 = False
col2 = False
start = True

start = True

player1_pos = 550
player1_2_pos = 600

player1 = pygame.Surface((10,50))
player1_2 = pygame.Surface((10,50))
player1.fill("white")
player1_2.fill("white")

player2_pos = 550
player2_2_pos = 600

player2 = pygame.Surface((10,50))
player2_2 = pygame.Surface((10,50))
player2.fill("white")
player2_2.fill("white")

ball = pygame.Surface((20,20))
ball.fill("white")

x_pos = width/2
y_pos = height/2

opponent_speed = 6
ball_speed_x = 5
ball_speed_y = 3.5


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if event.type == MOUSEBUTTONDOWN:
            if game_active == False:
                screen.fill("black")
                game_active = True
                player1_pos = 550
                player1_2_pos = 600
                player2_pos = 550
                player2_2_pos = 600

    user_input = pygame.key.get_pressed()

    if user_input[pygame.K_SPACE]:
        if game_active == False:
                screen.fill("black")
                game_active = True
                player1_pos = 550
                player1_2_pos = 600
                player2_pos = 550
                player2_2_pos = 600

    if user_input[pygame.K_UP]:
        if player2_rect.top <= 0:
            player2_pos = 0
        else:
            player2_pos -= 5
            player2_2_pos -= 5

    if user_input[pygame.K_DOWN]:
        if player2_rect.bottom >= height:
            player2_pos = height - 50
            player2_2_pos = height - 100
        else:
            player2_pos += 5
            player2_2_pos += 5

    if user_input[pygame.K_w]:
        if player1_rect.top <= 0:
            player1_pos = 0
        else:
            player1_pos -= 5
            player1_2_pos -= 5

    if user_input[pygame.K_s]:
        if player1_rect.bottom >= height:
            player1_pos = height - 50
            player1_2_pos = height - 100
        else:
            player1_pos += 5
            player1_2_pos += 5
        

        
    if game_active:
        start = False

        screen.fill("#18191A")

        sides_line = pygame.draw.line(screen,"white",(width/2,0),(width/2,height))

        score_counter1 = font2.render(str(p1_score),True,"white")
        screen.blit(score_counter1,((590,10)))

        score_counter2 = font2.render(str(p2_score),True,"white")
        screen.blit(score_counter2,((665,10)))
        
        player1_rect = player1.get_rect(topleft = (70,player1_pos))
        player1_2_rect = player1_2.get_rect(topleft = (70,player1_2_pos))
        screen.blit(player1,player1_rect)
        screen.blit(player1_2,player1_2_rect)

        player2_rect = player2.get_rect(topleft = (1210,player2_pos))
        player2_2_rect = player2_2.get_rect(topleft = (1210,player2_2_pos))
        screen.blit(player2,player2_rect)
        screen.blit(player2_2,player2_2_rect)

        ball_rect = ball.get_rect(center = (x_pos,y_pos))
        screen.blit(ball,ball_rect)

        x_pos += ball_speed_x
        y_pos += ball_speed_y

        if y_pos >= height or y_pos <= 0:
            ball_speed_y *= -1

        if ball_rect.left <= 0:
            p2_score += 1
            restart()
        if ball_rect.right >= width:
            p1_score += 1
            restart()

        collisions()

    else:
        ball_speed_x = 3.5
        ball_speed_y = 3
        if start:
            screen.fill("black")
        col1 = False
        col2 = False
        ball_speed_x *= choice((1,-1))
        ball_speed_y *= choice((1,-1))

        game_message1 = font.render("Click anywhere to play!",True,"white")
        screen.blit(game_message1,(480,400))

    clock.tick(60)
    pygame.display.update()
