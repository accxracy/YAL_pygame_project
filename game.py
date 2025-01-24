import random
from card import load_deck

class Game:
    def __init__(self, players):
        self.players = players
        self.deck = load_deck()  # Колода карт
        random.shuffle(self.deck)
        self.rounds_played = 0
        self.current_player_idx = 0
        self.table_cards = []

    def start_game(self):
        """Начать игру, раздать карты игрокам"""
        self.rounds_played = 0
        self.current_player_idx = 0
        for player in self.players:
            for _ in range(13):  # каждому игроку по 13 карт
                player.draw_card(self.deck)

    def start_round(self):
        """Запуск раунда"""
        while True:
            current_player = self.players[self.current_player_idx]
            print(f"Текущий игрок: {current_player.name}")

            # Первый игрок начинает кон
            if self.rounds_played == 0:
                discarded_cards, declared_rank = current_player.declare_cards()
                print(f"{current_player.name} начал кон, выбросив карты: {discarded_cards} с рангом {declared_rank}")
                self.table_cards.extend(discarded_cards)
                self.rounds_played += 1
            else:
                action = current_player.decide_action(declared_rank, is_liar=True)
                print(f"{current_player.name} выбрал действие: {action}")

                if action == "believe":
                    # Проверка на правдивость
                    is_liar = current_player.check_liar(discarded_cards, declared_rank)
                    if not is_liar:
                        print(f"{current_player.name} верит. {declared_rank} карты верны!")
                        # Игрок, который врал, проиграл раунд, карты забирает честный игрок.
                        self.next_turn()
                        break
                    else:
                        print(f"{current_player.name} не верит!")
                        break
                elif action == "not_believe":
                    # Аналогичная логика, если игрок не верит
                    pass
                elif action == "pass":
                    # Игрок передает ход
                    self.next_turn()
                    break

    def next_turn(self):
        """Переход хода к следующему игроку"""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
