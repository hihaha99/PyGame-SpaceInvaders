import pygame
import os, sys
import random 
import math
from Sprites import *
from pygame import mixer

filepath = os.path.dirname(__file__) 
SCREENSIZE=(800,600)

def initGame():
    pygame.init()
    game_images={}
    game_music={}
    ##music
    mixer.music.load(os.path.join(filepath, "background.wav"))
    mixer.music.play(-1)
    game_music["collision"]=mixer.Sound(os.path.join(filepath, "explosion.wav"))
    game_music["shoot"]=mixer.Sound(os.path.join(filepath, "laser.wav"))
    screen=pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load(os.path.join(filepath, "technology.png"))
    pygame.display.set_icon(icon)
    game_images["backgroundImg"]= pygame.image.load(os.path.join(filepath, "background.png"))
    game_images["playerImg "]= pygame.image.load(os.path.join(filepath, "arcade.png"))
    game_images["enemyImg"]=pygame.image.load(os.path.join(filepath, "alien.png"))
    game_images["bulletImg"]=pygame.image.load(os.path.join(filepath, "bullet.png"))
    return screen,game_images,game_music

def main():
    ## Initialization
    screen,game_images,game_music=initGame()
    ## Game Running Control
    running = True
    game_over = False
    ## Player 
    player=Player(image=game_images["playerImg "],position=(370,480))
    ## Bullet
    bullet_group = pygame.sprite.Group()
    ## Enemy
    enemyTimer=100
    enemy_group = pygame.sprite.Group()
    enemy=Enemy(image=game_images["enemyImg"],position=(random.randint(0,736),0))
    enemy_group.add(enemy)
    ## Score 
    score_value=0
    ## Score Font
    font = pygame.font.Font("Heatwood.ttf",32)
    # Game Over text
    over_font = pygame.font.Font("Heatwood.ttf",32)
    while running:
        screen.fill((0,0,0))
        screen.blit(game_images["backgroundImg"],(0,0))
        for event in pygame.event.get():
            ##  Quit Game
            if event.type == pygame.QUIT:
                running=False
            ## Fire Bullet
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_music["shoot"].play()
                bullet = Bullet(image=game_images["bulletImg"],position=(player.rect.left,player.rect.top))
                bullet_group.add(bullet)
        ## Player movement
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            player.move(SCREENSIZE, 'up')
        elif key_pressed[pygame.K_s]:
            player.move((SCREENSIZE[0],536), 'down')
        elif key_pressed[pygame.K_a]:
            player.move((SCREENSIZE), 'left')
        elif key_pressed[pygame.K_d]:
            player.move((736,SCREENSIZE[1]), 'right')
        ## Bullet Movement
        for bullet in bullet_group:
            if bullet.update():
                bullet_group.remove(bullet)
        ## Enemy Movement
        for enemy in enemy_group:
            if enemy.update():
                pass   
            else:
                gameOver(over_font,screen)
                game_over=True
        ## Collision of bullet and enemy
        for bullet in bullet_group:
            for enemy in enemy_group:
                if pygame.sprite.collide_mask(enemy,bullet):
                    if(game_over==False):
                        score_value+=1
                    game_music["collision"].play()
                    bullet_group.remove(bullet)
                    enemy_group.remove(enemy)
        ## Add Enemy
        enemyTimer-=1
        if enemyTimer==0:
            enemy=Enemy(image=game_images["enemyImg"],position=(random.randint(0,736),0))
            enemy_group.add(enemy)
            print(100-score_value//5)
            enemyTimer=max(20, 50-score_value)
        ## Draw Player
        player.draw(screen)
        ## Draw Enemyaaaa
        enemy_group.draw(screen)
        bullet_group.draw(screen)
        show_score(font,screen,score_value)
        pygame.display.update()

def show_score(font,screen,score_value):
    score = font.render("Score :" + str(score_value),True,(255,255,255))
    screen.blit(score,(10,10))

def gameOver(over_font,screen):
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

if __name__== "__main__":
    main()