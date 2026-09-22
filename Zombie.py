import pygame
from os.path import join as join_path, dirname
from random import randint
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
import Audio


class Zombie(pygame.sprite.Sprite):
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
        self.damage = 1
        self.change = 0
        self.attacktimer = 60
        self.player = None
        self.level = None
        # Stagger moans so the horde doesn't speak in unison
        self.moan_timer = randint(45, 240)

    def update(self):
        if self.health <= 0:
            self.die()
            return

        dist = 930 - self.rect.x
        if dist > 0:
            self.change = self.speed
            self.rect.x += self.change
            self.image = self.rightimage
        if dist < 0:
            self.change = -1 * self.speed
            self.rect.x += self.change
            self.image = self.leftimage

        self.moan_timer -= 1
        if self.moan_timer <= 0:
            if -100 < self.rect.centerx < SCREEN_WIDTH + 100:
                Audio.play_zombie_moan()
            self.moan_timer = randint(120, 360)

    def die(self):
        self.image = pygame.image.load(
            join_path(dirname(__file__), "Assets", "Sprites", "zombieblank.png")
        ).convert_alpha()
        self.damage = 0

    def attack(self, player):
        player.take_damage(self.damage)

    def take_damage(self, damage):
        self.health -= damage

    def is_dead(self):
        return self.health <= 0
