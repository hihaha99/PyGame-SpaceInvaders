import math
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,image,position):
        
        super().__init__
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed=5
    
    def move(self,screensize,direction):
        if direction == 'left':
            ##return max number between x and 0
            self.rect.left = max(self.rect.left-self.speed, 0)
        elif direction == 'right':
            self.rect.left = min(self.rect.left+self.speed, screensize[0])
        elif direction == 'up':
            self.rect.top = max(self.rect.top-self.speed, 0)
        elif direction == 'down':
            self.rect.top = min(self.rect.top+self.speed, screensize[1])

    def draw(self, screen):
        screen.blit(self.image,self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position
        self.speed=1
    
    def update(self):
        self.rect.top  += self.speed
        if self.rect.top < 600:
            return True
        return False

class Bullet(pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position
        self.speed=10
    
    def update(self):
        self.rect.top  -= self.speed
        if self.rect.top < 0:
            return True
        return False