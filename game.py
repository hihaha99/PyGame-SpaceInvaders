import pygame
import os, sys
import random 
import math
from pygame import mixer

##keep this as a practice as the directory using is python path not file path
filepath = os.path.dirname(__file__) 

pygame.init()

screen=pygame.display.set_mode((800,600))

##Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join(filepath, "technology.png"))
pygame.display.set_icon(icon)

##background
backgroundImg = pygame.image.load(os.path.join(filepath, "background.png"))
##background sound
mixer.music.load("background.wav")
mixer.music.play(-1)
## Player
playerImg = pygame.image.load(os.path.join(filepath, "arcade.png"))
playerX = 370
playerY = 480
playerX_change=0

## Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(os.path.join(filepath, "alien.png")))
    enemyX.append(random.randint(0,736))
    enemyY.append(50)
    enemyX_change.append(4)
    enemyY_change.append(40)

##Score
score_value=0
font = pygame.font.Font("Heatwood.ttf",32)
textX = 10
textY = 10


## Bullet
## Ready - You can't see the bullet on the screen
## Fire - The bullet is currently moving
bulletImg = pygame.image.load(os.path.join(filepath, "bullet.png"))
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = 'ready'

# Game Over text
over_font = pygame.font.Font("Heatwood.ttf",32)


def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance <27:
        return True
    else:
        return False
def show_score(x,y):
    score = font.render("Score :" + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def gameOver():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

running = True
while running:
    ##everything is drawn above the background
    screen.fill((0,0,0))
    screen.blit(backgroundImg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # if keystroke is pressed check whether its right or left
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change=-5
                print("Left arrow is pressed",playerX_change)
            if event.key == pygame.K_RIGHT:
                playerX_change=5
                print("Right arrow is pressed",playerX_change)
            if event.key == pygame.K_SPACE and bullet_state=="ready":
                bullet_sound=mixer.Sound("laser.wav")
                bullet_sound.play()
                bulletX=playerX
                fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key ==pygame.K_LEFT and playerX_change!=5:
                playerX_change=0
                print("Left arrow has been released",playerX_change)
            elif  event.key == pygame.K_RIGHT and playerX_change!=-5:
                playerX_change=0
                print("Right arrow has been released",playerX_change)            
    playerX+=playerX_change

## boundaries for player 
    if playerX<=0:
        playerX = 0
    elif playerX>=736:
        playerX = 736
    ## enemy movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            gameOver()
            break

        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i] +=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i] +=enemyY_change[i]
        

        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY=480
            bullet_state='ready'
            explosion_sound=mixer.Sound("explosion.wav")
            explosion_sound.play()
            score_value += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i]= random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)

## bullet movement
    if bullet_state =="fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()

