import pygame
from Building import Building
from Zombie import Zombie
from Level import Level
from Platform import Platform
from Satelite import Satelite
from random import randint
from os.path import join as join_path, dirname
from Settings import WHITE


def randspeed():
    ketchapp = randint(1, 3)
    if ketchapp > 2:
        return 6
    else:
        return 3


class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        background = pygame.image.load(
            join_path(dirname(__file__), "Assets", "Sprites", "background.png")
        ).convert()
        background = pygame.transform.scale(background, (5760, 1080))
        self.background = background
        self.background.set_colorkey(WHITE)

        building_positions = [3380, 3880, 2380, 1880]
        for pos_x in building_positions:
            building = Building(350, 350, pos_x, 730)
            building.player = self.player
            building.level = self
            self.Building_list.add(building)

        satelite = Satelite(350, 350)
        satelite.rect.x = 2880
        satelite.rect.y = 730
        satelite.player = self.player
        satelite.level = self
        self.satelite_list.add(satelite)

        wall = [
            [350, 350, 550, 730],
            [350, 350, 4800, 730],
        ]

        for platform in wall:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            block.image = pygame.image.load(
                join_path(dirname(__file__), "Assets", "Sprites", "emptyimage.png")
            ).convert_alpha()
            self.platform_list.add(block)

    def wavefunc(self, wave, zombie_list):
        newwave = wave * 2
        for _ in range(0, newwave):
            life = 1 + wave * 1.5
            if wave < 6:
                x = 80
                y = 160
                zombieimage = join_path(
                    dirname(__file__), "Assets", "Sprites", "zombie.png"
                )
            else:
                if randint(1, 3) == 3:
                    x = 121
                    y = 250
                    zombieimage = join_path(
                        dirname(__file__), "Assets", "Sprites", "largezombie.png"
                    )
                    life = 2 * life
                else:
                    x = 80
                    y = 160
                    zombieimage = join_path(
                        dirname(__file__), "Assets", "Sprites", "zombie.png"
                    )
            speed = randspeed()
            if speed > 3:
                life = life / 2
            if zombieimage == join_path(
                dirname(__file__), "Assets", "Sprites", "largezombie.png"
            ):
                speed = speed / 2
            zombie = Zombie(x, y, life, speed, zombieimage)
            if randint(1, 2) == 1:
                zombie.rect.x = -4000 + randint(1, 600)
            else:
                zombie.rect.x = 4000 - randint(1, 600)
            zombie.player = self.player
            zombie.level = self
            zombie_list.add(zombie)
