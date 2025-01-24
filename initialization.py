import pygame, sys, os
from main_menu_buttons import Button
from test import create_deck, deal_cards
from test import Player


pygame.init()
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Карточные игры)")
deck_number = 1


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


all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("arrow.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
pygame.mouse.set_visible(False)

BG_menu = pygame.image.load("data/BG/BG_menu.jpg")
BG_game = pygame.image.load("data/BG/BG_game.jpg")
font = pygame.font.Font('data/fonts/Verdana.ttf', 24)

def main_menu():
    flag = True
    settings_button = Button((515, 400), 250, 100, "Настройки", font,
                             "data/buttons/option_button.png",
                             "data/buttons/option_button_hover.png",
                             "data/sounds/click.wav")
    play_button = Button((515, 200), 250, 100, "Играть", font,
                         "data/buttons/play_button.png",
                         "data/buttons/play_button_hover.png",
                         "data/sounds/click.wav")
    quit_button = Button((515, 600), 250, 100, "Выход", font,
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.wav")



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

    with open('data/settings/settings.ini', 'r+') as fin:
        settings = fin.read()
        print(settings)
    global deck_number
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
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 30))
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


def game():

    deck = create_deck()
    all_hand = deal_cards(deck)
    flag = True
    back_button = Button((50, 50), 100, 60, "Назад", pygame.font.Font('data/fonts/Verdana.ttf', 15),
                         "data/buttons/quit_button.png",
                         "data/buttons/quit_button_hover.png",
                         "data/sounds/click.wav")

    game_buttons = [back_button]

    player = Player(all_hand[0])
    hand = player.return_hand()
    positions = [(100, 550), (150, 550), (200, 550), (250, 550), (300, 550),
                 (350, 550), (400, 550), (450, 550), (500, 550)]
    card_names = []
    translator_suits = {'0' : 'clubs', '1':'diamonds', '2':'hearts', '3':'spades'}
    translator_ranks = {'6':'6', '7':'7', '8':'8', '9':'9', '10':'10', '11':'jack',
                        '12':'queen', '13':'king', '14':'ace'}
    for i in hand:
        card_names.append(f"{translator_suits[i.split('_')[0]]}_{translator_ranks[i.split('_')[1]]}")
    print(card_names)

    for i in range(9):
        game_buttons.append(Button(positions[i], 90, 150, "", font, f"data/cards/cards_set_{deck_number}/{hand[i]}.png",
                f"data/cards/cards_set_{deck_number}/{hand[i]}.png", button_name={card_names[i]}))

    running = True


    while running:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG_game, (0, 0))



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

            for btn in game_buttons:
                btn.han_event(event)
        for btn in game_buttons:
            btn.checking_hover(pygame.mouse.get_pos())
            btn.draw(SCREEN)

        if flag:
            all_sprites.draw(SCREEN)
        pygame.display.flip()


