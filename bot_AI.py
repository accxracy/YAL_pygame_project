import random


class SimpleBot:
    def __init__(self, player_number, game):
        self.player_number = player_number
        self.game = game

    def make_move(self):
        hand = self.game.get_current_player_hand()
        if not hand:
            return 'skip'

        # Выбираем случайную карту
        card = random.choice(hand)
        rank = card.split()[0]
        num_cards = random.randint(1, 3)  # Бот случайно выбирает количество карт

        # Возможные варианты действий
        actions = ['translate', 'believe', 'dont_believe']
        action = random.choice(actions)
        return (rank, num_cards, action)


class SmartBot:
    def __init__(self, player_number, game):
        self.player_number = player_number
        self.game = game

    def make_move(self):
        hand = self.game.get_current_player_hand()
        if not hand:
            return 'skip'

        # Бот пытается выбрать наиболее частые карты в руке для ложных заявлений
        rank_counts = {}
        for card in hand:
            rank = card.split()[0]
            rank_counts[rank] = rank_counts.get(rank, 0) + 1

        # Выбираем наиболее распространённый ранг
        most_common_rank = max(rank_counts, key=rank_counts.get)
        num_cards = random.randint(1, 3)  # Опять же, выбираем случайное количество карт

        # Выбираем вариант действия в зависимости от предыдущего хода
        actions = ['translate', 'believe', 'dont_believe']
        action = random.choice(actions)
        return (most_common_rank, num_cards, action)