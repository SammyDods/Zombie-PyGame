import pygame
from Settings import BLUE


class Level(object):
    world_shift = 0
    level_limit = -2720

    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.Building_list = pygame.sprite.Group()
        self.zombie_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.globalzombie_list = pygame.sprite.Group()
        self.satelite_list = pygame.sprite.Group()
        self.player = player
        self.world_shift = 0
        self.background = None

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
        self.Building_list.update()
        self.bullet_list.update()
        self.zombie_list.update()
        self.satelite_list.update()
        self.globalzombie_list.update()

    def draw(self, screen):
        screen.fill(BLUE)
        screen.blit(self.background, (self.world_shift // 1, 0))

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.Building_list.draw(screen)
        self.zombie_list.draw(screen)
        self.globalzombie_list.draw(screen)
        self.satelite_list.draw(screen)

    def shift_world(self, shift_x):
        self.world_shift += shift_x

        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for building in self.Building_list:
            building.rect.x += shift_x

        for satelite in self.satelite_list:
            satelite.rect.x += shift_x

        for zombie in self.globalzombie_list:
            zombie.rect.x += shift_x

        for zombie in self.zombie_list:
            zombie.rect.x += shift_x
