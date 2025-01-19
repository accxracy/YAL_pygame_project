from random import shuffle


def create_deck():
    deck = []
    suits = ['0', '1', '2', '3']
    ranks = ['6', '7', '8', '9', '10', '11', '12', '13', '14']
    for suit in suits:
        for rank in ranks:
            deck.append(f"{suit}_{rank}")
    shuffle(deck)
    return deck

def deal_cards(deck):
    size = 9
    all_hand = [deck[i:i + size] for i in range(0, len(deck), size)]
    return all_hand

class Player:
    def __init__(self, hand):
        self.hand = hand
        self.moves = ['translate', 'trust', 'don`t trust']
    '''
    def move(self, move_number, card_number=None, cards=None):
        if move_number == 0:
            cards = cards
            card_number = card_number
            self.hand = list(set(self.hand) - set(cards))
        elif move_number == 1:
            pass
        elif move_number == 2:
            pass
    '''

    def return_hand(self):
        return self.hand

deck = create_deck()
all_hand = deal_cards(deck)

player = Player(all_hand[0])
print(player.return_hand())




