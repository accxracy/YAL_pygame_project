from bot_AI import SimpleBot, SmartBot
from card import create_deck


deck = create_deck()


def deal_cards(deck, num_players):
    hands = {i: [] for i in range(1, num_players+1)}
    while deck:
        for i in range(1, num_players + 1):
            if deck:
                hands[i].append(deck.pop())
    return hands


class Game:
    def __init__(self, num_players):
        self.deck = deck
        self.hands = deal_cards(self.deck, num_players)
        self.num_players = num_players
        self.turn = 1  # Номер игрока, чей ход
        self.pile = []  # Песочница (куда сбрасываются карты)

    def get_current_player_hand(self):
        return self.hands[self.turn]

    def next_turn(self):
        self.turn = (self.turn + 1) % self.num_players + 1

    def discard_cards(self, player, num_cards, rank):
        # Убираем карты игрока (например, по заданному рангу)
        hand = self.hands[player]
        discarded = []
        for _ in range(num_cards):
            for card in hand:
                if rank in card:
                    discarded.append(card)
                    hand.remove(card)
                    break
        return discarded

    def check_validity(self, rank, num_cards):
        """ Проверка, можно ли сделать ход с таким количеством карт этого ранга. """
        count = sum(1 for card in self.get_current_player_hand() if rank in card)
        return count >= num_cards


def play_game(num_players):
    game = Game(num_players)
    bots = [SimpleBot(i, game) if i % 2 == 0 else SmartBot(i, game) for i in range(1, num_players + 1)]

    while True:
        current_player = game.turn
        print(f"Player {current_player}'s turn")

        # Бот делает ход
        bot = bots[current_player - 1]
        move = bot.make_move()
        print(f"Bot {current_player} decides to: {move}")

        # Логика обработки хода: проверка, что можно перевести, верить или не верить
        # Мы будем пропускать детали реализации этих операций для упрощения

        # Переход к следующему ходу
        game.next_turn()

        # Условие окончания игры
        if all(len(hand) == 0 for hand in game.hands.values()):
            print("Game Over")
            break


play_game(4)
