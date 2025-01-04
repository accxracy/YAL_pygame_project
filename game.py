import random


def create_deck():
    # Колода состоит из 4 мастей и 13 карт каждой масти, плюс два джокера
    deck = []
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    # Добавляем карты для каждой масти
    for suit in suits:
        for rank in ranks:
            deck.append(f"{rank} of {suit}")

    # Добавляем два джокера
    deck.append('4 of 0')
    deck.append('4 of 1')

    # Перемешиваем колоду
    random.shuffle(deck)
    return deck


def deal_cards(deck, num_players):
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
        """
        Для человека: получение ввода и выбор действия.
        Если это первый ход, игрок может выбрать ранг и количество карт.
        """
        if self.is_human:
            return self.human_move(called_rank, first_turn)
        else:
            return self.bot_move(called_rank, first_turn)

    def human_move(self, called_rank, first_turn):
        """
        Для первого хода игрок сам выбирает ранг и количество карт.
        В дальнейшем игрок может перевести, поверить или не поверить.
        """
        self.sort_hand()  # Сортировка карт перед выводом на экран
        print(f"\nYour hand: {self.display_hand()}")

        if first_turn:
            # Если это первый ход, игрок может выбрать ранг и количество карт
            print("\nIt's the first turn! Choose the rank and number of cards to play.")
            called_rank = input("Enter the rank (2, 3, 4, ..., A): ").strip().upper()
            while called_rank not in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                print("Invalid rank! Please choose a valid rank.")
                called_rank = input("Enter the rank (2, 3, 4, ..., A): ").strip().upper()
            num_cards = int(input("How many cards of this rank do you want to play (1, 2, or 3)? "))
            while num_cards not in [1, 2, 3]:
                print("Invalid number of cards! Please choose between 1, 2, or 3.")
                num_cards = int(input("How many cards of this rank do you want to play (1, 2, or 3)? "))
            return ('start_turn', called_rank, num_cards)
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
        """
        Для бота: случайный выбор действия.
        Если это первый ход, бот может только перевести.
        """
        action = 'translate' if first_turn else random.choice(['translate', 'believe', 'dont_believe'])
        if action == 'translate':
            num_cards = random.randint(1, 3)
            return (action, self.select_cards(num_cards), called_rank)
        else:
            return (action, called_rank)

    def select_cards(self, num_cards):
        """
        Выбирает случайные карты из руки для перевода.
        """
        selected_cards = []
        available_cards = self.hand.copy()  # Чтобы не изменять оригинальную руку
        for _ in range(num_cards):
            card = random.choice(available_cards)
            selected_cards.append(card)
            available_cards.remove(card)
        return selected_cards

    def has_rank(self, rank):
        """
        Проверяет, есть ли у игрока карты с данным рангом.
        """
        return sum(1 for card in self.hand if rank in card) > 0

    def discard_cards(self, selected_cards):
        """
        Удаляет карты, которые были выкинуты.
        """
        for card in selected_cards:
            self.hand.remove(card)

    def sort_hand(self):
        """
        Сортирует карты по рангу (от 2 до A), а также собирает их в словарь с количеством карт одного ранга.
        """
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
        """
        Показывает отсортированную руку игрока с количеством карт каждого ранга.
        """
        return ', '.join(self.sorted_hand)


def check_move(player, called_rank, move_type):
    """
    Проверка хода: игрок говорит правду или нет.
    Если игрок врет, нужно убедиться, что он не обманывает с количеством карт.
    """
    if called_rank is None:
        return False  # Это ошибка, так как в первом ходе не должно быть None
    if move_type == 'truth':
        # Игрок честен, проверяем, есть ли у него такие карты
        return player.has_rank(called_rank)
    elif move_type == 'lie':
        # Игрок врет, проверяем, что количество карт не соответствует реальности
        if player.has_rank(called_rank):
            return False  # Врет, но не по количеству
        return True


def check_winner(players):
    """
    Проверяет, есть ли победитель в игре.
    Победитель - тот, кто избавился от всех карт.
    """
    for player in players:
        if len(player.hand) == 0:
            return True  # Игрок победил
    return False


def play_game(num_players):
    # Создаем колоду и раздаем карты
    deck = create_deck()
    players_hands = deal_cards(deck, num_players)

    # Создаем игроков
    players = [Player(hand, is_human=(i == 0)) for i, hand in enumerate(players_hands)]  # Первый игрок - человек

    # Игровой цикл
    current_player_idx = 0
    first_turn = True  # Для первого хода
    while True:
        current_player = players[current_player_idx]

        # Если это первый ход, игрок сам выбирает ранг и количество карт
        move = current_player.make_move(first_turn=first_turn)

        called_rank = move[1] if len(move) > 1 else None  # Получаем called_rank при первом ходе

        if move[0] == 'start_turn':
            print(f"Player {current_player_idx + 1} starts with {move[2]} cards of rank {called_rank}.")
        elif move[0] == 'translate':
            selected_cards = move[1]
            print(
                f"Player {current_player_idx + 1} translates with {len(selected_cards)} cards and says {called_rank}.")
            current_player.discard_cards(selected_cards)
        elif move[0] == 'believe':
            print(f"Player {current_player_idx + 1} decides to believe the previous player.")
            # Здесь будет логика проверки правды или лжи
        elif move[0] == 'dont_believe':
            print(f"Player {current_player_idx + 1} decides not to believe the previous player.")

        # Проверяем, кто выиграл
        if check_winner(players):
            print(f"Player {current_player_idx + 1} wins!")
            break

        # Переходим к следующему игроку
        current_player_idx = (current_player_idx + 1) % num_players
        first_turn = False  # После первого хода другие игроки могут выбирать все действия


play_game(4)