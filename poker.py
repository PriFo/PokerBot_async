from cards import Cards


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
        self.__stack: int = 0
        self.__hands: dict = {}
        self.__bets: dict = {}
        self.__dealer_id: [str, int] = 0
