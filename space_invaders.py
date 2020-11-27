import pygame
import random
import numpy as np
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
ship_image = pygame.image.load('spaceship.png')
background_image = pygame.image.load('space_background.png')
sx, sy = 380,500

mixer.music.load('game_music.mp3')
mixer.music.play(-1)

bullet_image = pygame.image.load('laser_beam.png')
bx, by = 0,500
bullet_change_y = 12
bullet_state = 'charge'

score = 0
font = pygame.font.Font('freesansbold.ttf',30)
text_x, text_y = 600,20

def show_score(x,y):
    global score
    points = font.render(f'SCORE: {score}', True, (0,150,255))
    screen.blit(points, (x,y))
over_x, over_y = 225,275
over_font = pygame.font.Font('freesansbold.ttf',60)
def game_over(x,y):
    over = over_font.render(f'GAME OVER', True, (0,150,50,200))
    screen.blit(over,(x,y))

invader_image, ix, iy, invader_change_x, invader_change_y = [],[],[],[],[]
enemies = 30

for i in range(enemies):
    invader_image.append(pygame.image.load('invader.png'))
    ix.append(random.randrange(64,704,64))
    iy.append(random.randrange(-360,200,70))
    invader_change_x.append(1.8)
    invader_change_y.append(70)

def ship(x,y):
    screen.blit(ship_image,(x,y))
def invader(x,y,i):
    screen.blit(invader_image[i],(x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'f'
    screen.blit(bullet_image,(x-10,y))
    

def collision(ix,iy,bx,by):
    dist = np.sqrt((ix-bx)**2 + (iy-by)**2)
    if dist <= 30:
        return True
    else:
        return False

run = True
while run:
    screen.blit(background_image,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            sx += 8
        if event.key == pygame.K_LEFT:
            sx -= 8
    if event.type == pygame.KEYDOWN:
        if bullet_state == 'charge':
            if event.key == pygame.K_UP:
                bx = sx
                fire_bullet(sx,sy)
                laser_sound = mixer.Sound('laser.wav')
                laser_sound.play()

    if sx <= 0: sx = 0
    if sx >= 737: sx = 736

    for i in range(enemies):
        if any(p >430 for p in iy):
            iy[i] = 1000
            game_over(over_x,over_y)
        ix[i] += invader_change_x[i]
        if ix[i] >= 736:
            invader_change_x[i] = - 1.8
            iy[i] += invader_change_y[i]
        elif ix[i] <= 0:
            invader_change_x[i] = 1.8
            iy[i] += invader_change_y[i]
     
        invader(ix[i],iy[i],i)

    if bullet_state == 'f':
        fire_bullet(bx,by)
        by -= bullet_change_y
    if by <= 0:
        by = 500
        bullet_state = 'charge'
    for i in range(enemies):
        col = collision(ix[i],iy[i],bx,by)
        if col == True:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            by = 500
            bullet_state = 'charge'
            score += 1
            ix[i] = random.randrange(50,735,64)
            iy[i] = random.randrange(-210,-70,70)
    
    clock = pygame.time.Clock()
    pygame.time.delay(5)
    clock.tick(60)
    show_score(text_x,text_y)
    ship(sx,sy)
    

    pygame.display.update()