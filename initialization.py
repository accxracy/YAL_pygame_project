import pygame
import sys
import os
from main_menu_buttons import Button
from card import load_deck, Card
from player import Player

pygame.init()

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Блеф")
deck_number = 1


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("arrow.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
pygame.mouse.set_visible(False)

BG_menu = pygame.image.load("data/BG/BG_menu.jpg")
BG_game = pygame.image.load("data/BG/BG_game.jpg")
font = pygame.font.Font('data/fonts/Verdana.ttf', 24)
deck = load_deck()


def main_menu():
    flag = True
    settings_button = Button((515, 400), 250, 100, "Настройки", font,
                             "data/buttons/option_button.png",
                             "data/buttons/option_button_hover.png",
                             "data/sounds/click.mp3")
    play_button = Button((515, 200), 250, 100, "Играть", font,
                         "data/buttons/play_button.png",
                         "data/buttons/play_button_hover.png",
                         "data/sounds/click.mp3")
    quit_button = Button((515, 600), 250, 100, "Выход", font,
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.mp3")

    running = True
    while running:
        SCREEN.blit(BG_menu, (0, 0))

        text_surface_title = font.render('Карточная игра "Блеф"', True, (255, 255, 255))
        text_rect_title = text_surface_title.get_rect(center=(WIDTH / 2, 30))
        SCREEN.blit(text_surface_title, text_rect_title)

        text_surface_desc = font.render('Избавьтесь от всех карт, обманув соперников и не дав обмануть себя.', True,
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

        if flag:
            all_sprites.draw(SCREEN)

        pygame.display.flip()


def settings_menu():
    flag = True
    back_button = Button((515, 600), 250, 100, "Назад", font,
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.mp3")
    deck1_button = Button((10, 300), 200, 200, None, font,
                          "data/buttons/full_1.png",
                          "data/buttons/full_1_hover.png",
                          "data/sounds/click.mp3")
    deck2_button = Button((300, 300), 200, 200, None, font,
                          "data/buttons/full_2.png",
                          "data/buttons/full_2_hover.png",
                          "data/sounds/click.mp3")
    running = True
    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_menu, (0, 0))

        text_surface = font.render("Настройки", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 30))
        SCREEN.blit(text_surface, text_rect)
        global deck_number
        text_surface_type = font.render(f"Тип колоды: {deck_number}", True, (255, 255, 255))
        text_rect_type = text_surface_type.get_rect(center=(200, 100))
        SCREEN.blit(text_surface_type, text_rect_type)

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

            if event.type == pygame.USEREVENT and event.button == deck1_button:
                deck_number = 1
            if event.type == pygame.USEREVENT and event.button == deck2_button:
                deck_number = 2

            for btn in [back_button, deck1_button, deck2_button]:
                btn.han_event(event)

        for btn in [back_button, deck1_button, deck2_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        if flag:
            all_sprites.draw(SCREEN)
        pygame.display.flip()


def game():
    index = 0
    flag = True

    back_button = Button((515, 600), 250, 100, "Назад", font,
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.mp3")

    players = [Player(f"Игрок {i + 1}") for i in range(4)]  # Создаем 4-х игроков
    deck = load_deck()

    # Раздаем карты игрокам
    for i, player in enumerate(players):
        player.hand = deck[i * 13:(i + 1) * 13]  # По 13 карт каждому

    current_player_idx = 0
    is_con_started = False
    cards_on_table = []

    running = True
    fps = 60
    clock = pygame.time.Clock()
    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_game, (0, 0))

        # Отображаем карты на руках игроков
        current_player = players[current_player_idx]
        x_offset = 100  # Начальная позиция для карт
        y_offset = 500  # Позиция для карт на экране (по Y)

        # Отображаем карты для каждого игрока
        for i, card in enumerate(current_player.hand):
            # Размещаем карты с небольшим отступом друг от друга
            SCREEN.blit(card, (x_offset + i * 30, y_offset))  # 30 - это шаг между картами

        # Проверка начала кона (для первого игрока)
        if not is_con_started:
            if current_player.is_turn:
                # Игрок делает кон
                selected_cards = current_player.play_card(num_cards=3, rank="5")  # Пример
                cards_on_table.extend(selected_cards)
                is_con_started = True
                current_player_idx = (current_player_idx + 1) % 4  # Переход хода
        else:
            if current_player.is_turn:
                # Игрок может выбрать Поверить, Не поверить, Перевести
                decision = "verify"  # Пример действия
                if decision == "verify":
                    # Поверить - проверяем карты предыдущего игрока
                    pass
                elif decision == "not_verify":
                    # Не верю - проверяем карты
                    pass
                elif decision == "pass":
                    # Перевести ход
                    current_player_idx = (current_player_idx + 1) % 4

        # Отображаем карты на столе и интерфейс
        for card in cards_on_table:
            SCREEN.blit(card, (100, 100))  # Примерная позиция

        pygame.display.flip()
        clock.tick(fps)
