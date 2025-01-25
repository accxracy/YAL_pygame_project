from random import shuffle
import pygame
from main_menu_buttons import Button
import sys, os
from cursor import all_sprites, sprite


pygame.init()


def create_deck():
    deck = []
    suits = ['0', '1', '2', '3']
    ranks = ['6', '7', '8', '9', '10', '11', '12', '13', '14']
    for suit in suits:
        for rank in ranks:
            deck.append(f"{suit}_{rank}")
    shuffle(deck)
    return deck


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


pygame.mouse.set_visible(False)


def nauru_game(SCREEN):

    with open('data/settings/settings.ini', 'r+') as fin:
        settings = fin.read()
        print(settings)
        deck_number = settings.split('deck_type=')[1]
        print(deck_number)

    back_button = Button((50, 50), 150, 75, "Выйти",
                         pygame.font.Font('data/fonts/Verdana.ttf', 20),
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.wav")

    deck_button =  Button((640, 300), 97, 136, "",
                         pygame.font.Font('data/fonts/Verdana.ttf', 20),
                         "data/cards/cards_set_1/back.png")

    deck = create_deck()

    print(len(deck))

    flag = True
    running = True
    started = False
    cards_left = True
    finished = False
    current_cards = []
    hands = [[], [], [], []]
    card_index = 0
    turn_number = 1

    suits = {'0' : 'Крести' , '1': 'Бубны' , '2':'Черви' , '3': 'Пики'}

    last_suit = None


    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_game, (0, 0))

        if not started:
            text_surface = font.render("Нажмите ENTER, чтобы начать", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(700, 500))
            SCREEN.blit(text_surface, text_rect)

        if started or finished:
            text_surface = font.render(f"Ход игрока номер:{turn_number}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(1000, 30))
            SCREEN.blit(text_surface, text_rect)

            text_surface = font.render(f"Последняя Масть: {suits[last_suit]}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(1000, 70))
            SCREEN.blit(text_surface, text_rect)

            text_surface = font.render(f"Осталось Карт: {36 - card_index}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(1000, 110))
            SCREEN.blit(text_surface, text_rect)

            text_surface = font.render(f"Игрок номер 2", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(200, 200))
            SCREEN.blit(text_surface, text_rect)

            text_surface = font.render(f"x{len(hands[1])}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(200, 230))
            SCREEN.blit(text_surface, text_rect)

            text_surface = font.render(f"Игрок номер 3", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(640, 100))
            SCREEN.blit(text_surface, text_rect)

            text_surface = font.render(f"x{len(hands[2])}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(640, 130))
            SCREEN.blit(text_surface, text_rect)

            text_surface = font.render(f"Игрок номер 4", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(1100, 200))
            SCREEN.blit(text_surface, text_rect)

            text_surface = font.render(f"x{len(hands[3])}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(1100, 230))
            SCREEN.blit(text_surface, text_rect)


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
                if event.key == pygame.K_RETURN:
                    started = True
                    deck_button.change_image(f'data/cards/cards_set_{deck_number}/{deck[card_index]}.png')
                    last_suit = deck[card_index].split('_')[0]
                    card_index += 1

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False

            if event.type == pygame.USEREVENT and event.button == deck_button:

                if started:

                    if cards_left:
                        deck_button.change_image(f'data/cards/cards_set_{deck_number}/{deck[card_index]}.png')
                        last_suit = deck[card_index].split('_')[0]
                        if current_cards:
                            if deck[card_index].split('_')[0] == current_cards[-1].split('_')[0]:
                                for i in current_cards:
                                    hands[turn_number - 1].append(i)
                                print(hands)
                                current_cards.clear()
                                card_index += 1
                                turn_number += 1
                                if turn_number == 5:
                                    turn_number = 1

                            else:
                                current_cards.append(deck[card_index])
                                card_index += 1
                                turn_number += 1
                                if turn_number == 5:
                                    turn_number = 1
                        else:
                            current_cards.append(deck[card_index])
                            card_index += 1
                            turn_number += 1
                            if turn_number == 5:
                                turn_number = 1


                    if card_index == 36:
                        winner = min(hands, key=lambda x: len(x))
                        print(f'Победил игрок номер: {hands.index(winner) + 1}')

                        hands = [[], [], [], []]
                        started = False
                        deck_button.change_image(f'data/cards/cards_set_1/back.png')
                        turn_number = 1
                        deck = create_deck()
                        finished = True
                        card_index = 0


            for btn in [back_button, deck_button]:
                btn.han_event(event)
        for btn in [back_button, deck_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        if flag:
            all_sprites.draw(SCREEN)
        pygame.display.flip()
