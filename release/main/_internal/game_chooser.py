import pygame
from main_menu_buttons import Button
import sys, os
from sprite_classes import all_sprites, sprite
from Nauru import nauru_game
from blackjack import blackjack_game


pygame.init()

BG_menu = pygame.image.load("./data/BG/BG_menu.jpg")
BG_game = pygame.image.load("./data/BG/BG_game.jpg")
font = pygame.font.Font('./data/fonts/Verdana.ttf', 24)


pygame.mouse.set_visible(False)


def game_chooser(SCREEN):

    flag = True
    back_button = Button((50, 50), 150, 75, "Назад", pygame.font.Font('./data/fonts/Verdana.ttf', 20),
                         "./data/buttons/quit_button.png",
                         "./data/buttons/quit_button_hover.png",
                         "./data/sounds/click.wav")

    nauru_button = Button((200, 300), 250, 100, "Курочка", pygame.font.Font('./data/fonts/Verdana.ttf', 20),
                         "./data/buttons/play_button.png",
                         "./data/buttons/play_button_hover.png",
                         "./data/sounds/click.wav")


    blackjack_button = Button((600, 300), 250, 100, "Блекджек", pygame.font.Font('./data/fonts/Verdana.ttf', 20),
                             "./data/buttons/play_button.png",
                             "./data/buttons/play_button_hover.png",
                             "./data/sounds/click.wav")

    running = True


    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_game, (0, 0))


        rules_nauru = font.render("Игроки по очереди тянут карты;", True, (255, 255, 255))
        text_rect = rules_nauru.get_rect(center=(315, 500))
        SCREEN.blit(rules_nauru, text_rect)
        rules_nauru = font.render("забирает все карты с рук соперников. ",
        True, (255, 255, 255))
        text_rect = rules_nauru.get_rect(center=(315, 560))
        SCREEN.blit(rules_nauru, text_rect)
        rules_nauru = font.render("тот, кто угадал масть последней карты,",
                                  True, (255, 255, 255))
        text_rect = rules_nauru.get_rect(center=(315, 530))
        SCREEN.blit(rules_nauru, text_rect)

        rules_nauru = font.render("Побеждает игрок с наименьшим",
                                  True, (255, 255, 255))
        text_rect = rules_nauru.get_rect(center=(315, 590))
        SCREEN.blit(rules_nauru, text_rect)

        rules_nauru = font.render("кол-вом карт.",
                                  True, (255, 255, 255))
        text_rect = rules_nauru.get_rect(center=(315, 620))
        SCREEN.blit(rules_nauru, text_rect)

        rules_bj = font.render("все знают правила",
                                  True, (255, 255, 255))
        text_rect = rules_bj .get_rect(center=(750, 500))
        SCREEN.blit(rules_bj , text_rect)



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

            if event.type == pygame.USEREVENT and event.button == nauru_button:
                nauru_game(SCREEN)

            if event.type == pygame.USEREVENT and event.button == blackjack_button:
                blackjack_game(SCREEN)



            for btn in [back_button, nauru_button, blackjack_button]:
                btn.han_event(event)
        for btn in [back_button, nauru_button, blackjack_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        if flag:
            all_sprites.draw(SCREEN)
        pygame.display.flip()