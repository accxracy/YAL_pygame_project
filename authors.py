import pygame
from main_menu_buttons import Button
import sys, os
from sprite_classes import all_sprites, sprite

pygame.init()

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


BG_game = pygame.image.load("data/BG/BG_menu.jpg")
font = pygame.font.Font('data/fonts/Verdana.ttf', 24)



pygame.mouse.set_visible(False)



def authors(SCREEN):

    back_button = Button((515, 600), 250, 100, "Назад", pygame.font.Font('data/fonts/Verdana.ttf', 20),
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.wav")

    flag = True
    running = True

    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_game, (0, 0))

        text_surface_title = font.render('Финальный экран', True,
                                         (255, 255, 255))
        text_rect_title = text_surface_title.get_rect(center=(600, 30))
        SCREEN.blit(text_surface_title, text_rect_title)
        text_surface_title = font.render('Проект подготовили: Смирнов Вячеслав и Павленко Григорий', True, (255, 255, 255))
        text_rect_title = text_surface_title.get_rect(center=(600, 60))
        SCREEN.blit(text_surface_title, text_rect_title)
        text_surface_title = font.render('Спасибо за внимание', True,
                                         (255, 255, 255))
        text_rect_title = text_surface_title.get_rect(center=(600, 90))
        SCREEN.blit(text_surface_title, text_rect_title)

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