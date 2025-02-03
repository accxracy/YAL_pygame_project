from random import shuffle
import pygame
from main_menu_buttons import Button
import sys, os
from sprite_classes import all_sprites, sprite, Card


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

font = pygame.font.Font('data/fonts/Verdana.ttf', 24)


pygame.mouse.set_visible(False)


def nauru_game(SCREEN):



    with open('data/settings/settings.ini', 'r+') as fin:
        settings = fin.read()

        deck_number = settings.split('deck_type=')[1]


    back_button = Button((50, 50), 150, 75, "Выйти",
                         pygame.font.Font('data/fonts/Verdana.ttf', 20),
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.wav")

    deck_button =  Button((640, 360), 97, 136, "",
                         pygame.font.Font('data/fonts/Verdana.ttf', 20),
                         "data/cards/cards_set_1/back.png", sound='data/sounds/card_sound.mp3')

    deck = create_deck()


    flag = True
    running = True
    started = False
    finished = False
    speed = 10

    current_cards = []
    current_hands = [[], [], [], []]
    hands = [[], [], [], []]
    last_lost = False
    card_index = 0
    turn_number = 1
    back = Card(0, 'data/cards/cards_set_1/back.png')

    card_sprites = {}


    for i in deck:
        sprite_card = Card(640,  f"data/cards/cards_set_{deck_number}/{i}.png")
        sprite_card.rect = sprite.image.get_rect()
        card_sprites[i] = sprite_card


    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_menu, (0, 0))

        if not started:
            text_surface = font.render("Нажмите ENTER, чтобы начать", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(700, 600))
            SCREEN.blit(text_surface, text_rect)

        if True:
            text_surface = font.render(f"Ход игрока номер:{turn_number}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(1000, 30))
            SCREEN.blit(text_surface, text_rect)

            text_surface = font.render(f"Осталось Карт: {36 - card_index}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(1000, 70))
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


        if last_lost and not finished:
            text_surface = font.render(f"Игрок номер {turn_number} забирает карты", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(640, 10))
            SCREEN.blit(text_surface, text_rect)

        if finished:
            if finished:
                global winner_num
                text_surface = font.render(f"Победил игрок номер {winner_num}!", True,
                                           (255, 255, 255))
                text_rect = text_surface.get_rect(center=(640, 10))
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
                    current_hands = [[], [], [], []]
                    hands = [[], [], [], []]
                    current_cards.clear()
                    turn_number = 1
                    deck = create_deck()
                    last_lost = False
                    started = True
                    finished = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False

            if ((event.type == pygame.USEREVENT and event.button == deck_button) or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):

                if started:

                    if last_lost:
                        current_hands = [[], [], [], []]
                        turn_number += 1
                        if turn_number == 5:
                            turn_number = 1
                        last_lost = False
                    else:
                        card_index += 1

                        if card_index == 36:

                            winner_list = min(hands, key=lambda x: len(x))
                            winner_num = hands.index(winner_list) + 1
                            if winner_num == 1:
                                with open('data/stat.txt', 'r+') as fin:
                                    stat = fin.read()
                                    wins_chicken = int(''.join(stat.split(';')[0]).split(':')[1]) + 1

                                    wins_blackjack = ''.join(stat.split(';')[1]).split(':')[1]

                                with open('data/stat.txt', 'w') as fout:
                                    fout.write(f'wins_chicken:{wins_chicken};')
                                    fout.write(f'wins_blackjack:{wins_blackjack};')


                            finished = True

                            started = False

                            SCREEN.blit(text_surface, text_rect)

                            card_index = 0

                        if current_cards:
                            if deck[card_index].split('_')[0] == current_cards[-1].split('_')[0]:
                                for i in current_cards:
                                    hands[turn_number - 1].append(i)



                                current_hands[turn_number - 1].append(deck[card_index])
                                for i in current_hands[turn_number - 1]:
                                    hands[turn_number - 1].append(i)

                                last_lost = True

                                current_cards.clear()

                            else:
                                current_hands[turn_number - 1].append(deck[card_index])
                                current_cards.append(deck[card_index])

                                turn_number += 1
                                if turn_number == 5:
                                    turn_number = 1

                        else:
                            current_hands[turn_number - 1].append(deck[card_index])
                            current_cards.append(deck[card_index])

                            turn_number += 1
                            if turn_number == 5:
                                turn_number = 1


            for btn in [back_button, deck_button]:
                btn.han_event(event)
        for btn in [back_button, deck_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        SCREEN.blit(back.image, (125, 250))
        SCREEN.blit(back.image, (575, 170))
        SCREEN.blit(back.image, (975, 250))
        if started:

            x_1 = 100
            y_1 = 500

            if current_hands[0] or hands[0]:
                for i in current_hands[0]:

                    SCREEN.blit(card_sprites[i].image, (x_1, y_1))
                    x_1 += 50
                for i in hands[0]:
                    if i not in current_hands[0]:
                        SCREEN.blit(card_sprites[i].image, (x_1, y_1))
                        x_1 += 50

            x_2 = 200

            if current_hands[1]:
                for i in current_hands[1]:
                   SCREEN.blit(card_sprites[i].image, (x_2, 250))
                   x_2 += 50

            x_3 = 600

            if current_hands[2]:
                for i in current_hands[2]:
                   SCREEN.blit(card_sprites[i].image, (x_3, 170))
                   x_3 += 50

            x_4 = 1000

            if current_hands[3]:
                for i in current_hands[3]:
                   SCREEN.blit(card_sprites[i].image, (x_4, 250))
                   x_4 += 50

        if flag:
            all_sprites.draw(SCREEN)

        pygame.display.flip()


