import pygame
from math import sin, cos, atan2, degrees
from os.path import join as join_path, dirname
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Bullet(pygame.sprite.Sprite):
    """Projectile that uses the bullet sprite matching the player's suit."""

    SCALE = 4
    effect_group = None

    SUIT_BULLETS = {
        "marki": "bulleti.png",
        "markii": "bulletii.png",
        "markiii": "bulletiii.png",
    }

    def __init__(self, start_x, start_y, dest_x, dest_y, suit="marki"):
        super().__init__()

        filename = self.SUIT_BULLETS.get(suit, "bulleti.png")
        path = join_path(dirname(__file__), "Assets", "Sprites", filename)
        image = pygame.image.load(path).convert_alpha()
        width = image.get_width() * self.SCALE
        height = image.get_height() * self.SCALE
        self.original_image = pygame.transform.scale(image, (width, height))

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = atan2(y_diff, x_diff)

        # Image faces right; pygame rotates counter-clockwise
        self.image = pygame.transform.rotate(self.original_image, -degrees(angle))
        self.rect = self.image.get_rect(center=(start_x, start_y))

        self.floating_point_x = float(start_x)
        self.floating_point_y = float(start_y)

        velocity = 30
        self.change_x = cos(angle) * velocity
        self.change_y = sin(angle) * velocity

    def spawn_explosion(self):
        if self.effect_group is None:
            return
        from Explosion import Explosion

        self.effect_group.add(Explosion(self.rect.centerx, self.rect.centery))

    def update(self):
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
        self.rect.center = (int(self.floating_point_x), int(self.floating_point_y))

        if self.hit_ground():
            import Audio

            Audio.play_explode()
            self.spawn_explosion()
            self.kill()
            return

        if (
            self.rect.right < 0
            or self.rect.left > SCREEN_WIDTH
            or self.rect.bottom < 0
            or self.rect.top > SCREEN_HEIGHT
        ):
            self.kill()

    def hit_ground(self):
        """True when the bullet reaches the floor."""
        return self.rect.bottom >= SCREEN_HEIGHT
