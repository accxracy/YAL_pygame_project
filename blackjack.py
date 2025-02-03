import pygame
import random
from Nauru import create_deck
from main_menu_buttons import Button
import sys, os
from sprite_classes import all_sprites, sprite
from sprite_classes import Card

pygame.init()

def load_image(name, colorkey=None):
    fullname = os.path.join('././data', name)
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

BG_menu = pygame.image.load("./././data/BG/BG_menu.jpg")

font = pygame.font.Font('./././data/fonts/Verdana.ttf', 24)


pygame.mouse.set_visible(False)


def stat_writer():
    with open('./././data/stat.txt', 'r+') as fin:
        stat = fin.read()
        wins_chicken = ''.join(stat.split(';')[0]).split(':')[1]

        wins_blackjack = int(''.join(stat.split(';')[1]).split(':')[1]) + 1

    with open('./././data/stat.txt', 'w') as fout:
        fout.write(f'wins_chicken:{wins_chicken};')
        fout.write(f'wins_blackjack:{wins_blackjack};')


back = Card(0, "./././data/cards/cards_set_1/back.png")


def finish_game(score_player, score_bot):
    if score_player > 21 and score_bot > 21:
        return 'Ничья'
    elif score_player == score_bot:
        return 'Ничья'
    elif score_player < 21 and score_bot < 21:
        if score_player > score_bot:
            stat_writer()
            return 'Выйграл Пользователь'

        return 'Выйграл Бот'

    elif score_player == 21 and score_bot == 21:
        return 'Ничья'

    elif score_bot > 21:
        stat_writer()
        return 'Выйграл пользователь'

    elif score_player > 21:
        return 'Выйграл бот'

    elif score_bot == 21:
        return 'Выйграл бот'

    elif score_player == 21:
        stat_writer()
        return 'Выйграл пользователь'


