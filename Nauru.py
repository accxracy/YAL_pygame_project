import pygame
from main_menu_buttons import Button
import sys, os
from cursor import all_sprites, sprite
from card import load_deck, get_back

pygame.init()

with open('data/settings/settings.ini', 'r+') as fin:
    settings = fin.read()
    print(settings)
global deck_number
deck_number = settings.split('deck_type=')[1]


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
deck = load_deck(deck_number)

pygame.mouse.set_visible(False)


def nauru_game(SCREEN):

    back_button = Button((50, 50), 150, 75, "Назад",
                         pygame.font.Font('data/fonts/Verdana.ttf', 20),
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.wav")

    flag = True
    running = True

    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_game, (0, 0))
        SCREEN.blit(get_back(), (700, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                coords = event.pos
                flag = pygame.mouse.get_focused()
                sprite.rect.x, sprite.rect.y = coords

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False

            for btn in [back_button]:
                btn.han_event(event)
        for btn in [back_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        if flag:
            all_sprites.draw(SCREEN)
        pygame.display.flip()


def nauru_rules(SCREEN):

    back_button = Button((50, 50), 150, 75, "Назад",
                         pygame.font.Font('data/fonts/Verdana.ttf', 20),
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.wav")

    flag = True
    running = True

    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_game, (0, 0))
        rules_nauru = font.render("ПРАВИЛА КУРОЧКИ", True, (255, 255, 255))
        text_rect = rules_nauru.get_rect(center=(640, 88))
        SCREEN.blit(rules_nauru, text_rect)
        text_coord = 400
        text = ['Каждый игрок вытаскивает из общей стопки карту и кладет ее на стол',
                'Если масти карты на столе, и карты, которую бросил игрок одинаковы,',
                'то игрок забирает все карты на столе.',
                'Забрав карты со стола, игрок ходит только ими, пока его рука не опустеет',
                '',
                '',
                '',
                '',
                '']

        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            SCREEN.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                coords = event.pos
                flag = pygame.mouse.get_focused()
                sprite.rect.x, sprite.rect.y = coords

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False

            for btn in [back_button]:
                btn.han_event(event)
        for btn in [back_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        if flag:
            all_sprites.draw(SCREEN)
        pygame.display.flip()