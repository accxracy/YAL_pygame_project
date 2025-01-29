import pygame
from main_menu_buttons import Button
import sys, os
from sprite_classes import all_sprites, sprite


pygame.init()

BG_menu = pygame.image.load("data/BG/BG_menu.jpg")
BG_game = pygame.image.load("data/BG/BG_game.jpg")
font = pygame.font.Font('data/fonts/Verdana.ttf', 24)


pygame.mouse.set_visible(False)


def settings_menu(SCREEN):
    flag = True

    with open('data/settings/settings.ini', 'r+') as fin:
        settings = fin.read()


    deck_number = settings.split('deck_type=')[1]


    back_button = Button((600, 600), 250, 100, "Назад", font,
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.wav")
    deck1_button = Button((10, 300), 200, 200, None, font,
                          "data/buttons/full_1.png",
                          "data/buttons/full_1_hover.png",
                          "data/sounds/click.wav")
    deck2_button = Button((300, 300), 200, 200, None, font,
                          "data/buttons/full_2.png",
                          "data/buttons/full_2_hover.png",
                          "data/sounds/click.wav")
    apply_button = Button((300, 600), 250, 100, 'Применить', font,
                          "data/buttons/option_button.png",
                          "data/buttons/option_button_hover.png",
                          "data/sounds/click.wav")
    running = True
    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_menu, (0, 0))

        text_surface = font.render("Настройки", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(720 / 2, 30))
        SCREEN.blit(text_surface, text_rect)
        text_surface_type = font.render(f"тип колоды: {deck_number}", True, (255, 255, 255))
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

            if event.type == pygame.USEREVENT and event.button == apply_button:
                with open('data/settings/settings.ini', 'w') as fout:
                    fout.write(f'deck_type={deck_number}')

            for btn in [back_button, deck1_button, deck2_button, apply_button]:
                btn.han_event(event)
        for btn in [back_button, deck1_button, deck2_button, apply_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        if flag:
            all_sprites.draw(SCREEN)
        pygame.display.flip()
