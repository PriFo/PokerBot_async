from enum import Enum

from cards import Cards


class Status(Enum):

    ALL_IN = 1
    PASS = 2
    CALL = 3
    NOT_IN_GAME = 4


class Table:

    def __init__(self, cards: Cards = None):
        if cards is None:
            self.__cards: Cards = Cards()
        else:
            self.__cards: Cards = cards
        self.__community_cards: list = []

    @property
    def cards(self):
        return self.__cards

    @property
    def community_cards(self):
        return self.__community_cards

    def get_community_cards(self):
        return self.__community_cards

    def get_last_card(self):
        return self.__cards.cards.pop()

    def __hash__(self):
        return hash((self.__cards, self.__community_cards))


class Poker:

    def __init__(self):
        self.__table: Table = Table()
        self.__users: list = []
        self.__users_hands: dict = {}
        self.__stack: int = 0
        self.__hands: dict = {}
        self.__bets: dict = {}
        self.__ready_dict: dict = {}
        self.__dealer_id: [str, int] = 0

    @property
    def table(self):
        return self.__table

    @property
    def users(self):
        return self.__users

    @property
    def stack(self):
        return self.__stack

    @property
    def hands(self):
        return self.__hands

    @property
    def bets(self):
        return self.__bets

    @property
    def dealer_id(self):
        return self.__dealer_id

    @stack.setter
    def stack(self, value: int):
        self.__stack += value


