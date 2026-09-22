import pygame
from Settings import SCREEN_WIDTH, SCREEN_HEIGHT, SMALLFONT, MEDFONT, LARGEFONT
from Settings import WHITE, BLACK, GREEN, LIGHT_GREEN, GRAY, DARK_GRAY, RED, LIGHT_RED
from Shop import buybuildingwall, buybuildingbank, buymark2, buymark3
import GameState


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
    import Audio

    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = x + width > cur[0] > x and y + height > cur[1] > y
    Audio.handle_button_hover(("shop", text, x, y), hovered)
    if hovered:
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


def menu_button(display, text, x, y, width, height, inactive_color, active_color, just_clicked):
    """Draw a button; return True if it was clicked this frame."""
    import Audio

    cur = pygame.mouse.get_pos()
    hovered = x + width > cur[0] > x and y + height > cur[1] > y
    Audio.handle_button_hover(("menu", text, x, y), hovered)
    color = active_color if hovered else inactive_color
    pygame.draw.rect(display, color, (x, y, width, height))
    text_to_button(display, text, BLACK, x, y, width, height)
    return just_clicked and hovered


def volume_slider(display, label, x, y, width, height, volume, dragging):
    """
    Draw a 0-100 volume slider.
    Returns (volume 0.0-1.0, dragging).
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_down = pygame.mouse.get_pressed()[0] == 1

    track_padding = 8
    track_rect = pygame.Rect(x, y + height // 3, width, height // 3)
    hit_rect = pygame.Rect(x, y, width, height)

    label_surf, label_rect = text_objects(
        "{}: {}%".format(label, int(round(volume * 100))),
        BLACK,
        "medium",
    )
    label_rect.midbottom = (x + width // 2, y - 10)
    display.blit(label_surf, label_rect)

    if mouse_down and (dragging or hit_rect.collidepoint(mouse_x, mouse_y)):
        dragging = True
        relative = (mouse_x - track_rect.x) / float(track_rect.width)
        volume = max(0.0, min(1.0, relative))
        volume = round(volume * 100) / 100.0  # snap to whole percent
    elif not mouse_down:
        dragging = False

    pygame.draw.rect(display, GRAY, track_rect, border_radius=6)
    fill_width = int(track_rect.width * volume)
    if fill_width > 0:
        fill_rect = pygame.Rect(track_rect.x, track_rect.y, fill_width, track_rect.height)
        pygame.draw.rect(display, LIGHT_GREEN, fill_rect, border_radius=6)

    knob_x = track_rect.x + int(track_rect.width * volume)
    knob_radius = height // 3
    pygame.draw.circle(display, DARK_GRAY, (knob_x, track_rect.centery), knob_radius)
    pygame.draw.circle(display, WHITE, (knob_x, track_rect.centery), knob_radius - 4)

    min_surf, min_rect = text_objects("0", BLACK, "small")
    max_surf, max_rect = text_objects("100", BLACK, "small")
    min_rect.topleft = (track_rect.x, track_rect.bottom + track_padding)
    max_rect.topright = (track_rect.right, track_rect.bottom + track_padding)
    display.blit(min_surf, min_rect)
    display.blit(max_surf, max_rect)

    return volume, dragging


def apply_volumes(lasersound=None):
    pygame.mixer.music.set_volume(GameState.music_volume * 0.1)
    import Audio

    Audio.apply_volumes()


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


def pause(display, lasersound=None):
    paused = True
    center_x = SCREEN_WIDTH // 2
    slider_width = 500
    slider_height = 40
    slider_x = center_x - slider_width // 2
    dragging_music = False
    dragging_sfx = False

    while paused:
        just_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_e, pygame.K_p, pygame.K_ESCAPE):
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                just_clicked = True

        display.fill(WHITE)

        title_surf, title_rect = text_objects("Paused", BLACK, "large")
        title_rect.center = (center_x, 160)
        display.blit(title_surf, title_rect)

        hint_surf, hint_rect = text_objects("E / P / Esc: resume", BLACK, "small")
        hint_rect.center = (center_x, 230)
        display.blit(hint_surf, hint_rect)

        GameState.music_volume, dragging_music = volume_slider(
            display,
            "Music",
            slider_x,
            340,
            slider_width,
            slider_height,
            GameState.music_volume,
            dragging_music,
        )
        GameState.sfx_volume, dragging_sfx = volume_slider(
            display,
            "SFX",
            slider_x,
            460,
            slider_width,
            slider_height,
            GameState.sfx_volume,
            dragging_sfx,
        )
        apply_volumes(lasersound)

        if menu_button(
            display, "Resume", center_x - 150, 580, 300, 70, LIGHT_GREEN, GREEN, just_clicked
        ):
            paused = False

        if menu_button(
            display, "Quit", center_x - 150, 680, 300, 70, RED, LIGHT_RED, just_clicked
        ):
            pygame.quit()
            quit()

        pygame.display.update()


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
