import pygame
from os.path import join as join_path, dirname
from Settings import RED
import GameState


class Satelite(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        sateliteimage = pygame.image.load(
            join_path(dirname(__file__), "Assets", "Sprites", "satelite.png")
        ).convert_alpha()
        sateliteimage = pygame.transform.scale(sateliteimage, (350, 350))
        self.image = sateliteimage
        self.rect = self.image.get_rect()
        self.player = None
        self.level = None

    def update(self):
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and GameState.q:
            GameState.sateliteshop = True