def blackjack_game(SCREEN):

    with open('./././data/settings/settings.ini', 'r+') as fin:
        settings = fin.read()

        deck_number = settings.split('deck_type=')[1]

    flag = True
    running = True
    started = False



    card_sprites = {}
    deck = create_deck()
    for i in deck:
        sprite_card = Card(640, f"./././data/cards/cards_set_{deck_number}/{i}.png")
        sprite_card.rect = sprite.image.get_rect()
        card_sprites[i] = sprite_card

    turn = 'Игрок'
    hands = [[], []]
    card_index = 0

    player_score = 0
    bot_score = 0

    stop_player = False

    global bot_stop
    bot_stop = False
    bot_choice = '-'

    finished = False

    ending = ''

    add_button = Button((800, 500), 150, 75, "Еще", pygame.font.Font('./././data/fonts/Verdana.ttf', 20),
                         "./././data/buttons/statistics_button.png",
                         "./././data/buttons/statistics_hover_button.png",
                         sound='./././data/sounds/card_sound.mp3')

    stop_button = Button((800, 400), 150, 75, "Стоп", pygame.font.Font('./././data/fonts/Verdana.ttf', 20),
                         "./././data/buttons/statistics_button.png",
                         "./././data/buttons/statistics_hover_button.png",
                         "./././data/sounds/click.wav")

    start_button = Button((800, 600), 150, 75, "Начать", pygame.font.Font('./././data/fonts/Verdana.ttf', 20),
                             "./././data/buttons/play_button.png",
                             "./././data/buttons/play_button_hover.png",
                             "./././data/sounds/click.wav")

    next_step = Button((800, 300), 150, 75, "Ход!", pygame.font.Font('./././data/fonts/Verdana.ttf', 20),
                         "././data/buttons/statistics_button.png",
                         "././data/buttons/statistics_hover_button.png",
                         sound='././data/sounds/card_sound.mp3')

    back_button = Button((1100, 600), 150, 75, "Выйти",
                         pygame.font.Font('././data/fonts/Verdana.ttf', 20),
                         "././data/buttons/quit_button.png",
                         "././data/buttons/quit_button_hover.png",
                         "././data/sounds/click.wav")

    buttons = [start_button, stop_button, add_button, next_step, back_button]

    while running:

        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_menu, (0, 0))

        SCREEN.blit(back.image, (640, 250))

        text_surface = font.render(f"Ваш Счет:{player_score}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(500, 600))
        SCREEN.blit(text_surface, text_rect)

        text_surface = font.render(f"Счет противника:{bot_score}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(500, 200))
        SCREEN.blit(text_surface, text_rect)

        text_surface = font.render(f"Ходит: {turn}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(1000, 30))
        SCREEN.blit(text_surface, text_rect)

        if stop_player:
            text_surface = font.render(f"Бот: {bot_choice}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(1000, 70))
            SCREEN.blit(text_surface, text_rect)
        if finished:
            text_surface = font.render(f"Исход: {ending}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(1000, 100))
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

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False

            if event.type == pygame.USEREVENT and event.button == start_button:
                started = True

                buttons.pop(0)

                deck = create_deck()
                turn = 'Игрок'
                hands = [[], []]
                card_index = 0
                player_score = 0
                bot_score = 0
                stop_player = False
                bot_stop = False
                bot_choice = '-'
                finished = False
                ending = ''


                hands[0].append(deck[card_index])
                score = int(deck[card_index].split('_')[1])
                if score > 10 and score != 14:
                    player_score += 10
                elif score == 14:
                    player_score += 1
                else:
                    player_score += score
                card_index += 1

                hands[0].append(deck[card_index])
                score = int(deck[card_index].split('_')[1])
                if score > 10 and score != 14:
                    player_score += 10
                elif score == 14:
                    player_score += 1
                else:
                    player_score += score
                card_index += 1

                hands[1].append(deck[card_index])
                score = int(deck[card_index].split('_')[1])
                if score > 10 and score != 14:
                    bot_score += 10
                elif score == 14:
                    bot_score += 1
                else:
                    bot_score += score
                card_index += 1

                hands[1].append(deck[card_index])
                score = int(deck[card_index].split('_')[1])
                if score > 10 and score != 14:
                    bot_score += 10
                elif score == 14:
                    bot_score += 1
                else:
                    bot_score += score
                card_index += 1

            if event.type == pygame.USEREVENT and event.button == add_button:
                if started:
                    if not stop_player:
                        hands[0].append(deck[card_index])
                        print(deck[card_index])
                        score = int(deck[card_index].split('_')[1])
                        if score > 10 and score != 14:
                            player_score += 10
                        elif score == 14:
                            player_score += 1
                        else:
                            player_score += score

                        if player_score >= 21:
                            ending = finish_game(player_score, bot_score)
                            buttons.insert(0, start_button)
                            finished = True
                            stop_player = True

                    card_index += 1

            if event.type == pygame.USEREVENT and event.button == stop_button:
                if started:
                    stop_player = True
                    turn = 'Бот'

            if event.type == pygame.USEREVENT and event.button == next_step:
                if started:
                    if stop_player:
                        while bot_score in range(16, 20):
                            step = random.randint(1, 2)
                            if step == 1:
                                bot_choice = 'Еще!'
                                hands[1].append(deck[card_index])
                                score = int(deck[card_index].split('_')[1])
                                if score > 10 and score != 14:
                                    bot_score += 10
                                elif score == 14:
                                    bot_score += 1
                                else:
                                    bot_score += score
                                card_index += 1

                            elif step == 2:
                                bot_choice = 'СТОП'
                                ending = finish_game(player_score, bot_score)
                                buttons.insert(0, start_button)
                                finished = True
                                bot_stop = True
                                break

                            if bot_score not in range(16, 20):
                                break

                        if 20 <= bot_score < 21:
                            bot_choice = 'СТОП'
                            bot_stop = True
                            ending = finish_game(player_score, bot_score)
                            buttons.insert(0, start_button)
                            finished = True

                        elif bot_score == 21:
                            bot_choice = 'СТОП'
                            bot_stop = True
                            ending = finish_game(player_score, bot_score)
                            buttons.insert(0, start_button)
                            finished = True

                        elif bot_score > 21:
                            bot_choice = '-'
                            bot_stop = True
                            ending = finish_game(player_score, bot_score)
                            buttons.insert(0, start_button)
                            finished = True

                        elif bot_score < 16:
                            bot_choice = 'Еще!'
                            hands[1].append(deck[card_index])
                            score = int(deck[card_index].split('_')[1])
                            if score > 10 and score != 14:
                                bot_score += 10
                            elif score == 14:
                                bot_score += 1
                            else:
                                bot_score += score
                            card_index += 1

                        elif player_score < bot_score < 21:
                            bot_choice = '-'
                            bot_stop = True
                            ending = finish_game(player_score, bot_score)
                            buttons.insert(0, start_button)
                            finished = True

                        elif bot_score < player_score < 21:
                            bot_choice = 'Еще!'
                            hands[1].append(deck[card_index])
                            score = int(deck[card_index].split('_')[1])
                            if score > 10 and score != 14:
                                bot_score += 10
                            elif score == 14:
                                bot_score += 1
                            else:
                                bot_score += score
                            card_index += 1

            for btn in buttons:
                btn.han_event(event)
        for btn in buttons:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)
        if started:
            x_1 = 100
            if hands[0] or hands[0]:
                for i in hands[0]:
                    SCREEN.blit(card_sprites[i].image, (x_1, 500))
                    x_1 += 50

            x_2 = 100

            if hands[1]:
                for i in hands[1]:
                    SCREEN.blit(card_sprites[i].image, (x_2, 50))
                    x_2 += 50

        if flag:
            all_sprites.draw(SCREEN)
        pygame.display.flip()

