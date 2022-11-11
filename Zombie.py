import pygame
import os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WHITE = (255, 255, 255)

class Zombie(pygame.sprite.Sprite):
    global zombie_list
    global playerhealth
    def __init__(self, width, height, startinghealth, speed, zombieimage):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image = pygame.image.load(zombieimage).convert_alpha()
        self.rightimage = pygame.image.load(zombieimage).convert_alpha()
        self.leftimage = pygame.transform.flip(self.rightimage, True, False)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.health = startinghealth
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.damage=1
        self.change=0
        self.attacktimer=60
        #Cmds that don't work??
        #self.player= Level.player
        #self.level = Level

    
    def update(self):
        global playerhealth
        global money
        if self.health <= 0:
            self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "Sprites" ,"zombieblank.png")).convert_alpha()
            self.damage=0
            globalzombie_list.remove(self)
            money+=10+wave*10
        dist = 930 - self.rect.x
        if dist > 0:
            self.change = self.speed
            self.rect.x += self.change
            self.image = self.rightimage
        if dist <0:
            self.change = -1*self.speed
            self.rect.x += self.change
            self.image = self.leftimage
        
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            playerhealth-=self.damage
        # Check and see if  the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            playerhealth-=self.damage
