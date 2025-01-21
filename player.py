class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []  # Список карт игрока
        self.is_turn = False  # Определяет, чей сейчас ход
        self.is_busted = False  # Показатель, пойман ли игрок на вранье
        self.claimed_rank = None  # Ранг, который игрок утверждает

    def play_card(self, num_cards, rank=None):
        """Игрок выбирает карты для кона."""
        selected_cards = []
        for _ in range(num_cards):
            selected_cards.append(self.hand.pop())  # Удаляем выбранные карты из руки
        self.claimed_rank = rank  # Утверждаем ранг карт
        return selected_cards

    def reset_turn(self):
        """Сброс состояния после хода."""
        self.is_busted = False
        self.claimed_rank = None
