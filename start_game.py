import pygame, sys, os
from main_menu_buttons import Button
from sprite_classes import all_sprites, sprite
from initialization import main_menu


pygame.init()
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Карточные игры)")
deck_number = 1


BG_menu = pygame.image.load("./data/BG/BG_plot.jpg")
font = pygame.font.Font('./data/fonts/Verdana.ttf', 24)


def start_game():
    pygame.mixer.music.load("./data/sounds/Jaz_Z.mp3")
    pygame.mixer.music.play(-1)
    vol = 0.01
    pygame.mixer.music.set_volume(vol)
    flag = True
    exit_button = Button((1000, 50), 150, 150, None, font,
                             "./data/buttons/exit_button.jpg",
                             "./data/buttons/exit_button.jpg",
                             "./data/sounds/click.wav")

    play_button = Button((80, 15), 300, 250, None, font,
                          "./data/buttons/full_1.png",
                          "./data/buttons/full_1_hover.png",
                          "./data/sounds/click.wav")

    running = True
    while running:
        SCREEN.blit(BG_menu, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                coords = event.pos
                flag = pygame.mouse.get_focused()
                sprite.rect.x, sprite.rect.y = coords

            if event.type == pygame.USEREVENT and event.button == play_button:
                main_menu()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [play_button, exit_button]:
                btn.han_event(event)

        for btn in [play_button, exit_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        if flag:
            all_sprites.draw(SCREEN)

        pygame.display.flip()

