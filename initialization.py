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
deck = load_deck()

BG_menu = pygame.image.load("data/BG/BG_menu.jpg")
BG_game = pygame.image.load("data/BG/BG_game.jpg")
font = pygame.font.Font('data/fonts/Verdana.ttf', 24)


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


def main_menu():
    flag = True
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

            if event.type == pygame.MOUSEMOTION:
                coords = event.pos
                flag = pygame.mouse.get_focused()

            if event.type == pygame.USEREVENT and event.button == play_button:
                game()

            if event.type == pygame.USEREVENT and event.button == quit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [play_button, quit_button]:
                btn.han_event(event)

        for btn in [play_button, quit_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        pygame.display.flip()


def game():
    index = 0
    flag = True
    players = [Player(f"Игрок {i + 1}") for i in range(4)]  # Создаем 4-х игроков
    deck = load_deck()

    # Раздаем карты игрокам
    for i, player in enumerate(players):
        player.hand = deck[i * 13:(i + 1) * 13]  # По 13 карт каждому

    current_player_idx = 0
    is_con_started = False
    cards_on_table = []

    running = True
    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_game, (0, 0))

        current_player = players[current_player_idx]

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
