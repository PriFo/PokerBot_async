from cards import Hand


class Blackjack:

    def __init__(self):
        ...


class BotBlackjack:
    """Класс, хранящий руку бота для игры в Blackjack"""

    def __init__(self):
        self.hand: Hand = Hand()
