import pygame
from os.path import join as join_path, dirname


class Explosion(pygame.sprite.Sprite):
    """Brief explosion flash at a bullet impact point."""

    SCALE = 4
    LIFETIME = 12  # frames at 60fps

    def __init__(self, x, y):
        super().__init__()
        path = join_path(dirname(__file__), "Assets", "Sprites", "explosion.png")
        image = pygame.image.load(path).convert_alpha()
        width = image.get_width() * self.SCALE
        height = image.get_height() * self.SCALE
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = self.LIFETIME

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
