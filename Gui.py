import pygame
from Settings import SCREEN_WIDTH, SMALLFONT, MEDFONT, LARGEFONT
from Settings import WHITE, BLACK
from Shop import buybuildingwall, buybuildingbank, buymark2, buymark3


def text_objects(text, color, size="small"):
    if size == "small":
        textSurface = SMALLFONT.render(text, True, color)
    elif size == "medium":
        textSurface = MEDFONT.render(text, True, color)
    else:
        textSurface = LARGEFONT.render(text, True, color)

    return textSurface, textSurface.get_rect()


def text_to_button(display, msg, color, buttonx, buttony, buttonwidth, buttonheight, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
    display.blit(textSurf, textRect)


def message_to_screen(display, msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_WIDTH / 2) + y_displace)
    display.blit(textSurf, textRect)


def moneyscore(display, money):
    text = SMALLFONT.render("Money: " + str(money), True, WHITE)
    display.blit(text, [0, 0])


def wavescore(display, wave):
    text = SMALLFONT.render("Wave: " + str(wave), True, WHITE)
    display.blit(text, [0, 50])


def button(display, player, text, x, y, width, height, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(display, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            if action == "buywall":
                buybuildingwall()
            if action == "buybank":
                buybuildingbank()
            if action == "buymark2":
                buymark2(player)
            if action == "buymark3":
                buymark3(player)
    else:
        pygame.draw.rect(display, inactive_color, (x, y, width, height))

    text_to_button(display, text, BLACK, x, y, width, height)


def endgamescreen(display, wave):
    endgame = True
    cooltext = "You survived " + str(wave) + " waves"
    display.fill(WHITE)
    message_to_screen(display, "DEATH", BLACK, -450, size="large")
    message_to_screen(display, cooltext, BLACK, -300, size="medium")
    message_to_screen(display, "Press q to quit", BLACK, -200, size="small")
    pygame.display.update()
    while endgame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def pause(display):
    paused = True
    display.fill(WHITE)
    message_to_screen(display, "Paused", BLACK, -450, size="large")
    message_to_screen(display, "Press E to continue playing or Q to quit", BLACK, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def start(display):
    startingtext = True
    message_to_screen(display, "ZOMBINATOR", BLACK, -450, size="large")
    message_to_screen(display, "By Sammy Dods", BLACK, -300, size="medium")
    message_to_screen(display, "wasd: movement, q: interact p: pause mouse: aim and fire", BLACK, -200, size="small")
    message_to_screen(display, "Press Space to Start", BLACK, -150, size="small")

    pygame.display.update()
    while startingtext:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startingtext = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
