from os.path import join as join_path, dirname
import pygame
import GameState

bankimage = None
wallimage = None


def load_shop_images():
    """Load after pygame.display is initialized."""
    global bankimage, wallimage
    bankimage = pygame.image.load(
        join_path(dirname(__file__), "Assets", "Sprites", "bank.png")
    ).convert_alpha()
    bankimage = pygame.transform.scale(bankimage, (350, 350))
    wallimage = pygame.image.load(
        join_path(dirname(__file__), "Assets", "Sprites", "Wall.png")
    ).convert_alpha()
    wallimage = pygame.transform.scale(wallimage, (350, 350))


def buybuildingwall():
    opener = GameState.buildingshopopener
    if opener is None or wallimage is None:
        return
    if GameState.money >= 300 and opener.Building != "wall":
        GameState.money -= 300
        if opener.Building == "bank":
            GameState.num_banks -= 1
        opener.Building = "wall"
        opener.health = 110
        opener.image = wallimage


def buybuildingbank():
    opener = GameState.buildingshopopener
    if opener is None or bankimage is None:
        return
    if GameState.money >= 450 and opener.Building != "bank":
        GameState.money -= 450
        opener.Building = "bank"
        opener.health = 15
        opener.image = bankimage
        GameState.num_banks += 1


def buymark2(player):
    if GameState.money >= 1000 and GameState.suit != "markii":
        GameState.money -= 1000
        player.change_suit("markii")
        GameState.suit = "markii"


def buymark3(player):
    if GameState.money >= 5000 and GameState.suit != "markiii":
        GameState.money -= 5000
        player.change_suit("markiii")
        GameState.suit = "markiii"
