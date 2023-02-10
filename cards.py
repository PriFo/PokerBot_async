from random import shuffle


class Card:
    """Класс, хранящий информацию о конкретной карте"""

    def __init__(self, value: int, suit: int):
        self.__value: int = value
        self.__suit: int = suit

    def __lt__(self, other):
        return self.__value < other.__value

    def __le__(self, other):
        return self.__value <= other.__value

    def __eq__(self, other):
        return self.__value == other.__value

    def __ne__(self, other):
        return self.__value != other.__value

    def __gt__(self, other):
        return self.__value > other.__value

    def __ge__(self, other):
        return self.__value >= other.__value

    def __str__(self):
        card_str = ""
        if 1 < self.__value < 11:
            card_str += str(self.__value)
        elif self.__value == 1 or self.__value == 14:
            card_str += "A"
        elif self.__value == 11:
            card_str += "J"
        elif self.__value == 12:
            card_str += "Q"
        elif self.__value == 13:
            card_str += "K"
        if self.__suit == 1:
            card_str += "♥ "
        elif self.__suit == 2:
            card_str += "♦ "
        elif self.__suit == 3:
            card_str += "♠ "
        elif self.__suit == 4:
            card_str += "♣ "
        return card_str

    def __hash__(self):
        return hash((self.__value, self.__suit))

    @property
    def suit(self):
        return self.__suit

    @property
    def value(self):
        return self.__value


class Cards:
    """Класс, хранящий информацию о колоде карт"""

    def __init__(self):
        self.__cards: list = []
        for i in range(1, 5):
            for j in range(1, 14):
                card = Card(j, i)
                self.__cards.append(card)
        shuffle(self.__cards)

    def __hash__(self):
        return hash((self.__cards,))

    @property
    def cards(self):
        return self.__cards


class Hand:
    """Класс, хранящий информацию о руке игроков (подходит как для покера, так и для Blackjack)"""

    def __init__(self):
        self.__cards: list = []

    def __hash__(self):
        return hash((self.__cards,))

    @property
    def cards(self):
        return self.__cards
