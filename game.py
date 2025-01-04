import random


def create_deck():
    """Создание колоды карт, включая два джокера"""
    deck = []
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    for suit in suits:
        for rank in ranks:
            deck.append(f"{rank} of {suit}")

    # Добавляем два джокера
    deck.append('4 of 0')
    deck.append('4 of 1')

    random.shuffle(deck)
    return deck


def deal_cards(deck, num_players):
    """Распределение карт между игроками"""
    players = [[] for _ in range(num_players)]
    while deck:
        for i in range(num_players):
            if deck:
                players[i].append(deck.pop())
    return players


class Player:
    def __init__(self, hand, is_human=False):
        self.hand = hand
        self.jokers = sum(1 for card in hand if "4 of" in card)
        self.is_human = is_human

    def make_move(self, called_rank=None, first_turn=False):
        """Определяет ход игрока. Для человека запрашивается ввод, для бота — выбирается случайно."""
        if self.is_human:
            return self.human_move(called_rank, first_turn)
        else:
            return self.bot_move(called_rank, first_turn)

    def human_move(self, called_rank, first_turn):
        """Обработка хода для человека"""
        self.sort_hand()  # Сортировка карт перед выводом на экран
        print(f"\nYour hand: {self.display_hand()}")

        if first_turn:
            return self.start_turn()  # Для первого хода — старт кона
        else:
            print(f"Called rank: {called_rank}")
            print("\nWhat do you want to do?")
            print("1. Translate (add more cards of the same rank)")
            print("2. Believe (check if the move is true)")
            print("3. Don’t believe (check if the move is false and take the cards)")
            action = input("Enter the number of your action (1, 2, or 3): ")

            if action == '1':
                # Перевести
                num_cards = int(input("How many cards of this rank do you want to play (1, 2, or 3)? "))
                print(f"Now select the cards you want to play:")
                selected_cards = self.select_cards(num_cards)
                return ('translate', selected_cards, called_rank)
            elif action == '2':
                # Поверить
                return ('believe', called_rank)
            elif action == '3':
                # Не поверить
                return ('dont_believe', called_rank)
            else:
                print("Invalid choice. Please try again.")
                return self.human_move(called_rank, first_turn)

    def bot_move(self, called_rank, first_turn):
        """Обработка хода для бота"""
        action = 'translate' if first_turn else random.choice(['translate', 'believe', 'dont_believe'])
        if action == 'translate':
            num_cards = random.randint(1, 3)
            return (action, self.select_cards(num_cards), called_rank)
        else:
            return (action, called_rank)

    def start_turn(self):
        """Начало хода — игрок выбирает карты и называет ранг"""
        print("You are starting a new turn!")

        # 1. Выбираем количество карт для выкидывания
        num_cards = int(input("How many cards do you want to play (1, 2, or 3)? "))
        while num_cards not in [1, 2, 3]:
            print("Invalid number of cards! Please choose between 1, 2, or 3.")
            num_cards = int(input("How many cards do you want to play (1, 2, or 3)? "))

        # 2. Выбираем карты, которые будем выкидывать
        selected_cards = self.select_cards(num_cards)

        # 3. Проверка на наличие карт с выбранным рангом
        chosen_rank = self.choose_rank(selected_cards)

        # 4. Название рандомного ранга для этих карт
        print(f"You selected {', '.join(selected_cards)}. You will say they are {chosen_rank}.")

        return ('start_turn', selected_cards, chosen_rank)

    def choose_rank(self, selected_cards):
        """Выбираем ранг карт, которые хотим выкинуть"""
        ranks_in_hand = set([card.split(' ')[0] for card in self.hand])  # Множество рангов в руке

        # Смотрим, с каким рангом мы можем выкидывать выбранные карты
        print(f"Chosen cards: {', '.join(selected_cards)}")
        chosen_rank = input("Choose a rank for these cards (from your hand): ").strip().upper()

        while chosen_rank not in ranks_in_hand:
            print(f"You don't have any cards of rank {chosen_rank} in your hand. Choose another rank.")
            chosen_rank = input("Choose a rank for these cards (from your hand): ").strip().upper()

        return chosen_rank

    def select_cards(self, num_cards):
        """Позволяет игроку выбрать карты из своей руки"""
        available_cards = [card for card in self.hand]
        selected_cards = []

        print("Available cards to select: ")
        for idx, card in enumerate(available_cards, 1):
            print(f"{idx}. {card}")

        for i in range(num_cards):
            card_idx = int(input(f"Select card {i + 1} (enter a number between 1 and {len(available_cards)}): "))
            while card_idx < 1 or card_idx > len(available_cards):
                print(f"Invalid choice. Please select a card between 1 and {len(available_cards)}.")
                card_idx = int(input(f"Select card {i + 1} (enter a number between 1 and {len(available_cards)}): "))
            selected_card = available_cards.pop(card_idx - 1)
            selected_cards.append(selected_card)

        return selected_cards

    def has_rank(self, rank):
        """Проверяет, есть ли у игрока карты с данным рангом"""
        return sum(1 for card in self.hand if rank in card) > 0

    def discard_cards(self, selected_cards):
        """Удаляет карты, которые были выкинуты"""
        for card in selected_cards:
            self.hand.remove(card)

    def sort_hand(self):
        """Сортирует карты по рангу и отображает их в упорядоченном виде"""
        rank_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        rank_count = {rank: 0 for rank in rank_order}

        # Подсчёт карт каждого ранга
        for card in self.hand:
            for rank in rank_order:
                if rank in card:
                    rank_count[rank] += 1
                    break

        # Создание отсортированного списка карт
        self.sorted_hand = []
        for rank in rank_order:
            if rank_count[rank] > 0:
                self.sorted_hand.append(f"{rank} x {rank_count[rank]}")

    def display_hand(self):
        """Отображает отсортированную руку игрока с количеством карт каждого ранга"""
        return ', '.join(self.sorted_hand)


def check_move(player, called_rank, move_type):
    """Проверка хода игрока"""
    if called_rank is None:
        return False
    if move_type == 'truth':
        return player.has_rank(called_rank)
    elif move_type == 'lie':
        if player.has_rank(called_rank):
            return False
        return True


def check_winner(players):
    """Проверяет, кто выиграл, если у одного игрока закончились карты"""
    for player in players:
        if len(player.hand) == 0:
            return True  # Игрок победил
    return False


def play_game(num_players):
    """Основная игровая функция"""
    deck = create_deck()
    players_hands = deal_cards(deck, num_players)

    players = [Player(hand, is_human=(i == 0)) for i, hand in enumerate(players_hands)]  # Первый игрок - человек

    current_player_idx = 0
    first_turn = True
    last_called_rank = None
    while True:
        current_player = players[current_player_idx]

        # Игрок начинает кон
        move = current_player.make_move(called_rank=last_called_rank, first_turn=first_turn)

        # Игрок начал ход, теперь проверяем
        if move[0] == 'start_turn':
            first_turn = False
            called_rank = move[2]
            current_player.discard_cards(move[1])
            print(f"{'Player ' + str(current_player_idx + 1)} starts with {len(move[1])} cards of rank {called_rank}.")

        # Перевод хода
        # Проверка победы
        if check_winner(players):
            print("Game Over! We have a winner!")
            break

        # Передаем ход
        current_player_idx = (current_player_idx + 1) % num_players


play_game(4)