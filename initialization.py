import pygame, sys, os
from main_menu_buttons import Button
from sprite_classes import sprite, all_sprites
from authors import authors
from settings import settings_menu
from game_chooser import game_chooser
from statistics import statisctis_screen


pygame.init()
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Карточные игры)")
deck_number = 1


def load_image(name, colorkey=None):
    fullname = os.path.join('./data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

pygame.mouse.set_visible(False)

BG_menu = pygame.image.load("./data/BG/BG_menu.jpg")
BG_game = pygame.image.load("./data/BG/BG_menu.jpg")
font = pygame.font.Font('./data/fonts/Verdana.ttf', 24)


def main_menu():
    pygame.mixer.music.load("./data/sounds/Jaz_Z.mp3")
    pygame.mixer.music.play(-1)
    vol = 0.01
    pygame.mixer.music.set_volume(vol)
    flag = True
    settings_button = Button((515, 300), 250, 100, "Настройки", font,
                             "./data/buttons/option_button.png",
                             "./data/buttons/option_button_hover.png",
                             "./data/sounds/click.wav")
    play_button = Button((515, 200), 250, 100, "Играть", font,
                         "./data/buttons/play_button.png",
                         "./data/buttons/play_button_hover.png",
                         "./data/sounds/click.wav")
    quit_button = Button((515, 600), 250, 100, "Выход", font,
                         "./data/buttons/quit_button.png",
                         "./data/buttons/quit_button_hover.png",
                         "./data/sounds/click.wav")

    final_button = Button((515, 500), 250, 100, "Авторы", font,
                         "./data/buttons/button_authors.png",
                         "./data/buttons/button_authors_hover.png",
                         "./data/sounds/click.wav")

    statistic_button = Button((515, 400), 250, 100, "Статистика", font,
                         "./data/buttons/statistics_button.png",
                         "./data/buttons/statistics_hover_button.png",
                         "./data/sounds/click.wav")



    running = True
    while running:
        SCREEN.blit(BG_menu, (0, 0))

        text_surface_title = font.render('Карточные игры)', True, (255, 255, 255))
        text_rect_title = text_surface_title.get_rect(center=(WIDTH / 2, 30))
        SCREEN.blit(text_surface_title, text_rect_title)

        text_surface_desc = font.render('Самые известные и веселые карточные игры собраны здесь', True,
                                        (255, 255, 255))
        text_rect_desc = text_surface_desc.get_rect(center=(WIDTH / 2, 100))
        SCREEN.blit(text_surface_desc, text_rect_desc)

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
                game_chooser(SCREEN)

            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_menu(SCREEN)

            if event.type == pygame.USEREVENT and event.button == final_button:
                authors(SCREEN)

            if event.type == pygame.USEREVENT and event.button == statistic_button:
                statisctis_screen(SCREEN)

            if event.type == pygame.USEREVENT and event.button == quit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [play_button, settings_button, quit_button, final_button, statistic_button]:
                btn.han_event(event)

        for btn in [play_button, settings_button, quit_button, final_button, statistic_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        if flag:
            all_sprites.draw(SCREEN)

        pygame.display.flip()


