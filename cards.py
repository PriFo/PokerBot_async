from random import shuffle


class Card:
    """Класс, хранящий информацию о конкретной карте"""

    def __init__(self, value: int, suit: int):
        self.value: int = value
        self.suit: int = suit

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        card_str = ""
        if 1 < self.value < 11:
            card_str += str(self.value)
        elif self.value == 1 or self.value == 14:
            card_str += "A"
        elif self.value == 11:
            card_str += "J"
        elif self.value == 12:
            card_str += "Q"
        elif self.value == 13:
            card_str += "K"
        if self.suit == 1:
            card_str += "♥ "
        elif self.suit == 2:
            card_str += "♦ "
        elif self.suit == 3:
            card_str += "♠ "
        elif self.suit == 4:
            card_str += "♣ "
        return card_str


class Cards:
    """Класс, хранящий информацию о колоде карт"""

    def __init__(self):
        self.cards: list = []
        for i in range(1, 4):
            for j in range(1, 13):
                card = Card(j, i)
                self.cards.append(card)
        shuffle(self.cards)


class Hand:
    """Класс, хранящий информацию о руке игроков (подходит как для покера, так и для Blackjack)"""

    def __init__(self):
        self.cards: list = []
