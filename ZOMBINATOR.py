import pygame
from os.path import join as join_path, dirname

from Player import Player
from Level_01 import Level_01
from Bullet import Bullet
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Settings import WHITE, GREEN, YELLOW, LIGHT_GREEN, LIGHT_YELLOW
from Gui import start, pause, wavescore, moneyscore, endgamescreen, button
from Shop import load_shop_images
import GameState

pygame.init()

# Set the height and width of the screen
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("Zombinator")

clock = pygame.time.Clock()
lasersound = pygame.mixer.Sound(
    join_path(dirname(__file__), "Assets", "Audio", "laser.wav")
)
load_shop_images()


def main():
    pygame.init()

    zombie_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen.fill(WHITE)
    pygame.display.set_caption("ZOMBINATOR")

    player = Player()

    level_list = []
    level_list.append(Level_01(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    # Use the level's zombie group so scrolling/collisions stay in sync
    zombie_list = current_level.globalzombie_list

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 2500
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    done = False
    clock = pygame.time.Clock()

    music_path = join_path(
        dirname(__file__), "Assets", "Audio", "ChasingGhosts.mp3"
    )
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    startingnow = True

    reload = 15
    GameState.wave = 0
    banking = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                    GameState.buildingshop = False
                    GameState.sateliteshop = False
                if event.key == pygame.K_d:
                    player.go_right()
                    GameState.buildingshop = False
                    GameState.sateliteshop = False
                if event.key == pygame.K_w:
                    player.jump()
                    GameState.buildingshop = False
                    GameState.sateliteshop = False
                if event.key == pygame.K_p:
                    pause(screen)

                if event.key == pygame.K_q:
                    GameState.q = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                    GameState.buildingshop = False
                    GameState.sateliteshop = False

                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()
                    GameState.buildingshop = False
                    GameState.sateliteshop = False

                if event.key == pygame.K_q:
                    GameState.q = False

            click = pygame.mouse.get_pressed()
            if click[0] == 1 and reload <= 0:
                lasersound.play()
                reload = 15
                pos = pygame.mouse.get_pos()
                bullet = Bullet(player.rect.x, player.rect.y + 50, pos[0], pos[1])
                active_sprite_list.add(bullet)
                bullet_list.add(bullet)

        reload -= 1

        if not zombie_list.sprites():
            GameState.wave += 1
            current_level.wavefunc(GameState.wave, zombie_list)

        if startingnow:
            startingnow = False
            start(screen)

        active_sprite_list.update()

        for bullet in list(bullet_list):
            zombie_hit_list = pygame.sprite.spritecollide(bullet, zombie_list, False)
            for zombie in zombie_hit_list:
                zombie.take_damage(player.damage)
                if zombie.is_dead():
                    zombie.die()
                    zombie_list.remove(zombie)
                    GameState.money += 10 + GameState.wave * 10
                bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)
                break
            else:
                if bullet.rect.y < -10:
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)

        for zombie in zombie_list:
            if pygame.sprite.collide_rect(zombie, player):
                zombie.attack(player)

        if player.rect.right >= 1020:
            diff = player.rect.right - 1020
            player.rect.right = 1020
            current_level.shift_world(-diff)

        if player.rect.left <= 900:
            diff = 900 - player.rect.left
            player.rect.left = 900
            current_level.shift_world(diff)

        current_level.update()

        banking += 2 * GameState.num_banks
        if banking >= 30:
            GameState.money += 2
            banking = 0

        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        if player.rect.left < 0:
            player.rect.left = 0

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        if GameState.buildingshop:
            button(
                screen,
                player,
                "Buy wall (350)",
                650,
                500,
                200,
                100,
                LIGHT_GREEN,
                GREEN,
                action="buywall",
            )
            button(
                screen,
                player,
                "Buy bank (450)",
                1110,
                500,
                200,
                100,
                YELLOW,
                LIGHT_YELLOW,
                action="buybank",
            )

        if GameState.sateliteshop:
            button(
                screen,
                player,
                "Buy Mark II (1000)",
                600,
                500,
                300,
                100,
                LIGHT_GREEN,
                GREEN,
                action="buymark2",
            )
            button(
                screen,
                player,
                "Buy Mark III (5000)",
                1150,
                500,
                300,
                100,
                YELLOW,
                LIGHT_YELLOW,
                action="buymark3",
            )

        moneyscore(screen, GameState.money)
        wavescore(screen, GameState.wave)

        if player.health <= 0:
            endgamescreen(screen, GameState.wave)

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
