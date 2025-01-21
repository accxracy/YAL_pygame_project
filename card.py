import pygame
import os
import sys
from random import shuffle

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


class Card:
    def __init__(self, set_number, suit, rank):
        self.card = load_image(f'cards/cards_set_{set_number}/{suit}_{rank}.png')
        self.flag = True
        self.set_number = set_number

    def get_card(self):
        if self.flag:
            return self.card
        else:
            return load_image(f'cards/cards_set_{self.set_number}/back.png')

    def change_flag(self):
        self.flag = not self.flag


def load_deck(deck_number):
    deck = []
    for j in range(4):
        for k in range(2, 15):
            deck.append(Card(deck_number, j, k).get_card())
    shuffle(deck)
    return deck
