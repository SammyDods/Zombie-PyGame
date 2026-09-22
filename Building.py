import pygame
from os.path import join as join_path, dirname
from Settings import WHITE
import GameState


class Building(pygame.sprite.Sprite):
    player = None
    level = None

    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image = pygame.image.load(
            join_path(dirname(__file__), "Assets", "Sprites", "emptybuilding.png")
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.Building = None
        self.health = 0

    def set_image(self, filename=None):
        if filename is not None:
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()

    def update(self):
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and GameState.q:
            GameState.buildingshop = True
            GameState.buildingshopopener = self

        if self.level is not None:
            zombieclist = pygame.sprite.spritecollide(
                self, self.level.globalzombie_list, False
            )
            for zombie in zombieclist:
                if self.health > 0:
                    if zombie.change > 0:
                        zombie.rect.right = self.rect.left
                    elif zombie.change < 0:
                        zombie.rect.left = self.rect.right
                    if zombie.attacktimer > 0:
                        zombie.attacktimer -= 1
                    elif zombie.attacktimer <= 0:
                        zombie.attacktimer = 6
                        self.health -= zombie.damage

        if self.health <= 0 and self.Building is not None:
            was_bank = self.Building == "bank"
            self.Building = None
            self.image = pygame.image.load(
                join_path(dirname(__file__), "Assets", "Sprites", "emptybuilding.png")
            ).convert_alpha()
            if was_bank:
                GameState.num_banks -= 1


class Bank(Building):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__(width, height, pos_x, pos_y)
        bank_image = pygame.image.load(
            join_path(dirname(__file__), "Assets", "Sprites", "bank.png")
        ).convert_alpha()
        bank_image = pygame.transform.scale(bank_image, (350, 350))
        self.image = bank_image
        self.Building = "bank"
        self.health = 15


class Wall(Building):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__(width, height, pos_x, pos_y)
        wall_image = pygame.image.load(
            join_path(dirname(__file__), "Assets", "Sprites", "Wall.png")
        ).convert_alpha()
        wall_image = pygame.transform.scale(wall_image, (350, 350))
        self.image = wall_image
        self.Building = "wall"
        self.health = 110
