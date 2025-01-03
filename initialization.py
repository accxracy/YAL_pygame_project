import pygame, sys, os
from main_menu_buttons import Button
from card import load_deck, Card


pygame.init()
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Блеф")


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


BG_menu = pygame.image.load("data/BG/BG_menu.jpg")
BG_game = pygame.image.load("data/BG/BG_game.jpg")
font = pygame.font.Font('data/fonts/Verdana.ttf', 24)


def main_menu():
    settings_button = Button((100, 360), 250, 100, "Настройки", font,
                             "data/buttons/option_button.png",
                             "data/buttons/option_button_hover.png",
                             "data/sounds/click.mp3")
    play_button = Button((640, 360), 250, 100, "Играть", font,
                         "data/buttons/play_button.png",
                         "data/buttons/play_button_hover.png",
                         "data/sounds/click.mp3")
    quit_button = Button((1000, 360), 250, 100, "Выход", font,
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.mp3")
    running = True
    while running:
        SCREEN.blit(BG_menu, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == play_button:
                game()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == quit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [play_button, settings_button, quit_button]:
                btn.han_event(event)

        for btn in [play_button, settings_button, quit_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        pygame.display.flip()


def settings_menu():
    back_button = Button((1000, 360), 250, 100, "Назад", font,
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.mp3")
    running = True
    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_menu, (0, 0))

        text_surface = font.render("Настройки", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 100))
        SCREEN.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:

                running = False

            back_button.han_event(event)
        back_button.checking_hover(pygame.mouse.get_pos())
        back_button.draw(SCREEN)

        pygame.display.flip()


def game():
    index = 0

    back_button = Button((1000, 360), 250, 100, "Назад", font,
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.mp3")
    running = True
    fps = 10
    clock = pygame.time.Clock()
    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_game, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    index = (index + 1) % 104
                # if event.key == pygame.K_q:
                #     Card.change_flag(self=Card)
            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False
            back_button.han_event(event)
        for btn in [back_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)
        SCREEN.blit(load_deck()[index], (10, 10))

        pygame.display.flip()
        clock.tick(fps)




