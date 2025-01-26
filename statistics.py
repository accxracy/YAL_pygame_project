import pygame
from main_menu_buttons import Button
import sys, os
from sprite_classes import all_sprites, sprite


pygame.init()

BG_menu = pygame.image.load("data/BG/BG_menu.jpg")
BG_game = pygame.image.load("data/BG/BG_game.jpg")
font = pygame.font.Font('data/fonts/Verdana.ttf', 24)









pygame.mouse.set_visible(False)


def statisctis_screen(SCREEN):
    flag = True

    with open('data/stat.txt', 'r+') as fin:

        stat = fin.read()

    wins = stat.split('wins:')[1]


    back_button = Button((515, 600), 250, 100, "Назад", font,
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.wav")

    running = True
    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_menu, (0, 0))

        text_surface = font.render("Статистика курочки", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(720 / 2, 30))
        SCREEN.blit(text_surface, text_rect)

        text_surface = font.render(f"Побед:{wins}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(720 / 2, 70))
        SCREEN.blit(text_surface, text_rect)

        text_surface_type = font.render(f"Статистика Футбольчика", True, (255, 255, 255))
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



            for btn in [back_button]:
                btn.han_event(event)
        for btn in [back_button]:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        if flag:
            all_sprites.draw(SCREEN)
        pygame.display.flip()
