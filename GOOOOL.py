"""ПРАВИЛА ФУТБОЛЬЧИКА (КОДИНГОВЫЕ)
Колода делиться на две равные части - колоду игрока и колоду бота.
После из этой колоды расставляются игроки на поле игрок берет
первые 4 карты и перетаскивает их в области (проверятеся коллизией) вратаря и трех защитников.
Бот просто первую карту из своей колоды ставит на место вратаря и три карты на защитника.
Потом игрок делает ход:
открывается верхняя карта из его колоды и игрок перетаскивает ее на одного из защитников
(конкретный защитник, которого бьют, определяется коллизией, после того как карта коснулась защитника,
карту больше нельзя тащить) и дальше проверяется, какая карта сильнее.
Если сильнее карта защитника - тогда защитник остается на месте и карта отакуещего
идет в конец колоды обороняющегося. Если же карта атакующего сильнее,
то тогда обе карты (и защитник и нападающий) идут в конец колоды атакующего.
Всего отакующих три. Если атакующие побили всех защитников, то вытаскивается последняя карта
и выходит на вратаря. Если карта атакующего сильнее карты вратаря, то атакующему игроку переходит очко 
(гол!) и обе карты(вратарь и атакующий) уходят в конец колоды атакующего,
а если карта вратаря сильнее, то обороняющийся забирает в конец колоды карту нападающего.
После каждой атаки идет проверка, все ли защитники (их должно быть 3)
на метсах, и если нет, то они восполняются из колоды

"""



import pygame
import random
from main_menu_buttons import Button
import sys, os
from sprite_classes import all_sprites, sprite, Card

pygame.init()

# Определяем размеры экрана
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def stat_writer():
    with open('data/stat.txt', 'r+') as fin:
        stat = fin.read()
        wins_chicken = ''.join(stat.split(';')[0]).split(':')[1]

        wins_blackjack = int(''.join(stat.split(';')[1]).split(':')[1])

        wins_football = int(''.join(stat.split(';')[1]).split(':')[1]) + 1

    with open('data/stat.txt', 'w') as fout:
        fout.write(f'wins_chicken:{wins_chicken};')
        fout.write(f'wins_blackjack:{wins_blackjack};')
        fout.write(f'wins_football:{wins_football}')


def create_deck():
    deck = []
    suits = ['0', '1', '2', '3']  # Масти от 0 до 3
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']  # Ранги от 2 до 14
    for suit in suits:
        for rank in ranks:
            deck.append(f"{suit}_{rank}")
    random.shuffle(deck)
    return deck


def finish_game(hands, score_player, score_bot):
    if len(hands[0]) == 0 or score_bot == 1:
        return 'Игрок 2 победил!'
    elif len(hands[1]) == 0 or score_player == 1:
        return 'Игрок 1 победил!'
    return None


def compare_cards(attacker_card, defender_card):
    rank_order = {rank: index for index, rank in enumerate(['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'])}
    attacker_rank = rank_order[attacker_card.split('_')[1]]
    defender_rank = rank_order[defender_card.split('_')[1]]
    return attacker_rank > defender_rank


def football_game(SCREEN):
    flag = True
    running = True

    back_button = Button((50, 50), 150, 75, "Назад", pygame.font.Font('data/fonts/Verdana.ttf', 20),
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.wav")

    deck = create_deck()
    player_deck = deck[:len(deck)//2]
    bot_deck = deck[len(deck)//2:]

    player_hand = []
    bot_hand = []

    # Расставляем карты на поле
    player_defenders = [None, None, None]  # Защитники игрока
    bot_defenders = [None, None, None]  # Защитники бота
    player_goalkeeper = None
    bot_goalkeeper = None

    # Игрок берет первые 4 карты
    for _ in range(4):
        player_hand.append(player_deck.pop(0))

    # Бот ставит карты
    bot_goalkeeper = bot_deck.pop(0)
    bot_defenders[0] = bot_deck.pop(0)
    bot_defenders[1] = bot_deck.pop(0)
    bot_defenders[2] = bot_deck.pop(0)

    # Создаем спрайты для карт
    player_cards = [Card(100 + i * 30, f"data/cards/cards_set_1/{card}.png") for i, card in enumerate(player_hand)]
    bot_cards = [Card(700 + i * 30, f"data/cards/cards_set_1/{card}.png") for i, card in enumerate(bot_defenders)]

    selected_card = None
    dragging = False
    mouse_offset = (0, 0)

    # Основной игровой цикл
    while running:
        SCREEN.fill((0, 0, 0))

        # Отображение состояния игры
        text_surface = pygame.font.Font('data/fonts/Verdana.ttf', 24).render(f"Игрок: {len(player_hand)} карт", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(400, 100))
        SCREEN.blit(text_surface, text_rect)

        text_surface = pygame.font.Font('data/fonts/Verdana.ttf', 24).render(f"Бот: {len(bot_deck)} карт", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(400, 150))
        SCREEN.blit(text_surface, text_rect)

        # Отображение вратарей и защитников
        if player_goalkeeper:
            SCREEN.blit(Card(100, f"data/cards/cards_set_1/{player_goalkeeper}.png").image, (100, 200))
        for i, defender in enumerate(player_defenders):
            if defender:
                SCREEN.blit(Card(100 + i * 100, f"data/cards/cards_set_1/{defender}.png").image, (100 + i * 100, 300))

        if bot_goalkeeper:
            SCREEN.blit(Card(700, f"data/cards/cards_set_1/{bot_goalkeeper}.png").image, (700, 200))
        for i, defender in enumerate(bot_defenders):
            if defender:
                SCREEN.blit(Card(700 + i * 100, f"data/cards/cards_set_1/{defender}.png").image, (700 + i * 100, 300))

        # Отображение рубашек карт для оставшихся карт в колоде
        for i in range(len(player_deck)):
            SCREEN.blit(Card(100 + i * 30, "data/cards/back.png").image, (100 + i * 30, 400))  # Колода игрока

        for i in range(len(bot_deck)):
            SCREEN.blit(Card(700 + i * 30, "data/cards/back.png").image, (700 + i * 30, 400))  # Колода бота

        # Проверка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    for index, card in enumerate(player_cards):
                        if card.rect.collidepoint(event.pos):
                            selected_card = card
                            mouse_offset = (card.rect.x - event.pos[0], card.rect.y - event.pos[1])
                            dragging = True
                            player_cards.pop(index)
                            break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    for index, defender in enumerate(bot_defenders):
                        if defender and selected_card.rect.collide_mask(defender):
                            if compare_cards(selected_card, defender):
                                player_hand.append(selected_card)
                                player_hand.append(defender)
                                bot_defenders[index] = bot_deck.pop(0) if bot_deck else None
                            else:
                                bot_hand.append(defender)
                                bot_defenders[index] = None
                            selected_card = None
                            dragging = False
                            break
                    else:
                        player_hand.append(selected_card)
                        selected_card = None
                        dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                if selected_card:
                    selected_card.rect.x = event.pos[0] + mouse_offset[0]
                    selected_card.rect.y = event.pos[1] + mouse_offset[1]
            
            

        pygame.display.flip()



# Вызов функции игры
# football_game(SCREEN)  # Не забудьте передать ваш экран в функцию